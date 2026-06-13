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
    page.insert_text((45, 60), "VOIDMAP AI — TEST CASE DOCUMENT", fontsize=14, color=(1, 1, 1))
    
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
    print("VOIDMAP AI - COMPILING ADDITIONAL DOMAIN PDF TEST CASES...")
    print("====================================================")
    
    # 1. Cybersecurity Ledger Audit (triggers Cybersecurity uploader)
    generate_pdf(
        "../cybersecurity_ledger_audit.pdf",
        "Core FinTech Ledger Node",
        "Cybersecurity",
        "Ledger Node",
        "Critical",
        "FastAPI, React, Docker, Solidity",
        ["Security", "Deployment", "Compliance", "Ethics"],
        "We are launching a completely secure FinTech ledger node utilizing smart contracts. It guarantees 100% unbreakable security for client transactions and will always execute instantly. The node contains transaction audit logging, key lifecycle rotation, and rate limiting."
    )
    
    # 2. Startup SaaS Audit (triggers Startup uploader)
    generate_pdf(
        "../startup_saas_audit.pdf",
        "Generic SaaS Reporting Platform",
        "Startup",
        "SaaS Platform",
        "Medium",
        "React, Node.js, PostgreSQL, Docker",
        ["Scalability", "Ethics"],
        "This technical proposal outlines the deployment parameters of a generic SaaS system. The design integrates scalable database components and processes user inputs to generate structured reporting pipelines, with basic access controls."
    )
    
    print("====================================================")
    print("ALL ADDITIONAL DOMAIN PDF TEST CASES SUCCESSFULLY COMPILED!")
    print("====================================================")

if __name__ == "__main__":
    main()
