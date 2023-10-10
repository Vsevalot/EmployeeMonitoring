import flet as ft
import requests
from .base_view import BaseView
from config import Config


class Participants(ft.UserControl, BaseView):
    PARTICIPANTS_ENDPOINT: str = f"http://{Config.BASE_URL}/api/v1/participants"

    def build(self):

        self.view = ft.Column(
            controls=[
                ft.Container(content=ft.Row(controls=[ft.TextButton("Посмотреть статистику по группам", on_click=self.on_stats_click)], alignment=ft.MainAxisAlignment.CENTER)),
                ft.Container(content=ft.Row(controls=[], wrap=True), alignment=ft.alignment.center),
            ]
        )
        return self.view

    def initialize(self, *args, **kwargs):
        self.set_all_participants(*args, **kwargs)

    def clean(self):
        pass

    def on_stats_click(self, e: ft.ControlEvent):
        e.page.go("/participants/stats")

    def on_participant_click(self, e: ft.ControlEvent):
        e.page.go(f"/participants/{e.control.data}/stats")

    def set_all_participants(self, page: ft.Page):
        response = requests.get(
            self.PARTICIPANTS_ENDPOINT,
            headers={
                "Authorization": page.client_storage.get('access_token')
            },
        )
        for container in self.view.controls:
            container.content.width = page.width

        self.view.controls[1].content.controls.clear()
        if response.status_code == 200:
            participants = response.json()
            participants = participants.get("result")
            for participant in participants:
                self.view.controls[1].content.controls.append(
                    ft.TextButton(
                        text=f"{participant.get('first_name')} {participant.get('last_name')}",
                        data=participant.get('id'),
                        width=100,
                        height=100,
                        on_click=self.on_participant_click,
                    )
                )
            self.update()
            page.update()
