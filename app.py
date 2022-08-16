
from flask import Flask , render_template , request , redirect , make_response, url_for
import mysql.connector 
import math



#some_varliabes 
max_results = 5

connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password =  "navadeepnasa1295",
    db = "notesmedia"

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
    cursor.execute("select * from notes")
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

@app.route("/preview/<note>")
def preview(note):
    print(note)
    cursor.execute(f"select * from notes where title = '{note}' ")
    data =  cursor.fetchall()[0]
    return  render_template("preview.html" , data = data)

@app.route("/sign_in" , methods = ["GET","POST" ] )
@app.route("/<path:path_before>/sign_in" , methods = ["GET","POST" ] )
def sign_in(path_before = ""):

    current_url = request.url
    current_url = "/"+current_url.replace(request.root_url , "")
    print("the current url is "+ current_url)

    

    if request.method == "POST":
        print("here")
        email = request.form["email"]
        password = request.form["password"]

        current_url_split  = current_url.split("/")
        
        

        cursor.execute(f"select password from users where email='{email}'")
        real_password = cursor.fetchone()[0]
        print(password , real_password)
        if password !=  real_password:
            
            return render_template("signin.html" , warning = "incorrect password" , path = current_url)
            
        else:
            current_url_split.remove("sign_in")
            if len(current_url_split) == 1:
                response_url = "/"
            else:
                response_url  = "/".join(current_url_split)
            
            print("your password is correct")
            print(current_url_split)
            response = make_response(redirect(response_url))
            response.set_cookie("email" , email)
            response.set_cookie("password" , password)
            return response
        
    else:
        
        return render_template("signin.html" ,warning = "" , path = current_url)

@app.route("/sign_up" , methods = ["GET","POST"])
def sign_up():
    
    if request.method == "POST":
        email = request.form["email"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        cursor.execute(f"select * from users where email = '{email}'")
        print(cursor.fetchone())
        if(cursor.fetchone()) is not None:
            return render_template("signup.html" , warning = "email already exists")
        elif password1 != password2:
            return  render_template("signup.html" , warning = "passwords dont match")
        else:
            cursor.execute(f"insert into users values(default , '{email}' , '{password1}')")
            connection.commit()

            response = make_response(redirect("/"))
            response.set_cookie("email" , email)
            response.set_cookie("password" , password1)
            return response
            
            
    else:
        return render_template("signup.html" , warning = "")

@app.route("/preview/<note>/purchase_complete")
def purchase_complete(note):
    
    email = request.cookies.get("email")
    
    password = request.cookies.get("password")
    print(email , password)
    cursor.execute(f"select password,uid from users where email='{email}'")
    data =  cursor.fetchone()
    
    # print("step 1")
    if data is not None:
        print("step 2")  
        real_password = data[0]   
        uid = data[1]
        if password == real_password:
            # print("step3")
      
            cursor.execute(f"insert into purchases values(default , '{note}' , {uid} , now() )")
            connection.commit()
            return render_template("purchase_complete.html")
    else:
        return redirect(f"{request.url}/sign_in")


@app.route("/mynotes")
def mynotes():
    email = request.cookies.get("email")
    command = f"select  note_name , subject  from purchases,  users , notes  where purchases.u_id =  users.uid and email = '{email}' and notes.title = purchases.note_name"
    cursor.execute(command)
    data = cursor.fetchall()
    return render_template("mynotes.html" , data = data)

@app.route("/mynotes/<note>")
def viewNotes(note):
    path = f"/static/notes/{note}.pdf"
    print(path)
    
    return render_template("viewnote.html", path =  path )
    


if __name__ == "__main__":
    app.run(debug=True)