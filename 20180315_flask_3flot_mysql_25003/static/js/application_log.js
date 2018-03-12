ws = new ReconnectingWebSocket("ws://"  + location.host + '/zeromqlog')

ws.onmessage = function(message) {
  //payload = JSON.parse(message.data);
  $('#latest_data').html( message.data );
};
