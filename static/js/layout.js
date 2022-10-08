
let cookie = document.cookie.split("; ");

console.log(cookie )


cookies = {}

cookie.forEach((item) => {
    let key_value_pair = item.split("=");

    console.log(key_value_pair)

    cookies[key_value_pair[0]] =  key_value_pair[1];

});
console.log("the cookies are " + cookies)



let sigin = document.getElementById("signinbutton");
let signedin = document.getElementById("signed_in");
let email_label = document.getElementById("email");

if ("email" in cookies && "password" in cookies) {
    console.log("sidned in")
    sigin.remove();
    let email =  cookies.email;
    email = email.replace('"' , '')
    // email_label.innerText = email;

}
else {
    console.log("not signed in")
    signedin.remove();
}

//================== code for showing and unshowing navbar===========================

let show_nav = document.getElementById("show_navbar");
let nav_list = document.getElementById("navbar");
let nav_list_items = document.querySelector("#navbar li")
let black_space = document.getElementById("allblack")




show_nav.addEventListener('click', (event) => {


    
    console.log("gonna show it");
    nav_list.style.animation = "navbar_entry 0.5s";
    // nav_list.style.display = "flex";
    // black_space.style.display = "block";
    nav_list.classList.add("active")
    black_space.classList.add("active")
    

})

black_space.addEventListener("click", (event) => {
    console.log("gonna hide it");
    // nav_list.style.animationPlayState = "running";
    // nav_list.style.animation = "navbar_exit";
    // nav_list.style.display = "none";
    // black_space.style .display = "none";
    nav_list.classList.remove("active")
    black_space.classList.remove("active")
});


// ================== fuctions of buttons






