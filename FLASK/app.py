
from urllib import request
from flask import Flask, render_template, request,redirect
app = Flask(__name__)
id = ""
password= ""
num = ["Atomic Structure" , "determinents", "D and F Block"]
data = []
name = ""

import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="ashvin2004",
  database = "notesmedia"
)
@app.route('/' , methods = ["POST" , "GET" ])

def first_page():

    
    
    if request.method == "POST":
        #print(request.form.get("user"))
        id = request.form.get("user")
        password = request.form.get("pass")

        print(id)
    

        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM PUBLISHERS WHERE PUBLISHER_NAME = '{id}'")

        data = mycursor.fetchall()
        print(data)
        try:

            if data[0][2] == password:
                print("verified")
                verified = True
                return redirect(f"/{id}")
            else:
                print("not verified")
                verified = False
        except:
            print("Not verified")
            verified = False


    return  render_template("index.html")



@app.route('/secondpage'  ,methods = ["POST", "GET"])
def  publishers_portal_page():

    
    email = request.form.get("email")

    mycursor = mydb.cursor()


    mycursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
    data = mycursor.fetchone()
    print(data)

    mycursor.execute(f"SELECT * FROM notes WHERE publisher_id = '{data[0]}'")
    publications = mycursor.fetchall()
    print(publications)

   
    


    return  render_template("about me.html" ,  data = data , publications = publications, id = data[0])

@app.route('/secondpage/insights' ,methods = ["POST", "GET"] )
def insights():
    global name
    name = request.form.get("user")
    #name = "MESSI"
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM publishers WHERE PUBLISHER_NAME = '{name}'")
    #print(name)
    data = mycursor.fetchall()
    print(data)
    id = data[0][0]
    print(id)
    mycursor.execute(f"SELECT * FROM published WHERE PID = '{id}'")
    data1 = mycursor.fetchall()
    print(data1)
    num = [item[1].upper() for item in data1]
    



    return  render_template("layout1.html" , list1 = num)


@app.route('/secondpage/publish'  ,methods = ["POST", "GET"])
def publish_page():
   
    id  = request.form.get("id")
    tittle = request.form.get("tittle")
    subject = request.form.get("subject")
    description = request.form.get("about")
    
    print(id , tittle )
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM  users WHERE user_id = '{id}'")
    data = mycursor.fetchall()

    print(" this shit was published by " + id)
    #id3 = data[0][0]
 #  if request.method == 'POST':



 #      p = request.files['file']
 #      p.save(f"C:/FLASK/notes/{id3}.pdf")

 # 
    return  render_template("layout.html" )
@app.route('/secondpage/publish/complete'  ,methods = ["POST", "GET"])
def complete_page():
    if request.method == 'POST':
        name_1 = request.form.get("id")
        p = request.files['file']
        
        tittle = request.form.get("tittle")
        subject = request.form.get("subject")
        description = request.form.get("about")
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT note_id FROM notes  ORDER BY note_id DESC")
        data = mycursor.fetchall()
        print(data)
        print(subject)
        print(description)
        NEW_NID = data[0][0] +1
        mycursor.execute(f"INSERT INTO notes VALUES ( '{NEW_NID}'  , '{tittle}',49,  '{subject}',1,1, '{description}')")
        p.save(f"C:/FLASK/notes/{NEW_NID}.pdf")
        mydb.commit()

    return  render_template("complete.html" )



app.run(debug = True)


    