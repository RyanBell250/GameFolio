$(document).ready(function() {

    $('#search-button').click(function(e) {
        var queryTerm = $('#search-bar').val()
        $('#query-parameter').attr("value", queryTerm)
    });
});