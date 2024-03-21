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
            $('#search-query-parameter').attr("value", ui.item.value);
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
            $.ajax({
                url: '/gamefolio/get-game/?id='+ui.item.id,
                success: function(data) {
                    $("#list-search-bar").val("");
                    if(!$("#" + ui.item.id).length) {
                        $("#list-games").append(data);
                    } else {
                        alert("Game already exists in list.")
                    }
                    return false;
                }
            })
        },
        minLength: 0
    })
    $("#list-games").on('click', "#list-entry", function() {
        $(this).remove()
    })
})
