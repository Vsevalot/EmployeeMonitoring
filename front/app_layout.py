import flet

from views import Login, MainPage, ManagerRegister
from flet import (
    Page,
    Row,
)


class AppLayout(Row):
    def __init__(self, page: Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page

        self.main_page = MainPage()
        self.login = Login()
        self.manager_register = ManagerRegister()

        self.alignment = flet.MainAxisAlignment.CENTER

        self.controls = [self.main_page, self.login, self.manager_register]

