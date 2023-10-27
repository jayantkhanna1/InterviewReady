
// get detfault mode
var mode = localStorage.getItem('interview_ready_mode');
console.log(mode)
// check if mode is dark
if (mode == 'dark' || mode == null){
    changeCss('dark');
}
else{
    changeCss('light');
}


function changeCss(mode){
    if (mode == 'dark'){
        // change css to dark mode
        document.getElementById('dark_css').disabled = false;
        document.getElementById('light_css').disabled = true;
        document.getElementById('toastcss').disabled = true;
        document.getElementById('moon').style.display = 'none';
        document.getElementById('sun').style.display = 'block';
        // set this as default
        localStorage.setItem('interview_ready_mode', 'dark');


    }
    else{
        // change css to light mode
        document.getElementById('dark_css').disabled = true;
        document.getElementById('light_css').disabled = false;
        document.getElementById('toastcss').disabled = false;
        document.getElementById('moon').style.display = 'block';
        document.getElementById('sun').style.display = 'none';
        // set this as default
        localStorage.setItem('interview_ready_mode', 'light');
    }
}