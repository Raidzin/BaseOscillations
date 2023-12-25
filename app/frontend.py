from fastapi import FastAPI
from nicegui import ui
from sympy import pretty

from app.oscillations import resolve_dynamic_system


def init(fastapi_app: FastAPI) -> None:
    @ui.page('/site/m/dynamic_system')
    def dynamic_system():
        ui.query('body').style('background-color: #eeeeff;')
        ui.page_title('Решение динамических систем')
        with ui.row().classes('full-width justify-center'), ui.card().classes('w-full max-w-screen-md min-h-[95dvh]'):
            def get_result():
                points.clear()
                try:
                    resp = resolve_dynamic_system(f1.value, f2.value)
                except Exception as error:
                    ui.notify('Ошибка вычислений', type='negative')
                    raise error
                with points:
                    for i, p in enumerate(resp[0]):
                        point(i, p, resp[1][i])

            with ui.column().classes('items-center full-width'):
                f1 = ui.input(
                    label='Первое уравнение',
                    value='x ** 3 + x * (y ** 2) - 10 * y',
                ).classes('full-width')
                f2 = ui.input(
                    label='Второе уравнение',
                    value='x + (x ** 2) * y + (y ** 3) - 7 * y',
                ).classes('full-width')
                ui.button('Рассчитать', on_click=get_result)
                points = ui.row().classes('full-width')

    ui.run_with(fastapi_app, storage_secret='secret123')


def point(i, point, res):
    with ui.card():
        x, y = point
        ui.label(res)
        ui.label(f'x{i}: {x}')
        ui.label(f'y{i}: {y}')
