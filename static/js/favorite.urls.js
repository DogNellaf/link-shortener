var selectedUrl = "";
var lastButton = null;

function showShareFrame(button, shortUrl) {
    if (lastButton != button) {
        selectedUrl = shortUrl;
        telegramUrl.href = "https://t.me/share/url?url=" + shortUrl + "&text=Делюсь с вами сокращенной ссылкой через сервис link.example.com";
        whatsappUrl.href = "https://api.whatsapp.com/send?text=Делюсь с вами сокращенной ссылкой " + shortUrl + " через сервис link.example.com";
        let coords = button.getBoundingClientRect();
        let bottom = coords.bottom + 20;
        let left = coords.left - 100;
        share.setAttribute("style", "top: " + bottom + "px; position: absolute; left: " + left + "px;");
        share.removeAttribute("hidden");
        lastButton = button;
    } else {
        share.setAttribute("hidden", "hidden");
        lastButton = null;
    }
}

function showEditFrame(title, shortUrl) {
    urlToEdit.value = shortUrl;
    titleInput.value = title;
    changeEditActive();
    edit.removeAttribute("hidden");
}

function copyUrl(shortUrl) {
    copyAlert.removeAttribute("hidden");
    copyTextFallback(shortUrl);
    setTimeout(() => {
        copyAlert.setAttribute("hidden", "hidden");
    }, 3000);
}

function showDeleteFrame(shortUrl) {
    urlToDelete.value = shortUrl;
    deleteFrame.removeAttribute("hidden");
}

document.querySelector('.search input').addEventListener('input', function () {
    const searchText = this.value.toLowerCase();
    const listItems = document.querySelectorAll('.list .list-item');

    listItems.forEach(item => {
        const titleText = item.querySelector('.title p').textContent.toLowerCase();
        if (titleText.includes(searchText)) {
            item.removeAttribute("style");
        } else {
            item.style.display = 'none';
        }
    });
});

function changeEditActive() {
    alert(titleInput.value);
    if (titleInput.value.trim() !== "") {
        editSubmitButton.classList.add("active");
    } else {
        editSubmitButton.classList.remove("active");
    }
};