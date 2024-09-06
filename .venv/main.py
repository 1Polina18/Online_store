from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

LOGIN = 'admin'
PASSWORD = '123'

# Функция для подключения к базе данных
def get_db_connection():
    return mysql.connector.connect(host='localhost', user='ppolinash', password='ZjBmPtk8aJ7', database='Online_store')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
def login():
    return render_template('auth.html')

@app.route('/auth', methods=['POST'])
def auth():
    login = request.form['login']
    password = request.form['password']
    if login == LOGIN and password == PASSWORD:
        return redirect(url_for('index'))
    else:
        return render_template('error.html')

@app.route("/db")
def exampleDb():
    dbMySql = get_db_connection()
    cursorMySql = dbMySql.cursor()
    query = "SELECT * FROM Goods"
    cursorMySql.execute(query)
    data = cursorMySql.fetchall()
    dbMySql.close()
    return render_template('db.html', data=data)


@app.route("/db/<int:item_id>")
def get_item(item_id):
    dbMySql = get_db_connection()
    cursorMySql = dbMySql.cursor()

    # Используем параметризованный запрос для извлечения товара по ID
    query = "SELECT * FROM Goods WHERE id = %s"
    cursorMySql.execute(query, (item_id,))
    item = cursorMySql.fetchone()
    dbMySql.close()
    if item:
        return render_template('item.html', item=item)
    else:
        return "Товар не найден", 404

# Create
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        availability_in_stock = request.form['availability_in_stock']
        quantity_in_stock = request.form['quantity_in_stock']

        dbMySql = get_db_connection()
        cursorMySql = dbMySql.cursor()
        query = "INSERT INTO Goods (Name, Description, Price, Availability_in_stock, Quantity_in_stock) VALUES (%s, %s, %s, %s, %s)"
        cursorMySql.execute(query, (name, description, price, availability_in_stock, quantity_in_stock))
        dbMySql.commit()
        dbMySql.close()
        return redirect(url_for('exampleDb'))
    return render_template('create.html')

# Update
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    dbMySql = get_db_connection()
    cursorMySql = dbMySql.cursor()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        availability_in_stock = request.form['availability_in_stock']
        quantity_in_stock = request.form['quantity_in_stock']

        query = "UPDATE Goods SET Name=%s, Description=%s, Price=%s, Availability_in_stock=%s, Quantity_in_stock=%s WHERE ID=%s"
        cursorMySql.execute(query, (name, description, price, availability_in_stock, quantity_in_stock, id))
        dbMySql.commit()
        dbMySql.close()
        return redirect(url_for('exampleDb'))

    query = "SELECT * FROM Goods WHERE ID=%s"
    cursorMySql.execute(query, (id,))
    good = cursorMySql.fetchone()
    dbMySql.close()
    return render_template('update.html', good=good)


# Delete
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    dbMySql = get_db_connection()
    cursorMySql = dbMySql.cursor()
    query = "DELETE FROM Goods WHERE ID=%s"
    cursorMySql.execute(query, (id,))
    dbMySql.commit()
    dbMySql.close()
    return redirect(url_for('exampleDb'))


# Ресурс для товаров
class GoodsResource(Resource):
    def get(self):
        dbMySql = get_db_connection()
        cursorMySql = dbMySql.cursor()
        query = "SELECT * FROM Goods"
        cursorMySql.execute(query)
        data = cursorMySql.fetchall()
        dbMySql.close()
        return jsonify(data)

    def post(self):
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        availability_in_stock = request.form['availability_in_stock']
        quantity_in_stock = request.form['quantity_in_stock']

        dbMySql = get_db_connection()
        cursorMySql = dbMySql.cursor()
        query = "INSERT INTO Goods (Name, Description, Price, Availability_in_stock, Quantity_in_stock) VALUES (%s, %s, %s, %s, %s)"
        cursorMySql.execute(query, (name, description, price, availability_in_stock, quantity_in_stock))
        dbMySql.commit()
        dbMySql.close()
        return '', 201

    def put(self, id):
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        availability_in_stock = request.form['availability_in_stock']
        quantity_in_stock = request.form['quantity_in_stock']

        dbMySql = get_db_connection()
        cursorMySql = dbMySql.cursor()
        query = "UPDATE Goods SET Name=%s, Description=%s, Price=%s, Availability_in_stock=%s, Quantity_in_stock=%s WHERE ID=%s"
        cursorMySql.execute(query, (name, description, price, availability_in_stock, quantity_in_stock, id))
        dbMySql.commit()
        dbMySql.close()
        return '', 200

    def delete(self, id):
        dbMySql = get_db_connection()
        cursorMySql = dbMySql.cursor()
        query = "DELETE FROM Goods WHERE ID=%s"
        cursorMySql.execute(query, (id,))
        dbMySql.commit()
        dbMySql.close()
        return '', 204


