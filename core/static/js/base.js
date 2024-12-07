const qrSizeInPixels = (window.innerWidth * 12.5) / 100;
const logoSizeInPixels = (window.innerWidth * 3) / 100;
let lastUrl = "";
let lastLogoPath = "";
let lastQrColor = "";
let lastBackgroundColor = "";
let isWithBackground = false;

function drawQR(canvas, url, logo_path, qr_color, background_color) {
    lastUrl = url;
    lastLogoPath = logo_path;
    lastQrColor = qr_color;
    lastBackgroundColor = background_color;

    const uniqueIdSuffix = `-${Date.now()}`;

    var qr = new QRCodeStyling({
        type: "svg",
        shape: "square",
        width: qrSizeInPixels,
        height: qrSizeInPixels,
        data: lastUrl,
        image: lastLogoPath,
        qrOptions: {
            typeNumber: "3",
            mode: "Byte",
            errorCorrectionLevel: "Q"
        },
        imageOptions: {
            saveAsBlob: true,
            hideBackgroundDots: true,
            imageSize: 0.7,
            margin: 5
        },
        dotsOptions: {
            type: "extra-rounded",
            color: lastQrColor,
            roundSize: true,
            gradient: null
        },
        backgroundOptions: {
            color: isWithBackground? lastBackgroundColor : "transparent"
        },
        cornersSquareOptions: {
            type: "extra-rounded",
            color: lastQrColor,
            gradient: null
        },
        svgOptions: {
            id: `qr-svg${uniqueIdSuffix}`,
        }
    });

    canvas.innerHTML = "";
    qr.append(canvas);
}

function changeUrl(url) {
    drawQR(
        url,
        lastLogoPath,
        lastQrColor,
        lastBackgroundColor
    )
}

function changeQrColor(color) {
    drawQR(
        qrEditorCanvas,
        lastUrl,
        lastLogoPath,
        color,
        lastBackgroundColor
    )
}

function changeBackgroundColor(color) {
    drawQR(
        qrEditorCanvas,
        lastUrl,
        lastLogoPath,
        lastQrColor,
        color
    )
}


function changeLogoPath(path) {
    drawQR(
        qrEditorCanvas,
        lastUrl,
        path,
        lastQrColor,
        lastBackgroundColor
    )
}

function changeBackgroundDraw() {
    isWithBackground = !isWithBackground;
    drawQR(
        qrEditorCanvas,
        lastUrl,
        lastLogoPath,
        lastQrColor,
        lastBackgroundColor
    )
}

qrColorPickerFrame.addEventListener('click',
    _ => qrColor.click()
);

qrColor.addEventListener('input', 
    _ => {
        let value = qrColor.value;
        qrColorLabel.innerHTML = value;
        changeQrColor(value);
    }
);

backgroundDrawToogle.addEventListener('input', 
    _ => changeBackgroundDraw()
);

backgroundColorPickerFrame.addEventListener('click', 
    _ => backgroundColor.click()
);

backgroundColor.addEventListener('input', 
    _ => {
        let value = backgroundColor.value;
        backgroundColorLabel.innerHTML = value;
        changeBackgroundColor(value);
    }
);

fileUploadButton.addEventListener('click', 
    _ => logo.click()
);

logo.addEventListener('change', (e) => {
    var selectedFile = e.target.files[0];
    if (selectedFile != null) {
        var reader = new FileReader();
  
        reader.onload = function(e) {
            changeLogoPath(e.target.result);
        };
      
        reader.readAsDataURL(selectedFile);
    }
});


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
    // downloadQrImage.innerHTML = document.getElementById(shortUrl + "-qr").innerHTML;
    downloadQrBlock.removeAttribute("hidden");
}

function showQR(shortUrl) {
    // qrImageFrame.innerHTML = document.getElementById(shortUrl + "-qr").innerHTML;
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
    downloadQrImage.innerHTML = "";
    qrEditorCanvas.innerHTML = "";
    frame.setAttribute("hidden", "hidden");
}