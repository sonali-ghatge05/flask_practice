from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "mysecretkey"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "sonali@05"
app.config["MYSQL_DB"] = "flask_demo"

mysql =MySQL(app)

@app.route("/employees")
def employee():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM employees WHERE salary > 30000")
    data = cursor.fetchall()
    cursor.close()
    return render_template("employee.html", employees=data)

@app.route("/add-employee", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        name = request.form["name"]
        department = request.form ["department"]
        salary = float(request.form["salary"])
        email = request.form["email"]
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO employees (name, department, salary, email) VALUES (%s, %s, %s, %s)", (name, department, salary, email))
        mysql.connection.commit()
        cursor.close()
        flash("Employee added successfully!", "success")
        return redirect(url_for('employee'))
    return render_template("add_employee.html")

@app.route("/delete-employee/<int:id>")
def delete_employee(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM employees WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    flash("Employee deleted successfully!", "success")
    return redirect(url_for('employee'))

@app.route('/update-employee/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    if request.method == 'POST':
        name = request.form["name"]
        department = request.form ["department"]
        salary =float(request.form["salary"])
        email = request.form["email"]

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE employees
            SET name=%s, department=%s, salary=%s, email=%s
            WHERE id=%s
        """, (name, department, salary, email, id))
        mysql.connection.commit()
        cursor.close()
        flash("Employee updated successfully!", "success")
        return redirect(url_for('employee'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM employees WHERE id=%s", (id,))
    employee = cursor.fetchone()
    cursor.close()
    return render_template('update_employee.html', employee=employee)


@app.route('/api/employees', methods = ["GET"])
def api_employee():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM employees")
    data = cursor.fetchall()
    cursor.close()

    employee_list = []
    for row in data:
        employee_list.append({
            'id' : row[0],
            'name' : row[1],
            'department' : row[2],
            'salary' : float(row[3]),
            'email' : row[4]
        })

    return jsonify({
        'status': 'success',
        'data': employee_list
    }), 200

@app.route("/api/employees/<int:id>", methods=["GET"])
def specific_emp(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM employees WHERE id = %s", (id,))
    data = cursor.fetchone()
    cursor.close()

    if data is None:
        return jsonify({
            'status': 'error',
            'message': 'Employee not found'
        }), 404
    else:
        employee = {
            'id': data[0],
            'name': data[1],
            'department': data[2],
            'salary': float(data[3]),
            'email': data[4]
        }
        return jsonify({
            'status': 'success',
            'data': employee
        }), 200
    
@app.route("/api/departments", methods = ["GET"])
def dept():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT department, COUNT(*) FROM employees GROUP BY department")
    data = cursor.fetchall()
    cursor.close()

    dept_list = []
    for row in data:
        dept_list.append({
            'department' : row[0],
            'count' :  row[1]
        })

    return jsonify({
        'status' : 'sucess',
        'data': dept_list
    }),200



if __name__ == "__main__":
    app.run(debug=True)