downloadSvgButton.addEventListener('click', function() {
    let svg = downloadQrImage.getElementsByClassName('segno')[0];
    svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    svg.setAttribute("width", "256");
    svg.setAttribute("height", "256");
    let blob = new Blob([svg.outerHTML], { type: 'image/svg+xml' });
    let url = URL.createObjectURL(blob);
    
    let a = document.createElement('a');
    a.href = url;
    a.download = 'qr.svg';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    downloadQrBlock.setAttribute("hidden", "hidden");
});

downloadPngButton.addEventListener('click', function() {
    let svg = downloadQrImage.getElementsByClassName('segno')[0];
    let svgData = new XMLSerializer().serializeToString(svg);
    let canvas = document.createElement('canvas');
    let ctx = canvas.getContext('2d');
    let img = new Image();

    img.onload = function() {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);
        let pngData = canvas.toDataURL('image/png');
        
        let a = document.createElement('a');
        a.href = pngData;
        a.download = 'qr.png';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    };

    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
    downloadQrBlock.setAttribute("hidden", "hidden");
});

function showDownload(shortUrl) {
    downloadQrImage.innerHTML = document.getElementById(shortUrl + "-qr").innerHTML;
    downloadQrBlock.removeAttribute("hidden");
}

function showQR(shortUrl) {
    qrImageFrame.innerHTML = document.getElementById(shortUrl + "-qr").innerHTML;
    showQrFrame.removeAttribute("hidden");
}

isColorFrameVisible = false;

function changeVisible() {
    if (isColorFrameVisible) {
        changeBackgroundFrame.setAttribute("hidden", "hidden");
    } else {
        changeBackgroundFrame.removeAttribute("hidden");
    }
    isColorFrameVisible = !isColorFrameVisible;
};

let colorsToButtons = new Map([
    ["default", defaultColorButton],
    ["yellow", yellowColorButton],
    ["red", redColorButton],
    ["blue", blueColorButton]
]);

function setColor(className) {
    localStorage.color = className;
    document.body.className = "";
    if (className != "default") {
        document.body.className = className;
    }

    for (let button of colorsToButtons.values()) {
        button.className = '';
    }

    let button = colorsToButtons.get(className);
    button.className = 'active-color';
}

if (!localStorage.color) {
    setColor("default");
} else {
    setColor(localStorage.color);
}

function closeFrame(frame) {
    frame.setAttribute("hidden", "hidden");
}