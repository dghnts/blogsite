function submitFile(file) {
    const form = document.querySelector("#icon_form");
    form.submit();
}

window.addEventListener("load", () => {
    const userIcon = document.querySelector("#icon");
    //console.log(userIcon);
    const updateIcon = () => {
        const uploadFile = userIcon.files[0];
        submitFile(uploadFile);
    };
    userIcon.addEventListener("change", updateIcon);
});
