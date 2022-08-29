
from urllib import request, response
from flask import Flask, render_template, request,redirect , make_response
import mysql.connector
about_me = ""
data = None
list1 = [ 1,2,3]
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="ashvin2004",
  database = "notesmedia"
)
app = Flask(__name__)
@app.route('/' , methods = ["POST" , "GET" ])
def first_page( ):
    name = request.form.get("user_name")
    email = request.form.get("email")
   # print(name)
   # print(email)
   # PASS = request.form.get("password")

    mycursor = mydb.cursor()
    mycursor.execute("select user_id from users ORDER BY user_id DESC")
    data = mycursor.fetchall()
    mycursor.reset()
    NEW_UID = data[0][0]+1
    #print(NEW_UID)
    #print(data)


    #mycursor.execute(f"INSERT INTO users VALUES ( '{NEW_UID}' , '{email}','{PASS}', '{name}', 1 ,null, null, null)")
    #mydb.commit()
    

    return  render_template("form.html")


@app.route('/otppage' , methods = ["POST" , "GET" ])
def otp_page( ):
    default_pass = "1234"
    name = request.form.get("user_name")
    email = request.form.get("email")
    password =  request.form.get("password")
    otp = request.form.get("otp")

    if None not in (name , email , password):

        response = make_response(render_template("otppage.html"))

        response.set_cookie('signup_name' , name)
        response.set_cookie('signup_email' , email)
        response.set_cookie('signup_pass' , password)

        return response

    elif otp is not None:
        
        name = request.cookies.get("signup_name")
        email = request.cookies.get("signup_email")
        password = request.cookies.get("signup_pass")

        if default_pass == otp:
            print(True)
            return f'{name} , {email} , {password}'


    return  render_template("otppage.html")
app.run(debug = True)
