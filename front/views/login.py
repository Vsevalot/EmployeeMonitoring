import flet as ft
from schemas import LoginRequestDTO, LoginResponseDTO
import requests
from config import Config


class Login(ft.UserControl):
    LOGIN_ENDPOINT: str = f"http://{Config.BASE_URL}/v1/login"

    def build(self):
        self.login_button = ft.ElevatedButton(text="Login", on_click=self.on_login_click)
        self.login_field = ft.TextField(label="login")
        self.password_field = ft.TextField(label="password", password=True, can_reveal_password=True)

        return ft.Column(
            width=600,
            controls=[
                self.login_field,
                self.password_field,
                ft.Row(controls=[
                    self.login_button
                ])
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )

    def clean(self):
        self.login_field.value = ""
        self.login_field.update()
        self.password_field.value = ""
        self.password_field.update()

    def on_login_click(self, e: ft.ControlEvent):
        body = LoginRequestDTO(email=self.login_field.value, password=self.password_field.value)
        self.clean()
        response = requests.get(self.LOGIN_ENDPOINT, json=body.dict())
        if response.status_code == 200:
            login_response = LoginResponseDTO(**response.json())
            e.page.client_storage.set("access_token", login_response.res)
            print(e.page.client_storage.get("access_token"))
            e.page.go("/main")
            e.page.update()


