import os
import subprocess
import shutil

def main():
    html_path = r"e:\VoidMap ai\temp_guide.html"
    scratch_pdf_path = r"C:\Users\GIRISH\.gemini\antigravity\scratch\comprehensive_analysis_guide.pdf"
    final_pdf_path = r"e:\VoidMap ai\comprehensive_analysis_guide.pdf"
    
    # Make sure we clean up any pre-existing files
    if os.path.exists(scratch_pdf_path):
        os.remove(scratch_pdf_path)
    if os.path.exists(final_pdf_path):
        os.remove(final_pdf_path)
        
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>VoidMap AI — Platform Quick Guide</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Fira+Code:wght@400;700&display=swap');
    
    body {
      font-family: 'Outfit', sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f8fafc;
      color: #0f172a;
      line-height: 1.5;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    
    @page {
      size: A4;
      margin: 15mm;
    }
    
    /* Cover Page */
    .cover-page {
      height: 260mm;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      background: linear-gradient(135deg, #6366f1 0%, #7c3aed 100%);
      color: white;
      text-align: center;
      padding: 30px;
      box-sizing: border-box;
      page-break-after: always;
      border-radius: 16px;
    }
    
    .cover-tag {
      font-family: 'Fira Code', monospace;
      font-size: 11px;
      background-color: rgba(255, 255, 255, 0.2);
      color: white;
      padding: 6px 14px;
      border-radius: 20px;
      margin-bottom: 20px;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      font-weight: 600;
    }
    
    .cover-title {
      font-size: 42px;
      font-weight: 800;
      letter-spacing: -0.04em;
      margin: 0 0 10px 0;
    }
    
    .cover-subtitle {
      font-size: 15px;
      font-weight: 600;
      color: #f3e8ff;
      margin: 0 0 40px 0;
      text-transform: uppercase;
      letter-spacing: 0.2em;
    }
    
    .cover-description {
      max-width: 480px;
      font-size: 14px;
      color: #e0e7ff;
      line-height: 1.6;
      margin-bottom: 50px;
    }
    
    .cover-footer {
      font-family: 'Fira Code', monospace;
      font-size: 10px;
      color: #ddd6fe;
    }
    
    /* Document Layout */
    .container {
      max-width: 800px;
      margin: 0 auto;
    }
    
    .page-break {
      page-break-before: always;
    }
    
    .header-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #e9d5ff;
      padding-bottom: 8px;
      margin-top: 10px;
      margin-bottom: 25px;
    }
    
    .section-title {
      font-size: 16px;
      font-weight: 800;
      color: #7c3aed;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin: 0;
    }
    
    .section-page-num {
      font-family: 'Fira Code', monospace;
      font-size: 11px;
      color: #94a3b8;
    }
    
    p {
      margin-top: 0;
      margin-bottom: 15px;
      color: #475569;
      font-size: 13.5px;
    }
    
    .highlight-box {
      background-color: #faf5ff;
      border-left: 4px solid #7c3aed;
      padding: 15px;
      border-radius: 0 10px 10px 0;
      margin-bottom: 20px;
      font-size: 13px;
      color: #4c1d95;
    }
    
    .highlight-title {
      font-weight: 700;
      text-transform: uppercase;
      font-size: 10px;
      letter-spacing: 0.05em;
      margin-bottom: 4px;
    }
    
    /* Visual Presentation Mode Components */
    .slide-layout {
      background-color: white;
      border: 1px solid #e2e8f0;
      border-radius: 16px;
      padding: 20px;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
      margin-bottom: 15px;
      page-break-inside: avoid;
    }
    
    .slide-title {
      font-size: 15px;
      font-weight: 800;
      color: #1e1b4b;
      margin: 0 0 15px 0;
      text-transform: uppercase;
      display: flex;
      align-items: center;
    }
    
    .slide-title::before {
      content: "";
      width: 8px;
      height: 8px;
      background-color: #7c3aed;
      border-radius: 50%;
      margin-right: 8px;
      display: inline-block;
    }
    
    .slide-content-split {
      display: grid;
      grid-template-cols: 1fr;
      gap: 15px;
    }
    
    .slide-bullets {
      margin: 0;
      padding-left: 15px;
      font-size: 12.5px;
      color: #475569;
      margin-bottom: 15px;
    }
    
    .slide-bullets li {
      margin-bottom: 8px;
    }
    
    .slide-img {
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
      background-color: #f1f5f9;
      padding: 10px;
      box-sizing: border-box;
      max-height: 120mm;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    
    .slide-img img {
      max-width: 100%;
      max-height: 100mm;
      display: block;
      height: auto;
      object-fit: contain;
    }
    
    /* Simply Explained Terms block */
    .simple-dictionary {
      display: grid;
      grid-template-cols: 1fr 1fr;
      gap: 15px;
      margin-bottom: 25px;
    }
    
    .dict-item {
      background-color: white;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 15px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.02);
      page-break-inside: avoid;
    }
    
    .dict-title {
      font-weight: 700;
      color: #7c3aed;
      font-size: 13.5px;
      margin-bottom: 6px;
      text-transform: uppercase;
    }
    
    .dict-simple {
      font-size: 12.5px;
      color: #1e1b4b;
      font-weight: 600;
      background-color: #faf5ff;
      padding: 6px 10px;
      border-radius: 6px;
      margin-bottom: 8px;
    }
    
    .dict-desc {
      font-size: 12px;
      color: #64748b;
      margin: 0;
      line-height: 1.5;
    }
  </style>
</head>
<body>

  <!-- PAGE 1: COVER -->
  <div class="cover-page">
    <div class="cover-tag">Visual Audit Companion</div>
    <div class="cover-title">VoidMap AI Guide</div>
    <div class="cover-subtitle">Simple, Visual & Easy-to-Understand</div>
    <div class="cover-description">
      An interactive-style visual guide detailing what our project is, how it functions under the hood, and how to understand each component at a glance with live screenshots.
    </div>
    <div class="cover-footer">VOIDMAP AI • SIMPLIFIED MANUAL</div>
  </div>

  <div class="container">
    
    <!-- PAGE 2: WHAT & HOW -->
    <div class="header-bar">
      <h2 class="section-title">1. What We Wanted to Do & How We Did It</h2>
      <span class="section-page-num">Page 02</span>
    </div>
    
    <div class="highlight-box">
      <div class="highlight-title">🎯 What We Wanted to Do (The Goal)</div>
      We set out to build an intelligent auditing assistant that detects **missing architecture requirements** (blueprint voids) in project specifications and dynamically simulates the system's risk under hostile conditions.
    </div>

    <div class="highlight-box" style="background-color: #eff6ff; border-left-color: #3b82f6; color: #1e3a8a; margin-top: 30px;">
      <div class="highlight-title" style="color: #1d4ed8;">🚀 How We Did It (The Implementation)</div>
      1. **Setup Blueprints:** Modeled expectation requirements for different domains inside a **Neo4j** graph database.
      <br/><br/>
      2. **Isolate Gaps:** Built a backend **Absence Engine** that reads user specs (checklists or plain text) and subtracts them from the blueprints to find Gaps.
      <br/><br/>
      3. **Simulate Shocks:** Developed a client-side **Counterfactual Simulator** (interactive sliders) to let users stress test their proposals.
      <br/><br/>
      4. **Visualize Cascades:** Built directed node maps to track failure ripples, and compared gaps against real historical disasters.
    </div>

    <!-- PAGE 3: SIMPLE DICTIONARY -->
    <div class="page-break"></div>
    <div class="header-bar">
      <h2 class="section-title">2. The Cool Terms Explained Simply</h2>
      <span class="section-page-num">Page 03</span>
    </div>
    
    <p>
      Here is the plain English dictionary of the platform's core terms, designed to make sense to anyone immediately.
    </p>

    <div class="simple-dictionary">
      
      <div class="dict-item">
        <div class="dict-title">Blindspot Index</div>
        <div class="dict-simple">📈 The "Danger Meter"</div>
        <div class="dict-desc">
          A score from 0% to 100% showing how risky your proposal is. More missing safeguards + higher simulator stress = higher Blindspot Index.
        </div>
      </div>

      <div class="dict-item">
        <div class="dict-title">Expectations Coverage</div>
        <div class="dict-simple">📋 The "Completeness Checklist"</div>
        <div class="dict-desc">
          What percentage of expected domain standard features you actually built. If there are 10 standard rules and you build 4, your coverage is 40%.
        </div>
      </div>

      <div class="dict-item">
        <div class="dict-title">Counterfactual Simulation</div>
        <div class="dict-simple">🎛️ The "What-If" Sandbox</div>
        <div class="dict-desc">
          Interactive sliders that simulate real-world disasters (like cyberattacks or new regulations) to test if your project will break.
        </div>
      </div>

      <div class="dict-item">
        <div class="dict-title">Consequence Ripple Tree</div>
        <div class="dict-simple">🔗 The "Domino Effect" Map</div>
        <div class="dict-desc">
          A visual node diagram showing how forgetting one simple security key triggers a chain reaction that crashes your whole system.
        </div>
      </div>

      <div class="dict-item">
        <div class="dict-title">Disaster DNA Proximity</div>
        <div class="dict-simple">⌛ The "Time Machine" Matcher</div>
        <div class="dict-desc">
          Compares your missing items to famous past software crashes (like Knight Capital) to warn you if you're about to repeat history.
        </div>
      </div>

      <div class="dict-item">
        <div class="dict-title">Boardroom Clash</div>
        <div class="dict-simple">🗣️ The "Advisor Debate"</div>
        <div class="dict-desc">
          Simulated chat log between virtual advisors (Security vs. Business) arguing over whether to build safety tools or deploy fast.
        </div>
      </div>

    </div>

    <!-- PAGE 4: VISUAL TOUR - INPUT TERMINALS (PLAIN TEXT) -->
    <div class="page-break"></div>
    <div class="header-bar">
      <h2 class="section-title">3. Inputting Your Proposal: Plain Text Mode</h2>
      <span class="section-page-num">Page 04</span>
    </div>
    
    <div class="slide-layout">
      <div class="slide-title">Plain Text Terminal Mode</div>
      <div class="slide-content-split">
        <ul class="slide-bullets">
          <li>**Super Simple Interface:** Users only input a Project Name, select a Domain, and paste a raw specifications paragraph.</li>
          <li>**No Complex Fields:** No need to check individual technical checkboxes; the system reads raw words.</li>
          <li>**How it works:** Behind the scenes, the engine scans the text for keywords and matches them to domain expectations.</li>
        </ul>
        <div class="slide-img">
          <img src="docs_images/plain_text_cropped.png" alt="Plain Text Input Screenshot" />
        </div>
      </div>
    </div>

    <!-- PAGE 5: VISUAL TOUR - INPUT TERMINALS (GUIDED) -->
    <div class="page-break"></div>
    <div class="header-bar">
      <h2 class="section-title">4. Inputting Your Proposal: Guided Form Mode</h2>
      <span class="section-page-num">Page 05</span>
    </div>

    <div class="slide-layout">
      <div class="slide-title">Guided Form Mode</div>
      <div class="slide-content-split">
        <ul class="slide-bullets">
          <li>**Structured Checklist:** Users select exact checkboxes representing technologies and active safeguards.</li>
          <li>**Domain Tuning:** Automatically updates fields based on selected domain rules.</li>
          <li>**Target Alignment:** Perfect for systematic design audits when specs are already well documented.</li>
        </ul>
        <div class="slide-img">
          <img src="docs_images/guided_form_cropped.png" alt="Guided Form Input Screenshot" />
        </div>
      </div>
    </div>

    <!-- PAGE 6: VISUAL TOUR - DETAILS GRID -->
    <div class="page-break"></div>
    <div class="header-bar">
      <h2 class="section-title">5. Active Metrics & Gaps Grid</h2>
      <span class="section-page-num">Page 06</span>
    </div>

    <div class="slide-layout">
      <div class="slide-title">KPI Header & Discovery Gaps Grid</div>
      <div class="slide-content-split">
        <ul class="slide-bullets">
          <li>**Instant Indicators:** Displays Blindspot Index and Expectations Coverage at a glance.</li>
          <li>**Export Button:** Contains the safe "Download Audit Report" button at the top right.</li>
          <li>**Gaps Sheet:** Tabulates every unaddressed safety rule, explaining what is missing and its specific downstream hazard.</li>
        </ul>
        <div class="slide-img">
          <img src="docs_images/metrics_gaps_cropped.png" alt="Active Details Screenshot" />
        </div>
      </div>
    </div>

    <!-- PAGE 7: VISUAL TOUR - SANDBOX SIMULATOR -->
    <div class="page-break"></div>
    <div class="header-bar">
      <h2 class="section-title">6. Counterfactual Simulation</h2>
      <span class="section-page-num">Page 07</span>
    </div>

    <div class="slide-layout">
      <div class="slide-title">Counterfactual Simulation Sandbox</div>
      <div class="slide-content-split">
        <ul class="slide-bullets">
          <li>**Disaster Sliders:** Adjust sliders to simulate hostile changes in regulatory focus, technical degradation, or server attacks.</li>
          <li>**Real-time Recalculations:** Scores update instantly to show if your system survives the shock.</li>
          <li>**Scenario Presets:** Buttons lock preset configurations (e.g. Zero-Day Cyberattack) to quickly model events.</li>
        </ul>
        <div class="slide-img">
          <img src="docs_images/counterfactual_sliders_cropped.png" alt="Simulator Screenshot" />
        </div>
      </div>
    </div>

    <!-- PAGE 8: VISUAL TOUR - RIPPLE TREES -->
    <div class="page-break"></div>
    <div class="header-bar">
      <h2 class="section-title">7. Interactive Causal ripple trees</h2>
      <span class="section-page-num">Page 08</span>
    </div>

    <div class="slide-layout">
      <div class="slide-title">Active Consequence Ripple Trees</div>
      <div class="slide-content-split">
        <ul class="slide-bullets">
          <li>**Causal Chain Map:** Renders directed arrows showing the exact path from a missing feature to a crash.</li>
          <li>**Interactive Nodes:** Fit to screen, zoom, and drag nodes to explore cascading security failures.</li>
          <li>**Domino Demonstration:** Visually proves that ignoring small tasks triggers major outages.</li>
        </ul>
        <div class="slide-img">
          <img src="docs_images/media__1780451570442.png" alt="Ripple Trees Map Screenshot" />
        </div>
      </div>
    </div>

    <!-- PAGE 9: VISUAL TOUR - NEO4J & REPORT -->
    <div class="page-break"></div>
    <div class="header-bar">
      <h2 class="section-title">8. Graph Databases & Compliance Reports</h2>
      <span class="section-page-num">Page 09</span>
    </div>

    <div class="slide-layout">
      <div class="slide-title">Neo4j Graph Network & Downloaded Report</div>
      <div class="slide-content-split">
        <ul class="slide-bullets">
          <li>**Neo4j Network Tab:** Visual network mapping addressed (green) vs unaddressed (red) standards query.</li>
          <li>**Downloaded Report:** Generates a structured `.md` file with a list of tasks for the developer.</li>
          <li>**End-User Action Plan:** Developers copy gaps straight into JIRA tickets to resolve and drop risk to 0%.</li>
        </ul>
        <div style="background-color: #faf5ff; border: 1px solid #ddd6fe; border-radius: 8px; padding: 25px; font-family: 'Fira Code', monospace; font-size: 11px; color: #4c1d95;">
          # AUDIT REPORT METRICS:
          <br/>- BLINDSPOT INDEX: 84%
          <br/>- LIKELIHOOD OF CRASH: 78%
          <br/>- ESTIMATED RISK LIABILITY COST: ₹4,500K
        </div>
      </div>
    </div>

  </div>

</body>
</html>
"""
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Created HTML document at: {html_path}")
    
    # Run Headless Chrome to compile PDF
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={scratch_pdf_path}",
        html_path
    ]
    
    print("Compiling PDF...")
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Chrome output:\n", res.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Chrome exited with error: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return
    except Exception as ex:
        print(f"Failed to run Chrome process: {ex}")
        return
        
    if os.path.exists(scratch_pdf_path):
        print(f"PDF successfully written to scratch: {scratch_pdf_path}")
        # Copy to final path
        shutil.copy(scratch_pdf_path, final_pdf_path)
        print(f"Copied PDF to workspace root: {final_pdf_path}")
        # Clean up temporary HTML
        if os.path.exists(html_path):
            os.remove(html_path)
            print("Cleaned up temp HTML file.")
    else:
        print("PDF was not created in the scratch directory.")

if __name__ == "__main__":
    main()
