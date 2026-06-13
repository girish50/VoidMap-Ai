import os
from PIL import Image

def crop_image(src_name, dest_name, box):
    image_dir = r"e:\VoidMap ai\docs_images"
    src_path = os.path.join(image_dir, src_name)
    dest_path = os.path.join(image_dir, dest_name)
    
    if not os.path.exists(src_path):
        print(f"Error: {src_path} does not exist.")
        return False
        
    try:
        img = Image.open(src_path)
        cropped = img.crop(box)
        cropped.save(dest_path)
        print(f"Successfully cropped {src_name} to {dest_name} with box {box}")
        return True
    except Exception as e:
        print(f"Failed to crop {src_name}: {e}")
        return False

def main():
    # 1. Guided Form: Crop the form panel (left half) of media__1780372529488.png
    # Size of media__1780372529488.png is 1024x585
    crop_image("media__1780372529488.png", "guided_form_cropped.png", (0, 0, 520, 585))
    
    # 2. KPI Metrics & Gaps: Crop the metrics and gaps table (right half, upper section) of media__1780372388831.png
    # Size of media__1780372388831.png is 1024x563
    crop_image("media__1780372388831.png", "metrics_gaps_cropped.png", (500, 0, 1024, 380))
    
    # 3. Sliders: Crop the sliders card (right half, lower section) of media__1780372388831.png
    crop_image("media__1780372388831.png", "counterfactual_sliders_cropped.png", (500, 360, 1024, 563))
    
    # 4. Plain Text Mode: Crop the input text terminal area from media__1780451055514.png
    # Size of media__1780451055514.png is 1024x419
    crop_image("media__1780451055514.png", "plain_text_cropped.png", (0, 0, 1024, 419))

if __name__ == "__main__":
    main()
