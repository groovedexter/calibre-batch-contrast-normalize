import io
from PIL import Image, ImageOps, ImageEnhance

def normalize_image(img_data):
    try:
        image = Image.open(io.BytesIO(img_data))
        print(f"Processing image with size {image.size}")  # Debug log
        
        # Apply normalization and enhancements
        normalized_image = ImageOps.autocontrast(image, cutoff=2)  # Use autocontrast with cutoff
        normalized_image = ImageEnhance.Brightness(normalized_image).enhance(1.2)  # Increase brightness by 20%
        normalized_image = ImageEnhance.Contrast(normalized_image).enhance(1.7)    # Increase contrast by 70%
        
        print(f"Normalized image with size {normalized_image.size}")  # Debug log
        
        # Convert to grayscale if not already in grayscale
        if normalized_image.mode != "L":
            normalized_image = normalized_image.convert("L")  # Convert to grayscale
        
        # Save the image with a lower JPEG quality to reduce file size
        buf = io.BytesIO()
        normalized_image.save(buf, format='JPEG', quality=75)  # Adjusted quality to 75
        return buf.getvalue()
    except Exception as e:
        print(f"Error normalizing image: {e}")
        return img_data  # Return original if error