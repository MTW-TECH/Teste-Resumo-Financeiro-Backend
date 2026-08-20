from dataclasses import dataclass


@dataclass(frozen=True)
class Company:
    id: int
    name: str
    cnpj: str
    state: str
    city: str
    active: bool
    tax_regime: str
