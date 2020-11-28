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
    const start_time = Number(sessionStorage.getItem('old_time'));
    console.log(song.currentTime);
    sessionStorage.getItem('on_hold') === 'yes' ? on_hold = 'no' : on_hold = 'yes';
    if (on_hold === 'yes') {
        song.pause();
    } else {
        song.currentTime = start_time;
        song.play();
    }
    sessionStorage.setItem('on_hold', on_hold);
}

function update_time() {
    sessionStorage.setItem('current_time', document.getElementById('background_audio').currentTime);
}
