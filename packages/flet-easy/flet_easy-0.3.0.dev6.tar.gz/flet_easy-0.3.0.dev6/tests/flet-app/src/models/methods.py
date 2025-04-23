from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session, select

from models.connection import engine
from models.models import User


def add_user(user: User):
    try:
        with Session(engine) as session:
            session.add(user)
            session.commit()
            return True
    except IntegrityError:
        return False


def check_user(user: User):
    try:
        with Session(engine) as session:
            statement = select(User).where(User.username == user.username)
            user_check = session.exec(statement).first()
            # print(user_check)
            if user_check:
                return user_check.password == user.password
            else:
                return False
    except NoResultFound or IntegrityError:
        return False


async def delete_user(user: User):
    try:
        with Session(engine) as session:
            statement = select(User).where(User.username == user.username)
            user_check = session.exec(statement).first()
            session.delete(user_check)
            session.commit()
            return True
    except NoResultFound or IntegrityError:
        return False
