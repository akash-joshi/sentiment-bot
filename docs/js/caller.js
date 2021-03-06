const record = document.querySelector('#startbutton')
const stop = document.querySelector('#stopbutton')
const running = document.querySelector('#running')
const emotion = document.querySelector('#emotion')
const { MediaRecorder, Blob } = window
const {startStream,stopStream} = AVStream

let num=1;
let flag=true;
let emotion_value = 0;
// disable stop button while not recording

stop.disabled = true

// main block for doing the audio recording

if (navigator.mediaDevices.getUserMedia) {
  console.log('getUserMedia supported.')

  const constraints = { audio: true }
  let chunks = [];

  const onSuccess = (stream) => {
    const mediaRecorder = new MediaRecorder(stream)

    record.onclick = () => {
      startStream(mediaRecorder,3000)
      console.log(mediaRecorder.state)
      console.log('recorder started')
      running.style.display = ""
      stop.disabled = false
      record.disabled = true
      record.style.display = "none"
    }

    stop.onclick = () => {
      stopStream()
      console.log(mediaRecorder.state)
      console.log('recorder stopped')
      running.style.display = "none"
      record.style.display = ""
      stop.disabled = true
      record.disabled = false
    }

    mediaRecorder.onstop = () => {
      console.log('data available after MediaRecorder.stop() called.')
      const blob = new Blob(chunks, { 'type' : 'audio/wav' })
      const fd = new FormData();
      fd.append('fname', num+'.wav');
      fd.append('data', blob);
      num++

      const options = {
        method:"POST",body:fd
      }

      fetch('https://NO',options).then(response=>response.text())
      .then(emote=>{
          emotion.textContent = normalizer(emote)
          console.log(emote)
      })
      chunks = [];
      if (mediaRecorder.state != 'recording')
      mediaRecorder.start()
    }

    mediaRecorder.ondataavailable = e => chunks.push(e.data);
  }

  navigator.mediaDevices.getUserMedia(constraints).then(onSuccess).catch((err)=>{console.error(err)})
} else {
  console.error('getUserMedia not supported on your browser!')
}
