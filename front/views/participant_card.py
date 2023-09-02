import flet as ft
import requests
from .base_view import BaseView
from config import Config


class ParticipantCard(ft.UserControl, BaseView):
    PARTICIPANT_STATS_ENDPOINT: str = f"http://{Config.BASE_URL}/api/v1/participants"

    def build(self):
        self.date_from = ft.TextField(label="date from", hint_text="YYYY-MM-DD")
        self.date_to = ft.TextField(label="date to", hint_text="YYYY-MM-DD")
        self.view = ft.Column(controls=[
            ft.Row(
                controls=[
                    self.date_from,
                    self.date_to,
                    ft.TextButton(text="Show", on_click=self.fill_chart)
                ]
            ),
        ])
        return self.view

    def initialize(self, *args, **kwargs):
        self._participant_id = kwargs.get("participant_id")
        pass

    def clean(self):
        try:
            if self.chart:
                self.page.controls.pop()
                self.chart = None
        except Exception:
            pass

    def fill_chart(self, e: ft.ControlEvent, date_from: str = "2000-01-01", date_to: str = "2025-01-01"):
        response = requests.get(
            self.PARTICIPANT_STATS_ENDPOINT + f"/{self._participant_id}/stats",
            headers={
                "Authorization": self.page.client_storage.get('access_token')
            },
            params={
                "date_from": self.date_from.value,
                "date_to": self.date_to.value,
            }
        )

        if response.status_code == 200:
            participant_stats = response.json()
            participant_stats = participant_stats.get("result")
            labels = [x.get("date") for x in participant_stats]
            morning_values = [ft.LineChartDataPoint(i + 1, x.get("morning").get("value")) for i, x in enumerate(participant_stats)]
            evening_values = [ft.LineChartDataPoint(i + 1, x.get("evening").get("value")) for i, x in enumerate(participant_stats)]

            data_1 = [
                ft.LineChartData(
                    data_points=morning_values,
                    stroke_width=8,
                    color=ft.colors.LIGHT_GREEN,
                    curved=True,
                    stroke_cap_round=True,
                ),
                ft.LineChartData(
                    data_points=evening_values,
                    color=ft.colors.PINK,
                    below_line_bgcolor=ft.colors.with_opacity(0, ft.colors.PINK),
                    stroke_width=8,
                    curved=True,
                    stroke_cap_round=True,
                ),
            ]

            labels = [ft.ChartAxisLabel(
                            value=i + 1,
                            label=ft.Container(
                                ft.Text(
                                    value,
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                                ),
                                margin=ft.margin.only(top=10),
                            ),
                        ) for i, value in enumerate(labels)][0:-1:int((len(labels) - 1)/2)]

            chart = ft.LineChart(
                data_series=data_1,
                border=ft.Border(
                    bottom=ft.BorderSide(10, ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE))
                ),
                left_axis=ft.ChartAxis(
                    labels=[
                        ft.ChartAxisLabel(
                            value=0,
                            label=ft.Text("0", size=14, weight=ft.FontWeight.BOLD),
                        ),
                        ft.ChartAxisLabel(
                            value=100,
                            label=ft.Text("100", size=14, weight=ft.FontWeight.BOLD),
                        ),
                        ft.ChartAxisLabel(
                            value=200,
                            label=ft.Text("200", size=14, weight=ft.FontWeight.BOLD),
                        ),
                        ft.ChartAxisLabel(
                            value=300,
                            label=ft.Text("300", size=14, weight=ft.FontWeight.BOLD),
                        ),
                        ft.ChartAxisLabel(
                            value=400,
                            label=ft.Text("400", size=14, weight=ft.FontWeight.BOLD),
                        ),
                    ],
                    labels_size=40,
                ),
                bottom_axis=ft.ChartAxis(
                    labels=labels,
                    labels_size=32,
                ),
                tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
                min_y=0,
                max_y=400,
                min_x=0,
                # max_x=14,
                # animate=5000,
                expand=True,
            )

            is_exists = False
            try:
                if self.chart:
                    is_exists = True
            except Exception:
                pass

            if is_exists:
                self.clean()

            participant_response = requests.get(
                self.PARTICIPANT_STATS_ENDPOINT + f"/{self._participant_id}",
                headers={
                    "Authorization": self.page.client_storage.get('access_token')
                }
            )
            participant = participant_response.json()
            participant = participant.get("result")

            self.chart = ft.Container(ft.Column(controls=[
                ft.Row(controls=[
                    ft.Text(participant.get("first_name"), size=25),
                    ft.Text(participant.get("last_name"), size=25),
                    ft.Text(participant.get("surname"), size=25),
                    ft.Text(participant.get("position"), size=25),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("Утро", size=70, color=ft.colors.LIGHT_GREEN),
                ft.Text("Вечер", size=70, color=ft.colors.PINK),
                ft.Container(chart),
            ]))

            self.page.add(self.chart)
            self.update()
            self.page.update()
