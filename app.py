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

# get product api
@app.route("/api/get_product")
def get_product():

    # create connection to my sql database
    connection=pymysql.connect(host="localhost",user="root",password="",database="mamba_sokogarden_stanley")

    # create a cursor
    cursor=connection.cursor(pymysql.cursors.DictCursor)

    # sql statement to insert the data
    sql="select * from products_details"

    # execute/run
    cursor.execute(sql)

    product=cursor.fetchall()

    # response
    return jsonify(product)

# Mpesa Payment Route/Endpoint 
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    if request.method == 'POST':
        amount = request.form['amount']
        phone = request.form['phone']
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,   # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/api/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return jsonify({"message": "Please Complete Payment in Your Phone and we will deliver in minutes"})
    




















































app.run(debug=True)