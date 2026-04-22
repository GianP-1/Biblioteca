import flet as ft
from components.Navbar import (
    COLORES, tarjeta, boton_primario, boton_error,
    titulo_seccion, snackbar_mensaje, chip_estado
)


class VistaPrestamos:
    """
    Vista para gestionar los préstamos de libros de la biblioteca.

    Permite seleccionar un libro disponible y un cliente registrado
    para realizar un préstamo, y también permite devolver libros prestados.

    Args:
        page     : Referencia a la página principal de Flet.
        libros   : Lista compartida de objetos Libro.
        clientes : Lista compartida de objetos Cliente.
    """

    def __init__(self, page: ft.Page, libros: list, clientes: list):
        self.page     = page
        self.libros   = libros
        self.clientes = clientes

    def _opciones_libros(self):
        return [
            ft.dropdown.Option(
                key=l.isbn,
                text=f"{l.titulo} — {l.autor}",
                content=ft.Text(f"{l.titulo} — {l.autor}", color=COLORES["texto"]),
            )
            for l in self.libros if l.esta_disponible()
        ]

    def _opciones_clientes(self):
        return [
            ft.dropdown.Option(
                key=c.cedula,
                text=c.nombre_completo(),
                content=ft.Text(c.nombre_completo(), color=COLORES["texto"]),
            )
            for c in self.clientes
        ]

    def build(self) -> ft.Control:

        # ── DROPDOWN LIBRO ───────────────────────────────────
        estilo_menu = ft.MenuStyle(bgcolor=COLORES["superficie"])

        self.dd_libro = ft.Dropdown(
            label="Seleccionar Libro Disponible",
            hint_text="Elige un libro...",
            options=self._opciones_libros(),
            menu_style=estilo_menu,
            border_radius=8,
            border_color=COLORES["subtexto"],
            focused_border_color=COLORES["primario"],
            label_style=ft.TextStyle(color=COLORES["subtexto"]),
            text_style=ft.TextStyle(color=COLORES["texto"]),
            bgcolor=COLORES["fondo"],
            expand=True,
        )

        # ── DROPDOWN CLIENTE ─────────────────────────────────
        self.dd_cliente = ft.Dropdown(
            label="Seleccionar Cliente",
            hint_text="Elige un cliente...",
            options=self._opciones_clientes(),
            menu_style=estilo_menu,
            border_radius=8,
            border_color=COLORES["subtexto"],
            focused_border_color=COLORES["primario"],
            label_style=ft.TextStyle(color=COLORES["subtexto"]),
            text_style=ft.TextStyle(color=COLORES["texto"]),
            bgcolor=COLORES["fondo"],
            expand=True,
        )

        # ── LISTA DE PRÉSTAMOS ACTIVOS ───────────────────────
        self.lista_prestamos = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        # Carga inicial de la lista (sin page.update, aún no está en la página)
        self._refrescar_lista(actualizar=False)

        # ── BOTÓN PRESTAR ────────────────────────────────────
        btn_prestar = boton_primario(
            "Confirmar Préstamo",
            self._prestar,
            icono=ft.Icons.SWAP_HORIZ,
        )

        # ── CONSTRUCCIÓN DE LA VISTA ─────────────────────────
        return ft.Container(
            padding=24,
            expand=True,
            content=ft.Column(
                controls=[
                    titulo_seccion("Préstamo de Libros"),
                    ft.Text(
                        "Asigna un libro disponible a un cliente registrado.",
                        color=COLORES["subtexto"],
                        size=14,
                    ),
                    ft.Container(height=8),

                    # Formulario de préstamo
                    tarjeta(
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Nuevo Préstamo",
                                    color=COLORES["texto"],
                                    weight=ft.FontWeight.BOLD,
                                    size=16,
                                ),
                                ft.Container(height=4),
                                self.dd_libro,
                                self.dd_cliente,
                                ft.Container(height=4),
                                ft.Row(
                                    [btn_prestar],
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                            ],
                            spacing=12,
                        )
                    ),

                    ft.Container(height=16),
                    ft.Text(
                        "Préstamos Activos",
                        color=COLORES["texto"],
                        size=18,
                        weight=ft.FontWeight.W_600,
                    ),
                    ft.Divider(color=COLORES["subtexto"] + "44"),
                    self.lista_prestamos,
                ],
                expand=True,
                spacing=8,
            ),
        )

    # ── LÓGICA ───────────────────────────────────────────────

    def _prestar(self, _):
        """Valida la selección y realiza el préstamo del libro al cliente."""

        # Validar que se seleccionó libro y cliente
        if not self.dd_libro.value or not self.dd_cliente.value:
            snackbar_mensaje(
                self.page,
                "Por favor selecciona un libro y un cliente.",
                error=True,
            )
            return

        # Buscar el libro y cliente seleccionados
        libro   = next((l for l in self.libros   if l.isbn    == self.dd_libro.value),   None)
        cliente = next((c for c in self.clientes if c.cedula  == self.dd_cliente.value), None)

        if not libro or not cliente:
            snackbar_mensaje(self.page, "Libro o cliente no encontrado.", error=True)
            return

        # Validar que el libro esté disponible
        if not libro.esta_disponible():
            snackbar_mensaje(
                self.page,
                f"El libro '{libro.titulo}' ya está prestado.",
                error=True,
            )
            return

        # Realizar el préstamo
        libro.prestar(cliente)

        snackbar_mensaje(
            self.page,
            f"'{libro.titulo}' prestado a {cliente.nombre_completo()} con éxito.",
        )

        # Limpiar selección y refrescar
        self.dd_libro.value   = None
        self.dd_cliente.value = None
        self._refrescar_dropdowns()
        self._refrescar_lista()

    def _devolver(self, isbn: str):
        """Cambia el estado del libro de vuelta a Disponible."""
        libro = next((l for l in self.libros if l.isbn == isbn), None)

        if not libro:
            snackbar_mensaje(self.page, "Libro no encontrado.", error=True)
            return

        libro.devolver()
        snackbar_mensaje(self.page, f"'{libro.titulo}' devuelto con éxito.")
        self._refrescar_dropdowns()
        self._refrescar_lista()

    # ── HELPERS ──────────────────────────────────────────────

    def _refrescar_dropdowns(self):
        """Actualiza las opciones de los dropdowns con datos actuales."""
        self.dd_libro.options   = self._opciones_libros()
        self.dd_cliente.options = self._opciones_clientes()
        self.page.update()

    def _refrescar_lista(self, actualizar: bool = True):
        """Vuelve a dibujar la lista de préstamos activos."""
        self.lista_prestamos.controls.clear()

        prestamos_activos = [l for l in self.libros if not l.esta_disponible()]

        if not prestamos_activos:
            self.lista_prestamos.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No hay préstamos activos.",
                        color=COLORES["subtexto"],
                        italic=True,
                    ),
                    padding=20,
                    alignment=ft.alignment.Alignment(0, 0),
                )
            )
        else:
            for libro in prestamos_activos:
                cliente = libro.cliente_asignado
                nombre_cliente = (
                    cliente.nombre_completo() if cliente else "Desconocido"
                )

                def hacer_devolucion(e, isbn=libro.isbn):
                    self._devolver(isbn)

                fila = tarjeta(
                    ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.BOOK,
                                color=COLORES["advertencia"],
                                size=28,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        libro.titulo,
                                        color=COLORES["texto"],
                                        weight=ft.FontWeight.BOLD,
                                        size=14,
                                    ),
                                    ft.Text(
                                        f"Prestado a: {nombre_cliente}  |  ISBN: {libro.isbn}",
                                        color=COLORES["subtexto"],
                                        size=12,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            chip_estado(False),
                            ft.IconButton(
                                icon=ft.Icons.UNDO,
                                icon_color=COLORES["primario"],
                                tooltip="Devolver libro",
                                on_click=hacer_devolucion,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                )
                self.lista_prestamos.controls.append(fila)

        if actualizar:
            self.page.update()
