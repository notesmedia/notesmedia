console.log("pdfviewer.js started")

const url = pdfPath ;

const allPages = document.getElementById("allpages");
const zoomin = document.getElementById("zoomin");
const fullScreenButton = document.getElementById("fullscreen");
const top_portion = document.getElementById("top_portion");
const container = document.getElementById("container");



const max_zoom_value = 200;

var fullscreen = false;

let pdfDoc = null,
  pageNum = 1,
  pageIsRendering = false,
  pageNumIsPending = null;

  let scale = 1.5;




const renderPage = (  pdfDoc , num )=> {
  


 
    pdfDoc.getPage(num).then(page => {
    // Set scale
    const viewport = page.getViewport({ scale });
    let canvas =  document.createElement("canvas");

    canvas.setAttribute("class" , "canvas");

    allpages.append(canvas);

    canvas.height = viewport.height;
    canvas.width = viewport.width;
    
    
    
    let ctx = canvas.getContext("2d")
    

    let renderCtx = {
      canvasContext: ctx,
      viewport: viewport
    };

      page.render(renderCtx)  

    });
  
};

// Get Document
pdfjsLib.getDocument(url).promise.then(pdfDoc => {
    
  console.log("here")
    for(let i = 0 ; i <= 4 ; i++){
      renderPage(pdfDoc , i+1)
    }


  })

  zoom.oninput = () => {
    let zoom_value = parseInt(zoom.value);

    // let zoom_value = parseInt((value / 100) * (max_zoom_value));


    allPages.style.width = `${zoom_value}%`;


  
}

    
fullScreenButton.addEventListener("click", ()=>{
    if (!fullscreen){
        top_portion.classList.add("fullScreenView");
        top_portion.style.height = "100vh"
        window.fullscreen =  true;
    }else{
        top_portion.classList.remove("fullScreenView");
        top_portion.style.height = "80vh";
        window.fullscreen =  false;
    }
})
  


