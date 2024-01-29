from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_sse import sse
#from redis import Redis
#from apscheduler.schedulers.background import BackgroundScheduler
import base64
from pyzbar.pyzbar import decode, ZBarSymbol
from PIL import Image
import pymysql
import json
import time

import os
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import logout_user
from flask_login import LoginManager,login_user

import logging
#logging.basicConfig(level=logging.DEBUG)
load_dotenv()

app = Flask(__name__)
app.secret_key = "cf1af03cab3c4a23a8bf29c98be721fd"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#client_id = os.getenv('GOOGLE_CLIENT_ID')
#client_id="735865591251-l0jkla2u8bhnlvv807cp8a0cd60714i9.apps.googleusercontent.com"
#client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
#client_secret = "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"
#app.secret_key = b'\xd4\xac\xa5\x1aX&\x82=\xda\xe309\xe1L\xbe\xd0'
#app.secret_key = "cf1af03cab3c4a23a8bf29c98be721fd"
#app.secret_key = os.getenv('secret_key')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

blueprint = make_google_blueprint(
    #client_id=client_id,
    client_id = "735865591251-l0jkla2u8bhnlvv807cp8a0cd60714i9.apps.googleusercontent.com",
    client_secret = "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",
    #app.secret_key = b'\xd4\xac\xa5\x1aX&\x82=\xda\xe309\xe1L\xbe\xd0'
    #client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    #client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email"],
    offline=True
)
app.register_blueprint(blueprint, url_prefix="/login")

#app.config["REDIS_URL"] = "redis://localhost"
#app.register_blueprint(sse, url_prefix='/stream')

@login_manager.user_loader
def load_user(user):
    return User.query.get(int(user))


@app.route("/")
def index():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()

    conn = pymysql.connect(
            db='shoppingcart',
            user='root',
            passwd='Anagha@02021998',
            host='localhost')
    c = conn.cursor()
    #c.execute("INSERT INTO espid_useremail VALUES (%s, %s);", (1, google_data["email"]))
    #conn.commit()
    c.execute("SELECT UID FROM Users WHERE EXISTS(SELECT * FROM Users WHERE User_Name=%s AND User_Email=%s);", (google_data["name"], google_data["email"]))
    records = c.fetchall()
    if c.rowcount == 0:
        c.execute("INSERT INTO Users(User_Name, User_Email) VALUES(%s, %s);", 
              (google_data["name"], google_data["email"]))
        conn.commit()
    return render_template('home.php',
                           google_data=google_data,
                           fetch_url=google.base_url + user_info_endpoint)

@app.route('/update',methods = ['GET'])
def update():
	return jsonify(result=time.time())

@app.route('/login')
def login():
    return redirect(url_for('google.login'))

@app.route('/logout')
def logout():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()
    
    conn = pymysql.connect(
            db='shoppingcart',
            user='root',
            passwd='Anagha@02021998',
            host='localhost')
    c = conn.cursor()
    c.execute("DELETE FROM espid_useremail WHERE useremail=%s;", (google_data["email"]))
    conn.commit()
    
    logout_user()
    return render_template('index.html')

@app.route('/cart', methods=['GET', 'POST'])
def index1():
    content_type = request.headers.get('Content-Type')
    img_encoded_json = request.get_json(force=True)

    img_encoded_string = img_encoded_json["img_key"]
    with open("/var/www/html/barcode_imgs/barcode_b.png" , "wb") as fh :
        fh.write(base64.b64decode(img_encoded_string))

    img = Image.open('/var/www/html/barcode_imgs/barcode_b.png')
    decoded_list = decode(img)
    if not decoded_list:
        webpage = "<html><body>No barcode found</body></html>"
        #sse.publish({"message": "No barcode found"}, type="publish")
        return webpage
        #return redirect("/mycart", 204)
    final_string1 = ""
    for i in decoded_list:
        final_string1 += i.data.decode("utf-8")
 
    conn = pymysql.connect(
            db='shoppingcart',
            user='root',
            passwd='Anagha@02021998',
            host='localhost')
    c = conn.cursor()
    c.execute("SELECT * FROM Products WHERE UPC=%s;", (int(final_string1)))
    records = c.fetchall()
    if c.rowcount == 0:
        webpage = "<html><body>[0]"+records[0][1]+"</body></html>"
        return webpage
    d = conn.cursor()
    d.execute("SELECT useremail FROM espid_useremail WHERE esp_id=1;")
    useremail = d.fetchall()
    sql = "INSERT INTO Items(UPC, user_Email, productName, productPrice, quantity) VALUES(%s, %s, %s, %s, %s);"
    try :
        c.execute(sql, (int(final_string1), str(useremail[0][0]), str(records[0][1]), int(records[0][2]), int(1)))
        conn.commit()
    except pymysql.Error as e:
        webpage = "<html><body>Error:"+e[0]+"</body></html>"
        return webpage

    webpage = "<html><body>The UPC Code is :"+final_string1+"</body></html>";
    return webpage

upc_global = []

@app.route('/display', methods=['GET'])
def display():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()

    conn = pymysql.connect(
            db='shoppingcart',
            user='root',
            passwd='Anagha@02021998',
            host='localhost')
    c = conn.cursor()
    c.execute("SELECT useremail FROM espid_useremail WHERE esp_id=1") 
    useremail = c.fetchall()

    c.execute("SELECT * FROM Items WHERE user_Email=%s;", (useremail))
    row_headers=[x[0] for x in c.description]
    records = c.fetchall()
