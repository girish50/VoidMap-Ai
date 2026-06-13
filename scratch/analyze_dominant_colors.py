import os
from collections import Counter
from PIL import Image

def get_dominant_colors(img_path, num_colors=10):
    img = Image.open(img_path).convert("RGB")
    # Resize to speed up calculation
    img.thumbnail((100, 100))
    pixels = list(img.getdata())
    counter = Counter(pixels)
    return counter.most_common(num_colors)

def main():
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
            continue
        print(f"\nImage: {img_name}")
        dom = get_dominant_colors(img_path)
        for rgb, count in dom:
            print(f"  RGB: {rgb} - count: {count}")

if __name__ == "__main__":
    main()
