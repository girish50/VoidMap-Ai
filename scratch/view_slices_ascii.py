import os
from PIL import Image

def generate_vertical_slices(image_name, out_file):
    image_dir = r"e:\VoidMap ai\docs_images"
    image_path = os.path.join(image_dir, image_name)
    if not os.path.exists(image_path):
        out_file.write(f"Image {image_name} not found.\n")
        return
        
    img = Image.open(image_path).convert("L")
    w, h = img.size
    slice_height = 80
    
    out_file.write(f"\n=========================================\n")
    out_file.write(f"SLICES FOR {image_name} ({w}x{h})\n")
    out_file.write(f"=========================================\n")
    
    # Slice the image vertically
    for i in range(0, h, slice_height):
        bottom = min(h, i + slice_height)
        crop_box = img.crop((0, i, w, bottom))
        
        # Convert to ASCII
        width = 100
        aspect = crop_box.size[1] / float(crop_box.size[0])
        new_h = int(aspect * width * 0.55)
        resized = crop_box.resize((width, max(1, new_h)))
        
        ASCII_CHARS = ["@", "#", "8", "&", "o", ":", "*", ".", " "]
        pixels = list(resized.getdata())
        
        out_file.write(f"--- Vertical Slice Y: {i} to {bottom} ---\n")
        ascii_str = ""
        for idx, pixel in enumerate(pixels):
            char_idx = min(len(ASCII_CHARS) - 1, pixel // (256 // len(ASCII_CHARS)))
            ascii_str += ASCII_CHARS[char_idx]
            if (idx + 1) % width == 0:
                ascii_str += "\n"
        out_file.write(ascii_str)
        out_file.write("\n")

def main():
    out_path = r"e:\VoidMap ai\scratch\slices_ascii.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        generate_vertical_slices("media__1780372388831.png", f)
        generate_vertical_slices("media__1780372529488.png", f)
        generate_vertical_slices("media__1780451055514.png", f)
        generate_vertical_slices("media__1780451570442.png", f)
    print(f"Slices ASCII written to {out_path}")

if __name__ == "__main__":
    main()
