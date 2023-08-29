import flet as ft
import requests

from config import Config
from schemas import ManagerRegisterDTO, LoginResponseDTO
from .base_view import BaseView


class ManagerSelfRegistration(ft.UserControl, BaseView):
    REGISTER_ENDPOINT: str = f"http://{Config.BASE_URL}/api/v1/register/managers"

    def build(self):
        self.login_button = ft.TextButton(text="Reg", on_click=self.on_reg_click)

        self.first_name = ft.TextField(label="first_name", on_focus=self.on_focus)
        self.last_name = ft.TextField(label="last_name", on_focus=self.on_focus)
        self.surname = ft.TextField(label="surname", on_focus=self.on_focus)
        self.birthdate = ft.TextField(
            label="birthdate",
            hint_text="YYYY-MM-DD",
            on_focus=self.on_focus,
        )
        self.phone = ft.TextField(label="phone", on_focus=self.on_focus)
        self.position = ft.TextField(label="position", on_focus=self.on_focus)
        self.email = ft.TextField(label="email", on_focus=self.on_focus)
        self.password_field = ft.TextField(
            label="password",
            password=True,
            can_reveal_password=True,
            on_focus=self.on_focus)
        self.company = ft.TextField(label="company", on_focus=self.on_focus)
        self.department = ft.TextField(label="department", on_focus=self.on_focus)

        self.view = ft.Column(
            width=600,
            controls=[
                self.first_name,
                self.last_name,
                self.surname,
                self.birthdate,
                self.phone,
                self.position,
                self.email,
                self.password_field,
                self.company,
                self.department,
                self.login_button,
            ],
            alignment=ft.alignment.center
        )
        return self.view

    def on_focus(self, e: ft.ControlEvent):
        e.control.border_color = ft.colors.BLACK
        e.control.update()

    def clean(self):
        for control in self.view.controls:
            if control.__class__ == ft.TextField:
                control.value = ""
                control.border_color = ft.colors.BLACK
                control.update()

    def on_reg_click(self, e: ft.ControlEvent):
        for control in self.view.controls:
            if control.__class__ == ft.TextField:
                if control.value == "":
                    control.border_color = ft.colors.RED
                    control.update()

        body = ManagerRegisterDTO(
            first_name=self.first_name.value,
            last_name=self.last_name.value,
            surname=self.surname.value,
            birthdate=self.birthdate.value,
            phone=self.phone.value,
            position=self.position.value,
            email=self.email.value,
            password=self.password_field.value,
            company=self.company.value,
            department=self.department.value,
        )
        # self.clean()
        response = requests.post(self.REGISTER_ENDPOINT, json=body.dict())
        if response.status_code == 200:
            reg_response = LoginResponseDTO(**response.json())
            e.page.client_storage.set("access_token", reg_response.result)
            print(e.page.client_storage.get("access_token"))
            e.page.go("/main")
            e.page.update()

