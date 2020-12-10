window.onunload = function () {
    document.getElementById('background_audio').pause();
}

window.onload = function () {
    sessionStorage.setItem('on_hold', 'yes');
    let old_time = sessionStorage.getItem('current_time')
    !old_time ? old_time = 0 : null;
    sessionStorage.setItem('old_time', old_time);
}

function toggle_play() {
    let on_hold;
    const song = document.getElementById('background_audio');
    const start_time = sessionStorage.getItem('old_time');
    console.log(song.currentTime);
    sessionStorage.getItem('on_hold') === 'yes' ? on_hold = 'no' : on_hold = 'yes';
    if (on_hold === 'yes') {
        song.pause();
    } else {
        // This works perfect in Firefox but not in Chrome (it is a reported bug)
        song.currentTime = start_time;
        song.play();
        // Found this explanation:
        // To be able to playback audio/video from a specific time using the HTML5 tag
        // your web server should be capable of serving the document using byte ranges.
        // The Google Chrome web browser want this to work. If this is not worked out,
        // then the seeking will be disabled and even if you set the currentTime, it will not work.
        // Test your web server, if it allows this ==>  "curl --dump-header - -r0-0 http://theurl"
    }
    sessionStorage.setItem('on_hold', on_hold);
}

function update_time() {
    sessionStorage.setItem('current_time', document.getElementById('background_audio').currentTime);
    sessionStorage.setItem('old_time', document.getElementById('background_audio').currentTime);
}
