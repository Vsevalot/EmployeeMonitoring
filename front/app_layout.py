import flet

from views import (
    Login,
    MainPage,
    ManagerRegister,
    ManagerInvite,
    Participants,
    ParticipantCard,
    ManagerSelfRegistration,
    ParticipantsStat
)
from flet import (
    Page,
    Row,
)


class AppLayout(Row):
    def __init__(self, page: Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page

        self.main_page = MainPage(self.page)

        self.login = Login()
        self.login.visible = False
        self.manager_register = ManagerRegister()
        self.manager_register.visible = False
        self.manager_invite = ManagerInvite()
        self.manager_invite.visible = False
        self.manager_self_registration = ManagerSelfRegistration()
        self.manager_self_registration.visible = False

        self.participants = Participants()
        self.participants.visible = False
        self.participant_card = ParticipantCard()
        self.participant_card.visible = False

        self.participants_stat = ParticipantsStat()
        self.participants_stat.visible = False

        self.alignment = flet.MainAxisAlignment.CENTER

        # self.wrap = True

        self.controls = [
            self.main_page,
            self.login,
            self.manager_register,
            self.manager_invite,
            self.participants,
            self.participant_card,
            self.manager_self_registration,
            self.participants_stat,
        ]

