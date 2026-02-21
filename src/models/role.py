from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import db
import sqlalchemy as sa

class Role(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String,unique=True, nullable=False)
    user: Mapped[list['user.User']] = relationship(back_populates='role')

    def __repr__(self) -> str:
        return f'Role(id={self.id!r}, name={self.name!r}'