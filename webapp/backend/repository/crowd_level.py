from sqlalchemy.orm import Session

from models import CrowdLevel


class CrowdLevelRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[CrowdLevel]:
        return self.db.query(CrowdLevel).all()
