import cv2


def read_qr_code(filename: str) -> str | None:
    try:
        img = cv2.imread(filename)
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        if points is None:
            return None
        codes_receipt = ['fn=', 'i=', 'fp=']
        if all(tech_codes in value for tech_codes in codes_receipt):
            return value
        return None
    except cv2.error:
        return None
