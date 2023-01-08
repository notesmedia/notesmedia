
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


const searchButton = document.getElementById("search-button");
const searchBox = document.getElementById("search-box");
const searchForm = document.getElementById("search-form");
const mainNavBar = document.getElementById("mainNavBar");
const closeButton = document.getElementById("close-search");

console.log(searchBox.style.display)

searchButton.addEventListener("click" , (event)=>{
    if(window.innerHeight >= window.innerWidth){

        if(searchBox.style.display == "none" || searchBox.style.display == ""){
            
            
            event.preventDefault();
            mainNavBar.style.flexDirection = "column"
            searchBox.style.display = "flex";
            searchForm.style.border = "2px solid blue";
            closeButton.style.display = "inline";
            
        }
    }
    })


closeButton.addEventListener("click" , (event)=>{
    event.preventDefault();
    // searchBox.value = "";
    // mainNavBar.style.flexDirection = 'row';
    // searchBox.style.display = "none";
    // searchForm.style.border = "0px";
    // closeButton.style.display = "none";
    mainNavBar.removeAttribute("style")
    searchBox.removeAttribute("style")
    searchForm.removeAttribute("style")
    closeButton.removeAttribute("style")
})


var reset = false;
if(window.innerWidth > window.innerHeight){
    reset = true;
}

window.addEventListener("resize" , ()=>{
    if(window.innerWidth > window.innerHeight ){

        if(reset){
            console.log("hiii")
            mainNavBar.removeAttribute("style")
            searchBox.removeAttribute("style")
            searchForm.removeAttribute("style")
            closeButton.removeAttribute("style")
            reset =  false ;

        }


    }
    else{
        reset = true;
    }
})



