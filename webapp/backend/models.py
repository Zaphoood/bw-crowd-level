from sqlalchemy import Column, Integer, String, Time
from database import Base


class CrowdLevel(Base):
    __tablename__ = "crowd_level"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(Time, index=True)
    branch = Column(String)
    level = Column(Integer)
