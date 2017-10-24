$(function() {
    $(document).ready(function() {

        var elem = document.getElementById("myBar");
        var width = 2;
        var id = setInterval(frame, 240);
        $("#myProgress2").show();

        function frame() {
            if (width >= 100) {
                clearInterval(id);
                window.location.href = "/secondround/scores";
            } else {
                width++;
                elem.style.width = width + '%';
                document.getElementById("label").innerHTML = width * 1 + '%';
            }
        }
    });

  });
