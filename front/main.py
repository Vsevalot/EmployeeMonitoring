import flet as ft
from app import App


def main(page: ft.Page):
    app = App(page)
    page.add(app)
    #TODO: добавить условие для дефолтной страницы
    page.go(page.route)
    page.update()


ft.app(target=main, port=8080, view=ft.AppView.WEB_BROWSER)
