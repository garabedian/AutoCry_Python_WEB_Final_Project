function reveal_photo_change() {
    if (document.getElementById('box_photo_change').checked) {
        document.getElementById("photo_change").hidden = false;
    } else
        document.getElementById("photo_change").hidden = true;
}
