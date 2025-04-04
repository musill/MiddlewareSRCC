import sqlite3
from flask import Flask, jsonify, request

# Conexión a la base de datos
def conectar():
    return sqlite3.connect('Middleware_P.db')

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Crear la tabla de estudiantes si no existe
conexion = conectar()
cursor = conexion.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS estudiantes (
        ci INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL
    )
''')
conexion.commit()
conexion.close()


# Ruta para obtener todos los estudiantes
@app.route('/estudiante', methods=['GET'])
def obtener_estudiantes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM estudiantes")
    estudiantes = cursor.fetchall()
    conexion.close()
    return jsonify(estudiantes)

# Ruta para obtener un estudiante por su ID
@app.route('/estudiante/<int:ci>', methods=['GET'])
def obtener_estudiante_por_id(ci):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM estudiantes WHERE ci = ?", (ci,))
    estudiante = cursor.fetchone()
    conexion.close()
    if estudiante:
        return jsonify(estudiante)
    else:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

# Ruta para crear un nuevo estudiante
@app.route('/estudiante', methods=['POST'])
def crear_nuevo_estudiante():
    data = request.get_json()
    if 'ci' in data and 'nombre' in data:
        conexion = conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO estudiantes (ci, nombre) VALUES (?, ?)", (data['ci'], data['nombre']))
            conexion.commit()
            mensaje = {'mensaje': 'Estudiante creado exitosamente'}
        except sqlite3.IntegrityError:
            mensaje = {'error': 'El CI ya existe'}
        conexion.close()
        return jsonify(mensaje), 201
    else:
        return jsonify({'error': 'CI y nombre son requeridos'}), 400

# Ruta para actualizar un estudiante
@app.route('/estudiante/<int:ci>', methods=['PUT'])
def actualizar_estudiante_por_id(ci):
    data = request.get_json()
    if 'nombre' in data:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("UPDATE estudiantes SET nombre = ? WHERE ci = ?", (data['nombre'], ci))
        conexion.commit()
        conexion.close()
        if cursor.rowcount > 0:
            return jsonify({'mensaje': 'Estudiante actualizado exitosamente'})
        else:
            return jsonify({'error': 'Estudiante no encontrado'}), 404
    else:
        return jsonify({'error': 'Nombre es requerido'}), 400

# Ruta para eliminar un estudiante
@app.route('/estudiante/<int:ci>', methods=['DELETE'])
def eliminar_estudiante_por_id(ci):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM estudiantes WHERE ci = ?", (ci,))
    conexion.commit()
    conexion.close()
    if cursor.rowcount > 0:
        return jsonify({'mensaje': 'Estudiante eliminado exitosamente'})
    else:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=False)  
