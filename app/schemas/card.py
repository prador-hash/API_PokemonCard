"""Esquemas de validação para a entidade Card."""

from pydantic import BaseModel, Field


class CardBase(BaseModel):
    """Esquema base para Card com atributos comuns."""
    nome: str = Field(..., min_length=1, max_length=150, description="Nome da carta")
    set_name: str = Field(..., min_length=1, max_length=100, description="Nome do set/expansão")
    numero: str = Field(..., min_length=1, max_length=10, description="Número da carta no set")
    tipo: str = Field(..., min_length=1, max_length=50, description="Tipo (Fogo, Água, Grama, etc)")
    preco: float = Field(..., gt=0, le=10000, description="Preço em Reais")
    quantidade: int = Field(default=0, ge=0, description="Quantidade em estoque")


class CardCreate(CardBase):
    """Esquema para criar uma nova carta."""
    pass


class CardUpdate(BaseModel):
    """Esquema para atualizar uma carta (todos os campos opcionais)."""
    nome: str | None = Field(None, min_length=1, max_length=150)
    set_name: str | None = Field(None, min_length=1, max_length=100)
    numero: str | None = Field(None, min_length=1, max_length=10)
    tipo: str | None = Field(None, min_length=1, max_length=50)
    preco: float | None = Field(None, gt=0, le=10000)
    quantidade: int | None = Field(None, ge=0)


class CardResponse(CardBase):
    """Esquema para resposta de Card (inclui ID)."""
    id: int

    class Config:
        from_attributes = True
