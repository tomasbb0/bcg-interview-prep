# CV DOCX Manipulation Cheat Sheet

**Purpose:** Reference for ANY future CV edits via Python. This documents exactly how
Tomás's CV DOCX works internally, what tools work, what doesn't, and the proven approach.

---

## 1. SOURCE FILES

| File | Path | Purpose |
|------|------|---------|
| **Original CV** | `~/Library/Mobile Documents/com~apple~CloudDocs/Professional/2 - My Stuff/CV/TomásBatalha_Resume_02_2026.docx` | Source of truth. ALWAYS start fresh from this. |
| **Working Script** | `0_ACTIVE_NOW/Google_AE_Application/tailor_cv_final2.py` | The proven script that works. Copy and modify for new roles. |
| **Output** | `~/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE.docx` | Generated tailored CV |
| **VBA Macros** | `_Tools/CV_Editor/CV_Editor_Complete.bas` | Interactive Word macros (cannot be called from Python) |

---

## 2. WHAT WORKS vs WHAT DOESN'T

### ✅ USE: lxml + zipfile (direct XML editing)
```python
import zipfile
from lxml import etree

with zipfile.ZipFile(SOURCE) as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)
# ... manipulate tree ...

modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)
```

### ❌ DON'T USE: python-docx
- **Why:** python-docx's table API can't see content inside fragmented XML runs
- **Specifically:** It misses Pairwire and Education sections entirely
- **Root cause:** The CV uses complex table nesting; python-docx flattens/misses nested table content

### ❌ DON'T USE: Adding/removing table rows
- Removing "empty" rows deletes section headers (EXPERIENCE, EDUCATION, etc.)
- Adding rows duplicates content (Pairwire duplication bug)
- **Rule:** Only modify TEXT within existing paragraphs and INDENT properties. Never add/remove structural elements.

---

## 3. DOCUMENT STRUCTURE

### Overall Layout
The CV is built entirely from **tables** (no body-level paragraphs for content).
Total: 9 tables, some NESTED inside others.

### Table Map

```
tbl#0 (tblInd=180) — Main Experience container
├── Row with: Pairwire header + dates
├── Row with: tbl#1 (tblInd=0) — Pairwire bullets (4 bullets, numId=14)
├── Row with: Google header + dates
├── Row with: Google bullets (3 bullets, numId=2)
├── Row with: Amazon header + dates
├── Row with: Amazon bullets (4 bullets, numId=2)
...

tbl#2 (tblInd=113) — EY
├── Row with: EY header + dates
├── Row with: EY bullets (2 bullets, numId=2)

tbl#3 (tblInd=142) — Fintech + Education container
├── Row with: Fintech header + dates
├── Rows with: Fintech bullets (3 bullets, numId=2)
├── Row with: tbl#4 (tblInd=0) — Education container
│   ├── NUS header + bullets (numId=5)
│   ├── Rotterdam header + bullets (numId=5)
│   ├── Row with: tbl#5 (tblInd=117) — NOVA Education
│   │   ├── NOVA header
│   │   ├── NOVA bullets (numId=4, numId=3)
│   ...

tbl#6 (tblInd=117) — Leadership: Nova Tech Club
├── Bullets (numId=2)

tbl#7 (tblInd=117) — Leadership: Social Consulting + Thirst Project
├── Bullets (numId=2)

tbl#8 (tblInd=180) — Skills section
├── Skills content (no bullets)
```

### Key Nesting Depths
| Section | Nesting Chain | Total tblInd |
|---------|--------------|-------------|
| Pairwire bullets | tbl#0 → tbl#1 | 180 + 0 = **180** |
| Google/Amazon bullets | tbl#0 only | **180** |
| EY bullets | tbl#2 only | **113** |
| Fintech bullets | tbl#3 only | **142** |
| NUS/Rotterdam Education | tbl#3 → tbl#4 | 142 + 0 = **142** |
| NOVA Education | tbl#3 → tbl#4 → tbl#5 | 142 + 0 + 117 = **259** |
| Leadership (Tech Club) | tbl#6 only | **117** |
| Leadership (Social/Thirst) | tbl#7 only | **117** |

---

## 4. BULLET INDENTATION — THE CRITICAL FORMULA

### How Word Calculates Absolute Position
```
Absolute Dash Position = SUM(all ancestor tblInd) + paragraph_left - paragraph_hanging
Absolute Text Position = SUM(all ancestor tblInd) + paragraph_left
```

### To Align ALL Bullets to the Same Page Position
```python
TARGET_ABS_TEXT = 854    # Matches Google/Amazon standard
TARGET_HANGING = 425     # Constant for all bullets

# For each bullet paragraph:
total_tbl_ind = sum_all_ancestor_table_indents(paragraph)
para_left = TARGET_ABS_TEXT - total_tbl_ind
# Set: left=para_left, hanging=TARGET_HANGING
```

### Per-Section Values (when target = 854/425)
| Section | total_tblInd | para_left | abs_dash | abs_text |
|---------|-------------|-----------|----------|----------|
| Pairwire | 180 | 674 | 429 | 854 |
| Google/Amazon | 180 | 674 | 429 | 854 |
| EY | 113 | 741 | 429 | 854 |
| Fintech | 142 | 712 | 429 | 854 |
| NUS/Rotterdam | 142 | 712 | 429 | 854 |
| NOVA | 259 | 595 | 429 | 854 |
| Leadership | 117 | 737 | 429 | 854 |

