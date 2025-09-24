import flet as ft
from core.models import Disk

class DiskCard(ft.Card):
    def __init__(self, disk: Disk, on_edit_click, on_delete_click):
        super().__init__()
        self.disk = disk
        self.on_edit_click = on_edit_click
        self.on_delete_click = on_delete_click
        self.elevation = 1
        
        # Define la distribución de columnas para diferentes tamaños de pantalla
        self.col = {"xl": 4, "sm": 12, "md": 6} # 1, 2 o 3 tarjetas por fila

        self.content = self._build_card_content()
        self.set_color_based_on_free_space()
        

    def _get_card_color(self) -> str:
        if self.disk.free_space_gb <= 100:
            return ft.Colors.RED_700
        elif self.disk.free_space_gb > 600:
            return ft.Colors.GREEN_700
        else:
            return ft.Colors.AMBER_700 # Usaremos AMBER para el intermedio

    def set_color_based_on_free_space(self):
        self.color = self._get_card_color()
        if self.page: # Asegurarse de que el control esté en una página antes de actualizar
            self.page.update()

    def _build_card_content(self):
        # Barrita de progreso
        progress_bar = ft.ProgressBar(
            value = self.disk.usage_percentage / 100,
            color = ft.Colors.BLUE_ACCENT_200,
            bgcolor = ft.Colors.BLUE_GREY_100,
            height = 8
        )

        return ft.Container(
            content=ft.Column(
                controls= [
                    ft.Text(value= self.disk.name, weight=ft.FontWeight.BOLD, size=18),
                    ft.Divider(),
                    ft.Row(
                        controls= [
                            ft.Text(f"Capacidad: {self.disk.total_capacity_gb} GB"),
                            ft.VerticalDivider(),
                            ft.Text(f"Usado: {self.disk.used_space_gb} GB"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Text(f"Libre: {self.disk.free_space_gb} GB", weight= ft.FontWeight.W_500),
                    progress_bar,
                    ft.Text(f"Contenido: {', '.join(self.disk.contents)[:50]}...", size=12, color=ft.Colors.WHITE), # Resumen
                    ft.Row(
                        [
                            ft.IconButton(
                                icon= ft.Icons.EDIT,
                                tooltip= "Editar",
                                on_click= lambda e: self.on_edit_click(self.disk)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Eliminar",
                                on_click=lambda e: self.on_delete_click(self.disk.id)
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                spacing=8
            ),
            padding=15,
            expand=True,
            # width=300 # Ancho fijo para las tarjetas -> ELIMINADO
        )

# Variables importantes:
# - disk: El objeto Disk que esta tarjeta representa.
# - on_edit_click, on_delete_click: Callbacks (funciones) que se ejecutarán al hacer clic en los botones.
# Métodos importantes:
# - _get_card_color(): Determina el color de la tarjeta según el espacio libre.
# - set_color_based_on_free_space(): Aplica el color.
# - _build_card_content(): Construye la UI interna de la tarjeta.