import time
from datetime import datetime, timedelta

import flet as ft

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
        self.timers = []  # タイマーリスト
        self.timer_list = ft.Column(
            spacing=10, expand=True, scroll=ft.ScrollMode.ADAPTIVE
        )
        self._save_button_disabled = False
        self.error_message = ft.Text(value="", size=12, color=ft.colors.RED)

    def check_timers(self):
        while True:
            now = datetime.now()
            # 時間の短い順にソート
            self.timers.sort(key=lambda t: t["time"])
            for timer in self.timers.copy():
                if now >= timer["time"]:
                    self.show_popup(timer)
                    self._sound.play_alarm_sound()
                    self.timers.remove(timer)
                    self.update_timer_list()
            time.sleep(1)

    def show_popup(self, timer):
        """タイマー終了時のポップアップ表示"""

        def stop_sound(e):
            self._sound.stop_alarm_sound()
            popup.open = False
            self._page.update()

        popup = ft.AlertDialog(
            modal=True,
            title=ft.Text("⏰ Timer Ended"),
            content=ft.Text(
                f"Timer '{timer['name']}' has reached the set time!",
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

    def update_timer_list(self):
        """タイマーリストのUIを更新"""
        self.timer_list.controls.clear()
        for timer in sorted(self.timers, key=lambda t: t["time"]):
            timer_text = ft.Row(
                controls=[
                    ft.Text(f"Name: {timer['name']}\nTime: {str(timer['time'])}"),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        icon_color=ft.colors.RED,
                        on_click=lambda e, timer=timer: self.delete_timer(timer),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            self.timer_list.controls.append(timer_text)
        self._page.update()

    def delete_timer(self, timer):
        """タイマーを削除"""
        self.timers.remove(timer)
        self.update_timer_list()

    def timer(self):
        def open_timer_popup(e):
            """タイマー設定ポップアップを表示"""

            # 入力フィールドと増減ボタン
            def create_field(label, initial_value):
                """フィールドと増減ボタンを作成"""
                value_field = ft.TextField(
                    value=initial_value,
                    width=60,
                    text_align=ft.TextAlign.CENTER,
                )

                def increase_value(e):
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

                def decrease_value(e):
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

            def save_timer(e):
                """タイマーを保存"""
                try:
                    # 入力値を取得
                    hours = int(hour_field.controls[1].value)
                    minutes = int(minute_field.controls[1].value)
                    seconds = int(second_field.controls[1].value)

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

                    timer_time = timedelta(
                        hours=hours, minutes=minutes, seconds=seconds
                    )
                    timer_name = (
                        name_field.value.strip()
                        if name_field.value
                        else f"Timer {len(self.timers) + 1}"
                    )

                    # タイマーをリストに追加
                    self.timers.append({"name": timer_name, "time": timer_time})
                    self.update_timer_list()
                    popup.open = False
                    self.error_message.value = ""
                    self._page.update()

                except ValueError:
                    # 無効な入力の場合のエラーメッセージ
                    self._page.snack_bar = ft.SnackBar(ft.Text("Invalid time entered!"))
                    self._page.snack_bar.open = True
                    self._page.update()

            def cancel_timer(e):
                """ポップアップを閉じる"""
                popup.open = False
                self.error_message.value = ""
                self._page.update()

            # ポップアップ内容
            popup = ft.AlertDialog(
                modal=True,
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
                            ft.Column(
                                spacing=10,
                                expand=True,
                                scroll=ft.ScrollMode.ADAPTIVE,
                            ),
                        ],
                        expand=True,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
        )
