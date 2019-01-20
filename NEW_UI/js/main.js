$(() => {

  let prev;
  let ready = false;
  let room;
  let thisme
  const cleanInput = input => $('<div/>').text(input).html();

  $("#sendform").submit( () => {
    const message = cleanInput($('#m').val());
    
    if(message){
      socket.emit('chat message', $('#m').val(),room);
      $('#m').val('');
    }
    
    return false;
  });

  socket.on("update", (msg) => {
    $('#messages').append('<li id="update" >' + msg);
    prev='';
  })

  socket.on("people-list", (people) => {
    for (person in people) {
        $('#online').append('<li id="' + people[person].id + '">' + people[person].nick);
    }
  });

  socket.on("disconnect", () => {
    $('#messages').append("<li id=\"update\">You have lost connection to server, check your internet or try to refresh the page");
    $('#sendform').hide();
  });
  socket.on("reconnect", ()=>{
    location.reload()
  })
  socket.on('chat message', (nick, msg) => {
    if (prev == nick) {
      $('#messages li:last-child > div').append("<div>" + msg + "</div>");
    } else {
      $('#messages').append("<li> <strong>" + nick + "</strong> : " + "<div id=\"innermsg\">" + msg + "</div></li>")
    }
    if(thisme != nick)
        displayNotification(nick,msg)
    prev = nick;
    $("#messages").animate({
      scrollTop: $('#messages').prop("scrollHeight")
    }, 100);
  });

  socket.on('message que', (nick, msg) => {
    if (prev == nick) {
      $('#messages li:last-child > div').append("<div>" + msg + "</div>");
    } else {
      $('#messages').append("<li> <strong>" + nick + "</strong> : " + "<div id=\"innermsg\">" + msg + "</div></li>");
    }

    prev = nick;
  });
});