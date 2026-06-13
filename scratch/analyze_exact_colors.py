import os
from collections import Counter
from PIL import Image

def analyze_palette(img_path):
    img = Image.open(img_path).convert("RGB")
    pixels = list(img.getdata())
    counter = Counter(pixels)
    print(f"\nFile: {os.path.basename(img_path)}")
    # Print top 30 colors
    top_colors = counter.most_common(30)
    for rgb, count in top_colors:
        # Check if it has color (not grayscale r==g==b)
        is_colored = not (abs(rgb[0] - rgb[1]) < 8 and abs(rgb[1] - rgb[2]) < 8)
        color_tag = " [COLORED]" if is_colored else ""
        print(f"  RGB: {rgb} - count: {count}{color_tag}")

def main():
    image_dir = r"e:\VoidMap ai\docs_images"
    images = [
        "media__1780451055514.png",
        "media__1780451570442.png"
    ]
    for img in images:
        img_path = os.path.join(image_dir, img)
        if os.path.exists(img_path):
            analyze_palette(img_path)

if __name__ == "__main__":
    main()
