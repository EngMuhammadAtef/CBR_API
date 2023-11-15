def get_nationalId(file):
    # import libraries
    import cv2
    import easyocr
    import numpy as np

    # Pre-Processing Image
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    resized_img = cv2.resize(img, (712, 512), interpolation=cv2.INTER_AREA)
    cropped_img = resized_img[resized_img.shape[0]*-7//24:resized_img.shape[0]*-1//10, resized_img.shape[1]*3//-5:]
    gray_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    remove_bg_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 16)

    # Create an OCR reader for Arabic
    reader = easyocr.Reader(['ar'])
    ar_en = {'٠':'0', '١':'1', '٢':'2', '٣':'3', '٤':'4',
             '٥':'5', '٦':'6', '٧':'7', '٨':'8', '٩':'9'}

    # Perform OCR on the image
    results = reader.readtext(remove_bg_img, detail=0, allowlist='٠١٢٣٤٥٦٧٨٩')
    nationalId = ''.join(ar_en[n] for n in results[0])[:14]

    return nationalId


# testing post request with commends 
# curl -X POST -F "file=@\"D:\WORK Space\GRADAUTION PROJECT\Extracting User Info From National ID\dataset\0.JPG\"" https://cbr-api-gdfd.onrender.com/extract_nationalId
# curl -X POST -F "file=@\"D:\WORK Space\GRADAUTION PROJECT\Extracting User Info From National ID\dataset\0.JPG\"" http://localhost:5000/extract_nationalId