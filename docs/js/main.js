const record = document.querySelector('#startbutton')
const stop = document.querySelector('#stopbutton')
const running = document.querySelector('#running')
const emotion = document.querySelector('#emotion')
const { MediaRecorder, Blob } = window
const {startStream,stopStream} = AVStream

let num=1;
let flag=true
// disable stop button while not recording

stop.disabled = true

// global emotion reading
// range: -10 to +10
// angry: -10 to -8
// satisfactory: -8 to +5
// happy: +5 to +10
global_emo_val = 0;
prev_emo_read = -1;

// calc emotion value
function red_emotion(val){
	if(val.localeCompare("4") || val.localeCompare("5") || val.localeCompare("6")){
		return 2;
	} else if (val.localeCompare("0") || val.localeCompare("1") || val.localeCompare("3")){
		return 0;
	}
	return 1;
}

function norm_emotion(cur_val){
	switch(red_emotion(cur_val)){
		case 0:
			global_emo_val += 1;
			if (global_emo_val < 0 || prev_emo_read == 0){
				global_emo_val += 1;
				prev_emo_read = -1;
			} else {
				prev_emo_read = 0;
			}
			break;
		case 1:
			if(prev_emo_read == 1){
				global_emo_val -= 2;
			} else {
				global_emo_val -= 3;
			}
			prev_emo_read = 1;
			break;
		case 2:
			global_emo_val -= 2;
			prev_emo_read = 2;
			break;
	}
	
	global_emo_val = Math.min(Math.max(-10, global_emo_val), 10);
	
	if(global_emo_val >= 5) {
		return "Happy";
	} else if (global_emo_val < -8) {
		return "Angry";
	} else {
		return "Satisfactory";
	}
}

function norm_emotion_orig(cur_val){
	val red_emo = red_emotion(cur_val)
	switch(){
		case 0:
			global_emo_val -= 2;
			break;
		case 1:
			global_emo_val -= 4;
			break;
		case 2:
			global_emo_val += 6;
			if(global_emo_val <= -5){
				global_emo_val += 3;
			} 
			if (global_emo_val <= -15) {
				global_emo_val += 10;
			}
			break;
	}
	
	if (global_emo_val >= 10){
		return "Happy";
	} else if (global_emo_val < 0){
		return "Sad";
	} else {
		return "Satisfactory";
	}
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

      fetch('https://sentiment-bot-api.herokuapp.com/voice-checker',options).then(response=>response.text())
      .then(emote=>{
          emotion.textContent = norm_emotion_orig(emote)
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