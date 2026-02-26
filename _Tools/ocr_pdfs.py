#!/usr/bin/env python3
"""OCR all CaseCoach PDFs from Downloads and save text output."""
import fitz  # PyMuPDF
import os

DOWNLOADS = os.path.expanduser("~/Downloads")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "0_ACTIVE_NOW", "BCG_Interview_Prep", "pdf_extracts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# CaseCoach course PDFs (no duplicates)
PDF_FILES = [
    "Top-10-case-frameworks.pdf",
    "The-AIM-test.pdf",
    "How-to-build-a-structure.pdf",
    "Academic-frameworks.pdf",
    "Logical-frameworks.pdf",
    "How-to-communicate-your-structure.pdf",
    "Case-structuring-in-action.pdf",
    "How-to-identify-insights.pdf",
    "Estimations-and-market-sizing.pdf",
    "Case-scorecard.pdf",
    "Fit-scorecard.pdf",
    "scorecard.pdf",
]

for pdf_name in PDF_FILES:
    pdf_path = os.path.join(DOWNLOADS, pdf_name)
    if not os.path.exists(pdf_path):
        print(f"SKIP: {pdf_name} not found")
        continue
    
    doc = fitz.open(pdf_path)
    text_parts = []
    for page_num, page in enumerate(doc, 1):
        text = page.get_text()
        if text.strip():
            text_parts.append(f"--- PAGE {page_num} ---\n{text}")
    doc.close()
    
    out_name = pdf_name.replace(".pdf", ".txt")
    out_path = os.path.join(OUTPUT_DIR, out_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(text_parts))
    
    print(f"OK: {pdf_name} -> {out_name} ({len(text_parts)} pages)")

print(f"\nAll done. Output in: {OUTPUT_DIR}")
