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
        self.timers = []
        self.timer_list = ft.Column(
            spacing=10, expand=True, scroll=ft.ScrollMode.ADAPTIVE
        )
