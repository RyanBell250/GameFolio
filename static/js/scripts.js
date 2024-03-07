$(document).ready(function() {

    $('#search-button').click(function(e) {
        var queryTerm = $('#search-bar').val()
        $('#query-parameter').attr("value", queryTerm)
    });

    var $pageButtons = jQuery('.page-link')
    $pageButtons.click(function(e) {
        var pageNumber = $(this).html();
        $('#page-parameter').attr("value", pageNumber-1)
    });
});