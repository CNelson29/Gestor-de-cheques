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

@app.route('/productos')
def productos():
    producto_s = query_db('''
        SELECT * FROM productos 
    ''')
    return render_template('productos.html', producto_s=producto_s)

@app.route('/productos/agregar', methods=['POST'])
def agregar_producto():
    nombre = request.form['nombre']
    tipo = request.form['tipo']
    marca = request.form['marca']
    stock = request.form['Stock']
    execute_db('''
        INSERT INTO productos (nombre, tipo, marca, Stock)
        VALUES (%s, %s, %s, %s)
    ''', (nombre, tipo, marca, stock))
    flash('Producto agregado exitosamente')
    return redirect(url_for('productos'))

@app.route('/productos/eliminar/<int:id>')
def eliminar_producto(id):
    execute_db('DELETE FROM productos WHERE id = %s', (id,))
    flash('Producto eliminado exitosamente')
    return redirect(url_for('productos'))

@app.route('/ventas')
def ver_ventas():
# Consulta para obtener las ventas y detalles de los productos
    ventas = query_db('''
        SELECT v.id, p.nombre AS producto, v.cantidad, v.fecha 
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
    ''')
    
    # Consulta para obtener todos los productos disponibles
    productos = query_db('SELECT * FROM productos')

    return render_template('ver_ventas.html', ventas=ventas, productos=productos)

@app.route('/ventas/agregar', methods=['GET', 'POST'])
def agregar_venta():
    if request.method == 'POST':
        producto_id = request.form['producto_id']
        cantidad = int(request.form['cantidad'])
        fecha = request.form['fecha']

        # Agregar la venta
        execute_db('''
            INSERT INTO ventas (producto_id, cantidad, fecha)
            VALUES (%s, %s, %s)
        ''', (producto_id, cantidad, fecha))

        # Actualizar el stock del producto
        execute_db('''
            UPDATE productos SET Stock = Stock - %s WHERE id = %s
        ''', (cantidad, producto_id))

        flash('Venta agregada exitosamente')
        return redirect(url_for('ver_ventas'))  # Asegúrate de que esta ruta exista

@app.route('/ventas/eliminar/<int:id>')
def eliminar_venta(id):
    execute_db('DELETE FROM ventas WHERE id = %s', (id,))
    flash('Venta eliminada exitosamente')
    return redirect(url_for('ver_ventas'))


#---------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)