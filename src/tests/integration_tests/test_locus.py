import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException

from src.repositories.locus import LocusRepository

@pytest.fixture
def mockSession():
    session = MagicMock()
    session.execute = AsyncMock()
    return session


@pytest.fixture
def repo(mockSession):
    return LocusRepository(mockSession)


def makeMockLocus(id=1, assembly_id="GRCh38", locus_members=None):
    locus = MagicMock()
    locus.id = id
    locus.assembly_id = assembly_id
    locus.locus_name = f"locus_{id}"
    locus.public_locus_name = "bekhzods_database"
    locus.chromosome = "1"
    locus.strand = "1"
    locus.locus_start = 1000
    locus.locus_stop = 2000
    locus.member_count = 3
    locus.locus_members = locus_members or []
    return locus


def setupMockResult(mockSession, loci):
    mockResult = MagicMock()
    mockResult.scalars.return_value.unique.return_value.all.return_value = loci
    mockSession.execute.return_value = mockResult

@pytest.mark.asyncio
async def test_invalidRole_raises400(repo, mockSession):
    setupMockResult(mockSession, [])
    with pytest.raises(HTTPException) as exc:
        await repo.get_loci(role="Bekhzod")
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_pageZero_raises400(repo, mockSession):
    with pytest.raises(HTTPException) as exc:
        await repo.get_loci(role="admin", page=0)
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_pageSizeZero_raises400(repo, mockSession):
    with pytest.raises(HTTPException) as exc:
        await repo.get_loci(role="admin", page_size=0)
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_normalUserSideload_raises403(repo, mockSession):
    with pytest.raises(HTTPException) as exc:
        await repo.get_loci(role="normal", sideload=True)
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_limitedUser_forbiddenRegion_raises403(repo, mockSession):
    with pytest.raises(HTTPException) as exc:
        await repo.get_loci(role="limited", region_id=998990771814)
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_limitedUser_allowedRegion_succeeds(repo, mockSession):
    setupMockResult(mockSession, [makeMockLocus()])
    result = await repo.get_loci(role="limited", region_id=86118093)
    assert result is not None


@pytest.mark.asyncio
async def test_limitedUser_noRegionGiven_usesDefaultRegions(repo, mockSession):
    setupMockResult(mockSession, [makeMockLocus()])
    result = await repo.get_loci(role="limited")
    assert result is not None


@pytest.mark.asyncio
async def test_validSortFields_allAccepted(repo, mockSession):
    setupMockResult(mockSession, [])
    for field in ["id", "assemblyId", "locusStart", "locusStop", "memberCount"]:
        result = await repo.get_loci(role="admin", sort_by=field)
        assert result is not None

@pytest.mark.asyncio
async def test_adminUser_returnsResults(repo, mockSession):
    loci = [makeMockLocus(id=1), makeMockLocus(id=2)]
    setupMockResult(mockSession, loci)
    result = await repo.get_loci(role="admin")
    assert len(result) == 2


@pytest.mark.asyncio
async def test_adminUser_canSideload(repo, mockSession):
    loci = [makeMockLocus(id=1)]
    setupMockResult(mockSession, loci)
    result = await repo.get_loci(role="admin", sideload=True)
    assert result is not None
