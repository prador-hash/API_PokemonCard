"""Rotas para gerenciamento de Cards."""

from fastapi import APIRouter, HTTPException
from app.schemas.card import CardCreate, CardUpdate, CardResponse

router = APIRouter(prefix="/cards", tags=["cards"], responses={404: {"description": "Card não encontrado"}})

cards_db = {}
card_id_counter = 1


@router.get("/", response_model=list[CardResponse])
def listar_cards():
    """Listar todas as cartas."""
    return list(cards_db.values())


@router.get("/{card_id}", response_model=CardResponse)
def obter_card(card_id: int):
    """Obter uma carta específica pelo ID."""
    if card_id not in cards_db:
        raise HTTPException(status_code=404, detail=f"Card com ID {card_id} não encontrado")
    return cards_db[card_id]


@router.post("/", response_model=CardResponse, status_code=201)
def criar_card(card: CardCreate):
    """Criar uma nova carta no catálogo."""
    global card_id_counter
    novo_id = card_id_counter
    card_id_counter += 1
    
    novo_card = {"id": novo_id, **card.model_dump()}
    cards_db[novo_id] = novo_card
    return novo_card


@router.put("/{card_id}", response_model=CardResponse)
def atualizar_card(card_id: int, card_atualizado: CardUpdate):
    """Atualizar uma carta existente."""
    if card_id not in cards_db:
        raise HTTPException(status_code=404, detail=f"Card com ID {card_id} não encontrado")
    
    card_existente = cards_db[card_id]
    dados_atualizacao = card_atualizado.model_dump(exclude_unset=True)
    card_existente.update(dados_atualizacao)
    
    return card_existente


@router.delete("/{card_id}", status_code=204)
def deletar_card(card_id: int):
    """Deletar uma carta do catálogo."""
    if card_id not in cards_db:
        raise HTTPException(status_code=404, detail=f"Card com ID {card_id} não encontrado")
    del cards_db[card_id]
