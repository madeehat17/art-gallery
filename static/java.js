function scrollToSection(id) {
    document.getElementById(id).scrollIntoView({
        behavior: "smooth"
    });
}
function openModal(title){
    alert("You clicked on: "+title);
}
