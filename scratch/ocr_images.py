import os
from PIL import Image

def main():
    print("Checking PIL installation...")
    try:
        import pytesseract
        print("pytesseract is installed.")
    except ImportError:
        print("pytesseract is NOT installed. Trying alternative...")
        pytesseract = None
        
    image_dir = r"e:\VoidMap ai\docs_images"
    images = [
        "media__1780372388831.png",
        "media__1780372529488.png",
        "media__1780451055514.png",
        "media__1780451570442.png"
    ]
    
    for img_name in images:
        img_path = os.path.join(image_dir, img_name)
        if not os.path.exists(img_path):
            print(f"{img_name} does not exist at {img_path}")
            continue
            
        print(f"\n--- Analyzing {img_name} ---")
        img = Image.open(img_path)
        print(f"Size: {img.size}, Format: {img.format}, Mode: {img.mode}")
        
        if pytesseract:
            try:
                # Set path to Tesseract if needed, but try default first
                text = pytesseract.image_to_string(img)
                print("OCR Text detected:")
                print(text[:300]) # print first 300 chars
            except Exception as e:
                print(f"OCR failed: {e}")
        else:
            # Let's inspect some pixels to find if they are dark/light, or look at pixel statistics
            # This is a fallback
            pass

if __name__ == "__main__":
    main()
