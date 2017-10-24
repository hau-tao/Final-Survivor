$(function() {
  $("textarea").attr({
    disabled: true,
  });

  /* var five_minutes = 300000;
   var roundCountdown = new Tock({
    countdown: true,
    start_time: five_minutes,
    on_tick: function() {
        $("#time-notification-area").text(roundCountdown.lap('Time left: {mm}:{ss}'));
    },
    on_complete: function() {
        $("#time-notification-area").text("Time is up! Gathering submissions...");
        $("#loading-bar").html('<img src="/static/img/loading-bar.gif">');
        // submit text
        setTimeout(function() {
           window.location.href = "/secondround/reminder"
         }, 3000);
    }
  });*/

  $("#second_round").click(function() {
      $(this).addClass("disabled");
      $("textarea").attr({ disabled: false });
      roundCountdown.start();

  });
  $("#second_finish").click(function(){ window.location.href = "/secondround/reminder"});

});
