import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def obtener_conexion():
    try:
        conexion = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            port=os.getenv('DB_PORT')
        )
        return conexion
    except Exception as error:
        print(f"❌ Error al conectar: {error}")
        return None

def crear_tablas():
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS jugadores (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                apellido VARCHAR(50) NOT NULL,
                fecha_nacimiento DATE NOT NULL,
                telefono VARCHAR(20),
                direccion TEXT,
                correo VARCHAR(100) UNIQUE NOT NULL
                posicion VARCHAR(30),
                pie_dominante VARCHAR(20),   
                altura FLOAT,                
                peso FLOAT,
            );
            """
            cursor.execute(query)
            conexion.commit()
            print("✅ Tabla 'jugadores' lista para usar.")
            cursor.close()
            conexion.close()
        except Exception as error:
            print(f"❌ Error al crear la tabla: {error}")

if __name__ == "__main__":
    crear_tablas()