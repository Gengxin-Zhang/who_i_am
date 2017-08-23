$(document).ready(function() {
    $(".button-collapse").sideNav();
    $(".dropdown-button").dropdown();
    $('.modal').modal();
    $('input#input_text, textarea#textarea1').characterCounter();
    $('#makeit').click(function() {
        var one = $("#whoiam").val();
        var two = $("#name").val();
        var three = $("#whatwewant").val();
        var four = $("#idontknow").val();
        var five = $("#when").val();
        var six = $("#now").val();
        $.get("/makeit", {
            'whoiam': one,
            'name': two,
            'whatwewant': three,
            'idontknow': four,
            'when': five,
            'now': six,
        }, function(rec) {
            if (rec == "None") {
                $('#modal1').modal('open');
            } else {
                var img = "data:image/png;base64," + rec;
                $("#result").attr("src", img)
            }
        })
    })
})