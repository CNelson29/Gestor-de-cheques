from urllib.parse import urlparse
from flask import Flask, make_response, render_template, request, redirect, session, url_for, flash ,send_file
from config import Config
from models import User, mysql, init_db, query_db, execute_db, queri_db
from models import User,get_user
from io import BytesIO
from MySQLdb import IntegrityError
#-------------------------------------------------------------------------------------------------------v--------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)
init_db(app)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

#-------------------------------------------------------------------------------------------------------------------------------------------------- parte nueva

@app.route('/home')
def home():
    return render_template('layout.html')

@app.route('/home/conceptos')
def concepto():
    conceptos = query_db('SELECT * FROM conceptos')
    return render_template('conceptos/index.html',conceptos=conceptos)

@app.route('/home/conceptos/Agregar', methods=['POST'])
def concepto_agregar():
    descripcion = request.form['descripcion']
    estado = request.form.get('estado', '0')  # Valor predeterminado '0' si no está marcado

    execute_db('''
        INSERT INTO conceptos (descripcion, estado)
        VALUES (%s, %s)
    ''', (descripcion, estado))
    flash('Concepto agregado exitosamente')
    return redirect(url_for('concepto'))


@app.route('/home/conceptos/eliminar/<int:id>')
def eliminar_concepto(id):
    execute_db('DELETE FROM conceptos WHERE id_concepto = %s', (id,))
    flash('Concepto eliminado exitosamente')
    return redirect(url_for('concepto'))

@app.route('/home/proveedores')
def proveedor():
# Consulta para obtener las ventas y detalles de los productos
    proveedor = query_db('''
        SELECT v.id, p.nombre AS producto, v.cantidad, v.fecha 
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
    ''')
    
    # Consulta para obtener todos los productos disponibles
    proveedores = query_db('SELECT * FROM proveedores')

    return render_template('proveedores/index.html', proveedores=proveedores)

@app.route('/home/proveedores/agregar', methods=['GET', 'POST'])
def agregar_proveedor():
    if request.method == 'POST':
        # Recuperar los datos del formulario
        nombre = request.form.get('nombre')
        tipo_persona = request.form.get('tipo_persona')
        identificacion = request.form.get('identificacion')
        balance = request.form.get('balance', 0.0)  # Balance opcional, valor predeterminado 0.0
        cuenta_contable = request.form.get('cuenta_contable', None)  # Campo opcional
        estado = request.form.get('estado', '1')  # Estado activo por defecto ('1' para activo, '0' para inactivo)

        # Validación simple
        if not nombre or not tipo_persona or not identificacion:
            flash("Por favor, completa todos los campos obligatorios.")
            return redirect(url_for('proveedor'))  # Redirige si falta algún campo obligatorio

        # Insertar el proveedor en la base de datos
        execute_db('''
            INSERT INTO proveedores (nombre, tipo_persona, identificacion, balance, cuenta_contable, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (nombre, tipo_persona, identificacion, balance, cuenta_contable, estado))

        flash('Proveedor agregado exitosamente')
        return redirect(url_for('proveedor'))

    # GET request para mostrar el formulario de agregar
    return render_template('proveedores/index.html')


@app.route('/home/proveedores/eliminar/<int:id>')
def eliminar_proveedor(id):
    execute_db('DELETE FROM proveedores WHERE id_proveedor = %s', (id,))
    flash('proveedor eliminado exitosamente')
    return redirect(url_for('proveedor'))


#---------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)