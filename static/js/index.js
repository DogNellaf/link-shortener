// Обработка нажатия на кнопку Удалить
crossButton.addEventListener("click", function () {
    urlInputField.value = "";
    submitButton.classList.remove("active");
    submitButton.classList.remove("sky-hovered");
});

// Обработка ввода
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