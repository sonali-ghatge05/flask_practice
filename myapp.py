from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/form")
def form():
    return render_template("name.html")

@app.route("/greet", methods=['POST'])
def greet():
    name = request.form["username"]
    return f"Hello, {name}! Thanks for submitting"

@app.route('/search')
def search():
    term = request.args.get('term')
    return f"You searched for: {term}"

if __name__ == "__main__":
    app.run(debug=True)