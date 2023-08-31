import flet as ft
import requests
from .base_view import BaseView
from config import Config


class ParticipantCard(ft.UserControl, BaseView):
    PARTICIPANT_CARD_ENDPOINT: str = f"http://{Config.BASE_URL}/v1/participant"

    def build(self):

        self.first_name = ft.Text(value="default")
        self.last_name = ft.Text(value="default")

        self.view = ft.Column(
            width=600,
            controls=[
                self.first_name,
                self.last_name,
            ],
            alignment=ft.alignment.center
        )
        return self.view

    def initialize(self, *args, **kwargs):
        self.set_participant(*args, **kwargs)

    def clean(self):
        pass

    def set_participant(self, page: ft.Page, participant_id: int):
        response = requests.get(f"{self.PARTICIPANT_CARD_ENDPOINT}/{participant_id}")
        if response.status_code == 200:
            participants = response.json()
            self.first_name.value = participants.get("name")
            self.last_name.value = participants.get("id")
            self.first_name.update()
            self.last_name.update()
            page.update()
