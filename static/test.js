$(document).ready(function() {
    //connect to the socket server.
    var socket = io.connect(
        'http://' + document.domain + ':' + location.port + '/web_socket',
        {transports: ['websocket', 'polling', 'flashsocket']}
    );
    var heater_numbers_received = [];
    var pressure_numbers_received = [];

    //receive details from server
    socket.on('heater', function (msg) {
        console.log("Received number" + msg.number);
        //maintain a list of ten numbers
        if (heater_numbers_received.length >= 10) {
            heater_numbers_received.shift()
        }
        heater_numbers_received.push(msg.number);
        heater_numbers_string = '';
        for (var i = 0; i < heater_numbers_received.length; i++) {
            heater_numbers_string = heater_numbers_string + '<p>' + heater_numbers_received[i].toString() + '</p>';
        }
        $('#heater').html(heater_numbers_string);
        socket.emit('callback', 'ok');
    });
    socket.on('pressure', function (msg) {
        console.log("Received number" + msg.number);
        //maintain a list of ten numbers
        if (pressure_numbers_received.length >= 10) {
            pressure_numbers_received.shift()
        }
        pressure_numbers_received.push(msg.number);
        pressure_numbers_string = '';
        for (var i = 0; i < pressure_numbers_received.length; i++) {
            pressure_numbers_string = pressure_numbers_string + '<p>' + pressure_numbers_received[i].toString() + '</p>';
        }
        $('#pressure').html(pressure_numbers_string);
        socket.emit('callback', 'ok');
    });
});
