from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

# Import models so Alembic discovers them.
from app.auth.models import User