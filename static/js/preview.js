console.log("preview.js started");

const showPreviewButton = document.getElementById("show_preview");
const container = document.getElementById("container");
const goBackButton = document.getElementById("goback");

showPreviewButton.addEventListener("click", ()=>{
    container.style.display = "flex";
    goBackButton.style.display   = "block"
})

goBackButton.addEventListener("click", ()=>{
    container.style.display = "none";
    goBackButton.style.display = "none"
})