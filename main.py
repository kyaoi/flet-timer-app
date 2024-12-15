import threading

import flet as ft

from components.alarm import Alarm
from components.sidebar import sidebar
from components.timer import Timer
from utils.sound import Sound

sound = Sound()


def main(page: ft.Page):
    page.title = "Alarm Manager"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    selected_index = 0
    alarm = Alarm(sound, page)
    timer = Timer(sound, page)
    content = ft.Container(
        expand=True,
    )
    content.content = alarm.alarm()

    def on_change(e: ft.ControlEvent):
        nonlocal selected_index
        selected_index = e.control.selected_index
        if selected_index == 0:
            content.content = alarm.alarm()
        else:
            content.content = timer.timer()
        page.update()

    rail = sidebar(on_change)
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                content,
            ],
            expand=True,
        )
    )

    alarm_thread = threading.Thread(target=alarm.check_alarms, daemon=True)
    alarm_thread.start()


ft.app(target=main)
