from productos.funciones import menu_productos
from ventas.funciones import menu_ventas
from utilidades import limpiar, pausar, mostrar_titulo

def menu_principal():
    opcion = 0
    while opcion != 3:
        limpiar()
        mostrar_titulo(
            "SISTEMA DE PUNTO DE VENTA"
        )
        print("""
        =============================
        1. Administración de productos
        2. Módulo de ventas
        3. Salir
        =============================
        """)
        try:
            opcion = int(
                input(
                    "Seleccione una opción: "
                )
            )
            if opcion == 1:
                menu_productos()
            elif opcion == 2:
                menu_ventas()
            elif opcion == 3:
                print(
                    """
                    Cerrando sistema...
                    Gracias por utilizar
                    el punto de venta
                    """
                )
            else:
                print(
                    "Opción no válida"
                )
                pausar()
        except ValueError:
            print(
                "Ingrese solamente números"
            )
            pausar()
menu_principal()