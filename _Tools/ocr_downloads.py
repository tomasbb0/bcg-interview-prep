#!/usr/bin/env python3
"""OCR all recent screenshots and extract PDF text from Downloads folder."""
import os
import subprocess
from pathlib import Path
from PIL import Image
import pytesseract

downloads = Path.home() / "Downloads"

# All the files from the last ~15 minutes (Feb 24 00:33-00:38 batch + cover letter + examples)
screenshot_files = [
    "Screenshot 2026-02-24 at 00.37.20.png",
    "Screenshot 2026-02-24 at 00.37.20 (2).png",
    "Screenshot 2026-02-24 at 00.37.22.png",
    "Screenshot 2026-02-24 at 00.37.25.png",
    "Screenshot 2026-02-24 at 00.37.40.png",
    "Screenshot 2026-02-24 at 00.37.44.png",
    "Screenshot 2026-02-24 at 00.37.48.png",
    "Screenshot 2026-02-24 at 00.37.59.png",
    "Screenshot 2026-02-24 at 00.38.02.png",
    "Screenshot 2026-02-24 at 00.38.05.png",
    "Screenshot 2026-02-24 at 00.38.09.png",
    "Screenshot 2026-02-24 at 00.38.12.png",
    "Screenshot 2026-02-24 at 00.38.15.png",
]

pdf_files = [
    "Examples_resumes.pdf",
    "Cover_letter_examples.pdf",
    "Resume Template 4.pdf",
]

rtf_file = "Cover_letter_template.rtf"

# Also include the slightly older screenshots
older_screenshots = [
    "Screenshot 2026-02-23 at 22.42.15.png",
    "Screenshot 2026-02-23 at 22.42.25.png",
    "Screenshot 2026-02-23 at 22.42.30.png",
    "Screenshot 2026-02-23 at 21.46.32.png",
    "Screenshot 2026-02-23 at 21.46.37.png",
]

output = []

# OCR Screenshots
print("=" * 80)
print("OCR-ing SCREENSHOTS")
print("=" * 80)

for fname in screenshot_files + older_screenshots:
    fpath = downloads / fname
    if fpath.exists():
        print(f"\n--- {fname} ---")
        try:
            img = Image.open(fpath)
            text = pytesseract.image_to_string(img)
            print(text)
            output.append(f"\n\n### FILE: {fname}\n{text}")
        except Exception as e:
            print(f"ERROR: {e}")
    else:
        print(f"NOT FOUND: {fname}")

# Extract PDF text
print("\n" + "=" * 80)
print("EXTRACTING PDF TEXT")
print("=" * 80)

for fname in pdf_files:
    fpath = downloads / fname
    if fpath.exists():
        print(f"\n--- {fname} ---")
        try:
            result = subprocess.run(
                ["pdftotext", "-layout", str(fpath), "-"],
                capture_output=True, text=True, timeout=30
            )
            print(result.stdout[:5000])  # First 5000 chars
            output.append(f"\n\n### FILE: {fname}\n{result.stdout}")
        except Exception as e:
            print(f"ERROR: {e}")
    else:
        print(f"NOT FOUND: {fname}")

# Extract RTF text
print("\n" + "=" * 80)
print("EXTRACTING RTF TEXT")
print("=" * 80)

rtf_path = downloads / rtf_file
if rtf_path.exists():
    print(f"\n--- {rtf_file} ---")
    try:
        result = subprocess.run(
            ["textutil", "-convert", "txt", "-stdout", str(rtf_path)],
            capture_output=True, text=True, timeout=30
        )
        print(result.stdout[:5000])
        output.append(f"\n\n### FILE: {rtf_file}\n{result.stdout}")
    except Exception as e:
        print(f"ERROR: {e}")

# RTF resume templates
print("\n" + "=" * 80)
print("EXTRACTING RESUME TEMPLATE RTFs")
print("=" * 80)
templates_dir = downloads / "Resume_templates"
if templates_dir.exists():
    for rtf in sorted(templates_dir.glob("*.rtf")):
        print(f"\n--- {rtf.name} ---")
        try:
            result = subprocess.run(
                ["textutil", "-convert", "txt", "-stdout", str(rtf)],
                capture_output=True, text=True, timeout=30
            )
            print(result.stdout[:3000])
            output.append(f"\n\n### FILE: {rtf.name}\n{result.stdout}")
        except Exception as e:
            print(f"ERROR: {e}")

# Save all output
outpath = Path("/Users/tomasbatalha/Projects/Planning and Advisory/Tomas_Batalha_Future_Plan/_Tools/ocr_output.md")
with open(outpath, "w", encoding="utf-8") as f:
    f.write("# OCR Output from Downloads\n")
    f.write("\n".join(output))

print(f"\n\nAll output saved to {outpath}")
