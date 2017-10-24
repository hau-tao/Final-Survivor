$(function() {


    $(".sortable").sortable({
        disabled: true
    });

   /* var time_to_complete = 180000;
    var roundCountdown = new Tock({
        countdown: true,
        start_time: time_to_complete,
        on_tick: function() {
            $("#time-notification-area").text(roundCountdown.lap('Time left: {mm}:{ss}'));
        },
        on_complete: function() {
            $("#time-notification-area").text("Time is up! Gathering submissions...");
            $("#loading-bar").html('<img src="/static/img/loading-bar.gif">');
            // submit serialized list
            setTimeout(function() {
                window.location.href = "/firstround/reminder"
            }, 3000);
        }
    });*/

    $("#start").click(function() {
        $(this).addClass("disabled");
        $(".sortable").sortable({
            disabled: false,
            axis: "y",
            containment: "#equipment",
            update: function(event, ui) {
                var order = $(this).sortable('toArray');
                $.ajax({
                    type: 'GET',
                    url: '/api/first_round_task/' + order
                });
            }
        });
        //roundCountdown.start();
        $('#game-started').css('display', '');
    });
    $("#finish").click(function(){ window.location.href = "/firstround/reminder"});


});
