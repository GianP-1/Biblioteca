import flet as ft
from components.Navbar import COLORES, Navbar, snackbar_mensaje
from views.vista_libros import vista_libros
from views.vista_clientes import VistaCliente
from views.vista_prestamos import VistaPrestamos


def main(page: ft.Page):
    """
    Punto de entrada principal de la aplicación Biblioteca.

    Configura la página, inicializa las listas compartidas de datos
    y gestiona la navegación entre las tres vistas principales:
    Libros, Clientes y Préstamos.
    """

    # ── CONFIGURACIÓN DE LA PÁGINA ───────────────────────────
    page.title            = "Sistema de Biblioteca"
    page.bgcolor          = COLORES["fondo"]
    page.padding          = 0
    page.window.width     = 1000
    page.window.height    = 700
    page.window.resizable = True

    # ── DATOS COMPARTIDOS ────────────────────────────────────
    # Estas listas son pasadas a todas las vistas para que
    # compartan el mismo estado durante la sesión.
    libros   = []
    clientes = []

    # ── CONTENEDOR PRINCIPAL DE VISTAS ──────────────────────
    contenido = ft.Container(expand=True)

    # ── NAVEGACIÓN ───────────────────────────────────────────
    def cambiar_vista(nombre: str):
        """
        Cambia la vista activa según la sección seleccionada
        en el Navbar y reconstruye el Navbar para reflejar
        el ítem activo.
        """

        # Reconstruir Navbar con la página activa actualizada
        navbar = Navbar(pagina_actual=nombre, on_cambiar=cambiar_vista)

        # Cargar la vista correspondiente
        if nombre == "libros":
            contenido.content = vista_libros(page, libros)

        elif nombre == "clientes":
            vista = VistaCliente(page, clientes)
            contenido.content = vista.build()

        elif nombre == "prestamos":
            vista = VistaPrestamos(page, libros, clientes)
            contenido.content = vista.build()

        # Reconstruir el layout completo con el Navbar actualizado
        page.controls.clear()
        page.controls.append(
            ft.Row(
                controls=[
                    navbar.build(),
                    ft.VerticalDivider(width=1, color=COLORES["subtexto"] + "33"),
                    contenido,
                ],
                expand=True,
                spacing=0,
            )
        )
        page.update()

    # ── VISTA INICIAL ────────────────────────────────────────
    cambiar_vista("libros")


# ── ARRANQUE DE LA APLICACIÓN ────────────────────────────────
ft.run(main)
