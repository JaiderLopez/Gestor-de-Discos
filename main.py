import flet as ft
from ui.views.home_view import HomeView

def main(page: ft.Page):
    page.title = "Gestor de Discos"
    page.window_width = 1200
    page.window_height = 700
    page.window_min_width = 800
    page.window_min_height = 600

    # Configuración del tema oscuro basado en el prototipo
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE_ACCENT_700, # Azul para botones y elementos principales
            primary_container=ft.Colors.BLUE_GREY_800,
            background="#202329", # Fondo principal oscuro
            surface="#2c313a", # Fondo para tarjetas y diálogos
            on_primary=ft.Colors.WHITE,
            on_surface=ft.Colors.WHITE,
            on_background=ft.Colors.WHITE,
        ),
        font_family="Roboto",
    )

    # Cargar la fuente Roboto desde Google Fonts
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"
    }

    home_view = HomeView(page)
    page.add(home_view)
    page.update()

if __name__ == '__main__':
    ft.app(target=main)
