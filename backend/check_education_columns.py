from app.database import SessionLocal
from sqlalchemy import inspect

db = SessionLocal()
inspector = inspect(db.bind)
cols = inspector.get_columns('education')
print("Current education table columns:")
for col in cols:
    print(f"  {col['name']}: {col['type']}")
db.close()
