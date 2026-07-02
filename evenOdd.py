from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/number-form")
def root():
    return render_template("EvenOdd.html")

@app.route("/number-result", methods=["POST"])
def evenOdd():
    num = int(request.form["num"])
    #D1
    if num % 2 == 0 : 
        decision = "Even"
    else:
        decision = "Odd"
    #D2
    if num > 0:
        result = "Positive"

    elif num < 0:
        result = "Negative"
    else:
        result = "zero"

    return f"{num} is {decision} and {result}"

if __name__ == "__main__":
    app.run(debug=True)
    
