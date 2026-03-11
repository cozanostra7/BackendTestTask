from typing import List, Optional
from fastapi import APIRouter, Query

from src.database import async_session_maker
from src.repositories.locus import LocusRepository
from src.schemas.locus import LocusResponse

router = APIRouter()


@router.get("/locus", response_model=List[LocusResponse])
async def getLoci(
    role: str,
    id: Optional[int] = Query(None),
    assembly_id: Optional[str] = Query(None),
    region_id: Optional[int] = Query(None),
    membership_status: Optional[str] = Query(None),
    sideload: bool = Query(False),
    page: int = Query(1, alias="page"),
    page_size: int = Query(1000, alias="pageSize"),
    sort_by: str = Query("id", alias="sortBy"),
    sort_order: str = Query("asc", alias="sortOrder"),
):
    async with async_session_maker() as session:
        repo = LocusRepository(session)

        loci = await repo.get_loci(
            role=role,
            id=id,
            assembly_id=assembly_id,
            region_id=region_id,
            membership_status=membership_status,
            sideload=sideload,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        return [LocusResponse.model_validate(locus) for locus in loci]