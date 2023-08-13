import flet as ft
from config import Config


class ManagerRegister(ft.UserControl):
    REGISTER_ENDPOINT: str = f"http://{Config.BASE_URL}/v1/manager-registration"

    def build(self):
        self.login_button = ft.TextButton(text="Reg", on_click=self.on_reg_click)

        self.first_name = ft.TextField(label="first_name", on_focus=self.on_focus)
        self.last_name = ft.TextField(label="last_name", on_focus=self.on_focus)
        self.surname = ft.TextField(label="surname", on_focus=self.on_focus)
        self.birthdate = ft.TextField(
            label="birthdate",
            hint_text="DD.MM.YYYY",
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
