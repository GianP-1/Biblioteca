# Sistema de Control de Biblioteca

Sistema de gestión de biblioteca desarrollado con **Python** y **Flet**, que permite administrar libros, clientes y préstamos desde una interfaz gráfica moderna con tema oscuro.

---

## Capturas de Pantalla

> La aplicación cuenta con tres secciones principales: Libros, Clientes y Préstamos, accesibles desde un panel de navegación lateral.

---

## Características

- **Gestión de libros**: Registrar, listar y visualizar el estado de disponibilidad de cada libro
- **Gestión de clientes**: Registrar clientes y ver cuántos libros tienen en préstamo
- **Sistema de préstamos**: Prestar libros a clientes y registrar devoluciones con un clic
- **Validaciones**: Previene ISBN y cédulas duplicadas, y campos vacíos
- **Interfaz moderna**: Tema oscuro, tarjetas con sombra, iconos, notificaciones emergentes y badges de estado
- **Arquitectura limpia**: Separación en modelos, vistas y componentes reutilizables

---

## Tecnologías

| Tecnología | Propósito |
|------------|-----------|
| Python 3.x | Lenguaje de programación principal |
| [Flet](https://flet.dev) | Framework para interfaces gráficas multiplataforma |

---

## Estructura del Proyecto

```
Biblioteca/
├── Main.py                   # Punto de entrada, configuración y navegación
├── components/
│   └── Navbar.py             # Navbar, paleta de colores y componentes UI reutilizables
├── models/
│   ├── libro.py              # Clase Libro (datos y lógica de préstamo)
│   └── cliente.py            # Clase Cliente (datos y préstamos activos)
└── views/
    ├── vista_libros.py       # Vista de inventario de libros
    ├── vista_clientes.py     # Vista de registro y listado de clientes
    └── vista_prestamos.py    # Vista de préstamos y devoluciones
```

---

## Instalación y Ejecución

### Requisitos previos

- Python 3.8 o superior
- pip

### Pasos

1. Clona o descarga el repositorio:

```bash
git clone <url-del-repositorio>
cd Biblioteca
```

2. Instala la dependencia:

```bash
pip install flet
```

3. Ejecuta la aplicación:

```bash
python Main.py
```

---

## Uso

### Libros

1. Navega a la sección **Libros** desde el panel lateral
2. Completa los campos: Título, Autor e ISBN
3. Haz clic en **Guardar Libro**
4. El libro aparece en la lista con un badge de estado (**Disponible** / **Prestado**)

### Clientes

1. Navega a la sección **Clientes**
2. Completa los campos: Nombre, Apellido y Cédula/ID
3. Haz clic en **Registrar Cliente**
4. El cliente aparece en la lista con la cantidad de libros que tiene en préstamo

### Préstamos

1. Navega a la sección **Préstamos**
2. Selecciona un libro disponible del dropdown (solo muestra libros disponibles)
3. Selecciona el cliente al que se le prestará
4. Haz clic en **Confirmar Préstamo**
5. Para devolver un libro, haz clic en el ícono **↶** junto al préstamo activo

---

## Arquitectura

### Modelos de Datos

#### `Libro`
| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `titulo` | str | Título del libro |
| `autor` | str | Autor del libro |
| `isbn` | str | Identificador único (ISBN) |
| `estado` | str | `"Disponible"` o `"Prestado"` |
| `cliente_asignado` | Cliente / None | Cliente que tiene el libro en préstamo |

**Métodos:** `prestar(cliente)`, `devolver()`, `esta_disponible()`

#### `Cliente`
| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `nombre` | str | Nombre del cliente |
| `apellido` | str | Apellido del cliente |
| `cedula` | str | Identificador único (cédula/documento) |
| `libros_prestados` | list | Lista de libros actualmente prestados |

**Métodos:** `tiene_libros()`, `nombre_completo()`

---

### Componentes Reutilizables (`Navbar.py`)

| Componente | Descripción |
|------------|-------------|
| `tarjeta()` | Contenedor con sombra y bordes redondeados |
| `boton_primario()` | Botón azul con icono opcional |
| `boton_exito()` | Botón verde para acciones de confirmación |
| `boton_error()` | Botón rojo con borde para acciones de eliminación |
| `campo_texto()` | Campo de entrada estilizado |
| `chip_estado()` | Badge visual de estado del libro |
| `titulo_seccion()` | Título destacado de sección |
| `snackbar_mensaje()` | Notificación emergente (verde/rojo) |

---

### Paleta de Colores

| Nombre | Hex | Uso |
|--------|-----|-----|
| Primario | `#6C63FF` | Botones y elementos de énfasis |
| Secundario | `#48CAE4` | Acentos |
| Fondo | `#1E1E2E` | Fondo principal |
| Superficie | `#2A2A3E` | Tarjetas y paneles |
| Texto | `#E0E0E0` | Texto principal |
| Subtexto | `#9E9E9E` | Texto secundario |
| Éxito | `#4CAF50` | Confirmaciones |
| Error | `#EF5350` | Alertas y errores |
| Advertencia | `#FF9800` | Avisos |

---

### Flujo de Datos

```
Main.py
  ├── Crea listas compartidas: libros = [], clientes = []
  ├── Pasa listas a vista_libros(page, libros)
  ├── Pasa listas a VistaCliente(page, clientes)
  └── Pasa ambas listas a VistaPrestamos(page, libros, clientes)

vista_libros     → agrega/lee lista libros
vista_clientes   → agrega/lee lista clientes
vista_prestamos  → lee ambas listas, modifica estados de Libro y Cliente
```

Los cambios en las listas se reflejan en tiempo real en todas las vistas porque se comparte la misma referencia de lista en memoria.

---

## Validaciones Implementadas

| Sección | Validación |
|---------|------------|
| Libros | Campos obligatorios (Título, Autor, ISBN) |
| Libros | ISBN único — no se permiten duplicados |
| Clientes | Campos obligatorios (Nombre, Apellido, Cédula) |
| Clientes | Cédula única — no se permiten duplicados |
| Préstamos | Libro y cliente deben estar seleccionados |
| Préstamos | El libro seleccionado debe estar disponible |

---

## Licencia

Este proyecto está bajo la licencia incluida en el archivo [LICENSE](LICENSE).
