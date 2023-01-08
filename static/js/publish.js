console.log("sanan kitti")

let number_of_notes = 1

let add = document.getElementById("add");
let single_note = document.getElementById("single_note")
let all_notes = document.getElementById("all_notes")

let number_of_notes_input = document.getElementById("number_of_upload")

let upload_button = document.getElementById("upload_button");

let form = document.getElementById("form")


let select_note_box = document.getElementById("select_note_box");
let allblack = document.getElementById("allblack")


const inputTypeSelect = document.getElementById("input_type");
const note_upload = document.getElementById("note_upload");
const package_upload = document.getElementById("package_upload");


function deleteInput(event) {
    event.preventDefault();
    let clickedButton = event.target;
    let deleteButtonNumber = Array.from(document.getElementsByClassName("deleteButton"));
    console.log(clickedButton)
    console.log(deleteButtonNumber)
    let index = deleteButtonNumber.indexOf(clickedButton);
    console.log(index);
    let note_input = document.getElementsByClassName("single_note")[index + 1];
    note_input.remove();

}




// fuction to select from note select


var current_selection_box = ""


console.log(single_note)
let select_note_button = single_note.querySelector("#select_note_button");
console.log(select_note_button)



let notes = select_note_box.getElementsByClassName("single_select_note");

console.log("the notes are ", notes)

Array.from(notes).forEach((element) => {
    console.log(element)
    element.addEventListener("click", () => {
        console.log("clicked")
        let note_id = element.querySelector("#select_note_id").innerText;

        let input_box = document.getElementsByClassName("single_note")[window.current_selection_box];

        let preview = input_box.querySelector("#selected_note")
        console.log(preview)

        if (preview.childElementCount > 0) {
            preview.firstChild.remove()
        }

        preview.append(element)

        input_box.querySelector("#selected_note_id").value = note_id;


        show_hide_selection_box(false);
        console.log("the note id is", note_id)
    })
})

select_note_button.addEventListener("click", (event) => {
    event.preventDefault();
    console.log(window.current_selection_box, "before")
    window.current_selection_box = 0;
    console.log(window.current_selection_box, "after")
    show_hide_selection_box(true)
})

allblack.addEventListener("click", () => {
    show_hide_selection_box(false)
})

function change_input_type(note) {

    let value = note.querySelector("#type").value;
    let new_note = note.querySelector(".new_note");
    let from_existing = note.querySelector(".from_existing");

    console.log(new_note);

    if (value == 2) {

        note.querySelector("#title").disabled = true
        note.querySelector("#subject").disabled = true
        note.querySelector("#about").disabled = true
        note.querySelector("#file").disabled = true
        note.querySelector("#selected_note_id").disabled = false


        new_note.style.display = "none";
        from_existing.style.display = "block";
        console.log(value)
    } else {

        note.querySelector("#title").disabled = false
        note.querySelector("#subject").disabled = false
        note.querySelector("#about").disabled = false
        note.querySelector("#file").disabled = false
        note.querySelector("#selected_note_id").disabled = true

        new_note.style.display = "block";
        from_existing.style.display = "none";

    }


}

function show_hide_selection_box(x) {
    if (x) {
        allblack.style.display = "block"
        select_note_box.style.display = "grid"
    } else {
        allblack.style.display = "none"
        select_note_box.style.display = "none"

    }
}


single_note.querySelector("#type").addEventListener("change", () => { change_input_type(single_note) })



add.addEventListener("click", (event) => {

    event.preventDefault()

    console.log("here")
    let new_single_note = single_note.cloneNode(true);

    new_single_note.setAttribute("class", "single_note")
    let type = new_single_note.querySelector("#type")



    number_of_notes++;

    console.log(new_single_note);


    let input_type = new_single_note.querySelector("#type");
    let title = new_single_note.querySelector("#title");
    let subject = new_single_note.querySelector("#subject");
    let about = new_single_note.querySelector("#about");
    let file = new_single_note.querySelector("#file");
    let selected_note_id = new_single_note.querySelector("#selected_note_id");

    // let deleteButton = document.createElement("button");
    // deleteButton.innerText = "delete";
    // deleteButton.setAttribute("class", "delete");
    // new_single_note.append(deleteButton);

    // deleteButton.addEventListener("click", (event) => {
        // deleteInput(event)
    // })

    let deleteButton = new_single_note.getElementsByClassName("deleteButton")[0];
    deleteButton.addEventListener("click" , deleteInput);
    deleteButton.style.display = "flex";

    input_type.setAttribute("name", "type");
    title.setAttribute("name", "title");
    subject.setAttribute("name", "subject");
    about.setAttribute("name", "about");
    file.setAttribute("name", "file");
    selected_note_id.setAttribute("name", "note_id");

    input_type.value = "1";
    title.value = "";
    subject.value = "";
    about.value = "";
    file.value = "";
    selected_note_id.value = "";

    change_input_type(new_single_note)

    // console.log(input_type.name)
    // console.log(title.name)
    // console.log(subject.name)
    // console.log(about.name)
    // console.log(input_type.name)


    let select_button = new_single_note.querySelector("#select_note_button");
    select_button.addEventListener("click", (event) => {
        event.preventDefault();
        let notes = document.getElementsByClassName("single_note");
        let note_number = Array.from(notes).indexOf(new_single_note)

        console.log(window.current_selection_box, "before");
        window.current_selection_box = note_number;
        console.log(window.current_selection_box, "after");

        show_hide_selection_box(true);
    })


    type.addEventListener("change", () => { change_input_type(new_single_note) });

    all_notes.append(new_single_note);


})

upload_button.addEventListener("click", (event) => {
    event.preventDefault();
    let note_nodes = document.getElementsByClassName("single_note");


    // console.log(note_nodes)

    Array.from(note_nodes).forEach((element, index) => {
        console.log(index, element)

        if (inputTypeSelect.value == 1) {

            form.submit();

        } else {



            // console.log(element.querySelector("#type"))
            element.querySelector("#type").setAttribute("name", "type" + (index + 1))
            element.querySelector("#title").setAttribute("name", "title" + (index + 1))
            element.querySelector("#subject").setAttribute("name", "subject" + (index + 1))
            element.querySelector("#about").setAttribute("name", "about" + (index + 1))
            element.querySelector("#file").setAttribute("name", "file" + (index + 1))
            element.querySelector("#selected_note_id").setAttribute("name", "note_id" + (index + 1))


            number_of_notes_input.setAttribute("value", note_nodes.length);

            form.submit();
            console.log("form submitted")
        }

    })
})


inputTypeSelect.addEventListener("change", () => {
    console.log(inputTypeSelect.value);
    if (inputTypeSelect.value == 1) {
        note_upload.style.display = "block";
        package_upload.style.display = "none";
        add.style.display = "none"
    } else {
        note_upload.style.display = "none";
        package_upload.style.display = "block";
        add.style.display = "inline"
    }
})