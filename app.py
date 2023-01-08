

from flask import Flask , render_template , request , redirect , make_response, request_started, session , json
import mysql.connector 
import math 

import os 
import random
import smtplib

from socket import gethostname 

import utilities
import json
import razorpay


expiry = 60*60*24*365

name =  gethostname()

if name == 'navadeep':
    db = "notemedia2"
    password = 'navadeepnasa1295'
elif name == 'ACER':
    db = "notesmedia"
    password = "ashvin2004"


client = razorpay.Client(auth=("rzp_test_Rzk0yIJJVLvjgn", "NG7em3kEJJcOTjYrhZZrjreP"))




#some_varliabes 
max_results = 5

connection = mysql.connector.connect(
    host = "localhost",
    user = 'root',
    password =   password ,
    db = db
)

cursor = connection.cursor( buffered=True)

app = Flask(__name__)
app.secret_key = "fkajsdflkajdlsfja"

print(type("nasa"))


@app.route('/publisher'  ,methods = ["POST", "GET"])
def  publisher_portal_page():
    #id = request.form.get("user")
    #password = request.form.get("pass")
    #print(id)
    
    id = request.cookies.get("email")
    password = request.cookies.get("password")

    print("the id is " , id , "the password is " , password)

    if id is None or password is None:
    

        res =  make_response(redirect("/sign_in"))
        session["next_path" ] = "/publisher"
        return res
    cursor.execute(f"SELECT user_id  , username , email , password , is_publisher, about about FROM users WHERE email = '{id}'")
    
    
    data = cursor.fetchone()

    if data[3] == password:
        if data[4] == 1:
            cursor.execute(f"SELECT * FROM notes WHERE publisher_id = '{data[0]}'")
            publications = cursor.fetchall()
            cursor.execute(f"SELECT * FROM packages WHERE publisher_id = '{data[0]}'")
            packages = cursor.fetchall()
            print(packages)
            print(publications) 
            x = len(publications)
            print(x)
            space = x//5
            fspace = space 
            area = 350 *fspace
            print(area)

            session["is_publisher"] = True 
            session["signed_in"] = True
            session["user"] = data[0]
            session["publications"] = publications
            session["data"] = data


            return  render_template("publisher_portal2.html" , packages = packages , data = data , publications = publications, id = data[0], x= x , rno = area, total_publication = len(publications))
        else:
            return(redirect("/publisher_form"))
    
    else:
        # res =  make_response(redirect("/sign_in"))
        # res.set_cookie("next_path", "/publisher_portal")
        session["next_path"] = "/publisher"
        return redirect("/sign_in")

@app.route('/publisher_form'  ,methods = ["POST", "GET"])
def publisher_form():
    phone = request.form.get("ph")
    about = request.form.get("about")
    email = request.cookies.get("email")
    password = request.cookies.get("password")
    if request.method == "POST":
   
        cursor.execute(f"UPDATE users SET phone = '{phone}', about = '{about}',is_publisher =  true  WHERE  email = '{email}' and password = '{password}'")
        connection.commit()
        return redirect("/publisher")
    


    

    return(render_template("form.html"))

@app.route('/publish'  ,methods = ["POST", "GET"])
def publish_page():
    
    # print("the sanam is" , dict(session))

    cursor.execute(f"select note_id , title from notes where publisher_id = {session.get('user_id')}")
    notes = cursor.fetchall()
    print( "value that we got are",dict(request.form))
    print(session.get("is_publisher"))
    
    if session.get("signed_in") == True and session.get("is_publisher") == True:

        

        if request.method == 'POST':
            input_type = request.form.get("input_type")
            
            if input_type == "1":
                print("uploding a note")
                title = request.form.get("title")
                description = request.form.get("about")
                subject = request.form.get("subject")
                file = request.form.get("file")

                query = f"insert into notes values(default, '{title}' , 0 , '{subject}' , {session.get('user_id')} , 1 , '{description}' , 0)"
                cursor.execute(query)
                connection.commit()
                return redirect("/publisher")
            else:

                print( "value that we got are",dict(request.form))

                email = session.get("user")

                # p = request.files['file']
