// Script changing immediately the old with new photo
document.getElementById('image_url_input').hidden = true;
document.getElementById('img_url_input').value = '';
document.getElementById('image_file_input').hidden = true;
document.getElementById('img_file_input').value = '';
document.getElementById('btn_create').hidden = true;

function updateImage() {
    let img = document.getElementById('web_img_preview');
    let url = this.value;
    if (getSelectedType() === 'web_image') img.src = url;
}

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

// Script getting selected value from dropdown
function getSelectedType() {
    let el = document.getElementById('id_image_type');
    let input_type = el.options[el.selectedIndex].value;
    console.log(input_type);
    if (input_type === 'web_image') {
        document.getElementById('image_file_input').hidden = true;
        document.getElementById('image_url_input').hidden = false;
        document.getElementById('img_url_input').addEventListener('input', updateImage);
    } else if (input_type === 'local_image') {
        document.getElementById('image_url_input').hidden = true;
        document.getElementById('image_file_input').hidden = false;
        document.getElementById('img_file_input').addEventListener('input', updateImage);
    } else if (input_type === 'no_image') {
        document.getElementById('image_url_input').hidden = true;
        document.getElementById('image_file_input').hidden = true;
    }
    document.getElementById('btn_create').hidden = false;
    return input_type;
}

document.getElementById('id_image_type').addEventListener('input', getSelectedType);


