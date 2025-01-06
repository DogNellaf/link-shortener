var selectedUrl = "";
var lastButton = null;

function showShareFrame(button, shortUrl) {
    if (lastButton != button) {
        selectedUrl = shortUrl;
        telegram_url.href = "https://t.me/share/url?url=" + shortUrl + "&text=Делюсь с вами сокращенной ссылкой через сервис link.example.com";
        whatsapp_url.href = "https://api.whatsapp.com/send?text=Делюсь с вами сокращенной ссылкой " + shortUrl + " через сервис link.example.com";
        let coords = button.getBoundingClientRect();
        let bottom = coords.bottom - 80;
        let left = coords.left - 600;
        share_frame.setAttribute("style", "top: " + bottom + "px; position: absolute; left: " + left + "px;");
        share_frame.removeAttribute("hidden");
        lastButton = button;
    } else {
        share_frame.setAttribute("hidden", "hidden");
        lastButton = null;
    }
}

function showEditFrame(title, shortUrl) {
    url_to_edit.value = shortUrl;
    titleInput.value = title;
    changeEditActive();
    edit_frame.removeAttribute("hidden");
}

function copyUrl(shortUrl) {
    copyAlert.removeAttribute("hidden");
    navigator.clipboard.writeText(shortUrl);
    setTimeout(() => {
        copyAlertFrame.setAttribute("hidden", "hidden");
    }, 3000);
}

function showDeleteFrame(shortUrl) {
    url_to_delete.value = shortUrl;
    delete_frame.removeAttribute("hidden");
}

document.querySelector('.search input').addEventListener('input', function () {
    const searchText = this.value.toLowerCase();
    const listItems = document.querySelectorAll('.list .list-item');

    listItems.forEach(item => {
        const titleText = item.querySelector('.title p').textContent.toLowerCase();
        if (titleText.includes(searchText)) {
            item.style.display = 'block';
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