#   
                # for item in dict(request.form):
                    # print(item , request.form[item])

                package_name = request.form.get("package_name")
                package_description = request.form.get("package_description")

                cursor.execute(f"insert into packages values(default , '{package_name}' , '{package_description}' , 139 , '{session.get('user_id')}' , 0)")
                cursor.execute("select package_id from packages order by package_id desc limit 1")
                package_id = cursor.fetchone()[0]
                if package_id is None:
                    package_id = 1
                print("the package is " , package_id)
                connection.commit()


                number_of_notes = request.form.get("number_of_upload")

                for i in range(int(number_of_notes)):
                    i = str(i+1)
                    type_of_note = request.form.get("type"+ i)



                    if type_of_note == "1":

                        title = request.form.get("title" + i)
                        subject = request.form.get("about" + i)
                        description = request.form.get("description" + i)
                        file = request.files.get("file" + i)
                        query = f"insert into notes values(default , '{title}' ,0 , '{subject}' , {session.get('user_id')}, 1 , '{description}' , 0  )"
                        cursor.execute(query)
                        cursor.execute("select note_id from notes order by note_id desc limit 1")


                        note_id = cursor.fetchone()[0]
                        cursor.execute(f"insert into package_mapping values( '{package_id}' , '{note_id}' )")

                        print(note_id , title, subject , description)

                        # file.save(f"static/notes/{note_id}.pdf")
                        # utilities.create_thumpnail(f"{note_id}.pdf")

                    elif type_of_note == "2":

                        note_id = request.form.get("note_id" + i)
                        cursor.execute(f"insert into package_mapping value( '{package_id}' , '{note_id}'  )")

                    connection.commit()

                return redirect("/publisher")

        return  render_template("publish_doc.html" , notes = notes)
    return "poda ooolle"
    
def check_cookies(request):
    email = request.cookies.get("email")
    password =  request.cookies.get("password")
    if email is not None and password is not None:
        cursor.execute(f"select password from users where email = {email}")
        data =  cursor.fetchall()
        if len(data) != 0:        
            real_password = data[0][2]
            if password == real_password:
                return True
    return False

def verify_login(request, session):
    print("the session data is" , dict(session))
    if session.get("signed_in"):
        print("sigin in found in session")
        return True 
    elif check_cookies(request):
        print("finding cookies")
        email = request.cookies.get("email")
        cursor.execute(f"select user_id, username from users where email = {email}")
        data= cursor.fetchone()
        user_id = data[0]
        username = data[1]
        print("the user id is" , user_id , username)
        session["user_id"] =  user_id
    
        session["username"] =  username
        return True 
    else:
        return False

@app.route("/")
def home():

    query = """
    select note_id , title , price, subject ,user_id,username,   description      from 
    notes, users 
    where notes.publisher_id = users.user_id
    """
    cursor.execute(query)
    notes = cursor.fetchall()

    return render_template("home.html" , notes = notes)

@app.route("/search" , methods = ["GET"])
def search():
    search = request.args.get("q")
    # print(request.cookies.get("email"))
    page = int(request.args.get("page"))
    
    query  = """select note_id , title , price , subject , users.user_id  , username , "1" as type
                from notes,users 
                where notes.publisher_id = users.user_id
                union 
                select package_id , package_name  , package_price ,  "" as subject , users.user_id , username , "2" as type
                from packages , users
                where packages.publisher_id = users.user_id
                
                
                """
    cursor.execute(query)
    data = cursor.fetchall()

    total_pages = math.ceil(len(data)/max_results)

    print(len(data))
    print(total_pages)

    if page > total_pages:
        page = total_pages 
    elif page < 1:
        page = 1

    if len(data[ (page-1)*max_results :]) > max_results:
        data = data[ (page-1)* max_results : page*max_results]
    else:
        data = data[(page-1)*max_results:]
    

    # buttons = []
    # if page != 1:
        # buttons.append(page-1)
    # buttons.append(page)
    # if page!=total_pages:
        # buttons.append(page+1)
    # 
    # buttons.append(total_pages)
