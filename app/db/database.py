from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db.models import Base

# ✅ Correct PostgreSQL connection URL
DATABASE_URL = "postgresql+psycopg2://postgres:2309@localhost:5432/Report_Generator_DB"

# ✅ No connect_args needed for PostgreSQL
engine = create_engine(DATABASE_URL)

# Session setup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables from models
Base.metadata.create_all(bind=engine)

# Dependency to use in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
