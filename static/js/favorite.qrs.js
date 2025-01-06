function showDeleteFrame(shortUrl) {
    urlToDelete.value = shortUrl;
    delete.removeAttribute("hidden");
}

document.querySelector('.search input').addEventListener('input', function () {
    const searchText = this.value.toLowerCase();
    const listItems = document.querySelectorAll('.list .list-item');

    listItems.forEach(item => {
        const titleText = item.querySelector('.title p').textContent.toLowerCase();
        if (titleText.includes(searchText)) {
            item.style.display = 'block'; // Показать элемент
        } else {
            item.style.display = 'none'; // Скрыть элемент
        }
    });
});