import flet as ft
from app import App


def main(page: ft.Page):
    page.client_storage.set("access_token", 0)
    app = App(page)
    page.add(app)
    page.go("/login")
    page.update()


ft.app(target=main, port=8080, view=ft.AppView.WEB_BROWSER)
