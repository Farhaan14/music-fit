window.onload = function(){
    setPage(0)
}

function setPage(index) {
    var page = "tab-" + index;
    var songCont = "song-cont-" + index;
    document.getElementById("tab-0").style.color = "#fafafa";
    document.getElementById("tab-1").style.color = "#fafafa";
    document.getElementById("tab-2").style.color = "#fafafa";
    document.getElementById(page).style.color = "#1DB954";

    document.getElementById("song-cont-0").style.display = "none";
    document.getElementById("song-cont-1").style.display = "none";
    document.getElementById("song-cont-2").style.display = "none";
    document.getElementById(songCont).style.display = "grid";
}

// function onYouTubeIframeAPIReady() {
//     player = new YT.Player('player', {
//         height: '360',
//         width: '640',
//         videoId: "s6HzzIcGe1U",
//         events: {
//             'onReady': onPlayerReady,
//             'onStateChange': onPlayerStateChange
//         }
//     });
// }

function getSong(e) {
    var songName = e.getElementsByClassName("song-name")[0].innerHTML;
    dict = {songName}
    s = JSON.stringify(dict)
    $.ajax({
        url: "/song",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(s),
        success: function(res) {
            
            // var p = document.getElementById("player")
            // p.src = `https://www.youtube.com/embed/${res}?enablejsapi=1&origin=http%3A%2F%2F127.0.0.1%3A5500&widgetid=1`
            // p.contentWindow.location.reload(true);

            var element =  document.getElementById('player');
            if (typeof(element) != 'undefined' && element != null)
            {
                element.remove();
                var div = document.createElement('div')
                div.id = "player"
                document.getElementById("audio-player-cont").insertBefore(div, document.getElementById("audio-player-cont").firstChild);

                player = new YT.Player('player', {
                    height: '360',
                    width: '640',
                    videoId: res,
                    events: {
                        'onReady': onPlayerReady,
                        'onStateChange': onPlayerStateChange
                    }
                });
            }
 
            swal({
                title: "Song Loaded!",
                icon: "success",
            });
        }
    })
}

  