# 
    # print(buttons)

    

    return render_template("search.html" , data = data, page = page , search = search , current_page = page, last_page = total_pages)

@app.route("/preview" , methods = ["GET" , "POST"])
def preview():

    
    if request.method == "GET":



    
        print(request.args.get("package"))

        if request.args.get("note") is not  None:
            type = "n"
            print("its a note")
            object_id = request.args.get("note")
            query = f"""select note_id , title , price , subject , notes.publisher_id , users.username   , notes.description 
                from notes,users
                where users.user_id = notes.publisher_id and
                note_id = '{request.args.get("note")}' """

        else:
            type = "p"
            object_id = request.args.get("package")
            query = f"""select package_id , package_name , package_price , "" as subject , publisher_id , users.username   , package_description
                from packages,users
                where users.user_id = packages.publisher_id and
                package_id = '{object_id}' """

        cursor.execute(query)

        data =  cursor.fetchall()[0]
            

        
        if verify_login(request ,session):
            logged_in = True 
            
            query2 = f"""
                select * from purchases 
                where user_id = {session.get('user_id')} 
                and note_id = {object_id}
                and type = '{type}'
                """
            print(session , type , object_id)
            cursor.execute(query2)
            data2 =  cursor.fetchall()
            print("the type is " , type)
            if len(data2) == 0:
                pre_owned = False
                payment_data = {
                   "amount": data[2]*100,
                   "currency": "INR",
                   "payment_capture":'1',
                   "notes" : {
                    "note_id": object_id,
                    "user_id": session.get("user_id"),
                    "type":type
                }
                }
                payment = client.order.create(data=payment_data)
                print("the data is " , data)
            else:
              
                payment = []
                pre_owned = True
                
        else:
            session["next_path"] = request.url
            logged_in= False
            pre_owned =  False 
            payment = []



        # cursor.execute(f"select count(rating) from purchases where note_id = {id}")
        # rating = cursor.fetchone()[0]

        return  render_template("preview.html" , data = data , rating = 0 , type = type, payment  = payment , logged_in = logged_in , pre_owned = pre_owned)
        # print(rating)
        
    elif request.method == "POST":
        
        if verify_login(request , session):

            data = request.form
            success  = client.utility.verify_payment_signature(dict(data))
            if success:
                data = client.order.payments(data["razorpay_order_id"])
                notes = data.get("items")[0].get("notes")
                print(dict(session))
                print("the notes are "  ,notes)
                object_id = notes.get("note_id")
                user_id = notes.get("user_id")
                type = notes.get('type')
                query =  f"insert into purchases values( default , {object_id} , {user_id} , now() , 0 ,'{type}' ,'' )"
                cursor.execute(query)
                connection.commit()
                if type == "n":
                    return redirect(f"/preview?note={object_id}")
                elif type == "p":
                    return redirect(f"/preview?package={object_id}")
            else:
                session["next_path"] = request.url 
                return redirect("/sign_in")

@app.route("/library")
def library():

    query = """
        select note_id , title , price, subject ,user_id,username,description  from 
        notes, users 
        where notes.publisher_id = users.user_id
        """
    cursor.execute(query)
    notes = cursor.fetchall()
    
    return render_template("library.html" , notes = notes)

@app.route("/sign_in" , methods = ["GET", "POST"])
def sign_in(  ):

    
    if request.method == "POST":    
        email = request.form.get("email")
        print(email)
        password = request.form.get("password") 
        
        
        cursor.execute(f"select user_id , password , username from users where email='{email}'")
        data = cursor.fetchone()
        real_password  =  data[1]
        print(real_password , password)

        if password !=  real_password:
            print("hiii123")
            
            return render_template("sign_in.html" , warning = "incorrect password" )    

        else:
            next_path = session.get("next_path")
            if next_path == None:
                next_path = "/"
            print("the next pathis " , next_path)
            response = make_response(redirect(next_path ))   

            response.set_cookie("email" , email)
            response.set_cookie("password" , password )
            session["signed_in"] =  True
            session["user_id"] = data[0]
            session["username"] = data[2]
            print("hii")
            return response
        
    
    return render_template("sign_in_temp.html" ,warning = ""  )



