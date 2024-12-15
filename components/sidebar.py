import flet as ft


def sidebar(func) -> ft.NavigationRail:
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=50,
        min_extended_width=100,
        group_alignment=-1,
        on_change=func,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.AV_TIMER_OUTLINED,
                selected_icon=ft.icons.AV_TIMER,
                label="Alarm",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.TIMER_OUTLINED,
                selected_icon=ft.icons.TIMER,
                label="Stop Watch",
            ),
        ],
    )

    return rail
