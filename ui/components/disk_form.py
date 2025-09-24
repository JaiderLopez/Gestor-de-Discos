import flet as ft
from core.models import Disk

class DiskForm(ft.Column):
    def __init__(self, on_save, on_clear, on_delete):
        super().__init__()
        self.on_save = on_save
        self.on_clear = on_clear
        self.on_delete = on_delete
        self.selected_disk_id = None

        # Estilo común para los campos de texto
        textfield_style = {
            "border_color": "transparent",
            "bgcolor": ft.Colors.WHITE10,
            "border_radius": 6,
        }

        self._name_input = ft.TextField(label="Nombre del Disco", **textfield_style)
        self._capacity_input = ft.TextField(label="Capacidad Total (GB)", input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]"), **textfield_style)
        self._used_input = ft.TextField(label="Espacio Usado (GB)", input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]"), **textfield_style)
        self._contents_input = ft.TextField(label="Contenidos (separados por coma)", **textfield_style)

        self._save_button = ft.ElevatedButton(
            text="Guardar Disco", 
            on_click=self._on_save_click,
            expand=True,
            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_ACCENT_700, color=ft.Colors.WHITE)
        )
        self._clear_button = ft.OutlinedButton(
            text="Limpiar", 
            on_click=lambda e: self.clear_form(),
            expand=True
        )
        self._delete_button = ft.ElevatedButton(
            text="Eliminar Disco", 
            icon=ft.Icons.DELETE_FOREVER,
            on_click=self._on_delete_click,
            visible=False,
            expand=True,
            style=ft.ButtonStyle(bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE)
        )

        self.controls = [
            ft.Text("Gestionar Disco", size=20, weight=ft.FontWeight.BOLD),
            self._name_input,
            self._capacity_input,
            self._used_input,
            self._contents_input,
            ft.Row([self._save_button, self._clear_button], spacing=10),
            self._delete_button
        ]
        self.spacing = 15

    def _on_save_click(self, e):
        try:
            name = self._name_input.value
            capacity = int(self._capacity_input.value)
            used = int(self._used_input.value)
            contents = [c.strip() for c in self._contents_input.value.split(',')] if self._contents_input.value else []

            if not name or capacity <= 0 or used < 0:
                # Simple feedback, could be improved with a dialog or error text
                return

            self.on_save(self.selected_disk_id, name, capacity, used, contents)
            self.clear_form()

        except (ValueError, TypeError):
            # Handle cases where conversion to int fails or fields are empty
            pass

    def _on_delete_click(self, e):
        if self.selected_disk_id and self.on_delete:
            self.on_delete(self.selected_disk_id)
            self.clear_form()

    def load_disk_into_form(self, disk: Disk):
        self.selected_disk_id = disk.id
        self._name_input.value = disk.name
        self._capacity_input.value = str(disk.total_capacity_gb)
        self._used_input.value = str(disk.used_space_gb)
        self._contents_input.value = ", ".join(disk.contents)
        self._delete_button.visible = True
        self.update()

    def clear_form(self):
        self.selected_disk_id = None
        self._name_input.value = ""
        self._capacity_input.value = ""
        self._used_input.value = ""
        self._contents_input.value = ""
        self._delete_button.visible = False
        self.update()



# Variables importantes:
# - selected_disk_id: Guarda el ID del disco que se está editando (o None si es nuevo).
# - _name_input, _capacity_input, etc.: Controles TextField para la entrada de datos.
# - _save_button, _clear_button, _delete_button: Botones de acción.
# - on_save, on_clear, on_delete: Callbacks para manejar las acciones del formulario.
# Métodos importantes:
# - _on_save_click(): Maneja el evento de guardar (crear o actualizar).
# - _on_delete_click(): Maneja el evento de eliminar.
# - load_disk_into_form(): Carga los datos de un disco en el formulario para edición.
# - clear_form(): Resetea el formulario.