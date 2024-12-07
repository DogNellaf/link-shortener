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
    qrEditorCanvas.innerHTML = "";
    frame.setAttribute("hidden", "hidden");
}