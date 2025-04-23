import asyncio

import flet as ft
import pytest

import flet_easy as fs


@pytest.fixture
def app():
    appx = fs.FletEasy()

    @appx.config
    def configx(page: ft.Page):
        page.run_task(exit_app, page)

    appx.run()

    return appx


async def exit_app(page: ft.Page):
    for i in range(2):
        print(i)
        await asyncio.sleep(1)
    page.window.destroy()


def test_view(app: fs.FletEasy):
    def index(data: fs.Datasy):
        return ft.View(
            controls=[ft.Text("Home page")],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    app.add_routes([fs.Pagesy("/", index)])

    assert len(app._pages) == 1


def test_view_config(app: fs.FletEasy):
    @app.view
    def view(data: fs.Datasy):
        return fs.Viewsy(
            appbar=ft.AppBar(title=ft.Text("Flet-Easy")),
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    assert app._view_config is not None
