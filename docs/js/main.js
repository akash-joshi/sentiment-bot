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

const reducer = input => {
	if(input == 5 || input == 6 || input == 4)
		return 2
	if(input == 0 || input == 1 || input == 3)
		return 0
	else return 1
};

const normalizer = input => {
	const reduced = reducer(input);
	if(reduced == 2){
		emotion_value+=6;
		if(emotion_value < -5)
			emotion_value+=3;
		if(emotion_value < -15)
			emotion_value+=10;	
	} else {
		if(reduced != 2 && reduced == 0)
			emotion_value-=2;
		else emotion_value-=4;
	}
	
	console.log(`emotion_value : ${emotion_value}`)

	if(emotion_value >= 10)
		return 'Anger'
	if(emotion_value < 0)
		return 'Happy'
	else return 'Neutral'
}

// main block for doing the audio recording

if (navigator.mediaDevices.getUserMedia) {
  console.log('getUserMedia supported.')

  const constraints = { audio: true }
  let chunks = [];

  const onSuccess = (stream) => {
    const mediaRecorder = new MediaRecorder(stream)

    record.onclick = () => {
      startStream(mediaRecorder,1000)
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

      fetch('https://chat-deploy.herokuapp.com/voice-checker',options).then(response=>response.text())
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
