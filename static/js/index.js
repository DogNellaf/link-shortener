
crossButton.addEventListener("click", function () {
    urlInputField.value = "";
    submitButton.classList.remove("active");
    submitButton.classList.remove("sky-hovered");
});

urlInputField.addEventListener("input", function () {
    if (urlInputField.value == "") {
        submitButton.classList.remove("active");
        submitButton.classList.remove("sky-hovered");
    }
    else
    {
        submitButton.classList.add("active");
        submitButton.classList.add("sky-hovered");
    }
});