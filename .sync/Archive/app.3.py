

from flask import Flask , render_template , request , redirect , make_response, request_started, session , json
import mysql.connector 
import math 

import os 

from socket import gethostname 

import utilities
import json


expiry = 60*60*24*365

name =  gethostname()

if name == 'navadeep':
    db = "notemedia2"
    password = 'navadeepnasa1295'
elif name == 'ACER':
    db = "notesmedia"
    password = "ashvin2004"




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


@app.route('/publisher'  ,methods = ["POST", "GET"])
def  publisher_portal_page():
    #id = request.form.get("user")
    #password = request.form.get("pass")
    #print(id)
    
    id = request.cookies.get("email")
    password = request.cookies.get("password")
    
    if id is None or password is None:
    

        res =  make_response(redirect("/sign_in"))
        session["next_path" ] = "/publisher"
        return res
    cursor.execute(f"SELECT * FROM users WHERE email = '{id}'")
    
    
    data = cursor.fetchone()

    if data[2] == password:
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


            return  render_template("publisher_portal.html" , packages = packages , data = data , publications = publications, id = data[0], x= x , rno = area, total_publication = len(publications))
        else:
            return(redirect("/publisher_form"))
   
    else:
        # res =  make_response(redirect("/sign_in"))
        # res.set_cookie("next_path", "/publisher_portal")
        session["next_path"] = "/publisher_portal"
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
    
    if session.get("signed_in") == True and session.get("is_publisher") == True:

        if request.method == 'POST':

            email = session.get("user")

            # p = request.files['file']

            for item in dict(request.form):
                print(item , request.form[item])

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
    print("hereeee")
    print("the session data is" , dict(session))
    return render_template("home.html" )

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

@app.route("/preview")
def preview():



    print(request.args.get("package"))

    if request.form.get("note") != None:
        type = 1
        query = f"""select note_id , title , price , subject , notes.publisher_id , users.username   , notes.description 
            from notes,users
            where users.user_id = notes.publisher_id and
            note_id = '{request.args.get("note")}' """

    else:
        type = 2
        query = f"""select package_id , package_name , package_price , "" as subject , publisher_id , users.username   , package_description
            from packages,users
            where users.user_id = packages.publisher_id and
            package_id = '{request.args.get("package")}' """



 
    
    
    cursor.execute(query)
    data =  cursor.fetchall()[0]

    # cursor.execute(f"select count(rating) from purchases where note_id = {id}")
    # rating = cursor.fetchone()[0]

    print(data)
    # print(rating)
    return  render_template("preview.html" , data = data , rating = 0 , type = type )

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
            response = make_response(redirect(next_path ))   

            response.set_cookie("email" , email)
            response.set_cookie("password" , password )
            session["signed_in"] =  True
            session["user_id"] = data[0]
            session["username"] = data[2]
            print("hii")
            return response
        
    
    return render_template("sign_in_temp.html" ,warning = ""  )

@app.route("/sign_up" , methods = ["GET","POST"])
def sign_up():
    
    if request.method == "POST":

        default_otp = "1234"

        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        otp = request.form.get("otp")
        print(otp)
        if otp is not None:
            if otp  == default_otp:
                
                next_path  = session.get("next_path")
                
                #username = session["signup_username"]
                #email = session["signup_email"]
                #password  = session["signup_password"]
#
                

                cursor.execute(f"INSERT INTO users VALUES ( default , '{email}','{password}', '{username}', false ,null, null, null)")
                cursor.execute(f"INSERT INTO users VALUES ( default ,  false ,null, null, null)")
                connection.commit()

                if next_path is  None:
                    next_path = "/"
                response = make_response(redirect(next_path))
                response.set_cookie("email" , email)
                response.set_cookie("password" , password)
                session["signed_in"]  = True

                return response
                
            

        cursor.execute(f"select * from users where email = '{email}'")
        print(cursor.fetchone())
        if(cursor.fetchone()) is not None:
            return render_template("sign_up.html" , warning = "email already exists")
        elif password1 != password2:
            return  render_template("sign_up.html" , warning = "passwords dont match")
        else:
            response = make_response(render_template("otppage.html"))

            session["signup_username"] = username
            session["signup_email"] = email 
            session["signup_password"] = password1

            return response

            
    
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
    if verify_login(request , session):
        user_id = session.get("user_id")
        command = f"""select  notes.note_id, title , subject  
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
    
    requestType = request.form.get("type")
    print(requestType)
    # form_data = json.loads(request.data)



    print("the form data is " , dict(request.form))


    if verify_login(request , session):

        if request.method == 'POST':
        
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

                
        else:
                print("gonna give the page")
                cursor = connection.cursor(buffered=True)
                note_id = request.args.get("note")
                
                query1 = f"""
                         select notes.note_id , notes.title , notes.description , subject , u.username , p.username , p.user_id
                         from purchases , users u , notes , users p
                         where
                         purchases.user_id = {session.get('user_id')} and
                         purchases.note_id = notes.note_id and
                         notes.publisher_id = p.user_id and
                         purchases.note_id = {note_id}
                """
                cursor.execute(query1)
                note = cursor.fetchall() 


                query2 = f"""
                            select comment_id , text  , username , date_format(date_time , "%b %d %Y") , users.user_id 
                            from comments , users where 
                            users.user_id = comments.user_id and    
                            note_id = {note_id} and
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
                
                if len(note) != 0:
                     return render_template("noteviewer.html" , data = note[0] , comments = comments  , reply_numbers = reply_numbers , name='"navadee"')
           
        



if __name__ == "__main__":
    app.run(debug=True)