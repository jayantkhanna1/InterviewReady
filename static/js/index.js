var acc = document.getElementsByClassName("accordion");
        // var panel = document.getElementsByClassName('panel')
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function () {
        this.classList.toggle("active");
        var panel = this.nextElementSibling;

        if (panel.style.maxHeight) {
            panel.style.maxHeight = null;
            panel.style.padding = "0px"
        } else {
            panel.style.padding = "33px 7px"
            panel.style.maxHeight = panel.scrollHeight + "px";
        }
    });
}

