import flet as ft

# ── TEMA DE COLORES ──────────────────────────────────────────
COLORES = {
    "primario":    "#6C63FF",
    "secundario":  "#48CAE4",
    "fondo":       "#1E1E2E",
    "superficie":  "#2A2A3E",
    "texto":       "#E0E0E0",
    "subtexto":    "#9E9E9E",
    "exito":       "#4CAF50",
    "error":       "#EF5350",
    "advertencia": "#FF9800",
}

class Navbar(ft.UserControl):
    def __init__(self, pagina_actual: str, on_cambiar):
        super().__init__()
        self.pagina_actual = pagina_actual
        self.on_cambiar    = on_cambiar

    def _crear_item(self, icono, icono_sel, texto, nombre):
        activo = (self.pagina_actual == nombre)

        def al_pulsar(e):
            self.on_cambiar(nombre)

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        name=icono_sel if activo else icono,
                        color=COLORES["primario"] if activo else COLORES["subtexto"],
                        size=22,
                    ),
                    ft.Text(
                        texto,
                        color=COLORES["primario"] if activo else COLORES["subtexto"],
                        weight=ft.FontWeight.BOLD if activo else ft.FontWeight.NORMAL,
                        size=14,
                    ),
                ],
                spacing=12,
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            border_radius=10,
            bgcolor=COLORES["primario"] + "22" if activo else "transparent",
            on_click=al_pulsar,
            animate=ft.animation.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            ink=True,
        )

    def build(self):
        items = [
            ("book_outlined",      "book",        "Libros",    "libros"),
            ("people_outlined",    "people",      "Clientes",  "clientes"),
            ("swap_horiz_outlined","swap_horiz",  "Préstamos", "prestamos"),
        ]

        return ft.Container(
            width=210,
            bgcolor=COLORES["superficie"],
            border_radius=ft.border_radius.only(top_right=16, bottom_right=16),
            padding=ft.padding.symmetric(vertical=24),
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Icon(ft.icons.LOCAL_LIBRARY,
                                        color=COLORES["primario"], size=36),
                                ft.Text("Biblioteca", color=COLORES["texto"],
                                        size=18, weight=ft.FontWeight.BOLD),
                                ft.Text("Sistema de Control",
                                        color=COLORES["subtexto"], size=11),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=4,
                        ),
                        padding=ft.padding.only(bottom=24),
                        alignment=ft.alignment.center,
                    ),
                    ft.Divider(color=COLORES["subtexto"] + "44", height=1),
                    ft.Container(height=8),
                    *[self._crear_item(*item) for item in items],
                    ft.Container(expand=True),
                    ft.Divider(color=COLORES["subtexto"] + "44", height=1),
                    ft.Container(
                        content=ft.Text("v1.0.0", color=COLORES["subtexto"], size=11),
                        padding=ft.padding.only(left=16, top=8),
                    ),
                ],
                expand=True,
                spacing=2,
            ),
        )


# ── COMPONENTES REUTILIZABLES ────────────────────────────────

def tarjeta(contenido: ft.Control, padding: int = 16) -> ft.Container:
    return ft.Container(
        content=contenido,
        bgcolor=COLORES["superficie"],
        border_radius=12,
        padding=padding,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color="#00000033",
            offset=ft.Offset(0, 4),
        ),
    )

def boton_primario(texto: str, on_click, icono=None) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text=texto,
        icon=icono,
        on_click=on_click,
        style=ft.ButtonStyle(
            bgcolor=COLORES["primario"],
            color=COLORES["texto"],
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
        ),
    )

def boton_exito(texto: str, on_click, icono=None) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text=texto,
        icon=icono,
        on_click=on_click,
        style=ft.ButtonStyle(
            bgcolor=COLORES["exito"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
        ),
    )

def boton_error(texto: str, on_click, icono=None) -> ft.OutlinedButton:
    return ft.OutlinedButton(
        text=texto,
        icon=icono,
        on_click=on_click,
        style=ft.ButtonStyle(
            color=COLORES["error"],
            side=ft.BorderSide(color=COLORES["error"], width=1),
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
        ),
    )

def campo_texto(label: str, hint: str = "") -> ft.TextField:
    return ft.TextField(
        label=label,
        hint_text=hint,
        border_radius=8,
        border_color=COLORES["subtexto"],
        focused_border_color=COLORES["primario"],
        label_style=ft.TextStyle(color=COLORES["subtexto"]),
        text_style=ft.TextStyle(color=COLORES["texto"]),
        cursor_color=COLORES["primario"],
        bgcolor=COLORES["fondo"],
    )

def chip_estado(disponible: bool) -> ft.Container:
    texto = "Disponible" if disponible else "Prestado"
    color = COLORES["exito"] if disponible else COLORES["advertencia"]
    return ft.Container(
        content=ft.Text(texto, color=color, size=12, weight=ft.FontWeight.BOLD),
        bgcolor=color + "22",
        border_radius=20,
        padding=ft.padding.symmetric(horizontal=10, vertical=4),
    )

def titulo_seccion(texto: str) -> ft.Text:
    return ft.Text(texto, size=22, weight=ft.FontWeight.BOLD, color=COLORES["texto"])

def snackbar_mensaje(page: ft.Page, mensaje: str, error: bool = False):
    page.snack_bar = ft.SnackBar(
        content=ft.Text(mensaje, color="#FFFFFF"),
        bgcolor=COLORES["error"] if error else COLORES["exito"],
        duration=3000,
    )
    page.snack_bar.open = True
    page.update()
