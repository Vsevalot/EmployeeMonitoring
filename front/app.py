import flet
from app_layout import AppLayout
from views import (
    Login,
    ManagerRegister,
    MainPage,
    ManagerInvite,
    Participants,
    ParticipantCard,
    ManagerSelfRegistration,
    ParticipantsStat,
)
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
    TextButton,
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
        button_text_style = {
            flet.MaterialState.HOVERED: flet.colors.BLACK,
            flet.MaterialState.DEFAULT: flet.colors.WHITE,
        }
        bg_button_style = {
            flet.MaterialState.HOVERED: flet.colors.WHITE,
        }

        self.appbar = AppBar(
            leading=Icon(icons.GRID_GOLDENRATIO_ROUNDED),
            leading_width=100,
            title=Text(f"Admin panel", font_family="Pacifico", size=32, text_align=flet.TextAlign.START),
            center_title=False,
            toolbar_height=75,
            bgcolor=colors.LIGHT_BLUE_ACCENT_700,
            actions=[
                Container(
                    content=TextButton(
                        text="Регистрация",
                        style=flet.ButtonStyle(
                            color=button_text_style,
                            bgcolor=bg_button_style
                        ),
                        on_click=self.on_reg_click
                    ),
                ),
                Container(
                    content=TextButton(
                        text="Авторизация",
                        style=flet.ButtonStyle(
                            color=button_text_style,
                            bgcolor=bg_button_style
                        ),
                        on_click=self.on_auth_clik
                    ),
                ),
                Container(
                    content=TextButton(
                        text="Список участников",
                        style=flet.ButtonStyle(
                            color=button_text_style,
                            bgcolor=bg_button_style
                        ),
                        on_click=self.on_participants_click
                    ),
                ),
                Container(
                    content=PopupMenuButton(items=self.appbar_items),
                    margin=margin.only(left=50, right=25),
                ),
            ],
        )
        self.page.appbar = self.appbar
        self.page.update()

    def on_reg_click(self, e: flet.ControlEvent):
        e.page.route = "/register/managers"
        e.page.update()

    def on_auth_clik(self, e: flet.ControlEvent):
        e.page.route = "/login"
        e.page.update()

    def on_participants_click(self, e: flet.ControlEvent):
        e.page.route = "/participants"
        e.page.update()

    def build(self):
        self.layout: AppLayout = AppLayout(self.page)
        return Container(self.layout)

    def logout(self, e):
        if self.page.client_storage.get("access_token"):
            self.page.client_storage.set("access_token", 0)
            self.page.go("/login")
            self.page.update()

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
                layout.initialize(*args, **kwargs)
                break

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

        if troute.match("/manager-invite"):
            if self.is_authorize():
                self.show_view(ManagerInvite)
            else:
                self.page.route = "/login"
            self.page.update()

        if troute.match("/participants"):
            if self.is_authorize():
                self.show_view(Participants, self.page)
            else:
                self.page.route = "/login"
            self.page.update()

        if troute.match("/participants/:participant_id"):
            try:
                participant_id = int(getattr(troute, "participant_id"))
                if self.is_authorize():
                    self.show_view(ParticipantCard, self.page, participant_id)
                else:
                    self.page.route = "/login"
                self.page.update()
            except ValueError:
                pass

        if troute.match("/register/managers"):
            if self.is_authorize():
                self.show_view(MainPage)
            else:
                self.show_view(ManagerSelfRegistration, self.page)
            self.page.update()

        if troute.match("/participants/stats"):
            if self.is_authorize():
                self.show_view(ParticipantsStat, self.page)
            else:
                self.page.route = "/login"
            self.page.update()

        if troute.match("/manager-registration/:invite_id"):
            if self.is_authorize():
                self.page.route = "/main"
            else:
                self.show_view(ManagerRegister, getattr(troute, "invite_id"))
            self.page.update()
