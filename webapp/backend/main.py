from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal
from services.crowd_level import CrowdLevelService

app = FastAPI(title="BW Crowd Level Backend")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/crowd_levels")
def get_crowd_levels():
    db = next(get_db())
    service = CrowdLevelService(db)
    return service.list_all()
