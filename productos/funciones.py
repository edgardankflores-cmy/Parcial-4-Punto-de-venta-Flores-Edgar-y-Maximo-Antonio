# productos/funciones.py


from productos.crud import (
    insertar_producto,
    consultar_productos,
    buscar_producto,
    buscar_producto_id,
    actualizar_producto,
    eliminar_producto
)

from utilidades import (
    limpiar,
    pausar,
    mostrar_titulo,
    validar_nombre,
    validar_entero,
    validar_decimal
)

# MENÚ DE PRODUCTOS
def menu_productos():
    opcion = 0
    while opcion != 6:
        limpiar()
        mostrar_titulo(
            "ADMINISTRACIÓN DE PRODUCTOS"
        )
        print("""
        1. Registrar producto
        2. Mostrar productos
        3. Buscar producto
        4. Actualizar producto
        5. Eliminar producto
        6. Regresar
        """)
        try:
            opcion = int(
                input("Seleccione una opción: ")
            )
            if opcion == 1:
                registrar_producto()
            elif opcion == 2:
                listar_productos()
            elif opcion == 3:
                buscar_productos()
            elif opcion == 4:
                modificar_producto()
            elif opcion == 5:
                borrar_producto()
            elif opcion == 6:
                print("Regresando...")
            else:
                print("Opción inválida")
                pausar()
        except ValueError:
            print("Ingrese solamente números")
            pausar()

# REGISTRAR PRODUCTO

def registrar_producto():
    limpiar()
    mostrar_titulo(
        "REGISTRAR PRODUCTO"
    )
    nombre = input(
        "Nombre del producto: "
    ).strip()
    # REGEX PARA NOMBRE
    if not validar_nombre(nombre):
        print(
            "El nombre solo puede contener letras"
        )
        pausar()
        return
    categoria = input(
        "Categoría: "
    ).strip()
    if categoria == "":
        print(
            "La categoría no puede estar vacía"
        )
        pausar()
        return
    precio_texto = input(
        "Precio: "
    )
    # REGEX PARA PRECIO
    if not validar_decimal(precio_texto):
        print(
            "Precio inválido"
        )
        pausar()
        return
    precio = float(
        precio_texto
    )
    stock_texto = input(
        "Stock inicial: "
    )
    # REGEX PARA STOCK
    if not validar_entero(stock_texto):
        print(
            "Stock inválido"
        )
        pausar()
        return
    stock = int(
        stock_texto
    )
    if precio <= 0:
        print(
            "El precio debe ser mayor a cero"
        )
        pausar()
        return
    producto = (
        nombre,
        categoria,
        precio,
        stock
    )
    resultado = insertar_producto(
        producto
    )
    if resultado:
        print(
            "\nProducto registrado correctamente"
        )
    else:
        print(
            "\nNo se pudo registrar el producto"
        )
    pausar()

# LISTAR PRODUCTOS
def listar_productos():
    limpiar()
    mostrar_titulo(
        "LISTA DE PRODUCTOS"
    )
    productos = consultar_productos()
    if len(productos) == 0:
        print(
            "No existen productos registrados"
        )
    else:
        print(
            "\nID | Nombre | Categoría | Precio | Stock"
        )
        print("-"*55)
        for producto in productos:
            print(
                f"{producto[0]} | "
                f"{producto[1]} | "
                f"{producto[2]} | "
                f"${producto[3]} | "
                f"{producto[4]}"
            )
    pausar()

# BUSCAR PRODUCTO
def buscar_productos():
    limpiar()
    mostrar_titulo(
        "BUSCAR PRODUCTO"
    )
    nombre = input(
        "Nombre del producto: "
    )
    producto = buscar_producto(
        nombre
    )
    if producto:
        print(
            """
            Producto encontrado
            --------------------
            """
        )
        print(
            f"ID: {producto[0]}"
        )
        print(
            f"Nombre: {producto[1]}"
        )
        print(
            f"Categoría: {producto[2]}"
        )
        print(
            f"Precio: ${producto[3]}"
        )
        print(
            f"Stock: {producto[4]}"
        )
    else:
        print(
            "Producto no encontrado"
        )
    pausar()

# ACTUALIZAR PRODUCTO
def modificar_producto():
    limpiar()
    mostrar_titulo(
        "ACTUALIZAR PRODUCTO"
    )
    try:
        id_producto = int(
            input("ID del producto: ")
        )
        producto_actual = buscar_producto_id(
            id_producto
        )
        if producto_actual is None:
            print(
                "Producto no encontrado"
            )
            pausar()
            return
        nombre = input(
            "Nuevo nombre: "
        )
        if nombre != "":
            if not validar_nombre(nombre):
                print(
                    "Nombre inválido"
                )
                pausar()

                return
        else:
            nombre = producto_actual[1]
        categoria = input(
            "Nueva categoría: "
        )
        if categoria == "":

            categoria = producto_actual[2]
        precio = input(
            "Nuevo precio: "
        )
        if precio == "":

            precio = producto_actual[3]
        else:
            if not validar_decimal(precio):
                print(
                    "Precio inválido"
                )
                pausar()
                return
            precio = float(precio)
        stock = input(
            "Nuevo stock: "
        )
        if stock == "":
            stock = producto_actual[4]
        else:
            if not validar_entero(stock):
                print(
                    "Stock inválido"
                )
                pausar()
                return
            stock = int(stock)
        datos = (
            nombre,
            categoria,
            precio,
            stock,
            id_producto
        )
        resultado = actualizar_producto(
            datos
        )
        if resultado:
            print(
                "Producto actualizado"
            )
        else:
            print(
                "No se pudo actualizar"
            )
    except ValueError:
        print(
            "ID inválido"
        )
    pausar()

# ELIMINAR PRODUCTO
def borrar_producto():
    limpiar()
    mostrar_titulo(
        "ELIMINAR PRODUCTO"
    )
    try:
        id_producto = int(
            input("ID del producto: ")
        )
        producto = buscar_producto_id(
            id_producto
        )
        if producto is None:
            print(
                "Producto no encontrado"
            )
            pausar()
            return
        print(
            f"""
            Producto:
            {producto[1]}

            Precio:
            ${producto[3]}
            """
        )
        confirmar = input(
            "¿Eliminar producto? S/N: "
        )
        if confirmar.upper() == "S":
            resultado = eliminar_producto(
                id_producto
            )
            if resultado:
                print(
                    "Producto eliminado"
                )
            else:
                print(
                    "No se pudo eliminar"
                )
        else:
            print(
                "Operación cancelada"
            )
    except ValueError:
        print(
            "ID inválido"
        )
    pausar()