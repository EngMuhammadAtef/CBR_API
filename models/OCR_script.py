def get_nationalId(file):
    # import libraries
    import cv2
    from pytesseract import pytesseract
    import numpy as np

    # Defining paths to tesseract.exe
    pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # Pre-Processing Image
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    resized_img = cv2.resize(img, (712, 512), interpolation=cv2.INTER_AREA)
    cropped_img = resized_img[resized_img.shape[0]*-7//24:resized_img.shape[0]*-1//10, resized_img.shape[1]*3//-5:]
    gray_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    remove_bg_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 16)

    # Convert image to text
    obj = pytesseract.image_to_string(remove_bg_img, lang='ara_number', config='--psm 7')
    nationalId = ''.join(c for c in obj if c.isdigit())[:14]

    return nationalId

# testing post request with commend
# curl -X POST -F "file=@\"D:\WORK Space\GRADAUTION PROJECT\Extracting User Info From National ID\dataset\0.JPG\"" http://localhost:5000/extract_nationalId