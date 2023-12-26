from fastapi import FastAPI, APIRouter

from app.schemas import DynamicSystem, EquilibriumPoint
from app import frontend
from app import oscillations

app = FastAPI()

router = APIRouter(prefix='/api')


@router.post('/dynamic_system/resolve')
async def resolve_dynamic_system(
        dynamic_system: DynamicSystem,
) -> list[EquilibriumPoint]:
    equilibrium_points = oscillations.resolve_dynamic_system(
        first_function_text=dynamic_system.first_equation,
        second_function_text=dynamic_system.second_equation,
    )
    return [
        EquilibriumPoint(
            x=str(x),
            y=str(y),
            equilibrium_state=state
        )
        for (x, y), state in equilibrium_points
    ]


app.include_router(router)

frontend.init(app)
