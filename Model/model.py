from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from Setting_db.setting import settings_db
from Setting_db.setting import Base


class Table_user(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(nullable=False)

    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    password_hash: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)


Base.metadata.create_all(bind=settings_db.CreateEngine())





