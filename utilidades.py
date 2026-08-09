import os
import re

def limpiar():
    os.system(
        "cls" if os.name == "nt" else "clear"
    )

def pausar():
    input(
        "\nPresione ENTER para continuar..."
    )

def mostrar_titulo(titulo):
    print("\n" + "=" * 45)
    print(
        titulo.center(45)
    )
    print("=" * 45)

def validar_nombre(nombre):
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$"
    return bool(
        re.match(
            patron,
            nombre
        )
    )

def validar_entero(numero):
    patron = r"^[0-9]+$"
    return bool(
        re.match(
            patron,
            numero
        )
    )

def validar_decimal(numero):
    patron = r"^[0-9]+(\.[0-9]+)?$"
    return bool(
        re.match(
            patron,
            numero
        )
    )

def validar_telefono(telefono):
    patron = r"^[0-9]{10}$"
    return bool(
        re.match(
            patron,
            telefono
        )
    )

def validar_correo(correo):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(
        re.match(
            patron,
            correo
        )
    )

def generar_ticket(
        productos,
        subtotal,
        descuento,
        iva,
        total,
        pago,
        cambio
):
    from datetime import datetime
    fecha = datetime.now()
    nombre_archivo = (
        f"Ticket_{fecha.strftime('%Y%m%d_%H%M%S')}.txt"
    )
    with open(
        nombre_archivo,
        "w",
        encoding="utf-8"
    ) as archivo:
        archivo.write(
            "========== PUNTO DE VENTA ==========\n\n"
        )
        archivo.write(
            f"Fecha: {fecha}\n\n"
        )
        archivo.write(
            "PRODUCTOS\n"
        )
        archivo.write(
            "-"*40 + "\n"
        )
        for producto in productos:
            archivo.write(
                f"""
Producto: {producto['nombre']}
Cantidad: {producto['cantidad']}
Precio: ${producto['precio']}
Importe: ${producto['importe']}

"""
            )
        archivo.write(
            "-"*40 + "\n"
        )
        archivo.write(
            f"Subtotal: ${subtotal:.2f}\n"
        )
        archivo.write(
            f"Descuento: ${descuento:.2f}\n"
        )
        archivo.write(
            f"IVA: ${iva:.2f}\n"
        )
        archivo.write(
            f"TOTAL: ${total:.2f}\n\n"
        )
        archivo.write(
            f"Pago: ${pago:.2f}\n"
        )
        archivo.write(
            f"Cambio: ${cambio:.2f}\n\n"
        )
        archivo.write(
            "====================================\n"
        )
        archivo.write(
            "Gracias por su compra\n"
        )
    return nombre_archivo