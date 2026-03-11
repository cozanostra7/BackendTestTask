from __future__ import annotations
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, ConfigDict, Field


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

    locusMemberId: int = Field(alias="id")
    regionId: Optional[int] = Field(default=None, alias="region_id")
    locusId: int = Field(alias="locus_id")
    membershipStatus: Optional[str] = Field(default=None, alias="membership_status")


class LocusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    assemblyId: str = Field(alias="assembly_id")
    locusName: str = Field(alias="locus_name")
    publicLocusName: Optional[str] = Field(default=None, alias="public_locus_name")
    chromosome: Optional[str] = None
    strand: Optional[str] = None
    locusStart: Optional[int] = Field(default=None, alias="locus_start")
    locusStop: Optional[int] = Field(default=None, alias="locus_stop")
    memberCount: Optional[int] = Field(default=None, alias="member_count")


class LocusWithMembersResponse(LocusResponse):
    locusMembers: List[LocusMemberResponse] = Field(default_factory=list)

    @classmethod
    def from_locus(cls, locus):
        base = LocusResponse.model_validate(locus)

        members = [
            LocusMemberResponse.model_validate(m)
            for m in (locus.locus_members or [])
        ]

        return cls(**base.model_dump(), locusMembers=members)

class PaginatedResponse(BaseModel):
    total: int
    page: int
    pageSize: int
    results: List[Union[LocusResponse, LocusWithMembersResponse]]