import mysql.connector
def conexion():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bd_ventas"
        )
        return con
    except mysql.connector.Error as error:
        print(
            "Error de conexión:",
            error
        )
        return None