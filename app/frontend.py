from asyncio import to_thread

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from nicegui import ui

from app.oscillations import resolve_dynamic_system

PAGE_TITLE = 'Решение динамических систем'

CANT_CALCULATE = 'Невозможно вычислить'
CALCULATE_ERROR = 'Ошибка вычислений'

FIRST_FUNCTION = 'Первая функция'
FIRST_FUNCTION_EXAMPLE = 'x ** 3 + x * (y ** 2) - 10 * y'
SECOND_FUNCTION = 'Вторая функция'
SECOND_FUNCTION_EXAMPLE = 'x + (x ** 2) * y + (y ** 3) - 7 * y'

CALCULATE = 'Рассчитать'


def init(fastapi_app: FastAPI) -> None:
    @ui.page('/')
    def main_page():
        return RedirectResponse('/site/m/dynamic_system')

    @ui.page('/site/m/dynamic_system')
    def dynamic_system():
        ui.query('body').style('background-color: #eeeeff;')
        ui.page_title(PAGE_TITLE)

        with ui.header().classes('justify-center'):
            with ui.row().classes(
                    'full-width max-w-screen-md justify-between'):
                ui.label(PAGE_TITLE).classes('text-h6')

        with ui.footer().classes('justify-center'):
            with ui.row().classes('justify-center full-width max-w-screen-md'):
                ui.label('made by Alexey Goncharuk')

        with (
            ui.row().classes('full-width justify-center'),
            ui.card().classes('w-full max-w-screen-md min-h-[80dvh]'),
        ):
            async def get_result():
                points_container.clear()
                b.props('loading')
                try:
                    points = await to_thread(
                        resolve_dynamic_system,
                        f1.value,
                        f2.value,
                    )
                except NotImplementedError as error:
                    ui.notify(CANT_CALCULATE, type='negative')
                    raise error
                except Exception as error:
                    ui.notify(CALCULATE_ERROR, type='negative')
                    raise error
                finally:
                    b.props(remove='loading')
                with points_container:
                    for point, state in points:
                        ui_point(point, state)

            with ui.column().classes('items-center full-width'):
                f1 = ui.input(
                    label=FIRST_FUNCTION,
                    value=FIRST_FUNCTION_EXAMPLE,
                ).props('clearable').classes('full-width')
                f2 = ui.input(
                    label=SECOND_FUNCTION,
                    value=SECOND_FUNCTION_EXAMPLE,
                ).props('clearable').classes('full-width')
                b = ui.button(CALCULATE, on_click=get_result)
                points_container = ui.row().classes('full-width')

    ui.run_with(fastapi_app, storage_secret='secret123')


def ui_point(point, state):
    with ui.card():
        x, y = point
        ui.label(state).classes('self-center')
        ui.separator()
        ui.label(f'x: {x}')
        ui.label(f'y: {y}')
