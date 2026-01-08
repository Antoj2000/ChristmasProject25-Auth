from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer


class Base(DeclarativeBase):
    pass

class CredentialsDB(Base): 

     __tablename__ = "credentials"

     id: Mapped[int] = mapped_column(primary_key=True)
     account_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
     account_no: Mapped[str] = mapped_column(String(6), unique=True, nullable=False, index=True)
     email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
     #Integrate bcrypt later on
     #password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
     password: Mapped[str] = mapped_column(String(255), nullable=False)