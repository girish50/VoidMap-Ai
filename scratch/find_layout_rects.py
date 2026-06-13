import os
import numpy as np
from PIL import Image

def analyze_regions(img_path):
    img = Image.open(img_path).convert("L")
    w, h = img.size
    arr = np.array(img)
    
    # Check vertical projections to find layout columns
    col_proj = np.mean(arr, axis=0)
    row_proj = np.mean(arr, axis=1)
    
    print(f"\nImage: {os.path.basename(img_path)} ({w}x{h})")
    # Count how many dark/light columns there are
    # For example, in a split pane, there's a strong vertical line or divider
    # Let's look for columns with very low variance
    col_vars = np.var(arr, axis=0)
    dividers = np.where(col_vars < 20)[0]
    print(f"  Low variance columns count: {len(dividers)}")
    if len(dividers) > 0:
        print(f"  Dividers at columns: {dividers[:10]}...")
        
    # Let's count potential white/light boxes (inputs) in dark theme
    # Dark theme background is very dark (values < 30).
    # Inputs/cards are slightly lighter or dark, but text is light (values > 200).
    # Let's look at the pixel distribution.
    light_pixels = np.sum(arr > 200)
    print(f"  Light pixels count: {light_pixels} ({light_pixels/(w*h):.2%})")

def main():
    image_dir = r"e:\VoidMap ai\docs_images"
    images = [
        "media__1780372388831.png",
        "media__1780372529488.png",
        "media__1780451055514.png",
        "media__1780451570442.png"
    ]
    for img in images:
        img_path = os.path.join(image_dir, img)
        if os.path.exists(img_path):
            analyze_regions(img_path)

if __name__ == "__main__":
    main()
