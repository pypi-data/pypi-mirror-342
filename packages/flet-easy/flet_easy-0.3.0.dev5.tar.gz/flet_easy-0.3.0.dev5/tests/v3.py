import flet as ft


def get_key(page: ft.Page):
    page.client_storage.set("key", "value-123")
    return page.client_storage.get("key")
    """ await page.client_storage.set_async("key", "value-123")
    return await page.client_storage.get_async("key") """
    # return page.run_task(page.client_storage.get_async, "key").result()


def view_append(page: ft.Page):
    print("routes", page.route)
    if page.route == "/":
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text(f"Flet app- {get_key(page)}"), bgcolor=ft.Colors.RED),
                    # ft.AppBar(
                    #    title=ft.Text(f"Flet app- {page.run_task(get_key, page).result(5)}"),
                    #    bgcolor=ft.Colors.SURFACE,
                    # ),
                    ft.ElevatedButton(
                        "Visit Store",
                        on_click=lambda _: page.go(route="/store", skip_route_change_event=True),
                    ),
                ],
            )
        )
    if page.route == "/store":
        page.views.append(
            ft.View(
                "/store",
                [
                    ft.AppBar(
                        automatically_imply_leading=False,
                        title=ft.Text("Store"),
                        bgcolor=ft.Colors.RED,
                    ),
                    ft.ElevatedButton(
                        "Go Home", on_click=lambda _: page.go("/", skip_route_change_event=True)
                    ),
                ],
            )
        )


async def main(page: ft.Page):
    page.title = "Routes Example"
    page.views.clear()

    def route_change(route):
        # page.views.clear()
        # = asyncio.get_event_loop()
        view_append(page)

        page.update()

    def view_pop(view):
        # page.views.clear()
        page.views.pop()
        print("views", page.views)
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(main)
