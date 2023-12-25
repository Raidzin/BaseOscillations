from fastapi import FastAPI
from nicegui import ui

from app.oscillations import resolve_dynamic_system


def init(fastapi_app: FastAPI) -> None:
    @ui.page('/site/m/dynamic_system')
    def dynamic_system():
        ui.query('body').style('background-color: #eeeeff;')
        ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet">')
        ui.page_title('Решение динамических систем')

        with ui.header().classes('justify-center'):
            with ui.row().classes('full-width max-w-screen-md justify-between'):
                ui.label('Решение динамических систем').classes('text-h6')

        with ui.footer().classes('justify-center'):
            with ui.row().classes('justify-center full-width max-w-screen-md'):
                ui.label('made by Alexey Goncharuk')

        with ui.row().classes('full-width justify-center'), ui.card().classes('w-full max-w-screen-md min-h-[80dvh]'):
            def get_result():
                points.clear()
                try:
                    resp = resolve_dynamic_system(f1.value, f2.value)
                except NotImplementedError:
                    ui.notify('Невозможно вычислить', type='negative')
                except Exception as error:
                    ui.notify('Ошибка вычислений', type='negative')
                with points:
                    for i, p in enumerate(resp[0]):
                        point(i, p, resp[1][i])

            with ui.column().classes('items-center full-width'):
                f1 = ui.input(
                    label='Первое уравнение',
                    value='x ** 3 + x * (y ** 2) - 10 * y',
                ).props('clearable').classes('full-width')
                f2 = ui.input(
                    label='Второе уравнение',
                    value='x + (x ** 2) * y + (y ** 3) - 7 * y',
                ).props('clearable').classes('full-width')
                ui.button('Рассчитать', on_click=get_result)
                points = ui.row().classes('full-width')

    ui.run_with(fastapi_app, storage_secret='secret123')


def point(i, point, res):
    with ui.card():
        x, y = point
        ui.label(res)
        ui.label(f'x{i}: {x}')
        ui.label(f'y{i}: {y}')
