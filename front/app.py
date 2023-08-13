import flet
from app_layout import AppLayout
from views import Login, ManagerRegister, MainPage, ManagerInvite
from flet import (
    AppBar,
    Container,
    Icon,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    TemplateRoute,
    Text,
    UserControl,
    colors,
    icons,
    margin,
)


class App(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.on_route_change = self.route_change
        self.page.on_connect = self.route_change
        self.logout_profile_button = PopupMenuItem(text="Log out", on_click=self.logout)
        self.appbar_items = [
            self.logout_profile_button,
            PopupMenuItem(),  # divider
            PopupMenuItem(text="Settings"),
        ]
        self.appbar = AppBar(
            leading=Icon(icons.GRID_GOLDENRATIO_ROUNDED),
            leading_width=100,
            title=Text(f"Admin panel", font_family="Pacifico", size=32, text_align=flet.TextAlign.START),
            center_title=False,
            toolbar_height=75,
            bgcolor=colors.LIGHT_BLUE_ACCENT_700,
            actions=[
                Container(
                    content=PopupMenuButton(items=self.appbar_items),
                    margin=margin.only(left=50, right=25),
                )
            ],
        )
        self.page.appbar = self.appbar
        self.page.update()

    def build(self):
        self.layout: AppLayout = AppLayout(self.page)
        return Container(self.layout)

    def logout(self, e):
        if self.page.client_storage.get("access_token"):
            self.page.client_storage.set("access_token", 0)
            self.page.go("/login")

    def is_authorize(self):
        return bool(self.page.client_storage.get("access_token"))

    def hide_all(self):
        for layout in self.layout.controls:
            layout.visible = False
            layout.clean()
            layout.update()

    def show_view(self, view_type: UserControl.__class__, *args, **kwargs):
        for layout in self.layout.controls:
            if layout.__class__ == view_type:
                layout.visible = True
                layout.update()
                # TODO: layout.fill_fields(*args, **kwargs)

    def route_change(self, e):
        troute = TemplateRoute(self.page.route)

        self.hide_all()

        if troute.match("/main"):
            if self.is_authorize():
                self.show_view(MainPage)
            else:
                self.page.route = "/login"
            self.page.update()

        if troute.match("/login"):
            if self.is_authorize():
                self.page.route = "/main"
            else:
                self.show_view(Login)
            self.page.update()

        if troute.match("/register-manager"):
            if self.is_authorize():
                self.show_view(ManagerInvite)
            else:
                self.page.route = "/login"
            self.page.update()

        if troute.match("/manager-registration/:invite_id"):
            if self.is_authorize():
                self.page.route = "/main"
            else:
                self.show_view(ManagerRegister, getattr(troute, "invite_id"))
            self.page.update()
