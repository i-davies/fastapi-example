from fastapi import FastAPI, status
from typing import List

# Importa os modelos e as funções CRUD dos outros arquivos
from . import models, crud

app = FastAPI(
    title="API de Gerenciador de Contatos",
    description="Uma API Simples para adicionar, visualizar e remover contatos.",
    version="1.0.0"
)

@app.post("/contatos", response_model=models.Contato, status_code=status.HTTP_201_CREATED, tags=["Contatos"])
def adicionar_novo_contato(contato: models.ContatoCreate):
    """Adiciona um novo contato à lista."""
    return crud.criar_contato(contato=contato)

@app.get("/contatos", response_model=List[models.Contato], tags=["Contatos"])
def listar_todos_os_contatos():
    """Lista todos os contatos cadastrados."""
    return crud.obter_contatos()

@app.get("/contatos/{contato_id}", response_model=models.Contato, tags=["Contatos"])
def obter_um_contato(contato_id: int):
    """Obtém um contato específico pelo seu ID."""
    return crud.obter_contato_por_id(contato_id=contato_id)

@app.delete("/contatos/{contato_id}", status_code=status.HTTP_200_OK, tags=["Contatos"])
def remover_um_contato(contato_id: int):
    """Remove um contato pelo seu ID."""
    return crud.deletar_contato(contato_id=contato_id)