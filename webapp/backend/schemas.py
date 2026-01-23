from pydantic import BaseModel, Field
from datetime import time


class CrowdLevelBase(BaseModel):
    timestamp: time
    branch: str = Field()
    level: int = Field(ge=0)


class CrowdLevelRead(CrowdLevelBase):
    class Config:
        orm_mode = True
        from_attributes = True
