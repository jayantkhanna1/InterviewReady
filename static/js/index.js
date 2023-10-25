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

data_error = document.getElementById('error_if_any').value
console.log(data_error)
data_error = data_error.replaceAll('\'', '"');
data_error = data_error.replaceAll('True', 'true');
data_error = data_error.replaceAll('False', 'false');
data_error = JSON.parse(data_error)
if (data_error["error_present"]) {
    error = data_error["error"]
    document.getElementById("desc").innerHTML = error
    launch_toast_correct()
}
