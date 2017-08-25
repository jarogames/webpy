ws = new ReconnectingWebSocket("ws://"  + location.host + '/zeromq')

ws.onmessage = function(message) {
  payload = JSON.parse(message.data);
  $('#latest_data').html('Shit'+message.data +'<img width="350px" height="300px" src="/static/tempin.jpg" >'  );
};
