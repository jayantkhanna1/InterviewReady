function check_if_resume(){
    var interview_type = document.getElementById("interview_type").value;
    if(interview_type == "background"){
        document.getElementById("job_description_textarea").value = "";
        document.getElementById("job_description_textarea").placeholder = "Enter Your Resume";
        document.getElementById("job_desc").innerHTML = "Resume:";

    }
    else if(interview_type == "custom"){
        document.getElementById("job_description_textarea").value = "";
        document.getElementById("job_description_textarea").placeholder = "Enter Custom Data";
        document.getElementById("job_desc").innerHTML = "Custom Data:";
    }           
    else{
        document.getElementById("job_description_textarea").value = "";
        document.getElementById("job_description_textarea").placeholder = "Enter Job Description";
        document.getElementById("job_desc").innerHTML = "Job Description:";

    }
}