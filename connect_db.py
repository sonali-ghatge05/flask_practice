from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

#MYSQL configuration

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = "sonali@05"
app.config['MYSQL_DB'] = "flask_Demo"

mysql = MySQL(app)

@app.route("/student")
def student():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM student")
    data = cursor.fetchall()
    cursor.close()
    return render_template("student.html", students=data)

if __name__ == "__main__":
    app.run(debug=True)
    