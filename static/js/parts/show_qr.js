function showQR(url, logo_path, qr_color, background_color, is_with_background) {
    drawQR(qrImageFrame, url, logo_path, qr_color, background_color, is_with_background)
    showQrFrame.removeAttribute("hidden");
}