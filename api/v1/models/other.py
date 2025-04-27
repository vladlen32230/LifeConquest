from typing import Any, Literal
from dataclasses import dataclass

@dataclass
class Route:
    path: str
    endpoint: Any
    status_code: int
    response_model: Any
    responses: dict[int, dict[str, Any]]
    methods: list[Literal['GET', 'POST', 'PATCH', 'DELETE']]
    description: str