from conexion import conexion

def insertar_producto(producto):
    con = None
    cursor = None
    try:
        con = conexion()
        cursor = con.cursor()
        sql = """
        INSERT INTO productos
        (nombre, categoria, precio, stock)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, producto)
        con.commit()
        return True
    except Exception as error:
        print("Error al registrar producto:", error)
        return False
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

def consultar_productos():
    con = None
    cursor = None
    try:
        con = conexion()
        cursor = con.cursor()
        sql = """
        SELECT 
        id_producto,
        nombre,
        categoria,
        precio,
        stock
        FROM productos
        ORDER BY id_producto
        """
        cursor.execute(sql)
        productos = cursor.fetchall()
        return productos
    except Exception as error:
        print("Error al consultar productos:", error)
        return []
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

def buscar_producto(nombre):
    con = None
    cursor = None
    try:
        con = conexion()
        cursor = con.cursor()
        sql = """
        SELECT
        id_producto,
        nombre,
        categoria,
        precio,
        stock
        FROM productos
        WHERE nombre LIKE %s
        """
        cursor.execute(
            sql,
            ("%"+nombre+"%",)
        )
        producto = cursor.fetchone()
        return producto
    except Exception as error:
        print("Error al buscar producto:", error)
        return None
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

def buscar_producto_id(id_producto):
    con = None
    cursor = None
    try:
        con = conexion()
        cursor = con.cursor()
        sql = """
        SELECT
        id_producto,
        nombre,
        categoria,
        precio,
        stock
        FROM productos
        WHERE id_producto=%s
        """
        cursor.execute(
            sql,
            (id_producto,)
        )
        producto = cursor.fetchone()
        return producto
    except Exception as error:
        print("Error al buscar producto:", error)
        return None
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

def actualizar_producto(producto):
    con = None
    cursor = None
    try:
        con = conexion()
        cursor = con.cursor()
        sql = """
        UPDATE productos
        SET
        nombre=%s,
        categoria=%s,
        precio=%s,
        stock=%s
        WHERE id_producto=%s
        """
        cursor.execute(
            sql,
            producto
        )
        con.commit()
        return cursor.rowcount > 0
    except Exception as error:
        print("Error al actualizar producto:", error)
        return False
    finally:
        if cursor:
            cursor.close()

        if con:
            con.close()

def eliminar_producto(id_producto):
    con = None
    cursor = None
    try:
        con = conexion()
        cursor = con.cursor()
        # Eliminar detalles relacionados
        cursor.execute(
            "DELETE FROM detalle_venta WHERE id_producto=%s",
            (id_producto,)
        )
        # Eliminar producto
        cursor.execute(
            "DELETE FROM productos WHERE id_producto=%s",
            (id_producto,)
        )
        eliminado = cursor.rowcount > 0
        con.commit()
        return eliminado
    except Exception as error:
        print(error)
        return False
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

def actualizar_stock(id_producto, cantidad):
    con = None
    cursor = None
    try:
        con = conexion()
        cursor = con.cursor()
        sql = """
        UPDATE productos
        SET stock = stock - %s
        WHERE id_producto=%s
        """
        cursor.execute(
            sql,
            (
                cantidad,
                id_producto
            )
        )
        con.commit()
        return cursor.rowcount > 0
    except Exception as error:
        print("Error al actualizar stock:", error)
        return False
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

def vaciar_productos():
    con = None
    cursor = None
    try:
        con = conexion()
        cursor = con.cursor()
        sql = """
        TRUNCATE TABLE productos
        """
        cursor.execute(sql)
        con.commit()
        return True
    except Exception as error:
        print(
            "Error al vaciar productos:",
            error
        )
        return False
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()