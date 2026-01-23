from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class CrowdLevel(Base):
    __tablename__ = "crowd_level"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    branch = Column(String)
    level = Column(Integer)
