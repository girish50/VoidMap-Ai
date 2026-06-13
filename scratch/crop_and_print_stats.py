import os
import numpy as np
from PIL import Image

def analyze_visual_features(img_path):
    img = Image.open(img_path).convert("RGB")
    width, height = img.size
    arr = np.array(img)
    
    # 1. Background type (Light vs Dark)
    # Check average brightness of the corners
    corners = [
        arr[0, 0], arr[0, -1], arr[-1, 0], arr[-1, -1],
        arr[10, 10], arr[10, -10], arr[-10, 10], arr[-10, -10]
    ]
    avg_corner = np.mean(corners, axis=0)
    brightness = np.mean(avg_corner)
    is_light = brightness > 128
    
    # 2. Check for purple lines/elements (#7c3aed / HSL purple)
    # Purple: R > 100, G < 100, B > 150
    purple_pixels = np.sum((arr[:, :, 0] > 100) & (arr[:, :, 1] < 100) & (arr[:, :, 2] > 150))
    
    # 3. Check for red lines/elements (#ef4444 / red danger)
    # Red: R > 180, G < 100, B < 100
    red_pixels = np.sum((arr[:, :, 0] > 180) & (arr[:, :, 1] < 100) & (arr[:, :, 2] < 100))
    
    # 4. Check for green lines/elements (#10b981 / green success)
    # Green: R < 100, G > 150, B < 150
    green_pixels = np.sum((arr[:, :, 0] < 100) & (arr[:, :, 1] > 150) & (arr[:, :, 2] < 150))
    
    # 5. Check for horizontal lines / projections
    # Let's count rows that are mostly constant color (indicating borders or dividers)
    # Row diffs
    row_diffs = np.sum(np.abs(arr[1:, :, :] - arr[:-1, :, :]), axis=(1, 2))
    flat_rows = np.sum(row_diffs < 10)
    
    # 6. Check for grid pattern (standard spacing of light/dark dots or lines)
    # In react flow grid background, the dots have a specific spacing (16px)
    # Let's see if there is periodicity in column/row variances
    col_vars = np.var(arr, axis=0)
    
    print(f"File: {os.path.basename(img_path)}")
    print(f"  Dimensions: {width} x {height}")
    print(f"  Theme: {'Light' if is_light else 'Dark'} (Corner brightness: {brightness:.1f})")
    print(f"  Color pixels: Purple={purple_pixels}, Red={red_pixels}, Green={green_pixels}")
    print(f"  Flat rows count: {flat_rows}")

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
            analyze_visual_features(img_path)

if __name__ == "__main__":
    main()
