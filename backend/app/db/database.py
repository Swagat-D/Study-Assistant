from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging
import ssl

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create SQLAlchemy engine for Neon PostgreSQL
try:
    # SSL context for secure connection to Neon
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # Create engine with specific settings for Neon
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,           # Verify connection before using it
        pool_size=5,                  # Connection pool size
        max_overflow=10,              # Allow up to 10 connections beyond pool_size
        pool_timeout=30,              # Wait up to 30 seconds for a connection
        pool_recycle=3600,            # Recycle connections after 1 hour
        connect_args={
            "sslmode": "require",     # Force SSL connection
        },
        echo=False,                   # Set to True for SQL query logging (development only)
    )
    logger.info("Neon PostgreSQL database connection established successfully")
except Exception as e:
    logger.error(f"Failed to connect to Neon PostgreSQL database: {e}")
    raise  # Re-raise the exception

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()