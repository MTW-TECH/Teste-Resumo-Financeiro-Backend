from dataclasses import dataclass


@dataclass(frozen=True)
class Company:
    id: int
    name: str
    industry: str
    founded_year: int
    employee_count: int
