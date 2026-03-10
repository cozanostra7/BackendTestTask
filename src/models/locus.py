from sqlalchemy import BigInteger, Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class RncLocus(Base):
    __tablename__ = "rnc_locus"
    __table_args__ = {"schema": "rnacen"}

    id = Column(BigInteger, primary_key=True, index=True)
    assembly_id = Column(String, nullable=False, index=True)
    locus_name = Column(String, nullable=False)
    public_locus_name = Column(String, nullable=True)
    chromosome = Column(String, nullable=True)
    strand = Column(String, nullable=True)
    locus_start = Column(BigInteger, nullable=True)
    locus_stop = Column(BigInteger, nullable=True)
    member_count = Column(Integer, nullable=True)

    locus_members = relationship(
        "RncLocusMembers",
        back_populates="locus",
        lazy="select",
    )


class RncLocusMembers(Base):

    __tablename__ = "rnc_locus_members"
    __table_args__ = {"schema": "rnacen"}

    id = Column(BigInteger, primary_key=True, index=True)
    region_id = Column(BigInteger, nullable=True, index=True)
    locus_id = Column(BigInteger, ForeignKey("rnacen.rnc_locus.id"), nullable=False, index=True)
    membership_status = Column(String, nullable=True)
    urs_taxid = Column(String, nullable=True)

    locus = relationship("RncLocus", back_populates="locus_members")