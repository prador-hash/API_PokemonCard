from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Cards(Base):
    __tablename__ = 'cards'
    
    id: Mapped[int]  = mapped_column(primary_key=True)
    descricao: Mapped[str] = mapped_column(unique=True)
    quantidade: Mapped[int]
    valor: Mapped[float]
    
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), server_default=func.now(),
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
  