function begin_interview(microphone_and_speaker_permission){
    // Getting questions
    questions = document.getElementById("questions").value;
    questions = questions.replaceAll('\'', '"');
    console.log(questions)
    questions = JSON.parse(questions);

    // Making visible
    document.getElementById("user_information").style.display = "none";
    document.getElementById("interview").style.display = "flex";

    // Adding first question
    html = get_HTML(questions,current_question = 0);
    document.getElementById("interview").innerHTML = html;

    // Make question speak
    if (microphone_and_speaker_permission){
        current_question = questions[0]
        speak(current_question);
    }
}

function speak(message){
    if ('speechSynthesis' in window) {
        let speech = new SpeechSynthesisUtterance();
        speech.lang = "en";
        speech.text = message;
        speech.volume = 1;
        speech.rate = 1;
        speech.pitch = 1;
        window.speechSynthesis.speak(speech);
    } else {
        console.error('Speech synthesis is not supported in this browser');
    }   
}

let mediaRecorder; // Define the mediaRecorder variable in a broader scope


// function startListening(output_field,start_button,stop_button,audiogif) {
//     const constraints = { audio: true };
//     const chunks = [];
//     document.getElementById(output_field).value = "Listening...";
//     document.getElementById(output_field).setAttribute('readonly',true)
//     document.getElementById(start_button).style.display = "none";
//     document.getElementById(stop_button).style.display = "block";
//     document.getElementById(audiogif).style.display = "block";
  
//     navigator.mediaDevices
//     .getUserMedia(constraints)
//     .then(function (stream) {
//       mediaRecorder = new MediaRecorder(stream);
//       mediaRecorder.ondataavailable = function (e) {
//         if (e.data.size > 0) {
//           chunks.push(e.data);
//         }
//       };

//       mediaRecorder.onstop = function () {
//         const audioBlob = new Blob(chunks, { type: 'audio/wav' });
//         const formData = new FormData();
//         csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
//         formData.append('csrfmiddlewaretoken', csrf_token);
//         formData.append('audio', audioBlob);

//         // Send audio data to Django backend using AJAX
//         const xhr = new XMLHttpRequest();
//         xhr.open('POST', 'asr', true);
//         xhr.onreadystatechange = function () {
//           if (xhr.readyState === 4 && xhr.status === 200) {
//             // Handle the response from the Django server, if needed
//             data = JSON.parse(xhr.responseText);
//             document.getElementById(output_field).value = data['result'];
//           }
//         };
//         xhr.send(formData);
//       };

//       mediaRecorder.start();
//     })
//     .catch(function (err) {
//       console.error('Error accessing microphone:', err);
//     });
// }
  
// function stopListening(output_field,start_button,stop_button,audiogif) {
//   document.getElementById(start_button).style.display = "block";
//   document.getElementById(stop_button).style.display = "none";
//   document.getElementById(output_field).value = "Please wait we are processing your answer...";
//   document.getElementById(audiogif).style.display = "none";
//   if (mediaRecorder && mediaRecorder.state === 'recording') {
//     mediaRecorder.stop();
//   }
// }
  
