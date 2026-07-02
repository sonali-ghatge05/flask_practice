from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__) 
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "sonali@05"
app.config["MYSQL_DB"] = "flask_demo"

mysql = MySQL(app)

@app.route("/delete-student/<int:id>")
def delete_student(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM student WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return "Student deleted successfully!"