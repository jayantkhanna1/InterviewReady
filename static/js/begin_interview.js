function begin_interview(microphone_and_speaker_permission){
    // Getting questions
    questions = document.getElementById("questions").value;
    questions = questions.replaceAll('\'', '"');
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
        console.log('Speaking');
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


function startListening(output_field,start_button,stop_button,audiogif) {
    const constraints = { audio: true };
    const chunks = [];
    document.getElementById(output_field).value = "Listening...";
    document.getElementById(output_field).setAttribute('readonly',true)
    document.getElementById(start_button).style.display = "none";
    document.getElementById(stop_button).style.display = "block";
    document.getElementById(audiogif).style.display = "block";
  
    navigator.mediaDevices
    .getUserMedia(constraints)
    .then(function (stream) {
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.ondataavailable = function (e) {
        if (e.data.size > 0) {
          chunks.push(e.data);
        }
      };

      mediaRecorder.onstop = function () {
        const audioBlob = new Blob(chunks, { type: 'audio/wav' });
        const formData = new FormData();
        csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        formData.append('csrfmiddlewaretoken', csrf_token);
        formData.append('audio', audioBlob);

        // Send audio data to Django backend using AJAX
        const xhr = new XMLHttpRequest();
        xhr.open('POST', 'asr', true);
        xhr.onreadystatechange = function () {
          if (xhr.readyState === 4 && xhr.status === 200) {
            // Handle the response from the Django server, if needed
            data = JSON.parse(xhr.responseText);
            document.getElementById(output_field).value = data['result'];
          }
        };
        xhr.send(formData);
      };

      mediaRecorder.start();
    })
    .catch(function (err) {
      console.error('Error accessing microphone:', err);
    });
}
  
function stopListening(output_field,start_button,stop_button,audiogif) {
  document.getElementById(start_button).style.display = "block";
  document.getElementById(stop_button).style.display = "none";
  document.getElementById(output_field).value = "Please wait we are processing your answer...";
  document.getElementById(audiogif).style.display = "none";
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.stop();
  }
}
  
function getNextQuestion(question_number){
  questions = document.getElementById("questions").value;
  questions = questions.replaceAll('\'', '"');
  questions = JSON.parse(questions);
  question = questions[question_number];
  html = get_HTML(questions,current_question = question_number);
  document.getElementById("interview").innerHTML += html;
  speak(question);
  const element = document.body;
  element.scrollIntoView({ behavior: "smooth", block: "end" });
}
function get_HTML(questions,question_number){
  var qu_no = question_number + 1;
  if (question_number > 6){
    // this is good just change to something else so it looks better but works
    return '<div class="question_div"><p class="question_number">7 <span class="lighter_color">/7</span></p><p class="question">Thank you for your time. We will get back to you soon.</p></div>'
  }
  question = questions[question_number];
  var html_string = '<div class="question_div"><p class="question_number">'+qu_no+' <span class="lighter_color">/7</span></p><p class="question">'+question+'</p><div class="answer"><textarea placeholder="Your Answer" readonly id="answer'+question_number+'"></textarea><img class="audiogif"  id="audiogif'+question_number+'" src="../static/images/audiogif.gif" alt=""></div><div class="answer_area"><div><a href="javascript:void(0)"  onclick="startListening(\'answer'+question_number+'\',\'startButton'+question_number+'\',\'stopButton'+question_number+'\',\'audiogif'+question_number+'\')" class="speak_answer" id="startButton'+question_number+'"> Start Speaking</a><a href="javascript:void(0)"  onclick="stopListening(\'answer'+question_number+'\',\'startButton'+question_number+'\',\'stopButton'+question_number+'\',\'audiogif'+question_number+'\')" class="speak_answer stopButton" id="stopButton'+question_number+'"> Stop Speaking</a><a href="javascript:void(0)"  onclick="allowUserToType(\'answer'+question_number+'\')" class="type_answer"><svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2.08594 15.4166H21.9193V2.58325H2.08594V15.4166ZM2.08594 17.1666C1.61927 17.1666 1.21094 16.9867 0.860938 16.627C0.510938 16.2673 0.335938 15.8638 0.335938 15.4166V2.58325C0.335938 2.11659 0.510938 1.70825 0.860938 1.35825C1.21094 1.00825 1.61927 0.833252 2.08594 0.833252H21.9193C22.3859 0.833252 22.7943 1.00825 23.1443 1.35825C23.4943 1.70825 23.6693 2.11659 23.6693 2.58325V15.4166C23.6693 15.8638 23.4943 16.2673 23.1443 16.627C22.7943 16.9867 22.3859 17.1666 21.9193 17.1666H2.08594ZM11.1276 6.22909H12.8776V4.47909H11.1276V6.22909ZM11.1276 9.87492H12.8776V8.12492H11.1276V9.87492ZM7.5401 6.22909H9.2901V4.47909H7.5401V6.22909ZM7.5401 9.87492H9.2901V8.12492H7.5401V9.87492ZM3.92344 9.87492H5.67344V8.12492H3.92344V9.87492ZM3.92344 6.22909H5.67344V4.47909H3.92344V6.22909ZM6.7526 13.5208H17.2526V11.7708H6.7526V13.5208ZM14.7443 9.87492H16.4943V8.12492H14.7443V9.87492ZM14.7443 6.22909H16.4943V4.47909H14.7443V6.22909ZM18.3318 9.87492H20.0818V8.12492H18.3318V9.87492ZM18.3318 6.22909H20.0818V4.47909H18.3318V6.22909ZM2.08594 15.4166V2.58325V15.4166Z" fill="currentColor"></path></svg></a></div><a href="javascript:void(0)" onclick="getNextQuestion('+qu_no+')" class="next"><img src="../static/images/arrow_right.png" alt=""></a></div><input type="hidden" readonly value="" id="confidence"></div>'
  return html_string;
}

function allowUserToType(answer_field,start_button, stop_button, audio_gif){
  document.getElementById(answer_field).removeAttribute('readonly')
  document.getElementById(answer_field).focus()
}