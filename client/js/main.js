const record = document.querySelector('#startbutton')
const stop = document.querySelector('#stopbutton')
const running = document.querySelector('#running')
const { MediaRecorder, Blob } = window

let repeat
let num=1
// disable stop button while not recording

stop.disabled = true

const constraints = { audio: true }
//document.querySelector('#ouraudio').setAttribute('controls','')
const onSuccess = (stream) => {
  const mediaRecorder = new MediaRecorder(stream)
  // generate a new file every 5s

  const record_and_send = () => {
     console.log(num)
     const chunks = [];
     mediaRecorder.ondataavailable = e => chunks.push(e.data);
     mediaRecorder.onstop = () => {
      console.log(mediaRecorder.state)
      console.log('recorder stopped')
      const blob = new Blob(chunks, { 'type' : 'audio/wav' })
      const fd = new FormData();
      fd.append('fname', num+'.wav');
      fd.append('data', blob);
      num++
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
     mediaRecorder.start();
     setTimeout(()=> mediaRecorder.stop(), 3000);
    }

    const startFunc = () => {
      repeat = setInterval(record_and_send, 3000);
    }

    const stopFunc = () => {
      clearInterval(repeat)
    }

  record.onclick = () => {
    startFunc()
    console.log(mediaRecorder.state)
    console.log('recorder started')
    running.style.display = ""
    stop.disabled = false
    record.disabled = true
    record.style.display = "none"

  }

  stop.onclick = () => {
    stopFunc()
    running.style.display = "none"
    record.style.display = ""
    stop.disabled = true
    record.disabled = false
  }

  /*mediaRecorder.onstop = () => {
    console.log('data available after MediaRecorder.stop() called.')
    console.log('recorder stopped')
  }

  mediaRecorder.ondataavailable = (e) => {
    const blob = new Blob([e.data], { 'type' : 'audio/wav' })
    const fd = new FormData();
    fd.append('fname', num+'.wav');
    fd.append('data', blob);
    num++
    const audio = document.querySelector('#ouraudio')
    const audioURL = window.URL.createObjectURL(blob);
    audio.src = audioURL;
    //console.log(fd.get('data').size)
    //console.log(blob.size)
      $.ajax({
      type: 'POST',
      url: 'http://localhost:8000/voice-checker',
      data: fd ,
      processData: false,
      contentType: false
    }).done(function(data) {
         console.log(data);
    });
    console.log('ondataavailable')
  }*/
}

navigator.mediaDevices.getUserMedia(constraints).then(onSuccess).catch((err)=>{console.error(err)})