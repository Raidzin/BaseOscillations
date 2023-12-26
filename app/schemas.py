from pydantic import BaseModel, Field, field_validator

from app.oscillations import EquilibriumState


class DynamicSystem(BaseModel):
    first_equation: str = Field(
        default=...,
        examples=['x ** 3 + x * (y ** 2) - 10 * y']
    )
    second_equation: str = Field(
        default=...,
        examples=['x + (x ** 2) * y + (y ** 3) - 7 * y']
    )


class EquilibriumPoint(BaseModel):
    x: str
    y: str
    equilibrium_state: EquilibriumState
