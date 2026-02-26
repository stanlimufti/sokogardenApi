from flask import *
import pymysql
import os
# initialize your app
app=Flask(__name__)
if not os.path.exists("static/images"):
    os.makedirs("static/images")

app.config["UPLOAD_FOLDER"]="static/images"

# signup route or endpoint
@app.route("/api/signup",methods=["POST"])
def signup():
    # request inputs from a user
    username=request.form["Username"]
    email=request.form["Email"]
    password=request.form["Password"]
    phone=request.form["Phone"]

    # connect to mysql database
    connection=pymysql.connect(host="localhost",user="root",password="",database="mamba_sokogarden_stanley")

    # create cursor
    cursor=connection.cursor()

    # sql statement to insert the records
    sql="insert into users(username,email,password,phone)values(%s,%s,%s,%s)"

    # prepare the data
    data=(username,email,password,phone)

    # execute/run
    cursor.execute(sql,data)

    # commit
    connection.commit()

    # return a response
    return jsonify({"Message":"Thank you for joining"})
    
# signin api
# signin route

@app.route("/api/signin",methods=["POST"])
def signin():
    # request user input
    email=request.form["email"]
    password=request.form["password"]

    # create a conection
    connection=pymysql.connect(host="localhost",user="root",password="",database="mamba_sokogarden_stanley")

    # create a cursor
    cursor=connection.cursor(pymysql.cursor.DictCursor)

    # sql stataement to check the user
    sql="select * from users where email=%s and password=%s"

    # prepare the data
    data=(email , password)

    # execute/run the query
    cursor.execute(sql,data)

    # response
    if cursor.rowcount==0:
        return jsonify({"Message":"Login failed"})
    else:
        user=cursor.fetchone()
        user.pop("password",None)
        return jsonify({"Message":"login success","user":user})
    
# add product api
@app.route("/api/add_product",methods=["POST"])
def add_product():
    # request user data
    product_name=request.form["product_name"]
    product_description=request.form["product_description"]
    product_cost=request.form["product_cost"]
    product_photo=request.files["product_photo"]

    # extract photo name
    filename=product_photo.filename

    photo_path=os.path.join(app.config["UPLOAD_FOLDER"],filename)

    product_photo.save(photo_path)

    # create connection
    connection=pymysql.connect(host="localhost",user="root",password="",database="mamba_sokogarden_stanley")

    # create a cursor
    cursor=connection.cursor()

    # sql statement to insert the data
    sql="insert into products_details(product_name,product_description,product_cost,product_photo)values(%s,%s,%s,%s)"

    # prepare data
    data=(product_name,product_description,product_cost,filename)

    # execute/run
    cursor.execute(sql,data)

    # commit/save
    connection.commit()

    # response
    return jsonify({"Message":"Product add successfully"})




















































app.run(debug=True)