def get_nationalId(file):
    # import libraries
    import cv2
    import numpy as np
    from pytesseract import pytesseract
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.environ['TESSDATA_PREFIX'] = r'/app/models'

    # Pre-Processing Image
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    resized_img = cv2.resize(img, (712, 512), interpolation=cv2.INTER_AREA)
    cropped_img = resized_img[resized_img.shape[0]*-7//24:resized_img.shape[0]*-1//10, resized_img.shape[1]*3//-5:]
    gray_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    remove_bg_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 16)

    obj = pytesseract.image_to_string(remove_bg_img, lang='ara_number', config='--psm 7')
    nationalId = obj.replace(' ', '')[:14]

    return nationalId


# testing post request with commends 
# curl -X POST -F "file=@\"D:\WORK Space\GRADAUTION PROJECT\Extracting User Info From National ID\dataset\0.JPG\"" http://localhost:5000/extract_nationalId
