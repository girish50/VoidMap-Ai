import os
from PIL import Image

def convert_header_to_ascii(image_path, width=120, header_height=120):
    try:
        image = Image.open(image_path)
    except Exception as e:
        return f"Error: {e}"
    
    # Crop the top header region
    w, h = image.size
    crop_h = min(h, header_height)
    header = image.crop((0, 0, w, crop_h))
    
    # Resize to width x height while maintaining aspect ratio or scale to fit
    aspect = crop_h / float(w)
    new_h = int(aspect * width * 0.5) # font ratio correction
    resized = header.resize((width, max(1, new_h)))
    
    # Convert to grayscale
    gray = resized.convert("L")
    
    # Map pixels to ascii characters
    ASCII_CHARS = ["@", "#", "8", "&", "o", ":", "*", ".", " "]
    pixels = list(gray.getdata())
    
    ascii_str = ""
    for idx, pixel in enumerate(pixels):
        char_idx = min(len(ASCII_CHARS) - 1, pixel // (256 // len(ASCII_CHARS)))
        ascii_str += ASCII_CHARS[char_idx]
        if (idx + 1) % width == 0:
            ascii_str += "\n"
            
    return ascii_str

def main():
    image_dir = r"e:\VoidMap ai\docs_images"
    images = [
        "media__1780372388831.png",
        "media__1780372529488.png",
        "media__1780451055514.png",
        "media__1780451570442.png"
    ]
    
    out_path = r"e:\VoidMap ai\scratch\headers_ascii.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        for img in images:
            f.write(f"\n=========================================\n")
            f.write(f"IMAGE: {img}\n")
            f.write(f"=========================================\n")
            img_path = os.path.join(image_dir, img)
            art = convert_header_to_ascii(img_path)
            f.write(art)
            f.write("\n\n")
            
    print(f"Header ASCII art written to {out_path}")

if __name__ == "__main__":
    main()
