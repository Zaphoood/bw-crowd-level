from fastapi import FastAPI
from database import SessionLocal
from services.crowd_level import CrowdLevelService

app = FastAPI(title="BW Crowd Level Backend")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/crowd")
def get_crowd():
    db = next(get_db())
    service = CrowdLevelService(db)
    return service.list_all()
