function comments() {
    document.getElementById('id_comment').value =
        `@${document.getElementById('refer_to').innerText}:\n`.replaceAll('\"', '');
}

function toggle_comment() {
    const div = document.querySelector("#extra");
    const btn = document.getElementById("more_less_btn");

    if (div.style.display === "block") {
        // The element is visualized and becomes NOT visualized
        div.style.display = "none";
        // Change button name
        btn.textContent = "Show comments";
        sessionStorage.setItem('comment', 'hidden');
    } else {
        // The element is NOT visualized and becomes visualized
        div.style.display = "block";
        // Change button name
        btn.textContent = "Hide comments";
        sessionStorage.setItem('comment', 'visible');
    }
}