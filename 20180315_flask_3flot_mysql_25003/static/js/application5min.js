ws = new ReconnectingWebSocket("ws://"  + location.host + '/zeromq5min')

ws.onmessage = function(message) {
  //payload = JSON.parse(message.data);
  $('#latest_data').html( message.data );
};
