from typing import List, Optional, cast
from sqlalchemy import select, asc, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.locus import RncLocus, RncLocusMembers

REGION_LIMITED = [86118093, 86696489, 88186467]

class LocusRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_loci(
        self,
        role: str,
        id: Optional[int] = None,
        assembly_id: Optional[str] = None,
        region_id: Optional[int] = None,
        membership_status: Optional[str] = None,
        sideload: bool = False,
        page: int = 1,
        page_size: int = 1000,
        sort_by: str = "id",
        sort_order: str = "asc",
    ) -> List[RncLocus]:

        if role == "normal":
            sideload = False
        elif role == "limited":
            sideload = False
            if region_id is not None:
                if region_id not in REGION_LIMITED:
                    region_id = None
            else:
                region_id = REGION_LIMITED

        q = select(RncLocus)

        if id:
            q = q.where(RncLocus.id == id)
        if assembly_id:
            q = q.where(RncLocus.assembly_id == assembly_id)

        join_members = False
        if role == "admin" and (sideload or region_id or membership_status):
            join_members = True
        elif role == "limited" and region_id:
            join_members = True

        if join_members:
            q = q.options(selectinload(RncLocus.locus_members))
            if region_id:
                if isinstance(region_id, list):
                    q = q.join(RncLocus.locus_members).where(RncLocusMembers.region_id.in_(region_id))
                else:
                    q = q.join(RncLocus.locus_members).where(RncLocusMembers.region_id == region_id)
            if membership_status:
                q = q.join(RncLocus.locus_members).where(RncLocusMembers.membership_status == membership_status)

        if sort_by in ["assemblyId"]:
            sort_field = getattr(RncLocus, "assembly_id")
        else:
            sort_field = getattr(RncLocus, sort_by, RncLocus.id)
        q = q.order_by(asc(sort_field) if sort_order == "asc" else desc(sort_field))

        offset = (page - 1) * page_size
        q = q.offset(offset).limit(page_size)

        result = cast(List[RncLocus], (await self.session.execute(q)).scalars().unique().all())
        return result