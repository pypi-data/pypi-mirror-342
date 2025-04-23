from pathlib import Path

from sqlmodel import SQLModel, create_engine

path = Path(__file__).parents[1] / "assets"

engine = create_engine(f"sqlite:///{path}/database.db")


def create_tables():
    SQLModel.metadata.create_all(engine)
