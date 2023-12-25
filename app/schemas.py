from pydantic import BaseModel, Field, field_validator


class DynamicSystem(BaseModel):
    first_equation: str = Field(
        default=...,
        examples=['x ** 3 + x * (y ** 2) - 10 * y']
    )
    second_equation: str = Field(
        default=...,
        examples=['x + (x ** 2) * y + (y ** 3) - 7 * y']
    )


class EquationSolution(BaseModel):
    solutions: list[tuple[str, str]] = Field(
        default=...,
        examples=[[('1', '2'), ('-2', '0')]]
    )

    @field_validator('solutions', mode='before')
    def validate_solutions(cls, value):
        return [(str(x), str(y)) for x, y in value]