### Critical Notes
- Paragraph-level `w:ind` OVERRIDES numbering definition indent (abstractNum)
- Only values PRESENT in paragraph ind override; absent values fall back to numbering def
- Always set BOTH `left` AND `hanging` explicitly to fully control position
- Remove `firstLine` attribute if present (conflicts with hanging)

---

## 5. TEXT REPLACEMENT — THE SAFE APPROACH

### How to Find Paragraphs
```python
# Match by first N characters of original text
prefix = "Designed and automated three globall"  # First ~35 chars
for p in tree.findall('.//w:p', NSMAP):
    text = get_para_text(p).strip()
    if text.startswith(prefix):
        set_para_text(p, new_full_text)
        break
```

### How to Replace Text (Preserving Formatting)
```python
def set_para_text(p, new_text):
    """Replace ALL text in a paragraph. Keeps first run's formatting, removes extra runs."""
    runs = p.findall('.//w:r', NSMAP)
    if not runs:
        return
    # Remove all runs except the first (preserves first run's rPr = font/size/bold)
    for run in runs[1:]:
        run.getparent().remove(run)
    # Set text on remaining run
    t = runs[0].find('.//w:t', NSMAP)
    if t is not None:
        t.text = new_text
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
```

### Why Multiple Runs Exist
Word splits text into multiple `<w:r>` (run) elements when:
- Different formatting mid-paragraph (bold, italic, font change)
- Track changes or spell check marks
- Manual editing creates split points

The CV has MANY fragmented runs — some single words are their own run.
`set_para_text()` collapses everything to one run, using the first run's formatting.

---

## 6. FONT & SIZE REFERENCE

| Element | Font Size (pt) | EMU Value | Bold |
|---------|---------------|-----------|------|
| Name (title) | 11 | 139700 | No |
| Section headers (EXPERIENCE, etc.) | 9 | 114300 | Yes |
| Body text / bullets | 7.5 | 95250 | No |
| Company names | 7.5 | 95250 | Yes |
| Dates | 7.5 | 95250 | No |

---

## 7. NUMBERING DEFINITIONS

| numId | abstractNumId | Bullet Char | Default left | Default hanging | Used By |
|-------|--------------|-------------|-------------|----------------|---------|
| 2 | 14 | - | 720 | 360 | Google, Amazon, EY, Fintech, Leadership |
| 3 | 10 | - | 720 | 360 | NOVA Education |
| 4 | 7 | - | 720 | 360 | NOVA Education (GPA) |
| 5 | 8 | - | 720 | 360 | NUS, Rotterdam Education |
| 14 | 3 | - | 609 | 360 | Pairwire |

**Note:** These default values are overridden by paragraph-level `w:ind` when present.
Always set explicit paragraph-level indent to avoid relying on these inconsistent defaults.

---

## 8. XML NAMESPACE

```python
NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

def qn(tag):
    """Qualified name helper."""
    return f'{{{W}}}{tag}'
```

---

## 9. WORKFLOW FOR TAILORING CV TO A NEW ROLE

1. **Copy `tailor_cv_final2.py`** to new application folder
2. **Update SOURCE/OUTPUT paths**
3. **Update the `replacements` dict** with new bullet text
   - Match originals by first ~35 characters
   - Keep new text roughly same LENGTH as original (prevent 2-page overflow)
4. **Run the script** — it handles fresh copy + text replacement + indent normalization
5. **Open in Word** — verify 1-page fit and visual alignment
6. **If bullets are too long:** Shorten individual bullet text (aim for same line count as original)

### Length Guidelines
- Max ~140 characters per bullet for single-line bullets at 7.5pt in this layout
- If original was 2 lines, new text can be ~250 characters
- Always check in Word — character count isn't exact due to proportional fonts

---

## 10. COMMON PITFALLS & FIXES

| Problem | Cause | Fix |
|---------|-------|-----|
| Bullets misaligned | Nested tables with different tblInd | Sum ALL ancestor tblInd, set para_left = 854 - total |
| Pairwire not visible via python-docx | Fragmented XML runs in nested table | Use lxml direct XML access instead |
| Content duplicated | Script added new rows instead of editing existing | Only edit text in existing paragraphs |
| Section headers disappeared | Script removed "empty" table rows | Never remove rows |
| 2-page CV | Replacement text too long | Shorten bullets to match original length |
| Dashes in text (em/en dash) | User wants no dashes except date ranges and bullet markers | Search for \u2013, \u2014 and remove/replace |
| Date ranges broken | Dash removal caught date range dashes too | Use targeted regex that preserves digit-dash-digit patterns |

---

## 11. DEBUGGING TOOLS CREATED

These scripts exist in `0_ACTIVE_NOW/Google_AE_Application/` and can be reused:

| Script | Purpose |
|--------|---------|
| `analyze_tables.py` | Dump table structure: widths, indents, grid columns, cell margins |
| `trace_nesting.py` | Trace full ancestor chain for every bullet paragraph |
| `dump_cv_text.py` | Extract all text (python-docx, incomplete) |
| `search_pairwire.py` | Search raw XML for specific text strings |

---

*Last updated: June 2025 — after successfully aligning all bullets across 9 tables with 3 levels of nesting.*
