console.log("publisher_portal2 started")

var Publications = document.getElementById("Publication-button");
var Packages = document.getElementById("Package-button");
var Insights = document.getElementById("Insights-button");

var Publications_box = document.getElementById("publication-grid");
var Packages_box = document.getElementById("packages-grid");
var Insights_box = document.getElementById("insightbox");

Publications.addEventListener("click", () => {
    Publications_box.style.display = "grid";
    Insights_box.style.display = "none";
    Packages_box.style.display = "none";
});
Insights.addEventListener("click", () => {
    console.log('insights clicked')
    Publications_box.style.display = "none";
    Packages_box.style.display = "none";
    Insights_box.style.display = "flex";
});
Packages.addEventListener("click", () => {
    Publications_box.style.display = "none";
    Packages_box.style.display = "none";
    Insights_box.style.display = "none";
    Packages_box.style.display = "grid";
});

function copy() {
    var input = document.getElementById('code');
    var box = document.getElementById('box');
    input.textContent = "ashvin1"
    box.focus();

    box.select();
    document.execCommand("copy");

}