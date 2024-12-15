from datetime import datetime, time
from typing import TypedDict

import flet as ft


class AlarmType(TypedDict):
    time: datetime
    time_text: ft.Text
    active: bool
    widget: ft.Row | None


class TimerType(TypedDict):
    id: str
    name: str
    time: time
    active: bool
    widget: ft.Container | None


class ActiveTimerType(TypedDict):
    id: str
    name: str
    time: time
    active: bool
