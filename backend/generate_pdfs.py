import os
import fitz  # PyMuPDF

def generate_pdf(filename, title, domain, project_type, risk, tech, considerations, description):
    print(f"Generating PDF: {filename}...")
    doc = fitz.open()
    page = doc.new_page()
    
    # Define vertical margin tracking
    y = 50
    
    # Draw a cobalt blue title block header
    page.draw_rect(fitz.Rect(30, 30, 565, 80), color=(0.02, 0.03, 0.08), fill=(0.02, 0.03, 0.08))
    
    # Title
    page.insert_text((45, 60), f"VOIDMAP AI — TEST CASE DOCUMENT", fontsize=14, color=(1, 1, 1))
    
    # Metadata block
    y = 110
    page.insert_text((45, y), f"PROJECT TITLE: {title}", fontsize=11, color=(0.1, 0.1, 0.15))
    y += 20
    page.insert_text((45, y), f"TARGET DOMAIN: {domain} | TYPE: {project_type}", fontsize=10, color=(0.3, 0.3, 0.35))
    y += 20
    page.insert_text((45, y), f"RISK LEVEL: {risk}", fontsize=10, color=(0.3, 0.3, 0.35))
    y += 20
    page.insert_text((45, y), f"TECH STACK: {tech}", fontsize=10, color=(0.3, 0.3, 0.35))
    y += 20
    page.insert_text((45, y), f"CHECKED SAFEGUARDS: {', '.join(considerations) if considerations else 'None'}", fontsize=10, color=(0.3, 0.3, 0.35))
    
    # Horizontal line
    y += 15
    page.draw_line((30, y), (565, y), color=(0.8, 0.8, 0.8), width=1)
    
    # Section Header
    y += 25
    page.insert_text((45, y), "TECHNICAL ARCHITECTURAL PROPOSAL SPECIFICATIONS", fontsize=11, color=(0.02, 0.03, 0.08))
    
    # Body Text (Wrapped lines)
    y += 25
    words = description.split(" ")
    line = []
    for word in words:
        line.append(word)
        # Simple character limit wrap
        if len(" ".join(line)) > 75:
            page.insert_text((45, y), " ".join(line[:-1]), fontsize=10, color=(0.2, 0.2, 0.2))
            y += 18
            line = [word]
    if line:
        page.insert_text((45, y), " ".join(line), fontsize=10, color=(0.2, 0.2, 0.2))
        y += 18
        
    # Footer Notice
    page.insert_text((45, 750), "CONFIDENTIAL - GENERATED FOR VOIDMAP AI COMPLIANCE AUDITING TESTS", fontsize=8, color=(0.6, 0.6, 0.6))
    
    doc.save(filename)
    doc.close()
    print(f"Saved PDF: {os.path.abspath(filename)}")

def main():
    print("====================================================")
    print("VOIDMAP AI - COMPILING REAL PDF TEST DOCUMENTS...")
    print("====================================================")
    
    # 1. Robust 90%
    generate_pdf(
        "../medical_robust_90.pdf",
        "AlphaMed Chest X-Ray CNN [Robust 90%]",
        "Healthcare",
        "Medical AI",
        "High",
        "React, FastAPI, PyTorch, Docker",
        ["Validation", "Security", "Ethics", "Compliance", "Monitoring"],
        "AlphaMed robust diagnostic proposal. We have completed clinical validation trials on independent radiological datasets. Standard patient privacy is enforced with HIPAA-compliant data encryption and automatic demographic bias mitigation across patient age cohorts. We are preparing legal documents for the FDA / CE Regulatory Pathway and have integrated explainability networks providing radiologists with attention heatmap highlights."
    )
    
    # 2. Moderate 70%
    generate_pdf(
        "../medical_moderate_70.pdf",
        "AlphaMed Chest X-Ray CNN [Moderate 70%]",
        "Healthcare",
        "Medical AI",
        "High",
        "React, FastAPI, PyTorch, Docker",
        ["Validation", "Security"],
        "AlphaMed moderate diagnostic model. The system processes chest scans to classify lung pathologies. We have run standard clinical validation against reference datasets and protect patient privacy via standard database encryption. Further bias validation and regulatory paths are pending."
    )
    
    # 3. Fragile 40%
    generate_pdf(
        "../medical_fragile_40.pdf",
        "AlphaMed Chest X-Ray CNN [Fragile 40%]",
        "Healthcare",
        "Medical AI",
        "High",
        "React, FastAPI, PyTorch",
        [],
        "AlphaMed raw model proposal. We claim this convolutional neural network has absolute 100% unbreakable diagnostic accuracy and runs instantly without lag. It integrates directly with public scanners and works perfectly."
    )
    
    print("====================================================")
    print("ALL REAL PDF TEST ASSETS SUCCESSFULLY COMPILED!")
    print("====================================================")

if __name__ == "__main__":
    main()
