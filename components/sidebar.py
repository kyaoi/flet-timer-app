import flet as ft


def sidebar() -> ft.NavigationRail:
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        group_alignment=-1,
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
