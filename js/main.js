const record = document.querySelector('#startbutton')
const stop = document.querySelector('#stopbutton')

const { MediaRecorder, Blob } = window

// disable stop button while not recording

stop.disabled = true

// main block for doing the audio recording

if (navigator.mediaDevices.getUserMedia) {
  console.log('getUserMedia supported.')

  const constraints = { audio: true }

  const onSuccess = (stream) => {
    const mediaRecorder = new MediaRecorder(stream)

    record.onclick = () => {
      mediaRecorder.start(3000)
      console.log(mediaRecorder.state)
      console.log('recorder started')

      stop.disabled = false
      record.disabled = true
    }

    stop.onclick = () => {
      mediaRecorder.stop()
      console.log(mediaRecorder.state)
      console.log('recorder stopped')

      stop.disabled = true
      record.disabled = false
    }

    mediaRecorder.onstop = () => {
      console.log('data available after MediaRecorder.stop() called.')
      console.log('recorder stopped')
    }

    mediaRecorder.ondataavailable = (e) => {
      const blob = new Blob([e.data], { 'type': 'audio/vnd.wav; codecs=opus' })
      const fd = new FormData();
      fd.append('fname', 'test.wav');
      fd.append('data', 'soundBlob');
      $.ajax({
        type: 'POST',
        url: 'http://localhost:8000/voice-checker',
        data: fd,
        processData: false,
        contentType: false
      }).done(function(data) {
           console.log(data);
      });
      console.log('ondataavailable')
    }
  }

  navigator.mediaDevices.getUserMedia(constraints).then(onSuccess).catch((err)=>{console.error(err)})
} else {
  console.error('getUserMedia not supported on your browser!')
}