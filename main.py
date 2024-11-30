import threading
import time
from datetime import datetime, timedelta

import flet as ft
import pygame

from components.sidebar import sidebar

pygame.mixer.init()


def play_alarm_sound():
    pygame.mixer.music.load("sound.wav")
    print("Playing alarm sound...")
    pygame.mixer.music.play(-1)


def stop_alarm_sound():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        print("Alarm sound stopped.")


def check_alarms(alarms, page):
    while True:
        now = datetime.now()
        for alarm in alarms.copy():
            if alarm["active"] and now >= alarm["time"]:
                alarm_text = ft.Text(
                    f"⏰ Alarm! It's {alarm['time'].strftime('%H:%M:%S')}",
                    color=ft.colors.RED,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                )
                page.add(alarm_text)
                show_stop_popup(page, alarm_text)
                play_alarm_sound()
                alarms.remove(alarm)
                page.update()
        time.sleep(1)


def show_stop_popup(page, alarm_text):
    def stop_alarm(e):
        stop_alarm_sound()
        popup.open = False
        page.controls.remove(alarm_text)
        page.update()

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

    page.dialog = popup
    popup.open = True
    page.update()


def main(page: ft.Page):
    page.title = "Alarm Manager"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    rail = sidebar()
    rail.on_change = lambda e: print("Success Click")
    alarms = []

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
            page.update()
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
                                on_change=lambda e, alarm=alarm: toggle_alarm(e, alarm),
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
                                on_click=lambda e, alarm=alarm: edit_alarm(e, alarm),
                            ),
                            ft.IconButton(
                                ft.icons.DELETE,
                                icon_color=ft.colors.RED,
                                tooltip="Delete Alarm",
                                on_click=lambda e, alarm=alarm: delete_alarm(e, alarm),
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
            alarms.append(alarm)
            alarm_list.controls.append(alarm["widget"])
            page.update()

    def toggle_alarm(e, alarm):
        alarm["active"] = e.control.value

    def delete_alarm(e, alarm):
        alarms.remove(alarm)
        alarm_list.controls.remove(alarm["widget"])
        page.update()

    def edit_alarm(e, alarm):
        nonlocal time_picker
        time_picker.on_change = lambda e: add_alarm(
            time_picker.value, alarm_to_edit=alarm
        )
        time_picker.open = True
        page.dialog = time_picker
        page.update()

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
        page.dialog = time_picker
        page.update()

    alarm_list = ft.Column(spacing=10, scroll=ft.ScrollMode.ADAPTIVE)

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column(
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
                        alarm_list,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
            ],
            expand=True,
        )
    )

    alarm_thread = threading.Thread(
        target=check_alarms, args=(alarms, page), daemon=True
    )
    alarm_thread.start()


ft.app(target=main)
