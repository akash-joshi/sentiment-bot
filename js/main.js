$(() => {
const record = document.querySelector('#startbutton')
const stop = document.querySelector('#stopbutton')

const { MediaRecorder, prompt, Blob } = window

// disable stop button while not recording

stop.disabled = true

// main block for doing the audio recording

  if (navigator.mediaDevices.getUserMedia) {
    console.log('getUserMedia supported.')

    const constraints = { audio: true }
    var chunks = []

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

      mediaRecorder.onstop = function (e) {
        console.log('data available after MediaRecorder.stop() called.')

        const blob = new Blob(chunks, { 'type': 'audio/vnd.wav; codecs=opus' })
        chunks = []
        var audioURL = window.URL.createObjectURL(blob)
        console.log('recorder stopped')
      }

      mediaRecorder.ondataavailable = function (e) {
        chunks.push(e.data)
      }
    }

    var onError = function (err) {
      console.log('The following error occured: ' + err)
    }

    navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError)
  } else {
    console.log('getUserMedia not supported on your browser!')
  }
});