function processResponse(question, response) {
    var chatwindow = $("#chatwindow");
    chatwindow.append("<div class=\"msg rounded request p-2 mb-1\">" + response.response + "</div>");
    chatwindow.scrollTop(chatwindow.prop('scrollHeight'));
    if (response.results) {
        $('#complex_answer').hide(100);
        if (response.results.length > 0) {
            $('#complex_answer_content').html(jsonPrettyPrint.toHtml(response.results));
            $('#complex_answer_title').html("Respuesta para: " + question);
            $('#complex_answer').show(1200);
        }
    }
}

function sendMessage() {
    var message = $('#message').val();
    if (message) {
        $('#message').val('');
        $("#chatwindow").append("<div class=\"msg rounded response p-2 mb-1\">" + message + "</div>");
        $.ajax({
            type: "POST",
            url: '/processmessage/',
            data: { message: message },
            success: function(data) { processResponse(message, data) },

        });
    }
}
$(document).ready(function() {
    $("#message").keypress(function(e) {
        if (e.which == 13) {
            sendMessage();
        }
    });
    $("#send").click(function(e) {
        sendMessage();
    });
    $("#close_complex").click(function(e) {
        $('#complex_answer').hide(800);
    });
    $('#k').val(3);
    $('#threshold').val(0);
});

var jsonPrettyPrint = {
    replacer: function(match, pIndent, pKey, pVal, pEnd) {
        var key = '<span class=json-key>';
        var val = '<span class=json-value>';
        var str = '<span class=json-string>';
        var r = pIndent || '';
        if (pKey)
            r = r + key + pKey.replace(/[": ]/g, '') + '</span>: ';
        if (pVal)
            r = r + (pVal[0] == '"' ? str : val) + pVal + '</span>';
        return r + (pEnd || '');
    },
    toHtml: function(obj) {
        var jsonLine = /^( *)("[\w]+": )?("[^"]*"|[\w.+-]*)?([,[{])?$/mg;
        return JSON.stringify(obj, null, 3)
            .replace(/&/g, '&amp;').replace(/\\"/g, '&quot;')
            .replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(jsonLine, jsonPrettyPrint.replacer);
    }
};