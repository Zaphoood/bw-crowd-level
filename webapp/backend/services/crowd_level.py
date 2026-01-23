from sqlalchemy.orm import Session
from repository.crowd_level import CrowdLevelRepository
from schemas import CrowdLevelRead


class CrowdLevelService:
    def __init__(self, db: Session) -> None:
        self.repo = CrowdLevelRepository(db)

    def list_all(self) -> list[CrowdLevelRead]:
        return [CrowdLevelRead.model_validate(c) for c in self.repo.get_all()]
