from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

class SideloadEnum(str, Enum):
    locusMembers = "locusMembers"


class SortByEnum(str, Enum):
    id = "id"
    assemblyId = "assemblyId"
    locusStart = "locusStart"
    locusStop = "locusStop"
    memberCount = "memberCount"


class SortOrderEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class LocusMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    locusMemberId: int
    regionId: Optional[int]
    locusId: int
    membershipStatus: Optional[str]

    @classmethod
    def from_orm_member(cls, m) -> "LocusMemberResponse":
        return cls(
            locusMemberId=m.id,
            regionId=m.region_id,
            locusId=m.locus_id,
            membershipStatus=m.membership_status,
        )


class LocusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    assemblyId: str
    locusName: str
    publicLocusName: Optional[str]
    chromosome: Optional[str]
    strand: Optional[str]
    locusStart: Optional[int]
    locusStop: Optional[int]
    memberCount: Optional[int]

    @classmethod
    def from_orm_locus(cls, locus) -> "LocusResponse":
        return cls(
            id=locus.id,
            assemblyId=locus.assembly_id,
            locusName=locus.locus_name,
            publicLocusName=locus.public_locus_name,
            chromosome=locus.chromosome,
            strand=locus.strand,
            locusStart=locus.locus_start,
            locusStop=locus.locus_stop,
            memberCount=locus.member_count,
        )


class LocusWithMembersResponse(LocusResponse):
    locusMembers: List[LocusMemberResponse] = []

    @classmethod
    def from_orm_locus(cls, locus) -> "LocusWithMembersResponse":
        base = super().from_orm_locus(locus)
        members = [
            LocusMemberResponse.from_orm_member(m)
            for m in (locus.locus_members or [])
        ]
        return cls(**base.model_dump(), locusMembers=members)


class PaginatedResponse(BaseModel):
    total: int
    page: int
    pageSize: int
    results: List[LocusResponse | LocusWithMembersResponse]