@app.route("/otppage" , methods = ["GET","POST"])
def checker():
    
    
    if  request.form.get("email")!= None:

        session["email"] = request.form.get("email")
    if request.form.get("password") != None:

        session["password"] = request.form.get("password")
    if request.form.get("repassword")!= None:
        session["repassword"] = request.form.get("repassword")
        
        
    
    
    if request.form.get("entered_otp") != None:
        session["entered_otp"] = request.form.get("entered_otp")  

    email = session["email"]
    password = session["password"]
    repassword = session["repassword"]
    entered_otp = session["entered_otp"]
    print(entered_otp)

    print(email)
    # username = request.form.get("username")
    # grade12 = request.form.get("grade12")
    # print(username)
    # print(grade12)
    # email = request.form.get("email")
    # password = request.form.get("password")
    print(password)
    # repassword = request.form.get("repassword")
    print(repassword)
   
   
   
   
    # put these imports on the top me ashvin


    OTP=""
    sotp = None
    try:
        sotp = session[otp]
    except :
        pass
    if sotp == None or str(sotp) != str(entered_otp):
        print("reached here")

        digits="0123456789"

        for i in range(6):
            OTP+=digits[math.floor(random.random()*10)]
        otp = OTP + " is your OTP"
        msg= otp
        print(otp)
        session["otp"] = OTP
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("ashvinpkumar2004@gmail.com", "fyrnczbqjptbtrwy")
        emailid = email
        print(emailid)
        print(msg)
        print("reached last")
        s.sendmail('&&&&&&&&&&&',emailid,msg)

        if email != None and password == repassword:
            cursor.execute("select user_id from users order by user_id DESC limit 1")
            data = cursor.fetchone()
            id = data[0]
            print(id)
            print(data)


            return render_template("otpchecker.html" )
        else:
            return render_template("sign_up.html")
    else:
        render_template("home.html")


@app.route("/sign_up" , methods = ["GET","POST"])
def sign_up():
    
    #f request.method == "POST":

    #   default_otp = "1234"

    #   username = request.form.get("username")
    #   email = request.form.get("email")
    #   password1 = request.form.get("password1")
    #   password2 = request.form.get("password2")

    #   otp = request.form.get("otp")
    #   print(otp)
    #   if otp is not None:
    #       if otp  == default_otp:
    #           
    #           next_path  = session.get("next_path")
    #           
    #           #username = session["signup_username"]
    #           #email = session["signup_email"]
    #           #password  = session["signup_password"]
#
    #           

    #           cursor.execute(f"INSERT INTO users VALUES ( default , '{email}','{password}', '{username}', false ,null, null, null)")
    #           cursor.execute(f"INSERT INTO users VALUES ( default ,  false ,null, null, null)")
    #           connection.commit()

    #           if next_path is  None:
    #               next_path = "/"
    #           response = make_response(redirect(next_path))
    #           response.set_cookie("email" , email)
    #           response.set_cookie("password" , password)
    #           session["signed_in"]  = True

    #           return response
    #           
    #       

    #   cursor.execute(f"select * from users where email = '{email}'")
    #   print(cursor.fetchone())
    #   if(cursor.fetchone()) is not None:
    #       return render_template("sign_up.html" , warning = "email already exists")
    #   elif password1 != password2:
    #       return  render_template("sign_up.html" , warning = "passwords dont match")
    #   else:
    #       response = make_response(render_template("otppage.html"))

    #       session["signup_username"] = username
    #       session["signup_email"] = email 
    #       session["signup_password"] = password1

    #       return response

            
    
    return render_template("sign_up.html" , warning = "")

@app.route("/signout" )
def sign_out():
    session["signed_in"] = False
    session["username" ] = ""
    session["user_id"] = ""
    response =  make_response(redirect("/"))
    response.delete_cookie('email')
    response.delete_cookie('password')
    return response

