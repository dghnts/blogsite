window.addEventListener("load", () => {
    const switches = document.querySelectorAll(".form-switch");
    switches.forEach(function (form) {
        const check = form.querySelector(".form-check-input");
        console.log(form);
        check.addEventListener("change", () => {
            form.submit();
        });
    });
});
