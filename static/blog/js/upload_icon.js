function submitFile(file) {
    const form = document.querySelector("#icon_form");
    form.submit();

    const reader = new FileReader();
    console.log(form);
    reader.onload = function (e) {
        console.log("OK");
    };
}

window.addEventListener("load", () => {
    const userIcon = document.querySelector("#icon");
    console.log(userIcon);
    const updateIcon = () => {
        const uploadFile = userIcon.files[0];
        submitFile(uploadFile);
    };
    userIcon.addEventListener("change", updateIcon);
});
