"""Esquemas de validação para a entidade Venda."""

from datetime import datetime
from pydantic import BaseModel, Field


class VendaBase(BaseModel):
    """Esquema base para Venda com atributos comuns."""
    card_id: int = Field(..., gt=0, description="ID da carta vendida")
    quantidade: int = Field(..., gt=0, le=100, description="Quantidade vendida")
    preco_unitario: float = Field(..., gt=0, description="Preço unitário na venda")
    cliente: str = Field(..., min_length=1, max_length=150, description="Nome do cliente")


class VendaCreate(VendaBase):
    """Esquema para criar uma nova venda."""
    pass


class VendaUpdate(BaseModel):
    """Esquema para atualizar uma venda (todos os campos opcionais)."""
    card_id: int | None = Field(None, gt=0)
    quantidade: int | None = Field(None, gt=0, le=100)
    preco_unitario: float | None = Field(None, gt=0)
    cliente: str | None = Field(None, min_length=1, max_length=150)


class VendaResponse(VendaBase):
    """Esquema para resposta de Venda (inclui ID e data)."""
    id: int
    data_venda: datetime
    total: float

    class Config:
        from_attributes = True
