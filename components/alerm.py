import time
from datetime import datetime, timedelta

import flet as ft

from utils.sound import Sound


class Alarm:
    def __init__(self, sound: Sound, page: ft.Page):
        self._sound = sound
        self._page = page
        self.alarms = []
        self.alarm_list = ft.Column(
            spacing=10, expand=True, scroll=ft.ScrollMode.ADAPTIVE
        )

    def check_alarms(self):
        while True:
            now = datetime.now()
            for alarm in self.alarms.copy():
                if alarm["active"] and now >= alarm["time"]:
                    alarm_text = ft.Text(
                        f"⏰ Alarm! It's {alarm['time'].strftime('%H:%M:%S')}",
                        color=ft.colors.RED,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    )
                    self._page.add(alarm_text)
                    self.show_stop_popup(alarm_text)
                    self._sound.play_alarm_sound()
                    self.alarms.remove(alarm)
                    self._page.update()
            time.sleep(1)

    def show_stop_popup(self, alarm_text):
        def stop_alarm(e):
            self._sound.stop_alarm_sound()
            popup.open = False
            if self._page.controls:
                self._page.controls.remove(alarm_text)
            self._page.update()

        popup = ft.AlertDialog(
            modal=True,
            title=ft.Text("⏰ Alarm!"),
            content=ft.Text("The alarm is ringing. Stop it?"),
            actions=[
                ft.ElevatedButton(
                    text="Stop Alarm",
                    on_click=stop_alarm,
                    bgcolor=ft.colors.RED,
                    color=ft.colors.WHITE,
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

        self._page.dialog = popup
        popup.open = True
        self._page.update()

    def alerm(self):
        def add_alarm(selected_time, alarm_to_edit=None):
            now = datetime.now()
            alarm_time = datetime.combine(now.date(), selected_time)

            if alarm_time < now:
                alarm_time += timedelta(days=1)

            if alarm_to_edit:
                alarm_to_edit["time"] = alarm_time
                alarm_to_edit[
                    "time_text"
                ].value = f"Alarm set for: {alarm_time.strftime('%H:%M:%S')}"
                self._page.update()
            else:
                alarm_text = ft.Text(
                    f"Alarm set for: {alarm_time.strftime('%H:%M:%S')}", size=16
                )
                alarm = {
                    "time": alarm_time,
                    "time_text": alarm_text,
                    "active": True,
                    "widget": None,
                }
                alarm["widget"] = ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Switch(
                                    value=True,
                                    on_change=lambda e, alarm=alarm: toggle_alarm(
                                        e, alarm
                                    ),
                                ),
                                ft.Container(
                                    content=alarm_text,
                                    padding=ft.Padding(5, 0, 0, 0),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    ft.icons.EDIT,
                                    icon_color=ft.colors.BLUE,
                                    tooltip="Edit Alarm",
                                    on_click=lambda e, alarm=alarm: edit_alarm(
                                        e, alarm
                                    ),
                                ),
                                ft.IconButton(
                                    ft.icons.DELETE,
                                    icon_color=ft.colors.RED,
                                    tooltip="Delete Alarm",
                                    on_click=lambda e, alarm=alarm: delete_alarm(
                                        e, alarm
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    width=400,
                    height=50,
                )
                self.alarms.append(alarm)
                self.alarm_list.controls.append(alarm["widget"])
                self._page.update()

        def toggle_alarm(e, alarm):
            alarm["active"] = e.control.value

        def delete_alarm(e, alarm):
            self.alarms.remove(alarm)
            self.alarm_list.controls.remove(alarm["widget"])
            self._page.update()

        def edit_alarm(e, alarm):
            nonlocal time_picker
            time_picker.on_change = lambda e: add_alarm(
                time_picker.value, alarm_to_edit=alarm
            )
            time_picker.open = True
            self._page.dialog = time_picker
            self._page.update()

        def handle_time_selected(e):
            if time_picker.value:
                add_alarm(time_picker.value)

        time_picker = ft.TimePicker(
            confirm_text="Set Alarm",
            error_invalid_text="Invalid time selected!",
            help_text="Pick the time for your alarm",
            on_change=handle_time_selected,
        )

        def open_time_picker(e):
            time_picker.on_change = handle_time_selected
            time_picker.open = True
            self._page.dialog = time_picker
            self._page.update()

        return ft.Column(
            [
                ft.Text(
                    "⏰ Alarm Manager",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLUE,
                ),
                ft.ElevatedButton(
                    text="Set Alarm",
                    icon=ft.icons.ALARM,
                    bgcolor=ft.colors.BLUE,
                    color=ft.colors.WHITE,
                    on_click=open_time_picker,
                ),
                self.alarm_list,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