@app.route("/complete_purchase" , methods = ["GET" , "POST"])
def purchase_complete():

    
    
    if verify_login(request , session):

        user_id = session.get("user_id")
        note_id =  request.form.get("note")
        type = request.form.get("type")

        
        if type == "1":
            cursor.execute(f"select note_id from purchases where user_id = {user_id} and note_id = {note_id} and type = 'n' ")
        elif type == "2":
            cursor.execute(f"select note_id from purchases where user_id = {user_id} and note_id = {note_id} and type = 'p' ")

        data =  cursor.fetchall()
        
        # print(data)
        # print(note_id)
        # print( all(item[0] != note_id for item in data ))

        if len(data) == 0:
            print("note is not there")
            

            if request.form.get("type") == "1":
                query  = f"insert into purchases values(default , '{note_id}' , {user_id} , now() , 0 , 'n')"

            elif request.form.get("type") == "2":
                query  = f"insert into purchases values(default , '{note_id}' , {user_id} , now() , 0 ,  'p')"


            cursor.execute(query)
            connection.commit()
            return render_template("purchase_complete.html")
        else:   
            return "you already have this note"
    else:
        session["next_path"] = request.base_url
        return redirect("/signin")
            
@app.route("/mynotes")
def mynotes():
    print( "testting type" , type("nasa") )
    if verify_login(request , session):
        user_id = session.get("user_id")
        command = f"""select  notes.note_id, title , subject  , type
                      from purchases,  users , notes  
                      where purchases.user_id =  users.user_id and 
                      users.user_id = '{user_id}' and
                      purchases.note_id = notes.note_id
                      """

        cursor.execute(command)
        data = cursor.fetchall()
        print(data)
        print("signed in")
        return render_template("mynotes.html" , data = data)
    else:
        session["next_path"] = "/mynotes"
        return redirect("/sign_in")

@app.route("/mynotes/<note>")
def viewNotes(note):
    path = f"/static/notes/{note}.pdf"
    print(path)
    
    return render_template("viewnote.html", path =  path )
    

@app.route("/verifier" , methods = ["GET" , "POST"])
def verifier_portal(): 

    def return_verifier_page():
            page = request.args.get("page")
            query = """ 
                select note_id , title , users.username , users.email , subject 
                from notes,users
                where notes.publisher_id = users.user_id 
                and verified= false
            """
            cursor.execute(query)
            data =  cursor.fetchall()
            response =  make_response(render_template("verifier.html" , data = data))
            response.set_cookie("verifier_email" , email)
            response.set_cookie("verifier_password" , password)
            return response
 
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        cursor.execute(f"select verifier_password from verifiers where verifier_email = '{email}'")
        data = cursor.fetchall()
    
        
        print(email  , password , data)
        if email is not None and password is not None and data != []:
            print("-"*20)
            real_password = data[0][0]
            if password == real_password:
                return return_verifier_page()
        return render_template("verifier_signin.html", warning = "incorrect username or password")

    email = request.cookies.get("verifier_email")
    password = request.cookies.get("verifier_password")
    if email is not None and password is not None:
        print("cookie found")
        cursor.execute(f"select verifier_password from verifiers where verifier_email = '{email}'")
        real_password = cursor.fetchone()[0]
        if real_password == password:
            print("rendering page")
            return return_verifier_page()
    return render_template("verifier_signin.html", warning = "")
        
@app.route("/verifier/<id>" , methods = ["GET" , "POST"])
def verifier_single_note(id):

    email  = request.cookies.get('verifier_email')
    password = request.cookies.get("verifier_password")
    cursor.execute(f"select verifier_password from verifiers where verifier_email = '{email}'")
    data =  cursor.fetchall()
    print(id)
    if data != []:
        print("passwrod found")
        real_password = data[0][0]
        if real_password == password:
            print("passwrod verifier")
            if request.method =="GET":
                approval = request.args.get("approve")   
                print(approval)   
                if approval  == "1":
                    print("approve")
                    cursor.execute(f"update notes set verified = true where note_id = {id}")
                    connection.commit()

                elif approval == "0":
                    print("rejected")
                    cursor.execute(f"delete from notes where note_id  = {id}")
                    connection.commit()

                elif approval is None:
                    return render_template("verifier_note.html" , id = id)

                
                print("its a get ")
                return redirect("/verifier")
            
            return render_template("verifier_note.html")
    return redirect("/verifier")


