from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from .config_env import config_env

POSTGRES_USER = config_env.postgres_user
POSTGRES_PASSWORD =config_env.postgres_password
POSTGRES_HOST = config_env.postgres_host
POSTGRES_PORT = config_env.postgres_port
POSTGRES_DB = config_env.postgres_db

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Reusable DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()