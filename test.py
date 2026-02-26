from flask import *


# initialize the flask app
app=Flask(__name__)

# create route
@app.route("/api/home")
def home():
    return jsonify({"Message":"Welcome to Home Api"})

# craete the product route
@app.route("/api/product")
def product():
    return jsonify({"Message":"Welcome to product Api"})

# create services route
@app.route("/api/services")
def service():
    return jsonify({"Message":"Welcome to our Services Api"})

# route for adding two numbers
@app.route("/api/calc",methods=["POST"])
def calc():
    # request the data
    num1=request.form["num1"]
    num2=request.form["num2"]

    sum=int(num1)+int(num2)

    return jsonify({"Answer":sum})

# route for multiplying two numbers
@app.route("/api/multiply",methods=["POST"])
def multiply():
    # request the data
    num1=request.form["num1"]
    num2=request.form["num2"]

    multiply=int(num1)*int(num2)

    return jsonify({"answer":multiply})

app.run(debug=True)