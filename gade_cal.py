from flask import Flask, request, render_template

app =Flask(__name__)

@app.route("/")
def home():
    return render_template("grade.html")

@app.route("/grade", methods=["POST"])
def grade():
    marks = int(request.form["marks"])

    if marks >= 90 and marks <= 100:
        return "Grade:A"
    elif marks >= 75 and marks <=89:
        return "Grade:B"
    elif marks >=60 and marks <=74:
        return "Grade:C"
    elif marks > 100 or marks < 0:
        return "Tnvalid marks"
    else:
        return "Grade:F"
    
if __name__ == "__main__":
    app.run(debug=True)
    
