function add_reference() {
    document.getElementById('id_comment').value =
        `@${document.getElementById('refer_to').innerText}:\n`.replaceAll('\"', '');
}