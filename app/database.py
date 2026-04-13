from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# The engine is the actual connection to PostgreSQL
# It reads the DATABASE_URL from our .env file
engine = create_engine(settings.database_url)

# SessionLocal is a factory that creates database sessions
# Each request to our API gets its own session
SessionLocal = sessionmaker(
    autocommit=False,  # We control when to save changes
    autoflush=False,   # We control when to send queries
    bind=engine        # Use our PostgreSQL connection
)

# Base is the parent class all our models will inherit from
# It keeps track of all tables we define
Base = declarative_base()

# This function gives each API request its own DB session
# and closes it automatically when the request is done
def get_db():
    db = SessionLocal()
    try:
        yield db        # Give the session to the route
    finally:
        db.close()      # Always close, even if there's an error