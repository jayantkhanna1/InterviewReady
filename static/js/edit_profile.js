

function changeName(){
    var first_name = document.getElementById('f_name_edit_p').value;
    var last_name = document.getElementById('l_name_edit_p').value;
    const formData = new FormData();
    formData.append('first_name', first_name);
    formData.append('last_name', last_name);
    csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    formData.append('csrfmiddlewaretoken', csrf_token);
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'changeName', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            location.reload();
        }
    };
    xhr.send(formData);
}

function changePassword(){
    var old_pwd = document.getElementById('c_pwd_edit_p').value;
    var new_pwd = document.getElementById('new_pwd_edit_p').value;
    const formData = new FormData();
    formData.append('old_pwd', old_pwd);
    formData.append('new_pwd', new_pwd);
    csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    formData.append('csrfmiddlewaretoken', csrf_token);
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'changePassword', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            location.reload();
        }
    };
    xhr.send(formData);
}