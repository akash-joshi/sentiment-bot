const AVStream = {
    startStream: ((mediaRecorder, time) => {
        if (mediaRecorder.state != 'recording')
            mediaRecorder.start(time)
        setTimeout(() => {
            if (mediaRecorder.state != 'inactive')
                mediaRecorder.stop()
        }, time);
        repeat = setInterval(() => {
            console.log(num)
            if (mediaRecorder.state != 'recording')
                mediaRecorder.start(time)

            setTimeout(() => {
                if (mediaRecorder.state != 'inactive') {
                    mediaRecorder.stop()
                }
            }, time);
        }, time);
    }),
    stopStream: (() => {
        clearInterval(repeat)
    })
}