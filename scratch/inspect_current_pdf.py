import fitz # PyMuPDF
import os

pdf_path = r"e:\VoidMap ai\comprehensive_analysis_guide.pdf"
if not os.path.exists(pdf_path):
    print("PDF not found at:", pdf_path)
else:
    doc = fitz.open(pdf_path)
    print(f"PDF Page count: {len(doc)}")
    for i in range(len(doc)):
        page = doc[i]
        print(f"\n--- Page {i+1} ---")
        text = page.get_text()
        safe_text = text.encode('ascii', errors='replace').decode('ascii')
        print("Text snippet:", repr(safe_text[:300]))
        images = page.get_images(full=True)
        print(f"Images count: {len(images)}")
        for img_idx, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            print(f"  Image {img_idx}: xref={xref}, ext={image_ext}, size={len(image_bytes)} bytes")
