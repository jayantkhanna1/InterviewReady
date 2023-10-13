// asking for mic and speaker permission
function ask_for_permission(){
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        // Request permission to use the microphone and speaker
        navigator.mediaDevices.getUserMedia({ audio: true, video: false })
          .then(function (stream) {
            // Permission granted, you can now use the microphone and speaker
            console.log('Microphone and speaker access granted');
            // stop accessing microphone now
            stream.getTracks().forEach(function (track) {
              track.stop();
            });
            begin_interview(true);
            // You can connect the stream to your audio elements or process it as needed.
          })
          .catch(function (error) {
            // Permission denied or an error occurred
            console.error('Error accessing microphone and speaker:', error);
            begin_interview(false);
          });
      } else {
        console.error('Web Speech API is not supported in this browser');
        begin_interview(false);
      }
}

function startListening(output_field){
  
  
}