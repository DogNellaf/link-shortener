function changeUrl(url) {
    drawQR(
        url,
        lastLogoPath,
        lastQrColor,
        lastBackgroundColor,
        isWithBackground
    )
}

function changeQrColor(color) {
    drawQR(
        qrEditorCanvas,
        lastUrl,
        lastLogoPath,
        color,
        lastBackgroundColor,
        isWithBackground
    )
}

function changeBackgroundColor(color) {
    drawQR(
        qrEditorCanvas,
        lastUrl,
        lastLogoPath,
        lastQrColor,
        color,
        isWithBackground
    )
}


function changeLogoPath(path) {
    drawQR(
        qrEditorCanvas,
        lastUrl,
        path,
        lastQrColor,
        lastBackgroundColor,
        isWithBackground
    )
}

function changeBackgroundDraw() {
    isWithBackground = !isWithBackground;
    drawQR(
        qrEditorCanvas,
        lastUrl,
        lastLogoPath,
        lastQrColor,
        lastBackgroundColor,
        isWithBackground
    )
}

function setWithBackground(value) {
    isWithBackground = value;
}

qrColorPicker.addEventListener('click',
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

backgroundColorPicker.addEventListener('click', 
    _ => backgroundColor.click()
);

backgroundColor.addEventListener('input', 
    _ => {
        let value = backgroundColor.value;
        backgroundColorLabel.innerHTML = value;
        changeBackgroundColor(value);
    }
);

logo.addEventListener('change', (e) => {
    var selectedFile = e.target.files[0];
    if (selectedFile != null) {
        var reader = new FileReader();
  
        reader.onload = changeLogoPath(e.target.result); /* TODO: проверить работу */
        reader.readAsDataURL(selectedFile);
    }
});
