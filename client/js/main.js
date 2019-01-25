const record = document.querySelector('#startbutton')
const stop = document.querySelector('#stopbutton')
const running = document.querySelector('#running')
const { MediaRecorder, Blob } = window

let flag=true
// disable stop button while not recording

stop.disabled = true

// main block for doing the audio recording

if (navigator.mediaDevices.getUserMedia) {
  console.log('getUserMedia supported.')

  const constraints = { audio: true }
  document.querySelector('#ouraudio').setAttribute('controls','')
  const onSuccess = (stream) => {
    const mediaRecorder = new MediaRecorder(stream)

    record.onclick = () => {
      mediaRecorder.start(6000)
      console.log(mediaRecorder.state)
      console.log('recorder started')
      running.style.display = ""
      stop.disabled = false
      record.disabled = true
      record.style.display = "none"
    }

    stop.onclick = () => {
      mediaRecorder.stop()
      console.log(mediaRecorder.state)
      console.log('recorder stopped')
      running.style.display = "none"
      record.style.display = ""
      stop.disabled = true
      record.disabled = false
    }

    mediaRecorder.onstop = () => {
      console.log('data available after MediaRecorder.stop() called.')
      console.log('recorder stopped')
    }

    mediaRecorder.ondataavailable = (e) => {
      const blob = new Blob([e.data], { 'type' : 'audio/wav' })
      const fd = new FormData();
      fd.append('fname', 'test.wav');
      fd.append('data', blob);
      const audio = document.querySelector('#ouraudio')
      const audioURL = window.URL.createObjectURL(blob);
      audio.src = audioURL;
      //console.log(fd.get('data').size)
      //console.log(blob.size)
      if(flag){
        $.ajax({
        type: 'POST',
        url: 'http://localhost:8000/voice-checker',
        data: fd ,
        processData: false,
        contentType: false
      }).done(function(data) {
           console.log(data);
      });
      }
      flag=false
      console.log('ondataavailable')
    }
  }

  navigator.mediaDevices.getUserMedia(constraints).then(onSuccess).catch((err)=>{console.error(err)})
} else {
  console.error('getUserMedia not supported on your browser!')
}