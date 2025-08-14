import mysql.connector


def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="2639#Lany",
            database="ht3"
        )
        if conn.is_connected():
            print("Conexion establecida")
            return conn
    except mysql.connector.Error as err:
        print(err)

    return None
