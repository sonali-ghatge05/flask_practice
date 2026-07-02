from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "sonali@05"
app.config["MYSQL_DB"] = "flask_demo"

mysql=MySQL(app)

@app.route("/books")
def books():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM books")
    info = cursor.fetchall()
    cursor.close()
    return render_template("books.html", books=info)

@app.route("/add-books", methods=["GET", "POST"])
def add_books():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        price = float(request.form["price"])

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO books (title,author,price) VALUES (%s, %s, %s)", (title, author, price))
        mysql.connection.commit()
        cursor.close()

        return "Students added sucessfully!"
    
    return render_template("add_books.html")

@app.route("/delete-books/<int:id>")
def delete_books(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return "Student deleted!"

@app.route("/api/books", methods=["GET"])
def books_api():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()
    cursor.close()

    books_list = []
    for row in data:
        books_list.append({
            'id' : row[0],
            'title' : row[1],
            'author' : row[2],
            'price' : float(row[3])
        })
    return jsonify({
        'status' : 'success',
        'data' : books_list,
        'message' : "data fetched"
    }), 200

@app.route("/api/books/<int:id>" , methods=["GET"])
def find_book(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM books WHERE id=%s", (id,))
    data = cursor.fetchone()
    cursor.close()

    if data is None:
        return jsonify({
            'status' : 'error',
            'message' : 'book not found'
        }), 404
    else:
        books = ({
            'id' : data[0],
            'title' : data[1],
            'author' : data[2],
            'price' : float(data[3])
        })
        return jsonify({
            'status' : 'success',
            'message' : 'book has found',
            'data': books
        }), 200

@app.route("/api/books/expensive", methods = ["GET"])
def expensive_book():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM books WHERE price > 800")
    data = cursor.fetchall()
    cursor.close()

    expensive_books = []
    for row in data:
        expensive_books.append({
            'id' : row[0],
            'title' : row[1],
            'author' : row[2],
            'price' : float(row[3])
        })
    return jsonify({
        'status' : 'success',
        'data': expensive_books
    }),200



if __name__ == "__main__":
    app.run(debug=True)
