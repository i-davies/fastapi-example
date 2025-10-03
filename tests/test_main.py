from fastapi.testclient import TestClient
import pytest
from app.main import app
# Importamos o módulo 'crud' para poder chamar a função 'reset_db'
from app import crud

# A fixture agora chama crud.reset_db()
@pytest.fixture(name="client")
def setup_fixture():
    """ Fixture para limpar o BD e instanciar o TestClient"""
    crud.reset_db()
    yield TestClient(app)

#
# O restante do arquivo de teste continua exatamente o mesmo!
# Nenhuma lógica de teste precisa ser alterada.
#

# === Cenários de SUCESSO ===

def test_criar_contato_sucesso(client):
    """ Testa a criação de um contato com dados válidos. """
    response = client.post(
        "/contatos",
        json={"nome": "Ana Banana", "email": "ana.b@example.com", "telefone": "123"}
    )
    data = response.json()
    assert response.status_code == 201
    assert data["id"] == 1
    assert data["nome"] == "Ana Banana"
    assert data["email"] == "ana.b@example.com"

def test_listar_contatos(client):
    """ Testa a listagem de contatos. """
    response = client.get("/contatos")
    assert response.status_code == 200
    assert response.json() == []

def test_listar_contatos_existentes(client):
    """ Testa a listagem de contatos já existente"""
    client.post("/contatos", json={"nome": "Beto Carrero", "email": "beto@example.com"})
    response = client.get("/contatos")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["nome"] == "Beto Carrero"

def test_deletar_contato(client):
    """ Testa a exclusão de um contato. """
    response_post = client.post(
        "/contatos",
        json={"nome": "Carlos Drummond", "email": "carlos@example.com"}
    )
    contato_id = response_post.json()["id"]

    response_delete = client.delete(f"/contatos/{contato_id}")
    assert response_delete.status_code == 200
    
    response_get = client.get(f"/contatos/{contato_id}")
    assert response_get.status_code == 404

# === Cenários de ERRO ESPERADO ===
def test_obter_contato_nao_existente(client):
    """ Testa buscar um contato com ID que não existe. """
    response = client.get("/contatos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Contato não encontrado."}

def test_criar_contato_com_email_duplicado(client):
    """ Testa a regra de negócio que impede e-mails duplicados. """
    client.post("/contatos", json={"nome": "Daniel Dantas", "email": "daniel@example.com"})
    
    response = client.post("/contatos", json={"nome": "Daniel Alves", "email": "daniel@example.com"})
    assert response.status_code == 400
    assert "já existe" in response.json()["detail"]

def test_criar_contato_com_email_invalido(client):
    """ Testa a validação do Pydantic para e-mails inválidos. """
    response = client.post(
        "/contatos",
        json={"nome": "Eva", "email": "email-invalido"}
    )
    assert response.status_code == 422 # Unprocessable Entity

@pytest.mark.xfail(reason="Este teste demonstra uma falha esperada.")
def test_criar_contato_sem_campo_obrigatorio(client):
    """ Testa a validação do Pydantic para campos obrigatórios (faltando 'nome'). """
    response = client.post(
        "/contatos",
        json={"email": "semnome@example.com"} # Falta o campo "nome"
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"
    assert response.json()["detail"][0]["loc"] == ["body", "nome"]