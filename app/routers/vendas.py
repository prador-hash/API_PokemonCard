"""Rotas para gerenciamento de Vendas."""

from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.schemas.venda import VendaCreate, VendaUpdate, VendaResponse
from app.routers.cards import cards_db

router = APIRouter(prefix="/vendas", tags=["vendas"], responses={404: {"description": "Venda não encontrada"}})

vendas_db = {}
venda_id_counter = 1


@router.get("/", response_model=list[VendaResponse])
def listar_vendas():
    """Listar todas as vendas."""
    return list(vendas_db.values())


@router.get("/{venda_id}", response_model=VendaResponse)
def obter_venda(venda_id: int):
    """Obter uma venda específica pelo ID."""
    if venda_id not in vendas_db:
        raise HTTPException(status_code=404, detail=f"Venda com ID {venda_id} não encontrado")
    return vendas_db[venda_id]


@router.get("/cards/{card_id}/vendas", response_model=list[VendaResponse])
def listar_vendas_por_card(card_id: int):
    """Listar todas as vendas de uma carta específica."""
    if card_id not in cards_db:
        raise HTTPException(status_code=404, detail=f"Card com ID {card_id} não encontrado")
    
    vendas_card = [v for v in vendas_db.values() if v["card_id"] == card_id]
    return vendas_card


@router.post("/", response_model=VendaResponse, status_code=201)
def criar_venda(venda: VendaCreate):
    """Criar uma nova venda."""
    if venda.card_id not in cards_db:
        raise HTTPException(status_code=400, detail=f"Card com ID {venda.card_id} não existe")
    
    card = cards_db[venda.card_id]
    if card["quantidade"] < venda.quantidade:
        raise HTTPException(status_code=400, detail="Quantidade insuficiente em estoque")
    
    global venda_id_counter
    novo_id = venda_id_counter
    venda_id_counter += 1
    
    total = venda.preco_unitario * venda.quantidade
    nova_venda = {
        "id": novo_id,
        "data_venda": datetime.now(),
        "total": total,
        **venda.model_dump()
    }
    
    # Atualizar estoque
    card["quantidade"] -= venda.quantidade
    
    vendas_db[novo_id] = nova_venda
    return nova_venda


@router.put("/{venda_id}", response_model=VendaResponse)
def atualizar_venda(venda_id: int, venda_atualizado: VendaUpdate):
    """Atualizar uma venda existente."""
    if venda_id not in vendas_db:
        raise HTTPException(status_code=404, detail=f"Venda com ID {venda_id} não encontrado")
    
    if venda_atualizado.card_id is not None:
        if venda_atualizado.card_id not in cards_db:
            raise HTTPException(status_code=400, detail=f"Card com ID {venda_atualizado.card_id} não existe")
    
    venda_existente = vendas_db[venda_id]
    dados_atualizacao = venda_atualizado.model_dump(exclude_unset=True)
    
    if "preco_unitario" in dados_atualizacao or "quantidade" in dados_atualizacao:
        preco = dados_atualizacao.get("preco_unitario", venda_existente["preco_unitario"])
        qtd = dados_atualizacao.get("quantidade", venda_existente["quantidade"])
        dados_atualizacao["total"] = preco * qtd
    
    venda_existente.update(dados_atualizacao)
    
    return venda_existente


@router.delete("/{venda_id}", status_code=204)
def deletar_venda(venda_id: int):
    """Deletar uma venda."""
    if venda_id not in vendas_db:
        raise HTTPException(status_code=404, detail=f"Venda com ID {venda_id} não encontrado")
    del vendas_db[venda_id]
