import flet as ft

def vista_libros(page: ft.Page):
    # --- Títulos y Estética ---
    titulo = ft.Text("Gestión de Libros", size=30, weight="bold", color=ft.colors.BLUE_700)
    subtitulo = ft.Text("Añade nuevos ejemplares al inventario", size=16, color=ft.colors.GREY_700)

    # --- Campos de Entrada (Formulario) ---
    tf_titulo = ft.TextField(
        label="Título del Libro", 
        hint_text="Ej: Cien años de soledad",
        border_radius=10
    )
    tf_autor = ft.TextField(
        label="Autor", 
        hint_text="Ej: Gabriel García Márquez",
        border_radius=10
    )
    tf_genero = ft.TextField(
        label="Género", 
        hint_text="Ej: Realismo Mágico",
        border_radius=10
    )

    # --- Lista donde se mostrarán los libros ---
    lista_libros = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, expand=True)

    # --- Función para el Botón ---
    def guardar_click(e):
        if not tf_titulo.value or not tf_autor.value:
            # Si faltan datos, mostramos un error simple
            tf_titulo.error_text = "Por favor, llena este campo"
            page.update()
        else:
            # Agregamos el libro a la lista visual
            lista_libros.controls.append(
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.icons.BOOK_ROUNDED, color=ft.colors.BLUE_ACCENT),
                        title=ft.Text(tf_titulo.value, weight="bold"),
                        subtitle=ft.Text(f"Autor: {tf_autor.value} | Género: {tf_genero.value}"),
                        trailing=ft.IconButton(ft.icons.DELETE_OUTLINE, icon_color=ft.colors.RED_400)
                    ),
                    bgcolor=ft.colors.GREY_100,
                    border_radius=10,
                )
            )
            # Limpiamos los campos
            tf_titulo.value = ""
            tf_autor.value = ""
            tf_genero.value = ""
            tf_titulo.error_text = None
            page.update()

    btn_guardar = ft.ElevatedButton(
        "Guardar Libro", 
        icon=ft.icons.SAVE,
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_700),
        on_click=guardar_click,
        height=50
    )

    # --- Construcción final de la Vista ---
    return ft.Container(
        padding=20,
        content=ft.Column([
            titulo,
            subtitulo,
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            tf_titulo,
            tf_autor,
            tf_genero,
            ft.Row([btn_guardar], alignment=ft.MainAxisAlignment.END),
            ft.Divider(height=30),
            ft.Text("Inventario Actual", size=20, weight="w600"),
            lista_libros
        ], expand=True)
    )