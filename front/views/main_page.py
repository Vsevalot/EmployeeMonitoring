import flet as ft
from config import Config

from .base_view import BaseView


class MainPage(ft.UserControl, BaseView):

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

    def build(self):
        self.somthing = ft.TextField(label="somthing else")

        self.content = ft.Row(
            controls=[
                self.somthing
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        return self.content

    def initialize(self, *args, **kwargs):
        self.content.width = self.page.width
        self.page.update()
