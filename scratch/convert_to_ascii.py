import os
from PIL import Image

def scale_image(image, new_width=100):
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width * 0.55) # 0.55 corrects aspect ratio for fonts
    new_image = image.resize((new_width, new_height))
    return new_image

def convert_to_grayscale(image):
    return image.convert("L")

def map_pixels_to_ascii(image, range_width=25):
    # Short ASCII chars ramp from dark to light
    ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
    pixels = image.getdata()
    new_pixels = [ASCII_CHARS[pixel // range_width] for pixel in pixels]
    return "".join(new_pixels)

def convert_image(image_path):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image {image_path}: {e}")
        return ""
        
    image = scale_image(image)
    image = convert_to_grayscale(image)
    
    pixels_to_ascii = map_pixels_to_ascii(image)
    len_pixels_to_ascii = len(pixels_to_ascii)
    
    # Construct ascii art
    ascii_img = ""
    for i in range(0, len_pixels_to_ascii, 100):
        ascii_img += pixels_to_ascii[i:i+100] + "\n"
        
    return ascii_img

def main():
    image_dir = r"e:\VoidMap ai\docs_images"
    images = [
        "media__1780372388831.png",
        "media__1780372529488.png",
        "media__1780451055514.png",
        "media__1780451570442.png"
    ]
    
    out_path = r"e:\VoidMap ai\scratch\ascii_art.txt"
    with open(out_path, "w") as f:
        for img_name in images:
            f.write(f"\n=========================================\n")
            f.write(f"IMAGE: {img_name}\n")
            f.write(f"=========================================\n")
            img_path = os.path.join(image_dir, img_name)
            art = convert_image(img_path)
            f.write(art)
            f.write("\n\n")
            
    print(f"ASCII art saved to {out_path}")

if __name__ == "__main__":
    main()
