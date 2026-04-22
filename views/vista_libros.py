import flet as ft
from models.libro import Libro
from components.Navbar import (
    COLORES, tarjeta, boton_primario,
    campo_texto, chip_estado, titulo_seccion, snackbar_mensaje
)


def vista_libros(page: ft.Page, libros: list) -> ft.Container:
    """
    Vista para gestionar el inventario de libros de la biblioteca.

    Permite registrar nuevos libros (Título, Autor, ISBN) y visualizar
    el inventario completo con el estado de cada libro.

    Args:
        page   : Referencia a la página principal de Flet.
        libros : Lista compartida de objetos Libro (se modifica en lugar).
    """

    # ── CAMPOS DEL FORMULARIO ────────────────────────────────
    tf_titulo = campo_texto("Título del Libro", "Ej: Cien años de soledad")
    tf_autor  = campo_texto("Autor",            "Ej: Gabriel García Márquez")
    tf_isbn   = campo_texto("ISBN",             "Ej: 978-3-16-148410-0")

    # ── LISTA VISUAL DE LIBROS ───────────────────────────────
    lista_libros = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def refrescar_lista():
        """Vuelve a dibujar la lista completa de libros."""
        lista_libros.controls.clear()

        if not libros:
            lista_libros.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No hay libros registrados aún.",
                        color=COLORES["subtexto"],
                        italic=True,
                    ),
                    padding=20,
                    alignment=ft.alignment.Alignment(0, 0),
                )
            )
        else:
            for libro in libros:
                fila = tarjeta(
                    ft.Row(
                        controls=[
                            ft.Icon(icon=ft.Icons.BOOK,
                                    color=COLORES["primario"], size=28),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        libro.titulo,
                                        color=COLORES["texto"],
                                        weight=ft.FontWeight.BOLD,
                                        size=14,
                                    ),
                                    ft.Text(
                                        f"Autor: {libro.autor}  |  ISBN: {libro.isbn}",
                                        color=COLORES["subtexto"],
                                        size=12,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            chip_estado(libro.esta_disponible()),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                )
                lista_libros.controls.append(fila)

        page.update()

    def guardar_click(e):
        """Valida el formulario, crea el Libro y lo agrega a la lista."""
        titulo = tf_titulo.value.strip()
        autor  = tf_autor.value.strip()
        isbn   = tf_isbn.value.strip()

        # ── Validaciones ────────────────────────────────────
        if not titulo or not autor or not isbn:
            snackbar_mensaje(
                page,
                "Por favor completa todos los campos (Título, Autor e ISBN).",
                error=True
            )
            return

        if not any(c.isalpha() for c in titulo):
            snackbar_mensaje(
                page,
                "El título debe contener letras, no puede ser solo números.",
                error=True
            )
            return

        if not all(c.isalpha() or c.isspace() for c in autor):
            snackbar_mensaje(
                page,
                "El autor solo puede contener letras y espacios.",
                error=True
            )
            return

        isbn_limpio = isbn.replace("-", "")
        if not isbn_limpio.isdigit() or len(isbn_limpio) not in (10, 13):
            snackbar_mensaje(
                page,
                "El ISBN debe tener 10 o 13 dígitos (guiones opcionales). Ej: 978-3-16-148410-0",
                error=True
            )
            return

        # Verificar ISBN duplicado
        if any(l.isbn == isbn for l in libros):
            snackbar_mensaje(
                page,
                f"Ya existe un libro con el ISBN '{isbn}'.",
                error=True
            )
            return

        # ── Crear y registrar el libro ───────────────────────
        nuevo_libro = Libro(titulo, autor, isbn)
        libros.append(nuevo_libro)

        # Limpiar campos
        tf_titulo.value = ""
        tf_autor.value  = ""
        tf_isbn.value   = ""

        snackbar_mensaje(page, f"Libro '{titulo}' registrado con éxito.")
        refrescar_lista()

    # ── BOTÓN GUARDAR ────────────────────────────────────────
    btn_guardar = boton_primario(
        "Guardar Libro",
        guardar_click,
        icono=ft.Icons.SAVE
    )

    # Carga inicial de la lista
    refrescar_lista()

    # ── CONSTRUCCIÓN DE LA VISTA ─────────────────────────────
    return ft.Container(
        padding=24,
        expand=True,
        content=ft.Column(
            controls=[
                titulo_seccion("Gestión de Libros"),
                ft.Text(
                    "Registra nuevos ejemplares en el inventario.",
                    color=COLORES["subtexto"],
                    size=14,
                ),
                ft.Container(height=8),

                # Formulario
                tarjeta(
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Nuevo Libro",
                                color=COLORES["texto"],
                                weight=ft.FontWeight.BOLD,
                                size=16,
                            ),
                            ft.Container(height=4),
                            tf_titulo,
                            tf_autor,
                            tf_isbn,
                            ft.Container(height=4),
                            ft.Row(
                                [btn_guardar],
                                alignment=ft.MainAxisAlignment.END
                            ),
                        ],
                        spacing=12,
                    )
                ),

                ft.Container(height=16),
                ft.Text(
                    "Inventario Actual",
                    color=COLORES["texto"],
                    size=18,
                    weight=ft.FontWeight.W_600,
                ),
                ft.Divider(color=COLORES["subtexto"] + "44"),
                lista_libros,
            ],
            expand=True,
            spacing=8,
        ),
    )