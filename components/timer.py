import uuid
from datetime import datetime, time, timedelta
from time import sleep

import flet as ft

from components.types import ActiveTimerType, TimerType
from utils.sound import Sound

# [Timerの設計]
# 24時間以内の時間設定
# 時間が来たら音声を鳴らす
#
# [TimerのUI]
# 左右に要素を分ける
# # 左側にタイマーのリストを表示する
# # # 時間の短い順に上から並べる
# # 右側に現在実行されているタイマーを表示する
# # # タイマーが複数セットされている場合、そのうち時間の短いタイマーを表示する
#
# [Timer終了時の表示]
# PopUpでどのタイマーの時間が来たかを表示し、停止を促す
# 停止ボタンを押したら音声を止める
# 音声を止めたらPopUpを閉じる


class Timer:
    def __init__(self, sound: Sound, page: ft.Page):
        self._sound = sound
        self._page = page
        self.timers: list[TimerType] = []  # タイマーリスト
        self.timer_list = ft.Column(
            spacing=10,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
        self._save_button_disabled = False
        self.error_message = ft.Text(value="", size=12, color=ft.colors.RED)
        self.active_timer: ActiveTimerType | None = None
        self.active_timer_content = ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def check_timers(self) -> None:
        while True:
            if self.active_timer is None:
                continue
            if self.active_timer["active"]:
                sleep(1)
                if not self.active_timer["active"]:
                    continue
                if self.active_timer["time"] != time(hour=0, minute=0, second=0):
                    self.active_timer["time"] = (
                        datetime.combine(datetime.min, self.active_timer["time"])
                        - timedelta(seconds=1)
                    ).time()
                    self._update_active_timer_content()
                    self._page.update()
                    if self.active_timer["time"] == time(hour=0, minute=0, second=0):
                        self._sound.play_alarm_sound()
                        self._show_popup()
                        self._page.update()

    def _trigger_off_timer_display(self) -> None:
        if self.active_timer and self.active_timer["active"]:
            self.active_timer["active"] = False
            for t in self.timers:
                print("hoge============")
                if t["id"] == self.active_timer["id"]:
                    t["active"] = False
            self._update_timer_list()
            self._page.update()

    def _show_popup(self) -> None:
        """タイマー終了時のポップアップ表示"""
        if self.active_timer is None:
            return

        def stop_sound(_):
            if self.active_timer is None:
                return
            self._sound.stop_alarm_sound()
            popup.open = False
            self._trigger_off_timer_display()
            self._page.update()

        popup = ft.AlertDialog(
            modal=True,
            title=ft.Text("⏰ Timer Ended"),
            content=ft.Text(
                f"Timer '{self.active_timer['name']}' has reached the set time!",
                color=ft.colors.RED,
            ),
            actions=[
                ft.ElevatedButton(
                    text="Stop Sound",
                    bgcolor=ft.colors.RED,
                    color=ft.colors.WHITE,
                    on_click=stop_sound,
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        self._page.dialog = popup
        popup.open = True
        self._page.update()

    def _update_timer_list(self):
        """タイマーリストのUIを更新"""
        self.timer_list.controls.clear()

        for timer in sorted(self.timers, key=lambda t: t["time"]):
            time_str = []
            if timer["time"].hour != 0:
                time_str.append(f"{timer['time'].hour}時間")
            if timer["time"].minute != 0:
                time_str.append(f"{timer['time'].minute}分")
            if timer["time"].second != 0:
                time_str.append(f"{timer['time'].second}秒")
            formatted_time = "".join(time_str) if time_str else "0秒"

            timer_details = ft.Column(
                controls=[
                    ft.Text(
                        f"{timer['name']}",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE_GREY_900,
                        no_wrap=True,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        max_lines=1,
                        width=200,
                    ),
                    ft.Text(
                        f"⏳ {formatted_time}",
                        size=14,
                        color=ft.colors.BLUE_GREY_700,
                    ),
                ],
                spacing=2,
            )

            action_buttons = ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.PAUSE if timer["active"] else ft.icons.PLAY_ARROW,
                        icon_color=ft.colors.GREEN,
                        on_click=lambda _, timer=timer: self._toggle_timer(timer),
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        icon_color=ft.colors.RED,
                        on_click=lambda _, timer=timer: self._delete_timer(timer),
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
            )

            timer["widget"] = ft.Container(
                content=ft.Row(
                    controls=[timer_details, action_buttons],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=10,
                border_radius=8,
                bgcolor=ft.colors.BLUE_GREY_50,
                margin=ft.margin.symmetric(vertical=5, horizontal=10),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=3,
                    color=ft.colors.BLUE_GREY_200,
                ),
            )

            self.timer_list.controls.append(timer["widget"])

        self._page.update()

    def _update_active_timer(self, timer: TimerType) -> None:
        self.active_timer = {
            "id": timer["id"],
            "name": timer["name"],
            "time": timer["time"],
            "active": False,
        }

    def _update_active_timer_content(self):
        if self.active_timer is None:
            return
        self.active_timer_content.controls.clear()
        self.active_timer_content.controls.append(
            ft.Text(
                f"{self.active_timer['name']}",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.BLUE_GREY_900,
            )
        )
        self.active_timer_content.controls.append(
            ft.Text(
                f"{self.active_timer['time']}",
                size=20,
                color=ft.colors.BLUE_GREY_700,
            )
        )
        self._page.update()

    def _trigger_off_active_timer(self, id: str) -> None:
        if not self.active_timer:
            return
        if self.active_timer["id"] == id:
            self.active_timer["active"] = not self.active_timer["active"]
            self._update_active_timer_content()
            self._page.update()

    def _toggle_timer(self, timer: TimerType):
        """タイマーの動作を制御"""
        if not timer["active"]:
            for t in self.timers:
                t["active"] = False
            self._update_active_timer(timer)

        self._trigger_off_active_timer(timer["id"])

        timer["active"] = not timer["active"]
        self._update_timer_list()

    def _delete_timer(self, timer: TimerType):
        """タイマーを削除"""
        self.timers.remove(timer)
        self._trigger_off_active_timer(timer["id"])
        self._update_timer_list()

    def timer(self) -> ft.Container:
        def open_timer_popup(_):
            """タイマー設定ポップアップを表示"""

            # 入力フィールドと増減ボタン
            def create_field(label: str, initial_value: str) -> ft.Column:
                """フィールドと増減ボタンを作成"""
                value_field = ft.TextField(
                    value=initial_value,
                    width=60,
                    text_align=ft.TextAlign.CENTER,
                )

                def increase_value(_):
                    if not value_field.value:
                        return
                    current_value = int(value_field.value)
                    if label == "Hours":
                        if current_value < 23:  # 時間は最大23
                            current_value += 1
                        if current_value >= 24:
                            current_value = 23
                    elif label != "Hours":
                        if current_value < 59:  # 分・秒は最大59
                            current_value += 1
                        if current_value >= 60:
                            current_value = 59
                    value_field.value = f"{current_value:02}"  # 2桁表示
                    self._page.update()

                def decrease_value(_):
                    if not value_field.value:
                        return
                    current_value = int(value_field.value)
                    if current_value > 0:  # 最小値は0
                        current_value -= 1
                    if current_value < 0:
                        current_value = 0
                    value_field.value = f"{current_value:02}"  # 2桁表示
                    self._page.update()

                return ft.Column(
                    [
                        ft.IconButton(
                            icon=ft.icons.ARROW_DROP_UP,
                            icon_size=20,
                            on_click=increase_value,
                        ),
                        value_field,
                        ft.IconButton(
                            icon=ft.icons.ARROW_DROP_DOWN,
                            icon_size=20,
                            on_click=decrease_value,
                        ),
                    ],
                    spacing=0,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )

            hour_field = create_field("Hours", "00")
            minute_field = create_field("Minutes", "00")
            second_field = create_field("Seconds", "00")

            name_field = ft.TextField(
                label="Timer Name", value=f"Timer {len(self.timers) + 1}"
            )

            def save_timer(_):
                """タイマーを保存"""
                try:
                    # 入力値を取得
                    if (
                        not isinstance(hour_field.controls[1], ft.TextField)
                        or not isinstance(minute_field.controls[1], ft.TextField)
                        or not isinstance(second_field.controls[1], ft.TextField)
                    ):
                        return

                    hours = int(str(hour_field.controls[1].value))
                    minutes = int(str(minute_field.controls[1].value))
                    seconds = int(str(second_field.controls[1].value))

                    # 入力値をチェック
                    if (
                        hours < 0
                        or hours > 23
                        or minutes < 0
                        or minutes > 59
                        or seconds < 0
                        or seconds > 59
                    ) or (hours == 0 and minutes == 0 and seconds == 0):
                        self.error_message.value = "Invalid time entered!"
                        self._page.update()
                        return

                    timer_time = time(hour=hours, minute=minutes, second=seconds)
                    timer_name = (
                        name_field.value.strip()
                        if name_field.value
                        else f"Timer {len(self.timers) + 1}"
                    )

                    timer: TimerType = {
                        "id": str(uuid.uuid4()),
                        "name": timer_name,
                        "time": timer_time,
                        "active": False,
                        "widget": None,
                    }

                    # タイマーをリストに追加
                    self.timers.append(timer)
                    self._update_timer_list()
                    popup.open = False
                    self.error_message.value = ""
                    self._page.update()

                except ValueError:
                    # 無効な入力の場合のエラーメッセージ
                    self._page.snack_bar = ft.SnackBar(ft.Text("Invalid time entered!"))
                    self._page.snack_bar.open = True
                    self._page.update()

            def cancel_timer(_):
                """ポップアップを閉じる"""
                popup.open = False
                self.error_message.value = ""
                self._page.update()

            # ポップアップ内容
            popup = ft.AlertDialog(
                title=ft.Text("Add New Timer", text_align=ft.TextAlign.CENTER),
                content=ft.Column(
                    [
                        ft.Row(
                            controls=[
                                hour_field,
                                ft.Text(":"),
                                minute_field,
                                ft.Text(":"),
                                second_field,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        name_field,
                        self.error_message,
                    ],
                    spacing=10,
                ),
                actions=[
                    ft.ElevatedButton(
                        text="Save",
                        on_click=save_timer,
                        bgcolor=ft.colors.BLUE,
                        color=ft.colors.WHITE,
                        disabled=self._save_button_disabled,
                    ),
                    ft.TextButton(text="Cancel", on_click=cancel_timer),
                ],
            )
            self._page.dialog = popup
            popup.open = True
            self._page.update()

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "⏱  Timer Manager",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE,
                    ),
                    ft.ElevatedButton(
                        text="Set Timer",
                        icon=ft.icons.ALARM,
                        bgcolor=ft.colors.BLUE,
                        color=ft.colors.WHITE,
                        on_click=open_timer_popup,
                    ),
                    ft.Divider(height=1),
                    ft.Row(
                        [
                            self.timer_list,
                            ft.VerticalDivider(width=1),
                            self.active_timer_content,
                        ],
                        expand=True,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
        )