#    records_json = []
    upc = []
    email = []
#    email.append(int(time.time()))
#    upc.append(int(time.time()))
    pname = []
    price=[]
    quantity = []
    for rec in records:
        if rec[0] in upc:
            index = upc.index(rec[0])
            quantity[index] = quantity[index]+1;
        else:        
       	    upc.append(rec[0])
            email.append(rec[1])
            pname.append(rec[2])
            price.append(rec[3])
            quantity.append(rec[4])
    
    global upc_global
    upc_global = upc
    return render_template('hiddencart.php',  upc=upc, email=email,pname=pname,price=price,quantity=quantity)
    #records_string = ""
#here   
#    for rec in records:
#        records_json.append(dict(zip(row_headers, rec)))
        #records_string+=str(rec)
#    return jsonify(records_json)

    #return records_string
    #render_template("mycart.php", google_data=google_data, fetch_url=google.base_url + user_info_endpoint)

@app.route('/mycart', methods=['GET', 'POST'])
def mycart():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()
    conn = pymysql.connect(
            db='shoppingcart',
            user='root',
            passwd='Anagha@02021998',
            host='localhost')
    c = conn.cursor()
    
    #try:
    #    c.execute("INSERT INTO espid_useremail VALUES (%s, %s);", (1, google_data["email"]))
    #    conn.commit()
    #except:
    #    return render_template("home.php", google_data=google_data, fetch_url=google.base_url + user_info_endpoint)

    #try:
    for i in upc_global:
        # app.logger.error("del:%s", request.form.get('deleteItem'))
        if request.form.get('deleteItem') == str(i):
            c.execute("DELETE FROM Items WHERE UPC=%s AND user_EMAIL=%s LIMIT 1;",(int(i),google_data["email"]))
            # app.logger.error("upc: %s, email: %s",(int(i),google_data["email"]))
            conn.commit()
    try :
        c.execute("INSERT INTO espid_useremail VALUES (%s, %s);", (1, google_data["email"]))
        conn.commit()
    except :
        return render_template("mycart.php", google_data=google_data, fetch_url=google.base_url + user_info_endpoint)
    
    #finally:
    return render_template("mycart.php", google_data=google_data, fetch_url=google.base_url + user_info_endpoint)

@app.route('/checkout', methods=['GET'])
def checkout():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()
        
    conn = pymysql.connect(
            db='shoppingcart',
            user='root',
            passwd='Anagha@02021998',
            host='localhost')
    c = conn.cursor()
    try :
        c.execute("DELETE FROM espid_useremail WHERE useremail=%s;", (google_data["email"]))
        c.execute("DELETE FROM Items WHERE user_Email=%s;", (google_data["email"]))
        conn.commit()
    except :
        return 
    finally:
        return render_template("home.php", google_data=google_data, fetch_url=google.base_url + user_info_endpoint)

@app.route('/del', methods=['GET', 'POST'])
def del_item():
    del_item_json = request.get_json(force=True)
    del_item_string = del_item_json["del_upc"]

    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()
        
    conn = pymysql.connect(
            db='shoppingcart',
            user='root',
            passwd='Anagha@02021998',
            host='localhost')
    c = conn.cursor()
    try :
        c.execute("DELETE FROM Items WHERE UPC=%s AND user_Email=%s;", (int(del_item_string), google_data["email"]))
        conn.commit()
    except:
        return
    finally:
        return render_template("mycart.php", google_data=google_data, fetch_url=google.base_url + user_info_endpoint)


@app.route('/test', methods=['GET','POST'])
def cart():    
    content_type = request.headers.get('Content-Type')
    #file = request.files['image']
    #img = Image.open(file.stream)
    #data = file.stream.read()

    #data = base64.b64encode(data).decode()

    img_encoded_json = request.get_json(force=True)
    #esp_id = img_encoded_json["esp_id"]
    #user_id = 2

    img_encoded_string = img_encoded_json["img_key"]
    decoded_img = base64.b64decode(img_encoded_string)

    with open("/var/www/html/barcode_imgs/barcode_a.png" , "wb") as fh :
        fh.write(decoded_img)

    #img = Image.open('/var/www/html/barcode_imgs/barcode_a.png')
    #decoded_list = decode(img)
    #if not decoded_list:
    #    webpage = "<html><body>No barcode found</body></html>"
    #    return webpage
    #img_type = decoded_list[0].type
    #final_string1 =
    #for i in decoded_list:
    #    final_string1 += i.data.decode("utf-8")

    #conn = pymysql.connect(
    #        db='shoppingcart',
    #        user='root',
    #        passwd='Anagha@02021998',
    #        host='localhost')
    #c = conn.cursor()

    #c.execute("INSERT INTO espID_userID_map VALUES (%s, %s);", (int(esp_id),
    #        int(user_id)));
    #conn.commit()

    webpage = f'<html><body><img src="data:image/jpeg;base64,{img_encoded_json.decode("utf-8")}"/></body></html>';

    #final_string = {'msg' : 'success',
    #                'size' : [img.width, img.height],
    #                'format' : img.format,
    #                'upcCode' : final_string1 }


    #webpage = "<html><body>The UPC Code is :"+final_string['upcCode']
    #webpage += "Image dimensions are : %s X %s" (int(final_string['size'][0]),int(final_string['size'][1]))
    #webpage += "Image format :"+final_string['format']+"</body></html>";
    return render_template(html)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
