from pydantic import BaseModel, Field
from datetime import datetime


class CrowdLevelBase(BaseModel):
    timestamp: datetime
    branch: str = Field()
    level: int = Field(ge=0)


class CrowdLevelRead(CrowdLevelBase):
    class Config:
        orm_mode = True
        from_attributes = True
