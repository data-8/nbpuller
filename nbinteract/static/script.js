function showProceedLink(proceed_url) {
  if (proceed_url) {
    $(".proceed-link").attr('href', proceed_url);
    $(".proceed-link").html(proceed_url);
  } else  {
    var domain = document.domain;
    $(".proceed-link").attr('href', domain);
    $(".proceed-link").html("http://" + domain);
  }
  $(".proceed-container").show();
}

function updateStatus(payload) {
  $('.status').html(payload);
}

function handleRedirect(payload) {
  $('.status').html('Redirecting you to ' + payload);
  window.location.href = payload;
}

function updateLog(payload) {
  $('.log').html(payload + '\n');
}

function showError(payload) {
  updateStatus(payload.message);
  showProceedLink(payload.proceed_url);
}

// Keep in sync with messages.py
var messageHandlers = {
  'LOG': updateLog,
  'STATUS': updateStatus,
  'REDIRECT': handleRedirect,
  'ERROR': showError,
};

// Launches a socket connection with server-side, receiving status updates and
// updating the page accordingly.
function openStatusSocket(socket_args) {
  var is_development = socket_args['is_development'];
  var base_url = socket_args['base_url'];
  var username = socket_args['username'];

  // Constructs a URL that looks like:
  //
  // ws://<host>/<base_url>/socket/<username>?<params>
  //
  // Uses wss in production.
  var url = [
    is_development ? 'ws://' : 'wss://',
    window.location.hostname,
    ':',
    window.location.port,
    base_url,
    'socket/',
    username,
    window.location.search,
  ].join('');

  var socket = new WebSocket(url);

  socket.onopen = function() {
    console.log('[Client] Connected to url: ' + url);
  };

  /**
   * This function takes in a message from messages.py as a JSON string.
   * It calls the corresponding handler for each message type.
   */
  socket.onmessage = function(event) {
    message = JSON.parse(event.data);

    if (is_development) {
      console.log(message);
    }

    var handler = messageHandlers[message.type];
    handler(message.payload);
  };
}

$(document).ready(function() {
  $('.console_log').on('click', function() {
    if ($('.log-container').is(':visible')) {
      $('.log-container').hide();
      $('.console_log').html('Show Console Log');
    } else {
      $('.log-container').show();
      $('.console_log').html('Hide Console Log');
    }
    return false;
  });

  $('.server-field').on('input', function() {
    value = $(this).val();
    $('.server-display').each(function() {
      if (value == '') {
        $(this).html('ds8.berkeley.edu');
      } else {
        $(this).html(value);
      }
    });
    $('.server-button').attr('href', 'http://' + value +
      $('.server-input .reversed').contents()[2].textContent);
  });
});

function getBrowserName(){
    var ua= navigator.userAgent, tem,
    M= ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
    if(/trident/i.test(M[1])){
        tem=  /\brv[ :]+(\d+)/g.exec(ua) || [];
        return 'IE '+(tem[1] || '');
    }
    if(M[1]=== 'Chrome'){
        tem= ua.match(/\b(OPR|Edge)\/(\d+)/);
        if(tem!= null) return tem.slice(1).join(' ').replace('OPR', 'Opera');
    }
    M= M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
    if((tem= ua.match(/version\/(\d+)/i))!= null) M.splice(1, 1, tem[1]);
    return M[0];
}
