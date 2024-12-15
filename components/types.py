from datetime import datetime
from typing import TypedDict

import flet as ft


class AlarmType(TypedDict):
    time: datetime
    time_text: ft.Text
    active: bool
    widget: ft.Row | None
