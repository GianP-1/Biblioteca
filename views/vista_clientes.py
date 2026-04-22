import flet as ft
from models.cliente import Cliente
from components.Navbar import (
    COLORES, tarjeta, boton_primario,
    campo_texto, titulo_seccion, snackbar_mensaje
)


class VistaCliente:
    """
    Vista para gestionar los clientes registrados en la biblioteca.

    Permite registrar nuevos clientes (Nombre, Apellido, Cédula) y visualizar
    la lista completa de clientes con sus préstamos activos.

    Args:
        page     : Referencia a la página principal de Flet.
        clientes : Lista compartida de objetos Cliente (se modifica en lugar).
    """

    def __init__(self, page: ft.Page, clientes: list = None):
        self.page     = page
        self.clientes = clientes if clientes is not None else []

    def build(self) -> ft.Control:

        # ── CAMPOS DEL FORMULARIO ────────────────────────────
        self.txt_nombre   = campo_texto("Nombre",      "Ej: Juan")
        self.txt_apellido = campo_texto("Apellido",    "Ej: Pérez")
        self.txt_cedula   = campo_texto("Cédula / ID", "Ej: 8-123-4567")

        # ── LISTA VISUAL DE CLIENTES ─────────────────────────
        self.lista_clientes = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        self._refrescar_lista()

        # ── BOTÓN GUARDAR ────────────────────────────────────
        btn_registrar = boton_primario(
            "Registrar Cliente",
            self._registrar,
            icono=ft.Icons.PERSON_ADD
        )

        # ── CONSTRUCCIÓN DE LA VISTA ─────────────────────────
        return ft.Container(
            padding=24,
            expand=True,
            content=ft.Column(
                controls=[
                    titulo_seccion("Gestión de Clientes"),
                    ft.Text(
                        "Registra los usuarios de la biblioteca.",
                        color=COLORES["subtexto"],
                        size=14,
                    ),
                    ft.Container(height=8),

                    # Formulario
                    tarjeta(
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Nuevo Cliente",
                                    color=COLORES["texto"],
                                    weight=ft.FontWeight.BOLD,
                                    size=16,
                                ),
                                ft.Container(height=4),
                                self.txt_nombre,
                                self.txt_apellido,
                                self.txt_cedula,
                                ft.Container(height=4),
                                ft.Row(
                                    [btn_registrar],
                                    alignment=ft.MainAxisAlignment.END
                                ),
                            ],
                            spacing=12,
                        )
                    ),

                    ft.Container(height=16),
                    ft.Text(
                        "Clientes Registrados",
                        color=COLORES["texto"],
                        size=18,
                        weight=ft.FontWeight.W_600,
                    ),
                    ft.Divider(color=COLORES["subtexto"] + "44"),
                    self.lista_clientes,
                ],
                expand=True,
                spacing=8,
            ),
        )

    # ── LÓGICA ───────────────────────────────────────────────

    def _registrar(self, _):
        """Valida el formulario, crea el Cliente y lo agrega a la lista."""
        nombre   = self.txt_nombre.value.strip()
        apellido = self.txt_apellido.value.strip()
        cedula   = self.txt_cedula.value.strip()

        # Decisión: ¿están todos los campos llenos?
        if not nombre or not apellido or not cedula:
            snackbar_mensaje(
                self.page,
                "Por favor completa todos los campos (Nombre, Apellido y Cédula).",
                error=True
            )
            return

        if not all(c.isalpha() or c.isspace() for c in nombre):
            snackbar_mensaje(
                self.page,
                "El nombre solo puede contener letras y espacios.",
                error=True
            )
            return

        if not all(c.isalpha() or c.isspace() for c in apellido):
            snackbar_mensaje(
                self.page,
                "El apellido solo puede contener letras y espacios.",
                error=True
            )
            return

        cedula_limpia = cedula.replace("-", "")
        if not cedula_limpia.isalnum():
            snackbar_mensaje(
                self.page,
                "La cédula solo puede contener números, letras y guiones. Ej: 8-123-4567",
                error=True
            )
            return

        # Decisión: ¿la cédula ya existe?
        if any(c.cedula == cedula for c in self.clientes):
            snackbar_mensaje(
                self.page,
                "Ya existe un cliente con esa cédula.",
                error=True
            )
            return

        # Guardar como objeto Cliente (no diccionario)
        nuevo_cliente = Cliente(nombre, apellido, cedula)
        self.clientes.append(nuevo_cliente)

        snackbar_mensaje(self.page, f"Cliente '{nombre} {apellido}' registrado con éxito.")
        self._limpiar()
        self._refrescar_lista()

    def _refrescar_lista(self):
        """Vuelve a dibujar la lista completa de clientes."""
        self.lista_clientes.controls.clear()

        if not self.clientes:
            self.lista_clientes.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No hay clientes registrados aún.",
                        color=COLORES["subtexto"],
                        italic=True,
                    ),
                    padding=20,
                    alignment=ft.alignment.Alignment(0, 0),
                )
            )
        else:
            for cliente in self.clientes:
                cantidad       = len(cliente.libros_prestados)
                texto_prestamo = (
                    f"{cantidad} libro(s) prestado(s)"
                    if cantidad > 0
                    else "Sin préstamos activos"
                )
                color_prestamo = (
                    COLORES["advertencia"] if cantidad > 0 else COLORES["subtexto"]
                )

                fila = tarjeta(
                    ft.Row(
                        controls=[
                            ft.CircleAvatar(
                                content=ft.Text(
                                    cliente.nombre[0].upper(),
                                    color=COLORES["texto"],
                                    weight=ft.FontWeight.BOLD,
                                    size=16,
                                ),
                                bgcolor=COLORES["primario"],
                                radius=22,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        cliente.nombre_completo(),
                                        color=COLORES["texto"],
                                        weight=ft.FontWeight.BOLD,
                                        size=14,
                                    ),
                                    ft.Text(
                                        f"Cédula: {cliente.cedula}",
                                        color=COLORES["subtexto"],
                                        size=12,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Text(
                                texto_prestamo,
                                color=color_prestamo,
                                size=12,
                                weight=ft.FontWeight.W_500,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                )
                self.lista_clientes.controls.append(fila)

        self.page.update()

    # ── HELPERS ──────────────────────────────────────────────

    def _limpiar(self):
        """Limpia todos los campos del formulario."""
        self.txt_nombre.value   = ""
        self.txt_apellido.value = ""
        self.txt_cedula.value   = ""
        self.page.update()