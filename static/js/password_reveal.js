function reveal_register() {
    if (document.getElementById('box_register').checked) {
        document.getElementById("id_password1").type = 'text';
        document.getElementById("id_password2").type = 'text';
    } else
        document.getElementById("id_password1").type = 'password';
    document.getElementById("id_password2").type = 'password';
}

// Depricated in favour of input type="checkbox"
function reveal_login() {
    if (document.getElementById('box_login').checked) {
        document.getElementById("id_password").type = 'text';
    } else
        document.getElementById("id_password").type = 'password';
}

// This will not work with Django register form
const old_item = document.getElementById("id_password");
const new_item = document.createElement('div');
new_item.innerHTML = '<input type="password" name="password" class="form-control" placeholder="Password" title="" required="" id="id_password"><span toggle="#id_password" class="fa fa-fw fa-eye field-icon toggle-password"></span>';
if (old_item) {
    old_item.parentNode.replaceChild(new_item, old_item);
}

$(".toggle-password").click(function () {
    $(this).toggleClass("fa-eye fa-eye-slash");
    let input = $($(this).attr("toggle"));
    if (input.attr("type") === "password") {
        input.attr("type", "text");
    } else {
        input.attr("type", "password");
    }
});
