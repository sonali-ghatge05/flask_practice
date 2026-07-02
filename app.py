from flask import Flask,render_template
app=Flask(__name__)

@app.route('/')
def hell0_world():
    return render_template('index.html')
    #return "hello world!"

@app.route('/products')
def products():
    return "This is products page"

if __name__ == "__main__":
    app.run(debug=True,port=8000)