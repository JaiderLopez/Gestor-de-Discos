import flet as ft
from  core.models import Disk
# import option

class DiskForm(ft.Column):
    def __init__(self, on_save, on_clear, on_delete):
        super().__init__()
        self.on_save = on_save
        self.on_clear = on_clear
        self.on_delete = on_delete # Solo se usará si hay un disco cargado
        self.selected_disk_id = None

        self._name_input = ft.TextField(label="Nombre del Disco")
        self._capacity_input = ft.TextField(label="Capacidad Total (GB)", input_filter= ft.InputFilter(allow=True, regex_string=r"[0-9]"))
        self._used_input = ft.TextField(label="Espacio Usado (GB)", input_filter= ft.InputFilter(allow=True, regex_string=r"[0-9]"))
        self._contents_input = ft.TextField(label="Contenidos (separados por coma)")

        self._save_button = ft.ElevatedButton(text="Guardar Disco", on_click=self._on_save_click)
        self._clear_button = ft.OutlinedButton(text="Limpiar Formulario", on_click=lambda e: self.clear_form())
        self._delete_button = ft.ElevatedButton(text="Eliminar Disco", icon=ft.Icons.DELETE,
                                                on_click = self._on_delete_click,
                                                style = ft.ButtonStyle(bgcolor=ft.Colors.RED_500),
                                                visible = True) # Visible solo al editar

        self.controls = [
            ft.Text("Gestionar Disco", size=20, weight=ft.FontWeight.BOLD),
            self._name_input,
            self._capacity_input,
            self._used_input,
            self._contents_input,
            ft.Row([self._save_button, self._clear_button]),
            self._delete_button # Agregamos el botón de eliminar al formulario
        ]

    def _on_save_click(self, e):
        # Validar entradas (simplificado para el ejemplo)
        try:
            name = self._name_input.value
            capacity = int(self._capacity_input.value)
            used = int(self._used_input.value)
            contents = [c.strip() for c in self._contents_input.value.split(',')] if self._contents_input.value else []

            if not name or capacity <= 0 or used < 0:
                self.page.overlay.append(ft.SnackBar(ft.Text("Por favor, complete todos los campos requeridos y asegúrese que los valores sean válidos."), open= True))
                self.page.update()
                return

            self.on_save(self.selected_disk_id, name, capacity, used, contents)
            self.clear_form()
            self.page.overlay.append(ft.SnackBar(ft.Text("Disco guardado con éxito."), open=True))
            self.page.update()

        except ValueError:
            self.page.overlay.append(ft.SnackBar(ft.Text("Por favor, ingrese números válidos para capacidad y espacio usado."), open=True))
            self.page.update()



    def _on_delete_click(self, e):
        if self.selected_disk_id and self.on_delete:
            self.on_delete(self.selected_disk_id)
            self.clear_form()
            self.page.overlay.append(ft.SnackBar(ft.Text("Disco eliminado."), open=True))
            self.page.update()


    def load_disk_into_form(self, disk):
        if disk:
            self.selected_disk_id = disk.id
            self._name_input.value = disk.name
            self._capacity_input.value = str(disk.total_capacity_gb)
            self._used_input.value = str(disk.used_space_gb)
            self._contents_input.value = ", ".join(disk.contents)
            self._delete_button.visible = True
        else:
            self.clear_form()
        if self.page: self.page.update()

    def clear_form(self):
        self.selected_disk_id = None
        self._name_input.value = ""
        self._capacity_input.value = ""
        self._used_input.value = ""
        self._contents_input.value = ""
        self._delete_button.visible = False
        if self.page: self.page.update()


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