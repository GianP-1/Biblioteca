import flet as ft


class VistaCliente:
    def __init__(self, page: ft.Page, clientes: list = None, on_volver=None):
        self.page = page
        self.clientes = clientes if clientes is not None else []
        self.on_volver = on_volver

    def build(self) -> ft.Control:
        self.txt_nombre = ft.TextField(label="Nombre", width=320)
        self.txt_apellido = ft.TextField(label="Apellido", width=320)
        self.txt_cedula = ft.TextField(
            label="Cédula / ID",
            width=320,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        self.msg = ft.Text("", size=13)

        return ft.Column(
            controls=[
                ft.Text("Registro de Cliente", size=26, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                self.txt_nombre,
                self.txt_apellido,
                self.txt_cedula,
                self.msg,
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Registrar", on_click=self._registrar),
                        ft.TextButton("Volver al menú", on_click=self._volver),
                    ],
                    spacing=12,
                ),
            ],
            spacing=14,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # lógica según el flujograma 

    def _registrar(self, _):
        nombre = self.txt_nombre.value.strip()
        apellido = self.txt_apellido.value.strip()
        cedula = self.txt_cedula.value.strip()

        # Decisión: ¿están todos los campos llenos?
        if not nombre or not apellido or not cedula:
            self._set_msg("Campos obligatorios vacíos.", ft.Colors.RED)
            return

        # Decisión: ¿la cédula ya existe?
        if any(c["cedula"] == cedula for c in self.clientes):
            self._set_msg("Cliente ya registrado.", ft.Colors.RED)
            return

        # Guardar
        self.clientes.append({"nombre": nombre, "apellido": apellido, "cedula": cedula})
        self._set_msg("Cliente registrado con éxito.", ft.Colors.GREEN)
        self._limpiar()

    def _volver(self, _):
        if self.on_volver:
            self.on_volver()

    # helpers 

    def _set_msg(self, texto: str, color):
        self.msg.value = texto
        self.msg.color = color
        self.page.update()

    def _limpiar(self):
        self.txt_nombre.value = ""
        self.txt_apellido.value = ""
        self.txt_cedula.value = ""
        self.page.update()


# ejecución para probar 
def main(page: ft.Page):
    page.title = "Vista Cliente"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    vista = VistaCliente(page)
    page.add(vista.build())


if __name__ == "__main__":
    ft.app(target=main)
