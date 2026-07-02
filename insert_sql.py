from flask import Flask, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "sonali@05"
app.config["MYSQL_DB"] = "flask_demo"

mysql =MySQL(app)

@app.route("/student")
def student():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM student")
    data = cursor.fetchall()
    cursor.close()
    return render_template("student.html", students=data)

@app.route("/add-student", methods = ["GET", "POST"])
def add_students():
    if request.method == "POST":
        name = request.form['name']
        age = int(request.form['age'])
        email = request.form['email']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO student (name, age, email) values (%s, %s, %s)", (name,age,email))
        mysql.connection.commit()
        cursor.close()

        return "Student added successfully!"
    
    
    return render_template('add_student.html')

@app.route('/delete-student/<int:id>')
def delete_student(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM student WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return "Student deleted!"

@app.route('/update-student/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        email = request.form['email']

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE student 
            SET name=%s, age=%s, email=%s 
            WHERE id=%s
        """, (name, age, email, id))
        mysql.connection.commit()
        cursor.close()
        return "Student updated!"

    # GET — fetch current data to pre-fill the form
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM student WHERE id=%s", (id,))
    student = cursor.fetchone()
    cursor.close()
    return render_template('update_student.html', student=student)

if __name__ == "__main__":
    app.run(debug=True)
