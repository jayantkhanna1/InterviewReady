
function launch_toast_correct() {
    var x = document.getElementById("toast")
    x.className = "show";
    setTimeout(function () { x.className = x.className.replace("show", ""); }, 5000);
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