import flet as ft
from ui.components.disk_card import DiskCard
from ui.components.disk_form import DiskForm
from services.supabase_service import SupabaseService
from core.models import Disk
from typing import List
from core.models import Disk, ContentItem

class HomeView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.disk_service = SupabaseService()
        self.expand = True
        self.padding = 1 # Añadir padding general

        self._disk_cards_container = ft.ResponsiveRow(
            controls=[],
            run_spacing=15,
            spacing=15,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
        self._disk_form = DiskForm(
            on_save=self._handle_disk_save,
            on_clear=lambda: self._disk_form.clear_form(),
            on_delete=self._handle_disk_delete
        )

        # Estilo para los filtros
        filter_style = {
            "border_color": "transparent",
            "bgcolor": ft.Colors.WHITE10,
            "border_radius": 6,
            "expand": True
        }

        self._filter_name_input = ft.TextField(label="Buscar por Nombre", on_change=self._apply_filters, **filter_style)
        self._filter_content_input = ft.TextField(label="Buscar por Contenido", on_change=self._apply_filters, **filter_style)
        self._filter_free_space_slider = ft.Slider(
            min=0, max=1000, divisions=20, label="Espacio Libre Mínimo: {value} GB",
            on_change_end=self._apply_filters,
            value=0,
            active_color=ft.Colors.BLUE_ACCENT_400,
            inactive_color=ft.Colors.WHITE30
        )

        self.content = ft.Row(
            controls=[
                ft.Column(
                    [self._disk_form],
                    width=350,
                    spacing=20
                ),
                ft.VerticalDivider(width=20, color="transparent"),
                ft.Column(
                    [
                        ft.Text("Discos Registrados", size=24, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                self._filter_name_input,
                                self._filter_content_input,
                                ft.IconButton(icon=ft.Icons.REFRESH, on_click=self._refresh_disk_list, tooltip="Recargar Discos")
                            ],
                            spacing=10
                        ),
                        ft.Text("Filtrar por Espacio Libre:"),
                        self._filter_free_space_slider,
                        ft.Divider(height=10, color="transparent"),
                        ft.Column([self._disk_cards_container], scroll=ft.ScrollMode.ADAPTIVE, expand=True)
                    ],
                    expand=True,
                    spacing=15
                )
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START
        )

        self._update_disk_cards()

        # Dialogo de confirmación para eliminar
        self._confirm_delete_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text("¿Estás seguro de que quieres eliminar este disco?"),
            actions=[
                ft.TextButton("Sí", on_click=self._confirm_delete_action),
                ft.TextButton("No", on_click=self._cancel_delete_action),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._disk_to_delete_id = None

    def _update_disk_cards(self, disks_to_display=None):
        self._disk_cards_container.controls.clear()
        disks = disks_to_display if disks_to_display is not None else self.disk_service.get_all_disks()

        for disk in disks:
            self._disk_cards_container.controls.append(
                DiskCard(
                    disk=disk,
                    on_edit_click=self._handle_edit_disk,
                    on_delete_click=self._handle_disk_delete
                )
            )
        self.page.update()


    def _handle_edit_disk(self, disk: Disk):
        self._disk_form.load_disk_into_form(disk)

    def _handle_disk_save(self, disk_id: str, name: str, capacity: int, contents: List[ContentItem]):
        if disk_id:
            self.disk_service.update_disk(disk_id, name, capacity, contents)
        else:
            self.disk_service.add_disk(name, capacity, contents)
        self._update_disk_cards()

    def _handle_disk_delete(self, disk_id: str):
        self._disk_to_delete_id = disk_id
        # self._confirm_delete_dialog.open = True
        self.page.overlay.append(self._confirm_delete_dialog)
        self._confirm_delete_dialog.open = True
        self.page.update()

    def _confirm_delete_action(self, e):
        if self._disk_to_delete_id:
            self.disk_service.delete_disk(self._disk_to_delete_id)
            self._disk_to_delete_id = None
            self._update_disk_cards() # Actualiza la lista de discos
        self._confirm_delete_dialog.open = False
        self.page.update()
        self.page.overlay.pop()

    def _cancel_delete_action(self, e):
        self._disk_to_delete_id = None
        self._confirm_delete_dialog.open = False
        self.page.update()
        self.page.overlay.pop()

    def _apply_filters(self, e=None):
        name_query = self._filter_name_input.value
        content_query = self._filter_content_input.value
        min_free_gb = int(self._filter_free_space_slider.value) if self._filter_free_space_slider.value else 0

        filtered_disks = self.disk_service.filter_disks(
            name_query=name_query,
            content_query=content_query,
            min_free_gb=min_free_gb
        )
        self._update_disk_cards(disks_to_display=filtered_disks)

    def _refresh_disk_list(self, e):
        self._filter_name_input.value = ""
        self._filter_content_input.value = ""
        self._filter_free_space_slider.value = 0
        self._update_disk_cards()



# Variables importantes:
# - page: Referencia a la página de Flet, necesaria para actualizar la UI.
# - disk_service: Instancia del servicio de lógica de negocio.
# - _disk_cards_container: Contenedor donde se mostrarán todas las DiskCard.
# - _disk_form: Instancia del formulario para crear/editar.
# - Controles de filtrado: _filter_name_input, _filter_content_input, _filter_free_space_slider.
# Métodos importantes:
# - _load_initial_data(): Carga discos de ejemplo.
# - _update_disk_cards(): Reconstruye la lista de tarjetas en la UI.
# - _handle_edit_disk(), _handle_disk_save(), _handle_disk_delete(): Callbacks para el CRUD.
# - _apply_filters(): Ejecuta la lógica de filtrado y actualiza la UI.
# - _refresh_disk_list(): Resetea filtros y recarga la lista.