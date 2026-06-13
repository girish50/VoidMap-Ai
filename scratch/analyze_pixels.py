import os
from PIL import Image

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
        
        img = Image.open(img_path).convert("RGB")
        width, height = img.size
        
        # Color counts
        reds = 0
        greens = 0
        purples = 0
        total = width * height
        
        for x in range(width):
            for y in range(height):
                r, g, b = img.getpixel((x, y))
                # Red color check (high R, low G, low B)
                if r > 180 and g < 100 and b < 100:
                    reds += 1
                # Green color check (low R, high G, low B)
                if r < 100 and g > 150 and b < 120:
                    greens += 1
                # Purple/Indigo check (high R, low G, high B)
                if r > 100 and g < 100 and b > 180:
                    purples += 1
                    
        print(f"Image: {img_name}")
        print(f"  Reds:   {reds} ({reds/total:.2%})")
        print(f"  Greens: {greens} ({greens/total:.2%})")
        print(f"  Purples: {purples} ({purples/total:.2%})")

if __name__ == "__main__":
    main()
