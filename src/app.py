from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import config
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_USER"] = config.MYSQL_USER
app.config["MYSQL_DB"] = config.MYSQL_DB
app.config["MYSQL_PASSWORD"] = config.MYSQL_PASSWORD
app.config['SECRET_KEY'] = config.HEX_SEC_KEY

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('principal.html')  # Renderiza principal.html

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        if user is not None:
            session['email'] = email
            session['name'] = user[1]
            return redirect(url_for('inicio'))  # Redirigir al usuario a la página de inicio
        else:
            return render_template('login.html', message="Oops! Parece que tu email o contraseña no son correctos. ¿Quieres intentarlo de nuevo?")
    else:
        return render_template('login.html')

@app.route("/tasks", methods=['GET'])
def tasks():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    return render_template('tasks.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        
        cur = mysql.connection.cursor()
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("INSERT INTO tasks (nombre, descripcion, cantidad, fecha) VALUES (%s, %s, %s, %s)",
                    (nombre, descripcion, cantidad, fecha_actual))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('tasks'))

@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        cantidad = request.form.get("cantidad")  # Obtener la nueva cantidad del formulario

        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE tasks SET nombre = %s, descripcion = %s, cantidad = %s WHERE id = %s",
            (nombre, descripcion, cantidad, task_id),  # Agregar la cantidad al query de actualización
        )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("tasks"))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cur.fetchone()
        cur.close()
        return render_template("edit_task.html", task=task)

@app.route('/delete_task', methods=['POST'])
def delete_task():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        id = request.form['task_id']
        cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('eliminarproductos'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        cur.close()
        
        session['email'] = email
        session['name'] = name
        
        return redirect(url_for('inicio'))  # Redirigir al usuario a la página de inicio

@app.route('/inicio')  # Nueva ruta para la página inicio.html
def inicio():
    return render_template('inicio.html')  # Renderiza la página inicio.html

@app.route('/contactanos')  # Nueva ruta para la página contactanos.html
def contactanos():
    return render_template('contactanos.html')  # Renderiza la página contactanos.html

@app.route('/acerca') 
def acerca():
    return render_template('acerca.html') 

@app.route('/verproductos') 
def verproductos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    return render_template('ver-productos.html', tasks=tasks) 

@app.route('/eliminarproductos', methods=['GET', 'POST'])
def eliminarproductos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    return render_template('eliminar-productos.html', tasks=tasks)

@app.route('/rentas')
def rentas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()
    cur.execute("SELECT * FROM productos_carrito")
    productos_carrito = cur.fetchall()
    cur.close()
    return render_template('rentas.html', productos=productos, productos_carrito=productos_carrito)

@app.route('/agregar_al_carrito')
def agregar_al_carrito():
    # Lógica para agregar productos al carrito
    return 'Agregado al carrito'




if __name__ == '__main__':
    app.run(debug=True)
