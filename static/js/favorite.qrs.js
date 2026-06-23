function showDeleteFrame(shortUrl) {
    urlToDelete.value = shortUrl;
    deleteFrame.removeAttribute("hidden");
}

function showQrFrame(url, logoPath, qrColor, backgroundColor, isWithBackground) {
    if (logoPath == "/media/") {
        logoPath = "";
    }
    drawQR(qrImage, url, logoPath, qrColor, backgroundColor, isWithBackground)
    showQr.removeAttribute("hidden");
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