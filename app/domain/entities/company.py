from dataclasses import dataclass


@dataclass(frozen=True)
class Company:
    id: int
    nome: str
    cnpj: str
    uf: str
    cidade: str
    ativo: bool
    regime_atual: str