@app.route("/noteviewer" , methods = ["GET" ,"POST"])
def noteviewer():
    
    
    # print( "testting type" , ("nasa") )
    # form_data = json.loads(request.data)

    cursor = connection.cursor()

    print("the form data is " , dict(request.form))

    
    if verify_login(request , session):

        if request.method == 'POST':
            requestType = request.form.get("type")
            print( "the request form is" ,dict(request.form))
            print("the request type is ", requestType)
           
            print("post request in noteviewer fuction")
        
            if requestType == "post_comment":

                print("gonna post a comment")
                comment = request.form.get("comment")
                note_id = request.form.get("note_id")
                user_id = session.get("user_id")
                parent_comment = request.form.get("parent_comment")
                print(comment , note_id , user_id , parent_comment)

                cursor = connection.cursor(buffered=True)

                query  = f"insert into comments values(default , '{comment}' , {parent_comment} , {note_id} , {user_id} , now())"

                cursor.execute(query )
                connection.commit()
            
                cursor.execute("select comment_id , date_format(date_time , '%b %d %Y')  from comments order by comment_id desc")
                data = cursor.fetchone()
                comment_id = data[0]
                date = data[1]
                

                print(comment , data)
                json_data = {
                    "username":f"{session.get('username')}",
                    "comment_id": f"{comment_id}",
                    "date": f"{date}"
                }
                json_data = json.dumps(json_data)
                print(json_data)
                return  json_data

            elif requestType == "show_reply" :
                cursor = connection.cursor(buffered=True)
                note_id = request.form.get("note_id")
                
                parentComment = request.form.get("parent_comment")
 
                print("the values are " , parentComment , note_id)
                query1 = f"""select comment_id , text ,  username , date_format(date_time , "%b %d %Y") , users.user_id
                            from comments , users where 
                            users.user_id = comments.user_id and    
                            note_id = {note_id} and
                            parent_comment = {parentComment}
                            order by comment_id desc
                            """
                print(query1)
                cursor.execute(query1)
                comments = str(cursor.fetchall())
                comments = comments.replace("(" , "[")
                comments = comments.replace(")" , "]")
                comments = comments.replace("'" , '"')
                

                response  = "{" + f' "comments" : {comments}' + "}"
                print(response)
                return  response


            elif requestType == "rating":
                print("in the rating")
                cursor =  connection.cursor(buffered=True)
                rating = request.form.get("rating")
                user_id = session.get("user_id")
                note_id = request.form.get("note_id")
                print(rating , user_id , note_id)
                cursor.execute(f"update purchases set rating = {rating} where user_id = {user_id} and note_id = {note_id}")
                connection.commit()   
            
                return "success"
            
            elif requestType == "post_review":
                print("in the post review plae")
                reviewText = request.form.get("review")
                note_id = int(request.form.get("note_id"))
                print(reviewText , note_id)

                query1 = f"select note_id from purchases where user_id  = {session.get('user_id')}"
                cursor.execute(query1)
                data = cursor.fetchall()
                print((note_id,))
                x = "nasa"
                # print( type(x) )
                # print("1",  type( cursor.fetchall()) ) 
                # print(any(  x[0] == note_id for x in cursor.fetchall() ))
                # print("2", type((note_id,)) )
  

                if any(  x[0] == note_id for x in data):

                    print(True)
                    query2 = f"update purchases set review= '{reviewText}' where user_id = {session.get('user_id')} and note_id = {note_id}"
                    cursor.execute(query2)
                    connection.commit()
                    
                    return "done"

                return 'failed'

            elif requestType == "get_reviews":
                print("giving reviews")
                query =  f"""
                            select rating , review , users.user_id , username
                            from purchases, users where
                            purchases.user_id = users.user_id and 
                            note_id = {request.form.get('id')}  and 
                            review is not null"""

                cursor.execute(query)
                data = { "reviews": cursor.fetchall() }
                data = json.dumps(data)
                print(data)
                
                return str(data)

                
        else:
                print("gonna give the page")
                cursor = connection.cursor(buffered=True)
                if request.args.get("note") is not None:
                    object_id =  request.args.get("note")
                    query1 = f"""
                             select notes.note_id , notes.title , notes.description , subject , u.username , p.username , p.user_id
                             from purchases , users u , notes , users p
                             where
                             purchases.user_id = {session.get('user_id')} and
                             purchases.note_id = notes.note_id and
                             notes.publisher_id = p.user_id and
                             purchases.note_id = {object_id}
                    """
                    type=  "n"

                    cursor.execute(query1)
                    results = cursor.fetchall()
                    if len(results) != 0:
                        main_data = results[0]
                    else:
                        main_data = None

                    
                elif request.args.get("package") is not None:
                    object_id = request.args.get("package")
                    
                    query1 = f"""
                            select package_mapping.note_id , title , description , '' as subject , u.username, p.username , notes.publisher_id 
                            from packages , package_mapping , purchases , notes , users p , users u 
                            where packages.package_id =  package_mapping.package_id
                            and purchases.note_id = packages.package_id 
                            and purchases.type  = "p"
                            and notes.note_id = package_mapping.note_id
                            and p.user_id = notes.publisher_id
                            and u.user_id = purchases.user_id
                            and purchases.user_id = {session.get('user_id')}
                            and packages.package_id = {object_id}
                    """

                    type = "p"

                    
                    
                    cursor.execute(query1)
                    data = cursor.fetchall()

                    package_details_query = f"select * from packages where package_id = {object_id}"
                    cursor.execute(package_details_query)
                    package_data = cursor.fetchall()[0]

                    print(data)

                    if request.args.get("index") is not None:
                        index = request.args.get("index")

                    else:
                        index = 0
                    if len(data) !=0 :
                        main_data = data[int(index)]
                    else:
                        main_data =  None
                print( "the main data is ", main_data)


                query2 = f"""
                            select comment_id , text  , username , date_format(date_time , "%b %d %Y") , users.user_id 
                            from comments , users where 
                            users.user_id = comments.user_id and    
                            note_id = {main_data[0]} and
                            parent_comment = 0
                            order by comment_id desc
                    """
                cursor.execute(query2)
                comments = cursor.fetchall()
        

                query3 = """
                select c2.comment_id , c2.text , count(c2.comment_id) 
                from comments c1 , comments c2 where c1.parent_comment = c2.comment_id 
                group by c2.comment_id
                """

                cursor.execute(query3)

                reply_numbers =  cursor.fetchall()

                for i in range(len(reply_numbers)):
                    # print(list(reply_numbers[i]))
                    reply_numbers[i] = list(reply_numbers[i])
                
                for i in range(len(comments)):
                    comments[i] = list(comments[i])
                   
                reply_numbers = json.dumps({"reply_comments" : reply_numbers})
                comments = json.dumps({"comments" : comments})
                print(comments) 
                # print(reply_numbers)

                if main_data[6] == session.get("user_id"):
                    is_publisher = True 
                else:
                    is_publisher = False

            
                if main_data is not None:
                    if type == "n":
                        return render_template("noteviewer.html" , main_data = main_data , comments = comments  , reply_numbers = reply_numbers , type = type , user_id = session.get("user_id") , is_publisher = is_publisher)
                    elif type == "p":
                        return render_template("noteviewer.html" , main_data = main_data , data = data , comments = comments  , reply_numbers = reply_numbers , type = type , length = len(data), package_data = package_data, user_id = session.get("user_id"), is_publisher = is_publisher)

           
        



if __name__ == "__main__":
    app.run(debug=True , host  = "0.0.0.0")