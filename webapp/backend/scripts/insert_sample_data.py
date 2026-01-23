from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parents[1]))

from database import Base, engine, SessionLocal
from models import CrowdLevel

Base.metadata.create_all(bind=engine)

db = SessionLocal()
now = datetime.now()
items = [
    CrowdLevel(timestamp=now - timedelta(hours=1), branch="muenchen_ost", level=10),
    CrowdLevel(timestamp=now - timedelta(minutes=30), branch="muenchen_ost", level=15),
    CrowdLevel(timestamp=now, branch="muenchen_ost", level=40),
]

db.add_all(items)
db.commit()
db.close()

print(
    f"Created database and inserted {len(items)} items into {CrowdLevel.__tablename__}"
)
