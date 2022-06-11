from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Step 1: connecting to sql database - setting up
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Step 2: Create an engine to connect
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Step 3: Create a SessionLocal which is a 'sessionmaker' class to create a database session per instance
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)

# Step 4: Create a 'Base' which handles the creation of models
Base = declarative_base()
