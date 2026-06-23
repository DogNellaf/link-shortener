
downloadSvgButton.addEventListener('click', async function() {
    let svg = qrImage.getElementsByTagName('svg')[0];
    svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");

    const images = svg.querySelectorAll('image');
    for (let image of images) {
        const href = image.getAttribute('href') || image.getAttribute('xlink:href');
        if (href && !href.startsWith('data:')) {
            try {
                const response = await fetch(href);
                const blob = await response.blob();
                const reader = new FileReader();
                reader.onload = function () {
                    image.setAttribute('href', reader.result);
                };
                reader.readAsDataURL(blob);
            } catch (error) {
                console.error('Ошибка при инлайнинге изображения:', error);
            }
        }
    }

    setTimeout(() => {
        let blob = new Blob([svg.outerHTML], { type: 'image/svg+xml' });
        let url = URL.createObjectURL(blob);
        
        let a = document.createElement('a');
        a.href = url;
        a.download = 'qr.svg';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        downloadQr.setAttribute("hidden", "hidden");
    }, 100);
});

downloadPngButton.addEventListener('click', async function() {
    let svg = qrImage.getElementsByTagName('svg')[0];

    const images = svg.querySelectorAll('image');
    for (let image of images) {
        const href = image.getAttribute('href') || image.getAttribute('xlink:href');
        if (href && !href.startsWith('data:')) {
            try {
                const response = await fetch(href);
                const blob = await response.blob();
                const reader = new FileReader();
                await new Promise((resolve, reject) => {
                    reader.onload = function () {
                        image.setAttribute('href', reader.result);
                        resolve();
                    };
                    reader.onerror = reject;
                    reader.readAsDataURL(blob);
                });
            } catch (error) {
                console.error('Ошибка при инлайнинге изображения:', error);
            }
        }
    }

    const svgData = new XMLSerializer().serializeToString(svg);
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();

    img.onload = function () {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);
        const pngData = canvas.toDataURL('image/png');
        
        let a = document.createElement('a');
        a.href = pngData;
        a.download = 'qr.png';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    };

    img.onerror = function (error) {
        console.error('Ошибка загрузки изображения:', error);
    };

    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
    downloadQr.setAttribute("hidden", "hidden");
});

function showDownloadWithParams(url, logoPath, qrColor, backgroundColor, isWithBackground) {
    drawQR(qrImage, url, logoPath, qrColor, backgroundColor, isWithBackground)
    downloadQr.removeAttribute("hidden");
}

function showDownload() {
    downloadQr.removeAttribute("hidden");
}