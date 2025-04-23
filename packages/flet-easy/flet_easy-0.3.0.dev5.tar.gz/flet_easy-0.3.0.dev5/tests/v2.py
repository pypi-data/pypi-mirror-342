import flet as ft

import flet_easy as fs

app = fs.FletEasy()


@app.page("/")
async def home_page(data: fs.Datasy):
    return ft.View(
        controls=[ft.Text("Home page")],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


app.run()
