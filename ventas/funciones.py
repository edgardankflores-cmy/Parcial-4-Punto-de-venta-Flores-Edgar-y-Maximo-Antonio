# ventas/funciones.py


from ventas.crud import (
    registrar_venta,
    consultar_ventas,
    buscar_venta,
    consultar_detalle_venta
)

from productos.crud import (
    buscar_producto,
    actualizar_stock,
    consultar_productos
)

from utilidades import (
    limpiar,
    pausar,
    mostrar_titulo,
    generar_ticket
)


# CONSTANTES

from decimal import Decimal

IVA = Decimal("0.16")
DESCUENTO_NORMAL = Decimal("0.05")
DESCUENTO_MAYOR = Decimal("0.10")


# MENÚ DE VENTAS

def menu_ventas():
    opcion = 0
    while opcion != 4:
        limpiar()
        mostrar_titulo(
            "MÓDULO DE VENTAS"
        )
        print("""
        1. Nueva venta
        2. Historial de ventas
        3. Detalle de venta
        4. Regresar
        """)
        try:
            opcion = int(
                input(
                    "Seleccione una opción: "
                )
            )
            if opcion == 1:

                realizar_venta()
            elif opcion == 2:
                historial_ventas()
            elif opcion == 3:
                detalle_venta()
            elif opcion == 4:
                print(
                    "Regresando..."
                )
            else:
                print(
                    "Opción incorrecta"
                )
                pausar()
        except ValueError:
            print(
                "Ingrese solamente números"
            )
            pausar()

def mostrar_productos():
    productos = consultar_productos()
    print("\n=============================================")
    print("             PRODUCTOS DISPONIBLES")
    print("=============================================")
    print(
        f"{'ID':<5}{'PRODUCTO':<20}{'PRECIO':<12}{'STOCK':<10}"
    )
    print("---------------------------------------------")
    for producto in productos:
        print(
            f"{producto[0]:<5}"
            f"{producto[1]:<20}"
            f"${producto[3]:<11}"
            f"{producto[4]:<10}"
        )
    print("=============================================\n")


# REALIZAR VENTA
def realizar_venta():
    limpiar()
    mostrar_titulo(
        "NUEVA VENTA"
    )
    carrito = []
    mostrar_productos()
    continuar = True
    while continuar:
        nombre = input(
            "\nProducto: "
        ).strip()
        producto = buscar_producto(
            nombre
        )
        if producto is None:
            print(
                "Producto no encontrado"
            )
        else:
            try:
                cantidad = int(
                    input(
                        "Cantidad: "
                    )
                )
                if cantidad <= 0:
                    print(
                        "Cantidad inválida"
                    )
                elif cantidad > producto[4]:
                    print(
                        "Stock insuficiente"
                    )
                else:
                    importe = (
                        producto[3]
                        *
                        cantidad
                    )
                    item = {
                        "id_producto":
                        producto[0],

                        "nombre":
                        producto[1],


                        "cantidad":
                        cantidad,

                        "precio":
                        producto[3],

                        "importe":
                        importe

                    }
                    carrito.append(
                        item
                    )
                    print(
                        "Producto agregado correctamente"
                    )
            except ValueError:
                print(
                    "Cantidad inválida"
                )
        opcion = input(
            "\n¿Agregar otro producto? S/N: "
        )
        if opcion.upper() != "S":

            continuar = False
    if len(carrito) == 0:
        print(
            "No existen productos en la venta"
        )
        pausar()
        return
    procesar_pago(
        carrito
    )


def procesar_pago(carrito):

    subtotal = 0
    cantidad_productos = 0

    for producto in carrito:
        subtotal += producto["importe"]
        cantidad_productos += producto["cantidad"]

    # APLICAR DESCUENTO
    if cantidad_productos > 5:
        descuento = (
            subtotal
            *
            DESCUENTO_MAYOR
        )
    else:
        descuento = (
            subtotal
            *
            DESCUENTO_NORMAL
        )

    subtotal_final = (
        subtotal
        -
        descuento
    )

    impuesto = (
        subtotal_final
        *
        IVA
    )

    total = (
        subtotal_final
        +
        impuesto
    )

    limpiar()

    mostrar_titulo(
        "TICKET DE VENTA"
    )

    for producto in carrito:

        print(
            f"""
Producto:
{producto['nombre']}

Cantidad:
{producto['cantidad']}

Importe:
${producto['importe']:.2f}

------------------------
"""
        )

    print(
        f"Subtotal: ${subtotal:.2f}"
    )

    print(
        f"Descuento: ${descuento:.2f}"
    )

    print(
        f"IVA: ${impuesto:.2f}"
    )

    print(
        f"TOTAL: ${total:.2f}"
    )

    try:

        pago = Decimal(
            input("Pago recibido: ")
        )

        while pago < total:

            print(
                "\nDinero insuficiente."
            )

            print(
                "No se ha realizado ningún cargo."
            )

            pago = Decimal(
                input("Ingrese nuevamente el pago: ")
            )

        cambio = (
            pago
            -
            total
        )

        resultado = registrar_venta(

            subtotal,

            descuento,

            impuesto,

            total,

            pago,

            cambio,

            carrito

        )

        if resultado:

            for producto in carrito:

                actualizar_stock(

                    producto["id_producto"],

                    producto["cantidad"]

                )

            archivo = generar_ticket(

                carrito,

                subtotal,

                descuento,

                impuesto,

                total,

                pago,

                cambio

            )

            print(
                "\nVenta realizada correctamente"
            )

            print(
                f"Cambio: ${cambio:.2f}"
            )

            print(
                f"Ticket generado: {archivo}"
            )

        else:

            print(
                "Error al guardar venta"
            )

    except ValueError:

        print(
            "Pago inválido"
        )

    pausar()

# HISTORIAL DE VENTAS
def historial_ventas():
    limpiar()
    mostrar_titulo(
        "HISTORIAL DE VENTAS"
    )
    ventas = consultar_ventas()
    if len(ventas) == 0:
        print(
            "No existen ventas registradas"
        )
    else:
        for venta in ventas:
            print(
                f"""
-------------------------

ID:
{venta[0]}

Fecha:
{venta[1]}

Total:
${venta[5]:.2f}

-------------------------
"""
            )



    pausar()

# DETALLE DE VENTA

def detalle_venta():
    limpiar()
    mostrar_titulo(
        "DETALLE DE VENTA"
    )
    try:
        id_venta = int(
            input(
                "ID de venta: "
            )
        )
        venta = buscar_venta(
            id_venta
        )
        if venta is None:
            print(
                "Venta no encontrada"
            )
        else:
            detalles = consultar_detalle_venta(
                id_venta
            )
            for detalle in detalles:
                print(
                    f"""
Producto:
{detalle[1]}

Cantidad:
{detalle[2]}

Precio:
${detalle[3]}

Importe:
${detalle[4]}

---------------------
"""
                )



    except ValueError:


        print(
            "ID inválido"
        )

    pausar()