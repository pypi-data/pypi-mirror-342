import flet as ft

import flet_easy as fs

app = fs.FletEasy(
    # route_prefix="/",
    route_init="/xd",
)


@app.view
async def view(data: fs.Datasy):
    return fs.Viewsy(
        appbar=ft.AppBar(title=ft.Text("Flet-Easy")),
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


@app.page("/xd")
async def home_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Home page"),
            ft.FilledButton("Go test", on_click=data.go("/test")),
            ft.FilledButton("close", on_click=lambda _: data.page.close()),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=data.view.appbar,
    )


@app.page("/test")
def test_page(data: fs.Datasy):
    data.view.appbar.title = ft.Text("Test page")
    return ft.View(
        controls=[
            ft.Text("Test page"),
            ft.FilledButton("x Go home", on_click=data.go_back()),
            ft.FilledButton("Go home", on_click=data.go("/xd")),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=data.view.appbar,
    )


""" print(len(app._pages))
print(app._view_config) """
app.run()
