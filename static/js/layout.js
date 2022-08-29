console.log("started")
let cookies = document.cookie.split("; ") ;

console.log(document.cookie)

let email = "";
let password = "";

cookies.forEach((item)=>{
    let key_value_pair  = item.split("=");

    console.log(key_value_pair)

    if(key_value_pair[0] == "email"){
        email = key_value_pair[1].substring(1 , key_value_pair[1].length - 1)
    }
    else if(key_value_pair[0] == "password"){
        password = key_value_pair[1]
    }
    console.log("the email is "+email);
    console.log("the password is "+password);

});

let sigin = document.getElementById("signinbutton");
let signedin = document.getElementById("signed_in");
let email_label = document.getElementById("email");

if(email != "" &&  password != ""){
    console.log("sidned in")
    sigin.remove();
    email_label.innerText = email;

}
else{
    console.log("not signed in")
    signedin.remove();
}