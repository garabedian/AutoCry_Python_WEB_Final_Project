// Script changing immediately the old with new photo
const x = document.getElementById("id_image_type").children;
for (let el = 0; el < x.length; ++el) {
    x[el].removeAttribute('selected');
}
document.getElementById('image_url_input').hidden = true;
document.getElementById('img_url_input').value = '';
document.getElementById('image_file_input').hidden = true;
document.getElementById('img_file_input').value = '';
// document.getElementById('btn_create').hidden = true;

function updateImage() {
    let img = document.getElementById('web_img_preview');
    let url = this.value;
    if (getSelectedType() === 'web_image') img.src = url;
}

function getSelectedType() {
// Script getting selected value from dropdown
    let el = document.getElementById('id_image_type');
    let input_type = el.options[el.selectedIndex].value;
    console.log(input_type);
    document.getElementById('image_url_input').hidden = true;
    document.getElementById('image_file_input').hidden = true;
    // document.getElementById('btn_create').hidden = true;
    if (input_type === 'web_image') {
        document.getElementById('image_file_input').hidden = true;
        document.getElementById('image_url_input').hidden = false;
        document.getElementById('img_url_input').addEventListener('input', updateImage);
        // document.getElementById('btn_create').hidden = false;
    } else if (input_type === 'local_image') {
        document.getElementById('image_url_input').hidden = true;
        document.getElementById('image_file_input').hidden = false;
        document.getElementById('img_file_input').addEventListener('input', updateImage);
        // document.getElementById('btn_create').hidden = false;
    }
    return input_type;
}

document.getElementById('id_image_type').addEventListener('input', getSelectedType);


