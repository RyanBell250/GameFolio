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

    const searchParams = new URLSearchParams(window.location.search);

    $('#search-button').click(function(e) {
        var queryTerm = $('#search-bar').val()
        $('#search-query-parameter').attr("value", queryTerm)
    });

    $("#page-form").on("submit", function(e) {

        var pageSearch = $("#page-search");
        var number = pageSearch.val();
        var pageNumber = 0;
        if(number != null) {
            alert(number)
            $("#sort-parameter").remove();
            pageNumber = number;
        }

        var currentSort = "0"
        if(searchParams.has("sort")) {
            currentSort = searchParams.get("sort");
        }
        
        if(pageNumber > 1 && !$("#page-parameter").length) {
            $('<input>').attr({
                type: 'hidden',
                value: pageNumber-1,
                name: "page",
                id: "page-parameter"
            }).appendTo($pageForm);
        }
        
        if(currentSort != "0" && !$("#sort-parameter").length) {
            $('<input>').attr({
                type: 'hidden',
                value: currentSort,
                name: "sort",
                id: "sort-parameter"
            }).appendTo($pageForm);
        }
        
        var query = ""
        if(searchParams.has("query")) {
            query = searchParams.get("query");
        }

        if(!$("#query-parameter").length && query != "") {
            $('<input>').attr({
                type: 'hidden',
                value: query,
                name: "query",
                id: "query-parameter"
            }).appendTo($pageForm);
        }

        if(searchParams.has('genre') &&  !$("#genre-parameter").length) {
            $('<input>').attr({
                type: 'hidden',
                value: searchParams.get('genre'),
                name: "genre",
                id: "genre-parameter"
            }).appendTo($pageForm);
        }

    })

    var $pageButtons = jQuery('.page-link')
    $pageButtons.click(function(e) {
        var pageNumber = $(this).val();

        $pageForm = $("#page-form");
        if(pageNumber > 1 && !$("#page-parameter").length) {
            $('<input>').attr({
                type: 'hidden',
                value: pageNumber-1,
                name: "page",
                id: "page-parameter"
            }).appendTo($pageForm);
        }

    });

    var $genreButtons = jQuery('.genre-button')
    $genreButtons.click(function(e) {
        $pageForm = $("#page-form");
        $("#genre-parameter").remove();
        $('<input>').attr({
            type: 'hidden',
            value: $(this).val(),
            name: "genre",
            id: "genre-parameter"
        }).appendTo($pageForm);
    })

    var $sortButtons = jQuery('.sort-option')
    $sortButtons.click(function (e) {  
        var currentSort = $(this).val();
        $pageForm = $("#page-form");

        $("#page-parameter").remove();
        $("#query-parameter").remove();
        $("#sort-parameter").remove();
        $("#genre-parameter").remove();
            
        if(currentSort != "0") {
            $('<input>').attr({
                type: 'hidden',
                value: currentSort,
                name: "sort",
                id: "sort-parameter"
            }).appendTo($pageForm);
        } else {
            $('<div>').attr({
                id: "sort-parameter"
            }).appendTo($pageForm);
        }
        
        if(searchParams.has('query')) {
            $('<input>').attr({
                type: 'hidden',
                value: searchParams.get('query'),
                name: "query",
                id: "query-parameter"
            }).appendTo($pageForm);
        }
        if(searchParams.has('genre')) {
            $('<input>').attr({
                type: 'hidden',
                value: searchParams.get('genre'),
                name: "genre",
                id: "genre-parameter"
            }).appendTo($pageForm);
        }
    })
    
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
});