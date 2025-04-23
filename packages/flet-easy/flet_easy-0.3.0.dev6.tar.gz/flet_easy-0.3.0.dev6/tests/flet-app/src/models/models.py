from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(default=None, unique=True)
    password: str = Field(default=None)
