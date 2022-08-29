
from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from urllib import response
from flask import Flask , render_template , request , redirect , make_response, url_for
import mysql.connector 
import math
import utilities



#some_varliabes 
max_results = 5

connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password =  "navadeepnasa1295",
    db = "notemedia2"



)


cursor = connection.cursor()

app = Flask(__name__)




@app.route("/")
def home():
    
    return render_template("home.html" )

@app.route("/search" , methods = ["GET"])
def search():
    search = request.args.get("q")
    # print(request.cookies.get("email"))
    page = int(request.args.get("page"))
    query  = "select note_id , title , price , subject , publishers.user_id from notes,publishers where notes.publisher_id = publishers.user_id"
    cursor.execute(query)
    data = cursor.fetchall()

    total_pages = math.ceil(len(data)/max_results)

    print(len(data))
    print(total_pages)

    if len(data[ (page-1)*max_results :]) > max_results:
        data = data[ (page-1)* max_results : page*max_results]
    else:
        data = data[(page-1)*max_results:]
    

    buttons = []
    if page != 1:
        buttons.append(page-1)
    buttons.append(page)
    if page!=total_pages:
        buttons.append(page+1)
    
    buttons.append(total_pages)

    print(buttons)
    

    return render_template("search.html" , data = data, page = page , search = search , buttons = buttons , last_page = total_pages)

@app.route("/preview/<id>")
def preview(id):
    print(id)
    query = f"""select note_id , title , price , subject , notes.publisher_id , users.username   , notes.description
                from notes,users
                where users.user_id = notes.publisher_id and
                note_id = '{id}' """

    cursor.execute(query)
    data =  cursor.fetchall()[0]

    cursor.execute(f"select count(rating) from purchases where note_id = {id}")
    rating = cursor.fetchone()[0]

    print(data)
    print(rating)
    return  render_template("preview.html" , data = data , rating = rating )

@app.route("/sign_in" , methods = ["GET","POST" ] )
def sign_in(  ):

    
    if request.method == "POST":    
        email = request.form.get("email")
        print(email)
        password = request.form.get("password") 

        cursor.execute(f"select password from users where email='{email}'")
        real_password = cursor.fetchone()[0]
        print(real_password , password)
        if password !=  real_password:
            
            return render_template("sign_in.html" , warning = "incorrect password" )          

        else:
            next_path = request.cookies.get("next_path")
            if next_path == None:
                next_path = "/"
            response = make_response(redirect(next_path ))   

            response.set_cookie("email" , email)
            response.set_cookie("password" , password)
            return response
        
    
    return render_template("sign_in.html" ,warning = ""  )

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
                next_path  = request.cookies.get("next_path")
                
                username = request.cookies.get("siginup_username")
                email = request.cookies.get("signup_email")
                password  = request.cookies.get("signup_password")

                cursor.execute(f"INSERT INTO users VALUES ( default , '{email}','{password}', '{username}', false ,null, null, null)")
                connection.commit()

                if next_path is  None:
                    next_path = "/"
                response = make_response(redirect(next_path))
                response.set_cookie("email" , email)
                response.set_cookie("password" , password)
                return response
                
            

        cursor.execute(f"select * from users where email = '{email}'")
        print(cursor.fetchone())
        if(cursor.fetchone()) is not None:
            return render_template("sign_up.html" , warning = "email already exists")
        elif password1 != password2:
            return  render_template("sign_up.html" , warning = "passwords dont match")
        else:
            response = make_response(render_template("otppage.html"))
            response.set_cookie("signup_username" , username)
            response.set_cookie("signup_email" , email)
            response.set_cookie("signup_password" , password1)
            return response

            
    
    return render_template("sign_up.html" , warning = "")

@app.route("/preview/<note>/purchase_complete")
def purchase_complete(note):
    
    email = request.cookies.get("email")
    
    password = request.cookies.get("password")
    print(email , password)
    cursor.execute(f"select password,user_id from users where email='{email}'")
    data =  cursor.fetchone()
    
    # print("step 1")
    if data is not None:
        print("step 2")  
        real_password = data[0]   
        uid = data[1]
        if password == real_password:
            # print("step3")
      
            cursor.execute(f"insert into purchases values(default , '{note}' , {uid} , now() , 0)")
            connection.commit()
            return render_template("purchase_complete.html")
    else:
        responce = make_response(redirect("/sign_in"))
        responce.set_cookie("next_path", request.base_url)
        return responce


@app.route("/mynotes")
def mynotes():
    email = request.cookies.get("email")
    command = f"select  notes.note_id, title , subject  from purchases,  users , notes  where purchases.user_id =  users.user_id and email = '{email}' and notes.note_id = purchases.note_id"
    cursor.execute(command)
    data = cursor.fetchall()
    return render_template("mynotes.html" , data = data)

@app.route("/mynotes/<note>")
def viewNotes(note):
    path = f"/static/notes/{note}.pdf"
    print(path)
    
    return render_template("viewnote.html", path =  path )
    
@app.route("/upload" ,methods = ["GET" , "POST"])
def upload():
    if request.method == "POST":
        print(request.form)
        file = request.files["file"]

        title = request.form.get("title")
        price = request.form.get("price")
        desc = request.form.get("desc")
        subject= request.form.get("subject")

        publisher_email =  request.form.get("email")

        query_to_get_userid = f"""select users.user_id 
                                from users, publishers 
                                where users.user_id = publishers.user_id and
                                users.email = '{publisher_email}'
                                """
        cursor.execute(query_to_get_userid)

        user_id = cursor.fetchone()[0]   


        cursor.execute("select note_id from notes order by note_id desc limit 1")
        note_id = int(cursor.fetchone()[0])+1

        print(note_id  , title  , price , subject , user_id , desc)

        cursor.execute(f"insert into notes values({note_id} , '{title}' , {price} , '{subject}' , {user_id} , False , '{desc}')")
        connection.commit()

        file.save(f"static/notes/{note_id}.pdf")
        utilities.create_thumpnail(file = f"{note_id}.pdf")

        return "uploaded"
    
    return render_template("upload.html")

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


@app.route("/publisher_portal")
def publisher_portal():
    
    email = request.cookies.get("email")
    cursor.execute(f"select user_id,email,username,about from users where email = '{email}'")
    data =  cursor.fetchone()
    
    cursor.execute(f"select * from notes where publisher_id = {data[0]}")
    publications = cursor.fetchall()

    print(data , publications)

    return render_template("publishers_portal.html" , data =  data , publications = publications)


if __name__ == "__main__":
    app.run(debug=True)