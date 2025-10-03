from pydantic import BaseModel, EmailStr, Field, ConfigDict

class ContatoBase(BaseModel):
    # Usamos '...' para indicar que o campo é obrigatório.
    nome: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    telefone: str | None = Field(None)

class ContatoCreate(ContatoBase):
    pass

class Contato(ContatoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)