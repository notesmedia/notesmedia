console.log("noteviewer.js started")



let comment_submit = document.getElementById("submit_comment");
let commentBox = document.getElementById("comment_box")
let comment_section = document.getElementById("comment_section");
let comments = document.getElementById("comments");

let replys = document.getElementById("replys");
let replys_section = document.getElementById("reply_section");

let note_id = document.getElementById("notename").value;

var backButton = document.getElementById("backToComments");
var all_comments = document.getElementsByClassName("comment");

var rating_system = document.getElementById("rating_system");

reply_mode = false
parent_comment = 0

console.log(comments_initial)

comments_initial.comments.forEach((comment,) => {
    make_comment(comment);
})
comment_submit.addEventListener("click", () => {

    console.log("comment submitted")
    let comment = commentBox.value;
    let request = new XMLHttpRequest();
    request.open("POST", "/noteviewer", true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.onload = () => {



        if (request.status === 200) {
            console.log(request.responseText);
            let data = JSON.parse(request.responseText);
            console.log("hereee")
            console.log(data)
            make_comment([data.comment_id, comment, data.username, data.date])

        }

    }
    let parameters = `comment=${comment}&note_id=${note_id}&type=post_comment&parent_comment=${parent_comment}`
    console.log(parameters)
    request.send(parameters);
})

Array.from(all_comments).forEach((comment, index) => {
    console.log("heree")
    console.log(comment)
    let replyButton = comment.getElementsByClassName("reply")[0];


    replyButton.addEventListener("click", () => {

        go_to_reply(comment);

    });
})

function go_to_reply(comment) {
    console.log("the comment is ", comment)
    let comment_id = comment.getElementsByClassName("comment_id")[0].value
    let request = new XMLHttpRequest();
    request.open("POST", "/noteviewer", true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.onload = () => {

        let all_comments = JSON.parse(request.responseText).comments;

        let divider = document.getElementById("divider")
        divider.style.display = "flex";



        let replys = document.getElementById("replys");
        let reply_comments = replys.getElementsByClassName("comment");

        Array.from(reply_comments).forEach((reply_comment) => {
            reply_comment.remove();
        })

        replys_section.style.display = "block";
        comments.style.display = "none";

        window.reply_mode = true;
        window.parent_comment = comment_id;

        console.log("opening replys")

        console.log(JSON.stringify(all_comments));

        all_comments.forEach((singleComment, index) => {
            console.log(singleComment)
            make_comment(singleComment)
        })

        // replys.insertBefore(divider , replys.firstChild);
        // replys.insertBefore(comment , replys.firstChild) ;

        replys_section.insertBefore(divider, replys_section.firstChild);
        replys_section.insertBefore(comment, replys_section.firstChild);


    }

    params = `type=show_reply&parent_comment=${comment_id}&note_id=${note_id}`
    request.send(params)

}

function make_comment(data) {


    console.log(data);

    let commentNode = document.getElementById("template_comment").cloneNode(true);

    commentNode.setAttribute("class", "comment");
    commentNode.style.display = "flex";
    commentNode.getElementsByClassName("comment_id")[0].value = data[0];
    commentNode.getElementsByClassName("commentText")[0].innerText = data[1];
    commentNode.getElementsByClassName("username")[0].innerText = data[2];
    commentNode.getElementsByClassName("date")[0].innerText = data[3]

    console.log(commentNode);

    let section;
    if (reply_mode == true) {
        console.log("reply mode")
        commentNode.getElementsByClassName("reply")[0].remove()
        section = replys;
    }
    else {
        let replyButton = commentNode.getElementsByClassName("reply")[0]
        section = comments;
        replyButton.addEventListener("click", () => {
            go_to_reply(commentNode);
        })
    }

    if (section.getElementsByClassName("comment").length != 0) {
        section.insertBefore(commentNode, section.firstChild);
    } else {

        section.append(commentNode)



    }



};

backButton.addEventListener("click", () => {

    console.log("going back to reply");
    comments.style.display = "block";
    replys_section.style.display = "none";
    reply_mode = false;
    parent_comment = 0;

})

let stars = document.getElementsByClassName("star");
let star_list = Array.from(stars)
star_list.forEach((star, index) => {


    star.addEventListener("click", () => {

        let request = new XMLHttpRequest()

        request.open("post", "/noteviewer", true);
        request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        request.onload = () => {
            console.log("rating done")
        }
        console.log("clicked")
        for (i = 0; i <= index; i = i + 1) {
            star_list[i].setAttribute("src", "static/res/star_yellow.svg")
        }
        for (i = index + 1; i < star_list.length; i = i + 1) {
            star_list[i].setAttribute("src", "static/res/star_white.svg")
        }
        parameters = `type=rating&rating=${index+1}&note_id=${note_id}`
        request.send(parameters);

    })



})

let insights_tab = document.getElementById("insights_tab");
let comments_tab = document.getElementById("comments_tab")

let comments_tab_button = document.getElementById("comments_tab_button");
let insights_tab_button = document.getElementById("insights_tab_button");

comments_tab_button.addEventListener("click" , ()=>{
    insights_tab.style.display  = "none";
    comments_tab.style.display = "block";
    
});
insights_tab_button.addEventListener('click' , ()=>{
    
  
    comments_tab.style.display = "none";
    insights_tab.style.display = "inline";
    
})

save_button =  document.getElementById("save");
save_button.addEventListener("click" , (event)=>{
    event.preventDefault();

    let request = new XMLHttpRequest();
    request.open("POST" , "/noteviewer" , true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    let title = document.getElementById("note_title_input").value;
    let description = document.getElementById("description").value;

    request.onload = ()=>{
        console.log(request.responseText)
    }
    
    let params  = `title=${title}&description=${description}&type=update`;
    request.send(params)
    
})


