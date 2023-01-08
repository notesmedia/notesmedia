console.log("running home.js")

const controls = document.getElementById("controls")
const slides = document.getElementById("slides")
const all_slides = Array.from(document.getElementsByClassName("slide"))
const controlButtons = controls.getElementsByClassName("slide_button");

const rowButtons = document.getElementsByClassName("row_button");

const all_tiles = document.getElementsByClassName("all_tiles");
const hscroll = document.getElementsByClassName("hScroll");


let first_slide = all_slides[0].cloneNode(true);
slides.appendChild(first_slide)



Array.from(controlButtons).forEach((control_button, index) => {

    control_button.addEventListener("change", () => {
        if (control_button.checked) {

            let newMargin = `${-100 * (index)}vw`
            slides.style.marginLeft = newMargin;

        }
    })


})

var current_page = 0;
setInterval(() => {

    current_page++;

    let newMargin = `${-100 * (current_page)}vw`;
    slides.style.marginLeft = newMargin;


    if (current_page == 3) {

        setTimeout(() => {

            slides.style.transition = "0s";
            console.log(slides.style.transition)
            // slides.classList.add("noTransition")

            slides.style.marginLeft = "0vw"
            setTimeout(() => { slides.style.transition = "0.5s"; }, 100)

            // slides.classList.remove("noTransition")

            current_page = 0

        }, 500)

    }
    console.log(current_page)

    controlButtons[current_page].checked = true;



}, 5000)


var recTilesMargin = 0;
var libTilesMargin = 0;

Array.from(rowButtons).forEach((rowButton) => {

    var hscrollWidth = hscroll[0].offsetWidth;
    var allTilesWidth = all_tiles[0].offsetWidth;

    console.log(hscrollWidth, allTilesWidth)

    rowButton.addEventListener("click", () => {

        console.log("clicked.....")

        let rowButtonClasses = Array.from(rowButton.classList)

        console.log(rowButtonClasses);

        if (rowButtonClasses.includes("reccRowButton")) {
            var row = document.querySelector("#recomendations .hScroll .all_tiles")
        } else if (rowButtonClasses.includes("libraryRowButton")) {
            var row = document.querySelector("#library .hScroll .all_tiles")
        }





        if (rowButtonClasses.includes("back") && (window.recTilesMargin + hscrollWidth) <= 0) {

            window.recTilesMargin += hscrollWidth;

        } else if (rowButtonClasses.includes("forward") && -(window.recTilesMargin - hscrollWidth) <= allTilesWidth) {

            console.log("widths are",  -(window.recTilesMargin - hscrollWidth) - allTilesWidth , hscrollWidth/2  )

            if(  -(window.recTilesMargin - hscrollWidth) - allTilesWidth > hscrollWidth/2 ){
                window.recTilesMargin -= hscrollWidth/2;
            }else{
                window.recTilesMargin -= hscrollWidth/2;
            }

            // window.recTilesMargin -= hscrollWidth;
        }

        console.log(recTilesMargin)

        row.style.marginLeft = `${recTilesMargin}px`
    })

})

    