function getNextQuestion(question_number){
  // Checking if user has answered previous questions before we move on
  prev_answer = document.getElementById("answer"+(question_number-1)).value;
  if (prev_answer == ""){
    document.getElementById("desc").innerHTML = "Please answer the question"
    launch_toast_correct()
    return;
  }
  // Getting list of all questions
  questions = document.getElementById("questions").value;
  questions = questions.replaceAll('\'', '"');
  questions = JSON.parse(questions);

  // Getting next question
  question = questions[question_number];

  // Checking if we have reached the end of the interview
  if (question_number > 6){
    // We have reached the end now we show final page
    document.getElementById('user_information').style.display = "none";

    // Collecting all answers
    var answer_array = []
    for (var i=0;i<7;i++){
      answer_array[i] = document.getElementById('answer'+i).value
    }

    var ques_answer_pair = []

    // Showing 2nd last modal before loading final page
    document.getElementById('interview').style.display = "none";
    document.getElementById("final").style.display = "flex"

    // Getting result for final answer from the backend
    const formData = new FormData();
    var final_answer = document.getElementById("answer6").value;
    var final_question = questions[6];
    formData.append('answer', final_answer);
    formData.append('question', final_question);
    csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    formData.append('csrfmiddlewaretoken', csrf_token);
    const xhr_new = new XMLHttpRequest();
    xhr_new.open('POST', 'getResultForOnePair', true);
    xhr_new.onreadystatechange = function () {
      if (xhr_new.readyState === 4 && xhr_new.status === 200) {
        data = JSON.parse(xhr_new.responseText);
        console.log(data)
        // final answer received
        document.getElementById('confidence6').value = data["result"]
        var confidence_array = []

        // Getting all answers for all previous quesitons and making one array with all questions and answers etc
        var all_confidence = document.getElementsByClassName('confidence')
        for (var i=0;i<all_confidence.length;i++){
          confidence_array.push(all_confidence[i].value)
        }
        console.log(confidence_array)
        // Making questions answer pair
        for (var i=0;i<7;i++){
          var temp_jso = {
            "question" : questions[i],
            "answer" : answer_array[i],
            "confidence" : confidence_array[i]
          }
          ques_answer_pair.push(temp_jso)
        }
        console.log(ques_answer_pair)


        const formData = new FormData();
        formData.append('question_answer_pair', JSON.stringify(ques_answer_pair));
        csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        formData.append('csrfmiddlewaretoken', csrf_token);
        const xhr = new XMLHttpRequest();
        xhr.open('POST', 'saveInterviewResult', true);
        xhr.onreadystatechange = function () {
          if (xhr.readyState === 4 && xhr.status === 200) {
            console.log("Interview result saved")
            window.location = "showInterviewResult";
          }
        }
        xhr.send(formData);   
      }
    };
    xhr_new.send(formData);
  }
  else{
    // We have not reached the end yet so getting next question HTML
    html = get_HTML(questions,current_question = question_number);

    // getting old answers as they will be rewritten
    all_answers = document.getElementsByClassName("answer_textarea")
    answer = []
    for (var i=0;i<all_answers.length;i++){
      answer.push(all_answers[i].value)
    }

    document.getElementById("interview").innerHTML += html;

    // putting old answers back
    for (var i=0;i<answer.length;i++){
      console.log(answer[i])
      document.getElementById("answer"+i).value = answer[i]
    }

    // Making question speak
    speak(question);
    const element = document.body;
    element.scrollIntoView({ behavior: "smooth", block: "end" });

    // Getting result for the previous answer from the backend
    prev_answer = document.getElementById("answer"+(question_number-1)).value;
    prev_question = questions[question_number-1];
    const formData = new FormData();
    formData.append('answer', prev_answer);
    formData.append('question', prev_question);
    csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    formData.append('csrfmiddlewaretoken', csrf_token);
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'getResultForOnePair', true);
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        data = JSON.parse(xhr.responseText);
        console.log(data)
        prev_ques = question_number-1 
        document.getElementById('confidence' +prev_ques).value = data["result"]
      }
    };
    xhr.send(formData);

  }
}
function get_HTML(questions,question_number){
  var qu_no = question_number + 1;
  if (question_number > 6){
    // this is good just change to something else so it looks better but works
    return '<div class="question_div"><p class="question_number">7 <span class="lighter_color">/7</span></p><p class="question">Thank you for your time. We will get back to you soon.</p></div>'
  }
  question = questions[question_number];
  var html_string = '<div class="question_div"><p class="question_number">'+qu_no+' <span class="lighter_color">/7</span></p><p class="question">'+question+'</p><div class="answer"><textarea class="answer_textarea" placeholder="Your Answer" id="answer'+question_number+'"></textarea><img class="audiogif"  id="audiogif'+question_number+'" src="../static/images/audiogif.gif" alt=""></div><div class="answer_area"><a href="javascript:void(0)" onclick="getNextQuestion('+qu_no+')" class="next"><img src="../static/images/arrow_right.png" alt=""></a></div><input type="hidden" readonly value="" id="confidence'+question_number+'" class="confidence"></div>'
  return html_string;
}

function allowUserToType(answer_field,start_button, stop_button, audio_gif){
  document.getElementById(answer_field).removeAttribute('readonly')
  document.getElementById(answer_field).focus()
}