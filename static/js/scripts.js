$(document).ready(function() {

    $('#search-button').click(function(e) {
        var queryTerm = $('#search-bar').val()
        $('#query-parameter').attr("value", queryTerm)
    });

    var $pageButtons = jQuery('.page-link')
    $pageButtons.click(function(e) {
        var pageNumber = $(this).val();
        if(e.screenX == 0) {
            var pageSearch = $("#page-search");
            var number = pageSearch.val();
            if(number != "") {
                pageNumber = number;
            }
        }
        $('#page-parameter').attr("value", pageNumber-1);
    });
});