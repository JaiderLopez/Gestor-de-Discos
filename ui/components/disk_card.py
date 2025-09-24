import flet as ft
from core.models import Disk

class DiskCard(ft.Card):
    def __init__(self, disk: Disk, on_edit_click, on_delete_click):
        super().__init__()
        self.disk = disk
        self.on_edit_click = on_edit_click
        self.on_delete_click = on_delete_click
        
        self.col = {"xs": 12, "sm": 6, "md": 4}
        self.elevation = 4
        self.content = self._build_card_content()

    def _get_status_color(self) -> str:
        usage = self.disk.usage_percentage
        if usage > 80:
            return ft.Colors.RED_600
        elif usage > 50:
            return ft.Colors.AMBER_700
        else:
            return ft.Colors.GREEN_600

    def _build_card_content(self):
        status_color = self._get_status_color()

        progress_bar = ft.ProgressBar(
            value=self.disk.usage_percentage / 100,
            color=status_color,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
            height=6
        )

        content_summary = ", ".join(item.description for item in self.disk.contents)

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(self.disk.name, weight=ft.FontWeight.BOLD, size=16),
                    ft.Text(f"{self.disk.free_space_gb} GB Libres", size=12, color=ft.Colors.WHITE70),
                    ft.Text(f"Contenido: {content_summary[:40]}...", size=11, color=ft.Colors.WHITE54, italic=True),
                    progress_bar,
                    ft.Row(
                        [
                            ft.Text(f"{self.disk.used_space_gb} GB / {self.disk.total_capacity_gb} GB", size=10, color=ft.Colors.WHITE54),
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT_OUTLINED,
                                    tooltip="Editar",
                                    on_click=lambda e: self.on_edit_click(self.disk),
                                    icon_size=18,
                                    icon_color=ft.Colors.WHITE70
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    tooltip="Eliminar",
                                    on_click=lambda e: self.on_delete_click(self.disk.id),
                                    icon_size=18,
                                    icon_color=ft.Colors.WHITE70
                                ),
                            ])
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ],
                spacing=6
            ),
            padding=12,
            border=ft.border.only(left=ft.border.BorderSide(5, status_color)),
            border_radius=ft.border_radius.all(6)
        )


# Variables importantes:
# - disk: El objeto Disk que esta tarjeta representa.
# - on_edit_click, on_delete_click: Callbacks (funciones) que se ejecutarán al hacer clic en los botones.
# Métodos importantes:
# - _get_card_color(): Determina el color de la tarjeta según el espacio libre.
# - set_color_based_on_free_space(): Aplica el color.
# - _build_card_content(): Construye la UI interna de la tarjeta.