let qrSizeInPixels = (window.innerWidth * 12.5) / 100;
let logoSizeInPixels = (window.innerWidth * 3) / 100;
let lastUrl = "";
let lastLogoPath = "";
let lastQrColor = "";
let lastBackgroundColor = "";
let isWithBackground = false;

function drawQR(canvas, url, logoPath, qrColor, backgroundColor, isWithBackground) {
    lastUrl = url;
    lastLogoPath = logoPath;
    lastQrColor = qrColor;
    lastBackgroundColor = backgroundColor;

    var qr = new QRCodeStyling({
        type: "svg",
        shape: "square",
        width: qrSizeInPixels,
        height: qrSizeInPixels,
        data: lastUrl,
        margin: 0,
        qrOptions: {
          typeNumber: 3,
          mode: "Byte",
          errorCorrectionLevel: "Q" 
        },
        imageOptions: {
          saveAsBlob: true,
          hideBackgroundDote: true,
          imageSize: 0.65,
          margin: 10
        },
        dotsOptions: {
          type: "dots",
          color: lastQrColor,
          roundSize: true,
          gradient: null
        },
        backgroundOptions: {
          round: 0,
          color: isWithBackground? lastBackgroundColor : "transparent"
        },
        image: lastLogoPath,
        dotsOptionsHelper: {
          colorType: {
            single: true,
            gradient: false
          },
          gradient: {
            linear: true,
            radial: false,
            color1: lastQrColor,
            color2: lastQrColor,
            rotation: 0 
          }
        },
        cornersSquareOptions: {
          type: "extra-rounded",
          color: lastQrColor,
          gradient: null
        },
        cornersSquareOptionsHelper: {
          colorType: {
            single: true,
            gradient: false
          },
          gradient: {
            linear: true,
            radial: false,
            color1: lastQrColor,
            color2: lastQrColor,
            rotation: 0 
          }
        },
        cornersDotOptions: {
          type: "dot",
          color: lastQrColor
        },
        cornersDotOptionsHelper: {
          colorType: {
            single: true,
            gradient: false
          },
          gradient: {
            linear: true,
            radial: false,
            color1: lastQrColor,
            color2: lastQrColor,
            rotation: 0 
          }
        },
        backgroundOptionsHelper: {
          colorType: {
            single: true,
            gradient: false
          },
          gradient: {
            linear: true,
            radial: false,
            color1: lastBackgroundColor,
            color2: lastBackgroundColor,
            rotation: 0 
          }
        }
    });

    canvas.innerHTML = "";
    qr.append(canvas);
}

isColorFrameVisible = false;

function changeVisible() {
    if (isColorFrameVisible) {
        changeBackground.setAttribute("hidden", "hidden");
    } else {
        changeBackground.removeAttribute("hidden");
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

function copyTextFallback(text) {
  const tempInput = document.createElement("textarea");
  tempInput.value = text; // Устанавливаем текст, который нужно скопировать
  tempInput.style.position = "absolute";
  tempInput.style.left = "-9999px"; // Прячем элемент за пределами видимости
  document.body.appendChild(tempInput);

  // Выделяем текст и выполняем команду копирования
  tempInput.select();
  try {
      document.execCommand("copy");
  } catch (err) {
      console.error("Не удалось скопировать текст: ", err);
  }

  // Удаляем временный элемент
  document.body.removeChild(tempInput);
}