# Добавление ресурсов в API
api.add_resource(GoodsResource, '/goods', '/goods/<int:id>')






@app.route("/clients")
def clients():
    dbMySql = get_db_connection()
    cursorMySql = dbMySql.cursor()
    query = "SELECT * FROM Clients"
    cursorMySql.execute(query)
    clients = cursorMySql.fetchall()
    dbMySql.close()
    return render_template('clients.html', clients=clients)

@app.route("/clients/<int:item_id>")
def get_item2(item_id):
    dbMySql = get_db_connection()
    cursorMySql = dbMySql.cursor()
    # Используем параметризованный запрос для извлечения клиента по ID
    query = "SELECT * FROM Goods WHERE id = %s"
    cursorMySql.execute(query, (item_id,))
    item = cursorMySql.fetchone()
    dbMySql.close()
    if item:
        return render_template('item2.html', item=item)
    else:
        return "Клиент не найден", 404

@app.route('/create2', methods=['GET', 'POST'])
def create2():
    if request.method == 'POST':
        full_name = request.form['full_name']
        address = request.form['address']
        telephone = request.form['telephone']
        email = request.form['email']
        order_history = request.form['order_history']
        login = request.form['login']
        password = request.form['password']

        dbMySql = get_db_connection()
        cursorMySql = dbMySql.cursor()
        query = "INSERT INTO Clients (full_name, address, telephone, email, order_history, login, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursorMySql.execute(query, (full_name, address, telephone, email, order_history, login, password))
        dbMySql.commit()
        dbMySql.close()
        return redirect(url_for('clients'))
    return render_template('create2.html')


@app.route('/update2/<int:id>', methods=['GET', 'POST'])
def update2(id):
    dbMySql = get_db_connection()
    cursorMySql = dbMySql.cursor()

    if request.method == 'POST':
        full_name = request.form['full_name']
        address = request.form['address']
        telephone = request.form['telephone']
        email = request.form['email']
        order_history = request.form['order_history']
        login = request.form['login']
        password = request.form['password']

        query = "UPDATE Clients SET Full_name=%s, Address=%s, Telephone=%s, Email=%s, Order_history=%s, Login=%s, Password=%s WHERE ID=%s"
        cursorMySql.execute(query, (full_name, address, telephone, email, order_history, login, password, id))
        dbMySql.commit()
        dbMySql.close()
        return redirect(url_for('clients'))

    query = "SELECT * FROM Clients WHERE ID=%s"
    cursorMySql.execute(query, (id,))
    client = cursorMySql.fetchone()
    dbMySql.close()
    return render_template('update2.html', client=client)

@app.route('/delete2/<int:id>', methods=['POST'])
def delete2(id):
    dbMySql = get_db_connection()
    cursorMySql = dbMySql.cursor()
    query = "DELETE FROM Clients WHERE ID=%s"
    cursorMySql.execute(query, (id,))
    dbMySql.commit()
    dbMySql.close()
    return redirect(url_for('clients'))

# Ресурс для клиентов
class ClientsResource(Resource):
    def get(self):
        dbMySql = get_db_connection()
        cursorMySql = dbMySql.cursor()
        query = "SELECT * FROM Clients"
        cursorMySql.execute(query)
        data = cursorMySql.fetchall()
        dbMySql.close()
        return jsonify(data)

    def post(self):
        full_name = request.form['full_name']
        address = request.form['address']
        telephone = request.form['telephone']
        email = request.form['email']
        order_history = request.form['order_history']
        login = request.form['login']
        password = request.form['password']

        dbMySql = get_db_connection()
        cursorMySql = dbMySql.cursor()
        query = "INSERT INTO Clients (full_name, address, telephone, email, order_history, login, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursorMySql.execute(query, (full_name, address, telephone, email, order_history, login, password))
        dbMySql.commit()
        dbMySql.close()
        return '', 201

    def put(self, id):
        full_name = request.form['full_name']
        address = request.form['address']
        telephone = request.form['telephone']
        email = request.form['email']
        order_history = request.form['order_history']
        login = request.form['login']
        password = request.form['password']

        dbMySql = get_db_connection()
        cursorMySql = dbMySql.cursor()
        query = "UPDATE Clients SET Full_name=%s, Address=%s, Telephone=%s, Email=%s, Order_history=%s, Login=%s, Password=%s WHERE ID=%s"
        cursorMySql.execute(query, (full_name, address, telephone, email, order_history, login, password, id))
        dbMySql.commit()
        dbMySql.close()
        return '', 200

    def delete(self, id):
        dbMySql = get_db_connection()
        cursorMySql = dbMySql.cursor()
        query = "DELETE FROM Clients WHERE ID=%s"
        cursorMySql.execute(query, (id,))
        dbMySql.commit()
        dbMySql.close()
        return '', 204

# Добавление ресурсов в API
api.add_resource(ClientsResource, '/clients', '/clients/<int:id>')

