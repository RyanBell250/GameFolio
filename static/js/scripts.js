$(document).ready(function() {

    const searchParams = new URLSearchParams(window.location.search);

    $('#search-button').click(function(e) {
        var queryTerm = $('#search-bar').val();
        $('#search-query-parameter').attr("value", queryTerm);
        if($('#page-form').length) {
            $('#page-form').trigger("submit");
            e.preventDefault();
        }
    });
    $('#reset-button').click(function(e) {
        $('#search-bar').val("");
        if($('#page-form').length) {
            $('#page-form').trigger("submit");
        }
    });
    
    //Tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
});