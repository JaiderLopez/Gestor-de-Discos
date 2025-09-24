import flet as ft
from core.models import Disk, ContentItem
from typing import List

# Clase auxiliar para una fila de contenido
class ContentItemRow(ft.Row):
    def __init__(self, item: ContentItem, on_delete):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.description_input = ft.TextField(value=item.description, hint_text="Descripción", expand=True)
        self.size_input = ft.TextField(value=str(item.size_gb), hint_text="GB", width=80, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]"))
        
        self.controls = [
            self.description_input,
            self.size_input,
            ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, on_click=lambda e: on_delete(self), icon_color=ft.Colors.RED_400, tooltip="Eliminar Contenido")
        ]

class DiskForm(ft.Column):
    def __init__(self, on_save, on_clear, on_delete):
        super().__init__()
        self.on_save = on_save
        self.on_clear = on_clear
        self.on_delete = on_delete
        self.selected_disk_id = None

        textfield_style = {"border_color": "transparent", "bgcolor": ft.Colors.WHITE10, "border_radius": 6}

        self._name_input = ft.TextField(label="Nombre del Disco", **textfield_style)
        self._capacity_input = ft.TextField(label="Capacidad Total (GB)", input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]"), **textfield_style)
        
        self._contents_list = ft.Column(spacing=10)
        self._add_content_button = ft.TextButton("Añadir Contenido", icon=ft.Icons.ADD, on_click=self._add_content_row)

        self._save_button = ft.ElevatedButton(text="Guardar Disco", on_click=self._on_save_click, expand=True, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_ACCENT_700, color=ft.Colors.WHITE))
        self._clear_button = ft.OutlinedButton(text="Limpiar", on_click=lambda e: self.clear_form(), expand=True)
        self._delete_button = ft.ElevatedButton(text="Eliminar Disco", icon=ft.Icons.DELETE_FOREVER, on_click=self._on_delete_click, visible=False, expand=True, style=ft.ButtonStyle(bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE))

        self.controls = [
            ft.Text("Gestionar Disco", size=20, weight=ft.FontWeight.BOLD),
            self._name_input,
            self._capacity_input,
            ft.Divider(),
            ft.Text("Contenidos del Disco"),
            self._contents_list,
            self._add_content_button,
            ft.Divider(),
            ft.Row([self._save_button, self._clear_button], spacing=10),
            self._delete_button
        ]
        self.spacing = 15

    def _add_content_row(self, e, item: ContentItem = None):
        if item is None:
            item = ContentItem(description="", size_gb=0)
        
        row = ContentItemRow(item, on_delete=self._remove_content_row)
        self._contents_list.controls.append(row)
        self.update()

    def _remove_content_row(self, row: ContentItemRow):
        self._contents_list.controls.remove(row)
        self.update()

    def _on_save_click(self, e):
        try:
            name = self._name_input.value
            capacity = int(self._capacity_input.value)
            
            if not name or capacity <= 0:
                return # Add user feedback

            # Gather content items from the dynamic rows
            contents: List[ContentItem] = []
            for row in self._contents_list.controls:
                if isinstance(row, ContentItemRow):
                    desc = row.description_input.value
                    size = int(row.size_input.value) if row.size_input.value else 0
                    if desc and size > 0:
                        contents.append(ContentItem(description=desc, size_gb=size))
            
            self.on_save(self.selected_disk_id, name, capacity, contents)
            self.clear_form()

        except (ValueError, TypeError):
            pass # Add user feedback

    def _on_delete_click(self, e):
        if self.selected_disk_id and self.on_delete:
            self.on_delete(self.selected_disk_id)
            self.clear_form()

    def load_disk_into_form(self, disk: Disk):
        self.clear_form() # Start fresh
        self.selected_disk_id = disk.id
        self._name_input.value = disk.name
        self._capacity_input.value = str(disk.total_capacity_gb)
        
        # Populate content rows
        for item in disk.contents:
            self._add_content_row(None, item=item)
            
        self._delete_button.visible = True
        self.update()

    def clear_form(self):
        self.selected_disk_id = None
        self._name_input.value = ""
        self._capacity_input.value = ""
        self._contents_list.controls.clear()
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