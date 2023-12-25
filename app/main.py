from fastapi import FastAPI, APIRouter

from app.schemas import DynamicSystem, EquationSolution
from app import frontend
from app import oscillations

app = FastAPI()

router = APIRouter(prefix='/api')


@router.post('/dynamic_system/resolve')
async def resolve_dynamic_system(
        dynamic_system: DynamicSystem,
) -> EquationSolution:
    rs = oscillations.resolve_dynamic_system(
        first_equation=dynamic_system.first_equation,
        second_equation=dynamic_system.second_equation,
    )
    return EquationSolution(solutions=rs)


app.include_router(router)

frontend.init(app)