from flask import Flask, request, jsonify
from flask_cors import CORS
from database import obtener_conexion

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "⚽ Servidor de MiOnce funcionando correctamente"

@app.route('/registrar', methods=['POST'])
def registrar_jugador():
    datos = request.json 
    
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
                INSERT INTO jugadores (nombre, apellido, fecha_nacimiento, telefono, direccion, correo, posicion, pie_dominante, altura, peso)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (
                datos['nombre'], 
                datos['apellido'], 
                datos['fecha_nacimiento'], 
                datos['telefono'], 
                datos['direccion'], 
                datos['correo'],
                datos['posicion'],
                datos['pie_dominante'],
                datos['altura'],
                datos['peso']
            )
            
            cursor.execute(query, valores)
            conexion.commit()
            
            cursor.close()
            conexion.close()
            return jsonify({"mensaje": "Jugador registrado con éxito en MiOnce"}), 201
            
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

@app.route('/jugadores', methods=['GET'])
def listar_jugadores():
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, apellido, fecha_nacimiento, telefono, direccion, correo, posicion, pie_dominante, altura, peso FROM jugadores ORDER BY id DESC")
            filas = cursor.fetchall()
            
            jugadores = []
            for fila in filas:
                jugadores.append({
                    "id": fila[0],
                    "nombre": fila[1],
                    "apellido": fila[2],
                    "fecha_nacimiento": str(fila[3]),
                    "telefono": fila[4],
                    "direccion": fila[5],
                    "correo": fila[6],
                    "posicion": fila[7],
                    "pie_dominante": fila[8],
                    "altura": fila[9],
                    "peso": fila[10]
                })
            
            cursor.close()
            conexion.close()
            return jsonify(jugadores), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
@app.route('/editar/<int:id>', methods=['PUT'])
def editar_jugador(id):
    datos = request.json
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            altura = float(datos.get('altura', 0) or 0)
            peso = float(datos.get('peso', 0) or 0)
            query = """
                UPDATE jugadores 
                SET nombre=%s, apellido=%s, fecha_nacimiento=%s, telefono=%s, direccion=%s, correo=%s, posicion=%s, pie_dominante=%s, altura=%s, peso=%s
                WHERE id=%s
            """
            valores = (
                datos['nombre'], datos['apellido'], datos['fecha_nacimiento'],
                datos['telefono'], datos['direccion'], datos['correo'], datos['posicion'], datos['pie_dominante'],
                datos['altura'], datos['peso'], id
            )
            cursor.execute(query, valores)
            conexion.commit()
            cursor.close()
            conexion.close()
            return jsonify({"mensaje": "Datos actualizados correctamente"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "Error de conexión"}), 500
    
@app.route('/eliminar/<int:id>', methods=['DELETE'])
def eliminar_jugador(id):
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "DELETE FROM jugadores WHERE id = %s"
            cursor.execute(query, (id,))
            conexion.commit()
            
            cursor.close()
            conexion.close()
            return jsonify({"mensaje": "Jugador eliminado con éxito"}), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)