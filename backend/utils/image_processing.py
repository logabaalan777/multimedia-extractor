import imghdr
from PIL import Image
import pytesseract
from langdetect import detect
from io import BytesIO

async def extract_text_from_image(file):
    content = await file.read()

    if not content:
        raise ValueError("Empty file content.")

    filename = file.filename
    file_extension = filename.split('.')[-1].lower()

    valid_formats = ['png', 'jpeg', 'jpg']
    if file_extension not in valid_formats:
        raise ValueError("Invalid file format. Only PNG, JPEG, and JPG are allowed.")

    file_type = imghdr.what(None, content)
    if file_type not in valid_formats:
        raise ValueError(f"Invalid image file type: {file_type}. Expected JPG, JPEG, or PNG.")

    try:
        img = Image.open(BytesIO(content))
        img = img.convert('RGB')  

        text = pytesseract.image_to_string(img, lang="eng+tam+hin")  # Specify the languages to detect

        try:
            lang = detect(text)
        except:
            lang = "unknown"

        return {
            "text": text.replace('\u200c', '').replace('\n', ' '),  
            "language": lang
        }

    except Exception as e:
        raise ValueError(f"Could not process the image file: {str(e)}")
