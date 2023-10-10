import flet as ft
import requests
from .base_view import BaseView
from config import Config


class ParticipantsStat(ft.UserControl, BaseView):
    GROUP_STATS_ENDPOINT: str = f"http://{Config.BASE_URL}/api/v1/participants/stats"
    PARTICIPANT_ME_ENDPOINT: str = f"http://{Config.BASE_URL}/api/v1/participants/me"

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
            self.GROUP_STATS_ENDPOINT,
            headers={
                "Authorization": self.page.client_storage.get('access_token')
            },
            params={
                "date_from": self.date_from.value,
                "date_to": self.date_to.value,
            }
        )
        chart = ft.BarChart(
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(
                labels_size=40, title=ft.Text("Количество голосов"), title_size=40
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300),
            max_y=110,
            interactive=True,
            expand=True,
        )
        if response.status_code == 200:
            stats = response.json()
            stats = stats.get("result")
            bar_groups = []
            labels = []
            for i, group in enumerate(stats):
                category = group.get("category")
                voted = group.get("voted")
                labels.append(ft.ChartAxisLabel(
                    value=i,
                    label=ft.Container(ft.Text(category), padding=10)
                ))
                bar_groups.append(
                    ft.BarChartGroup(
                        x=i,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=int(voted),
                                width=40,
                                color=ft.colors.AMBER,
                                tooltip=f"{category}, {voted}",
                                border_radius=0
                            )
                        ]
                    )
                )
            chart.bar_groups = bar_groups
            chart.bottom_axis = ft.ChartAxis(labels=labels, labels_size=40)

            is_exists = False
            try:
                if self.chart:
                    is_exists = True
            except Exception:
                pass

            if is_exists:
                self.clean()

            participant_response = requests.get(
                self.PARTICIPANT_ME_ENDPOINT,
                headers={
                    "Authorization": self.page.client_storage.get('access_token')
                }
            )
            me = participant_response.json()
            me = me.get("result")

            self.chart = ft.Container(chart)
            self.chart = ft.Container(ft.Column(controls=[
                ft.Row(controls=[
                    ft.Text(me.get("company"), size=25),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(chart),
            ]))

            self.page.add(self.chart)

            self.update()
            self.page.update()
