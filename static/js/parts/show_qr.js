function showQR(url, logoPath, qrColor, backgroundColor, isWithBackground) {
    drawQR(qrImage, url, logoPath, qrColor, backgroundColor, isWithBackground)
    showQr.removeAttribute("hidden");
}