class Cliente:
    """
    Representa un cliente registrado en la biblioteca.

    Atributos:
        nombre (str): Nombre del cliente.
        apellido (str): Apellido del cliente.
        cedula (str): Cédula o ID único del cliente.
        libros_prestados (list): Lista de libros que el cliente tiene actualmente prestados.
    """

    def _init_(self, nombre: str, apellido: str, cedula: str):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.libros_prestados = []

    def tiene_libros(self) -> bool:
        """Retorna True si el cliente tiene al menos un libro prestado."""
        return len(self.libros_prestados) > 0

    def nombre_completo(self) -> str:
        """Retorna el nombre completo del cliente."""
        return f"{self.nombre} {self.apellido}"

    def _str_(self) -> str:
        return f"{self.nombre} {self.apellido} - CI: {self.cedula}"

    def _repr_(self) -> str:
        return f"Cliente(nombre='{self.nombre}', apellido='{self.apellido}', cedula='{self.cedula}')"
    