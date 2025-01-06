function showQR(url, logo_path, qr_color, background_color, is_with_background) {
    drawQR(qrImage, url, logo_path, qr_color, background_color, is_with_background)
    showQr.removeAttribute("hidden");
}