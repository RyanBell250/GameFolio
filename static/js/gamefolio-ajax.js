$(document).ready(function() {
    
    $("#search-bar").autocomplete({
        source: function(request, response) {
            var query;
            query = $("#search-bar").val();
            $.ajax({
                url: '/gamefolio/suggest/?suggestion='+query,
                success: function(data) {
                    response(JSON.parse(data)["games"])
                }
            });
        },
        select: function(event, ui) {
            $('#search-query-parameter').attr("value", ui.item.label);
            $("#search-form").submit();
        },
        minLength: 0
    })
    $("#list-search-bar").autocomplete({
        source: function(request, response) {
            var query;
            query = $("#list-search-bar").val();
            $.ajax({
                url: '/gamefolio/suggest/?suggestion='+query,
                success: function(data) {
                    response(JSON.parse(data)["games"])
                }
            });
        },
        select: function(event, ui) {
            var query;
            query = $("#list-search-bar").val();
            $.ajax({
                url: '/gamefolio/get-game/?id='+ui.item.value,
                success: function(data) {
                    $("#list-games").append(data);
                    $("#list-search-bar").val("");
                    return false;
                    return data;
                }
            })
        },
        minLength: 0
    })
    $("#list-games").on('click', "#list-entry", function() {
        $(this).remove()
    })
})
