from fastapi import HTTPException, status
from typing import Dict, List
from . import models

# Simulação de um banco de dados em memória
db_contatos: Dict[int, models.Contato] = {}
next_id: int = 1

def reset_db():
    """ Limpa o banco de dados para os testes. """
    global db_contatos, next_id
    db_contatos = {}
    next_id = 1

def criar_contato(contato: models.ContatoCreate) -> models.Contato:
    """ Cria um novo contato, validando se o e-mail já existe. """
    global next_id
    for c in db_contatos.values():
        if c.email == contato.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Contato com o e-mail '{contato.email}' já existe."
            )
    
    novo_contato = models.Contato(id=next_id, **contato.model_dump())
    db_contatos[next_id] = novo_contato
    next_id += 1
    return novo_contato

def obter_contatos() -> List[models.Contato]:
    """ Retorna todos os contatos. """
    return list(db_contatos.values())

def obter_contato_por_id(contato_id: int) -> models.Contato:
    """ Retorna um único contato pelo seu ID. """
    contato = db_contatos.get(contato_id)
    if not contato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contato não encontrado."
        )
    return contato

def deletar_contato(contato_id: int) -> Dict[str, str]:
    """ Deleta um contato pelo seu ID. """
    if contato_id not in db_contatos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contato não encontrado."
        )
    del db_contatos[contato_id]
    return {"message": "Contato deletado com sucesso."}