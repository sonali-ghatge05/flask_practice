from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/form")
def form():
    return render_template("login.html")

@app.route("/check-login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username == "admin" and password == "1234":
        return "Welcome Admin"
    else:
        return "wrong Credentials"
if __name__ == "__main__":
    app.run(debug=True)