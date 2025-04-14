function validate_form() {
    let file_input = document.querySelector('input[name="image"]');
    let file_path = file_input.value;
    let allowed_extensions = /\.(jpg|jpeg|png|gif)$/i;

    if (!allowed_extensions.exec(file_path)) {
        alert("Please upload a valid image file.");
        file_input.value = "";
        return false;
    }

    return true;
}

addEventListener("DOMContentLoaded", () => {
    let form = document.querySelector("form");

    form.addEventListener("submit", event => {
        let inputs = document.querySelectorAll("input, textarea");

        for (let input of inputs) {
            if (input.value.trim() === "") {
                alert("All fields must be filled out.");
                event.preventDefault();
                return;
            }
        }


        if (!validate_form()) {
            event.preventDefault();
        }
    });
});


//this is the form validation in Javascript to properly validate uploading new item info.
// fields to fill are: item name, description, usage notes, and an image upload.

// This JavaScript checks for empty fields and valid image file extensions (png, jpg, etc.)