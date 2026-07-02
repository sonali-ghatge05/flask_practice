from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "sonali@05"
app.config["MYSQL_DB"] = "flask_demo"

mysql=MySQL(app)

@app.route("/products")
def products():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products")
    info = cursor.fetchall()
    cursor.close()
    return render_template("products.html", products=info)

@app.route("/add-products", methods=["GET", "POST"])
def add_products():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        stock = int(request.form["stock"])
        price = float(request.form["price"])

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO products (name, category, stock, price) VALUES (%s, %s, %s, %s)", (name, category, stock, price))
        mysql.connection.commit()
        cursor.close()
        return "Products added successfully!"
    
    return render_template("add_products.html")

@app.route('/delete-products/<int:id>')
def delete_product(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return "Product deleted!"

@app.route('/update-products/<int:id>', methods=['GET', 'POST'])
def update_products(id):
    if request.method == 'POST':
        name = request.form["name"]
        category = request.form["category"]
        stock = int(request.form["stock"])
        price = float(request.form["price"])

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE products 
            SET name=%s, category=%s, stock=%s, price=%s
            WHERE id=%s
        """, (name, category, stock, price, id))
        mysql.connection.commit()
        cursor.close()
        return "Products updated!"
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products WHERE id=%s", (id,))
    product = cursor.fetchone()
    cursor.close()
    return render_template('update_products.html', product=product)

if __name__ == "__main__":
    app.secret_key = "your_secret_key"
    app.run(debug=True)
