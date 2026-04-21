class Libro:
    """
    Representa un libro dentro del sistema de biblioteca.

    Atributos:
        titulo (str): Título del libro.
        autor (str): Nombre del autor del libro.
        isbn (str): Identificador único del libro (ISBN).
        estado (str): Estado actual del libro, "Disponible" o "Prestado".
        cliente_asignado (Cliente | None): Cliente que tiene el libro prestado, o None si está disponible.
    """

    def __init__(self, titulo: str, autor: str, isbn: str):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.estado = "Disponible"
        self.cliente_asignado = None

    def prestar(self, cliente) -> bool:
        """
        Presta el libro a un cliente.
        Retorna True si se prestó correctamente, False si ya estaba prestado.
        """
        if self.estado == "Prestado":
            return False
        self.estado = "Prestado"
        self.cliente_asignado = cliente
        cliente.libros_prestados.append(self)
        return True

    def devolver(self) -> bool:
        """
        Devuelve el libro a la biblioteca.
        Retorna True si se devolvió correctamente, False si ya estaba disponible.
        """
        if self.estado == "Disponible":
            return False
        if self.cliente_asignado:
            self.cliente_asignado.libros_prestados.remove(self)
        self.estado = "Disponible"
        self.cliente_asignado = None
        return True

    def esta_disponible(self) -> bool:
        """Retorna True si el libro está disponible para préstamo."""
        return self.estado == "Disponible"

    def __str__(self) -> str:
        return f"{self.titulo} - {self.autor} | ISBN: {self.isbn} | {self.estado}"

    def __repr__(self) -> str:
        return f"Libro(titulo='{self.titulo}', autor='{self.autor}', isbn='{self.isbn}', estado='{self.estado}')"