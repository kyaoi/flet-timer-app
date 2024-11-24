import flet as ft


class Timer:
    def __init__(self):
        pass

    def build(self):
        return ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Timer App",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLACK,
                        text_align=ft.TextAlign.CENTER,
                    )
                ),
                ft.Container(
                    content=ft.Text(
                        "Test Text",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLACK,
                        text_align=ft.TextAlign.CENTER,
                    )
                )
            ]
        )

def main(page: ft.Page):
    page.title = "Timer App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    timer = Timer()
    page.add(timer.build())


ft.app(target=main)
