function readURL(input) {
    if (input.files && input.files[0]) {
        let reader = new FileReader();
        reader.onload = function (e) {
            console.log(e.target.result)
            document.getElementById('local_img_preview').src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}


