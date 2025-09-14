import flet as ft
from ui.components.disk_card import DiskCard
from ui.components.disk_form import DiskForm
from services.disk_service import DiskService
from core.models import Disk
import asyncio

class HomeView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.disk_service = DiskService() # Instancia del servicio de discos
        self.expand = True # Para que ocupe todo el espacio disponible
                        
        self._disk_cards_container = ft.ResponsiveRow(controls=[],
                                                      run_spacing= {"xs": 10}, spacing= {"xs": 10}, vertical_alignment= ft.CrossAxisAlignment.START) # Contenedor para las tarjetas
        self._disk_form = DiskForm(
            on_save=self._handle_disk_save,
            on_clear=lambda: self._disk_form.clear_form(),
            on_delete=self._handle_disk_delete
        )

        # Controles de filtrado
        self._filter_name_input = ft.TextField(label="Search by Name", on_change=self._apply_filters, expand=True)
        self._filter_content_input = ft.TextField(label="Search by Content", on_change=self._apply_filters, expand=True)
        self._filter_free_space_slider = ft.Slider(
            min= 0, max= 1000, divisions= 10, label="Espacio Libre Mínimo: {value} GB",
            on_change_end=self._apply_filters,
            value= 0, # Valor inicial
            expand= True
        )

        self.content = ft.Row(
            controls= [
                # Columna izquierda: Formulario de gestión
                ft.Column(
                    [
                        self._disk_form
                    ],
                    width=400,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.VerticalDivider(),
                # Columna derecha: Listado de discos y filtros
                ft.Column(
                    [
                        ft.Text("Discos Registrados", size=24, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                self._filter_name_input,
                                self._filter_content_input,
                                ft.IconButton(icon=ft.Icons.REFRESH, on_click=self._refresh_disk_list, tooltip="Recargar Discos")
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),
                        ft.Text("Filtrar por Espacio Libre:", size=14),
                        self._filter_free_space_slider,
                        ft.Divider(),
                        self._disk_cards_container
                    ],
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    scroll=ft.ScrollMode.ADAPTIVE # Habilita el scroll si hay muchas tarjetas
                )
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START
        )

        self._load_initial_data() # Cargar algunos datos de ejemplo al iniciar
        # print("cargar datos iniciales...")

    def _load_initial_data(self):
        # Datos de ejemplo
        self.disk_service.add_disk("SSD Principal", 500, 450, ["Sistema Operativo", "Apps"])
        self.disk_service.add_disk("HDD Backups", 2000, 1200, ["Fotos Familiares", "Documentos"])
        self.disk_service.add_disk("NVMe Juegos", 1000, 100, ["Juegos Actuales"])
        self.disk_service.add_disk("USB Trabajo", 128, 10, ["Proyectos Activos"])
        self.disk_service.add_disk("Servidor Media", 4000, 3800, ["Peliculas", "Series"])
        self._update_disk_cards()

    def _update_disk_cards(self, disks_to_display = None):
        # Limpia el contenedor y añade nuevas tarjetas
        self._disk_cards_container.controls = []
        disks = disks_to_display if disks_to_display is not None else self.disk_service.get_all_disks()

        for disk in disks:
            self._disk_cards_container.controls.append(
                DiskCard(
                    disk = disk,
                    on_edit_click=self._handle_edit_disk,
                    on_delete_click=self._handle_disk_delete
                )
            )
        self.page.update()

    def _handle_edit_disk(self, disk: Disk):
        self._disk_form.load_disk_into_form(disk)

    def _handle_disk_save(self, disk_id, name: str, capacity: int, used: int, contents: list[str]):
        if disk_id:
            self.disk_service.update_disk(disk_id, name, capacity, used, contents)
        else:
            self.disk_service.add_disk(name, capacity, used, contents)
        self._update_disk_cards() # Refresca la lista de tarjetas
        self.page.update()

    def _handle_disk_delete(self, disk_id: str):
        self.disk_service.delete_disk(disk_id)
        self._update_disk_cards()
        self.page.update()

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
        self._update_disk_cards() # Mostrar todos los discos sin filtrar
        self.page.update()


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