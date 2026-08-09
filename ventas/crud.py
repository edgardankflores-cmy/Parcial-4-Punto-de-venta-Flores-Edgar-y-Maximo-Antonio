# ventas/crud.py

from conexion import conexion
from datetime import datetime
# ==========================================
# REGISTRAR VENTA COMPLETA
# ==========================================
def registrar_venta(
    subtotal,
    descuento,
    iva,
    total,
    pago,
    cambio,
    productos
):
    con = None
    cursor = None
    try:
        con = conexion()
        cursor = con.cursor()
        # Iniciar transacción
        fecha = datetime.now()
        sql_venta = """
        INSERT INTO ventas
        (
            fecha,
            subtotal,
            descuento,
            iva,
            total,
            pago,
            cambio
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s)

        """
        datos_venta = (
            fecha,
            subtotal,
            descuento,
            iva,
            total,
            pago,
            cambio
        )
        cursor.execute(
            sql_venta,
            datos_venta
        )
        # Obtener ID generado
        id_venta = cursor.lastrowid
        registrar_detalle_venta(
            cursor,
            id_venta,
            productos
        )
        con.commit()
        return True
    except Exception as error:
        if con:
            con.rollback()
        print(
            "Error al registrar venta:",
            error
        )
        return False
    finally:
        if cursor:

            cursor.close()
        if con:
            con.close()
# ==========================================
# REGISTRAR DETALLE DE VENTA
# ==========================================
def registrar_detalle_venta(
    cursor,
    id_venta,
    productos
):
    sql = """
    INSERT INTO detalle_venta
    (
        id_venta,
        id_producto,
        cantidad,
        precio,
        importe
    )
    VALUES
    (%s,%s,%s,%s,%s)

    """
    for producto in productos:
        datos = (

            id_venta,
            producto["id_producto"],
            producto["cantidad"],
            producto["precio"],
            producto["importe"]

        )
        cursor.execute(
            sql,
            datos
        )
# ==========================================
# CONSULTAR TODAS LAS VENTAS
# ==========================================
def consultar_ventas():
    con = None
    cursor = None
    try:
        con = conexion()
        cursor = con.cursor()
        sql = """
        SELECT
        id_venta,
        fecha,
        subtotal,
        descuento,
        iva,
        total,
        pago,
        cambio
        FROM ventas
        ORDER BY id_venta DESC
        """
        cursor.execute(sql)
        ventas = cursor.fetchall()
        return ventas
    except Exception as error:
        print(
            "Error al consultar ventas:",
            error
        )
        return []
    finally:
        if cursor:

            cursor.close()
        if con:
            con.close()
# ==========================================
# BUSCAR VENTA POR ID
# ==========================================
def buscar_venta(id_venta):
    con = None
    cursor = None
    try:
        con = conexion()
        cursor = con.cursor()
        sql = """
        SELECT
        id_venta,
        fecha,
        subtotal,
        descuento,
        iva,
        total,
        pago,
        cambio
        FROM ventas
        WHERE id_venta=%s

        """
        cursor.execute(
            sql,
            (id_venta,)
        )
        venta = cursor.fetchone()
        return venta
    except Exception as error:
        print(
            "Error al buscar venta:",
            error
        )
        return None
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()
# ==========================================
# MOSTRAR DETALLE DE UNA VENTA
# ==========================================
def consultar_detalle_venta(id_venta):
    con = None
    cursor = None
    try:
        con = conexion()
        cursor = con.cursor()
        sql = """
        SELECT
        d.id_producto,
        p.nombre,
        d.cantidad,
        d.precio,
        d.importe
        FROM detalle_venta d

        INNER JOIN productos p
        ON d.id_producto = p.id_producto
        WHERE d.id_venta=%s
        """
        cursor.execute(
            sql,
            (id_venta,)
        )
        detalle = cursor.fetchall()
        return detalle
    except Exception as error:
        print(
            "Error al consultar detalle:",
            error
        )
        return []
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

# ELIMINAR VENTA

def eliminar_venta(id_venta):
    con = None
    cursor = None
    try:
        con = conexion()
        cursor = con.cursor()
        # Primero eliminamos detalles
        sql_detalle = """
        DELETE FROM detalle_venta
        WHERE id_venta=%s
        """
        cursor.execute(
            sql_detalle,
            (id_venta,)
        )
        # Después eliminamos venta
        sql_venta = """
        DELETE FROM ventas
        WHERE id_venta=%s
        """
        cursor.execute(
            sql_venta,
            (id_venta,)
        )
        con.commit()
        return cursor.rowcount > 0
    except Exception as error:
        print(
            "Error al eliminar venta:",
            error
        )
        return False
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

# ACTUALIZAR VENTA

def actualizar_venta(datos):
    con = None
    cursor = None
    try:
        con = conexion()
        cursor = con.cursor()
        sql = """
        UPDATE ventas
        SET
        subtotal=%s,
        descuento=%s,
        iva=%s,
        total=%s,
        pago=%s,
        cambio=%s
        WHERE id_venta=%s
        """
        cursor.execute(
            sql,
            datos
        )
        con.commit()
        return cursor.rowcount > 0
    except Exception as error:
        print(
            "Error al actualizar venta:",
            error
        )
        return False
    finally:
        if cursor:

            cursor.close()
        if con:
            con.close()

# VACIAR VENTAS

def vaciar_ventas():
    con = None
    cursor = None
    try:
        con = conexion()
        cursor = con.cursor()
        cursor.execute(
            "DELETE FROM detalle_venta"
        )
        cursor.execute(
            "DELETE FROM ventas"
        )
        con.commit()
        return True
    except Exception as error:
        print(
            "Error al vaciar ventas:",
            error
        )
        return False
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()