#!/usr/bin/env python3
"""Compare character spacing between Google and Pairwire bullet paragraphs."""
import zipfile
from lxml import etree
from pathlib import Path

# Analyze the TAILORED version (the one with spacing issues)
SRC = Path.home() / "Downloads" / "TomásBatalha_Resume_02_2026_GOOGLE_AE.docx"
ORIG = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Professional/2 - My Stuff/CV/TomásBatalha_Resume_02_2026.docx"

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
def qn(tag): return f'{{{W}}}{tag}'

def analyze_doc(path, label):
    print(f"\n{'='*60}")
    print(f"  {label}: {path.name}")
    print(f"{'='*60}")
    
    with zipfile.ZipFile(path) as z:
        xml = z.read('word/document.xml')
    
    tree = etree.fromstring(xml)
    
    for p in tree.findall('.//w:p', ns):
        pPr = p.find('w:pPr', ns)
        if pPr is None:
            continue
        if pPr.find('w:numPr', ns) is None:
            continue
        
        runs = p.findall('.//w:r', ns)
        text = ''.join(t.text or '' for r in runs for t in r.findall('w:t', ns))
        
        if not text.strip():
            continue
        
        # Check paragraph-level justification
        jc = pPr.find('w:jc', ns)
        jc_val = jc.get(qn('val')) if jc is not None else 'none'
        
        # Check paragraph-level spacing
        p_spacing = pPr.find('w:spacing', ns)
        p_spacing_info = ""
        if p_spacing is not None:
            for attr in ['before', 'after', 'line', 'lineRule']:
                v = p_spacing.get(qn(attr))
                if v:
                    p_spacing_info += f" {attr}={v}"
        
        # Check each run's formatting
        run_info = []
        for r in runs:
            rPr = r.find('w:rPr', ns)
            if rPr is None:
                run_info.append("(no rPr)")
                continue
            
            info = []
            
            # Character spacing (w:spacing)
            sp = rPr.find('w:spacing', ns)
            if sp is not None:
                val = sp.get(qn('val'))
                if val:
                    info.append(f"charSpacing={val}")
            
            # Font size
            sz = rPr.find('w:sz', ns)
            if sz is not None:
                info.append(f"sz={sz.get(qn('val'))}")
            
            # Font name
            rFonts = rPr.find('w:rFonts', ns)
            if rFonts is not None:
                fname = rFonts.get(qn('ascii')) or rFonts.get(qn('cs'))
                if fname:
                    info.append(f"font={fname}")
            
            # Kerning
            kern = rPr.find('w:kern', ns)
            if kern is not None:
                info.append(f"kern={kern.get(qn('val'))}")
            
            # Bold
            b = rPr.find('w:b', ns)
            if b is not None:
                info.append("BOLD")
            
            # w:w (character width/scaling)
            w_elem = rPr.find('w:w', ns)
            if w_elem is not None:
                info.append(f"width={w_elem.get(qn('val'))}")
            
            t = r.find('w:t', ns)
            t_text = t.text[:20] if t is not None and t.text else ''
            
            run_info.append(f"  Run: [{', '.join(info)}] '{t_text}'")
        
        # Only show first 60 chars of text
        prefix = text[:60].strip()
        section = ""
        if "GTM" in text or "discovery" in text or "revenue" in text or "funnel" in text:
            section = "[PAIRWIRE]"
        elif "dashboard" in text or "reporting" in text or "keynote" in text or "Future Trends" in text or "ROAS" in text:
            section = "[GOOGLE]"
        elif "Amazon" in text or "Portugal" in text and "KPI" in text:
            section = "[AMAZON]"
        elif "EY" in text or "financial statements" in text or "asset" in text:
            section = "[EY]"
        
        print(f"\n{section} {prefix}...")
        print(f"  Justify: {jc_val} | ParaSpacing:{p_spacing_info or ' none'}")
        print(f"  Runs: {len(runs)}")
        for ri in run_info:
            print(f"    {ri}")

analyze_doc(SRC, "TAILORED (spacing issue)")
print("\n\n")
analyze_doc(ORIG, "ORIGINAL (for comparison)")
