import flet as ft
from config import Config


class MainPage(ft.UserControl):

    def build(self):
        self.somthing = ft.TextField(label="somthing else")

        return ft.Column(
            width=600,
            controls=[
                self.somthing
            ],
            alignment=ft.alignment.center
        )


