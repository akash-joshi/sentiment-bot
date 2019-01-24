const {JSDOM} = require('jsdom');
const dom = new JSDOM();
const $ = (require('jquery'))(dom.window);
const FormData = require('form-data');

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