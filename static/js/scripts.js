$(window).bind("pageshow", function () {
    $("#page-parameter").remove();
    $("#query-parameter").remove();
    $("#sort-parameter").remove();
    $("#genre-parameter").remove();
    
    if(!$("#searched").length) {
        $('#search-bar').val("")
    }
})

$(document).ready(function() {

    $('#search-button').click(function(e) {
        var queryTerm = $('#search-bar').val()
        $('#search-query-parameter').attr("value", queryTerm)
    });

    $("#page-form").on("submit", function(e) {
        var pageSearch = $("#page-search");
        var number = pageSearch.val();
        if(number != "") {
            pageNumber = number;
        }
        
        if(pageNumber > 1 && !$("#page-parameter").length) {
            $('<input>').attr({
                type: 'hidden',
                value: pageNumber-1,
                name: "page",
                id: "page-parameter"
            }).appendTo($pageForm);
        }

        if(currentSort != "relevance" && !$("#sort-parameter").length) {
            $('<input>').attr({
                type: 'hidden',
                value: currentSort,
                name: "sort",
                id: "sort-parameter"
            }).appendTo($pageForm);
        }
        
        if(!$("#query-parameter").length) {
            $('<input>').attr({
                type: 'hidden',
                value: $('#search-bar').val(),
                name: "query",
                id: "query-parameter"
            }).appendTo($pageForm);
        }
    })

    var $pageButtons = jQuery('.page-link')
    $pageButtons.click(function(e) {
        var pageNumber = $(this).val();
        var currentSort= "relevance";
        $pageForm = $("#page-form");
        if(pageNumber > 1 && !$("#page-parameter").length) {
            $('<input>').attr({
                type: 'hidden',
                value: pageNumber-1,
                name: "page",
                id: "page-parameter"
            }).appendTo($pageForm);
        }

        if(currentSort != "relevance" && !$("#sort-parameter").length) {
            $('<input>').attr({
                type: 'hidden',
                value: currentSort,
                name: "sort",
                id: "sort-parameter"
            }).appendTo($pageForm);
        }
        
        if(!$("#query-parameter").length) {
            $('<input>').attr({
                type: 'hidden',
                value: $('#search-bar').val(),
                name: "query",
                id: "query-parameter"
            }).appendTo($pageForm);
        }

    });

    var $genreButtons = jQuery('.genre-button')
    $genreButtons.click(function(e) {
        if(e.screenX == 0) {
            return;
        }
        $pageForm = $("#page-form");
        if($("#genre-parameter").length) {
            return;
        }
        $('<input>').attr({
            type: 'hidden',
            value: $(this).val(),
            name: "genre",
            id: "genre-parameter"
        }).appendTo($pageForm);
    })
    
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
});