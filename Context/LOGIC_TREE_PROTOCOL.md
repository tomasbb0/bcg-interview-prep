# LOGIC TREE PROTOCOL

**Trigger phrase:** "trigger logic tree protocol"

**Template file:** [LOGIC_TREE_TEMPLATE.html](LOGIC_TREE_TEMPLATE.html)

---

## ⚠️ CRITICAL SERVER RULES - NEVER FORGET ⚠️

```
╔══════════════════════════════════════════════════════════════════╗
║  🚨 AFTER EVERY HTML CHANGE:                                     ║
║                                                                  ║
║  1. RESTART SERVER:                                              ║
║     lsof -ti:8888 | xargs kill -9; sleep 1;                     ║
║     cd [folder] && python3 -m http.server 8888                  ║
║                                                                  ║
║  2. END EVERY MESSAGE WITH:                                      ║
║     🔗 **http://localhost:8888/LOGIC_TREE_YOUNG_WOOK.html**     ║
║                                                                  ║
║  NO EXCEPTIONS. EVER.                                            ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## When to Use This Protocol

- When you receive a message and need to decide how to respond
- When you're unsure of someone's true intentions
- When a decision has multiple possible outcomes depending on the other party's mindset
- When you want to "game out" a negotiation or conversation before committing
- When stakes are high and you want to avoid reactive/emotional responses
- When you need to see all possible paths before choosing one

---

## What This Protocol Does

When triggered, I will help you build a **decision logic tree** layer by layer. We map:
1. What THEY might be thinking (their intentions)
2. What YOU could do (your responses)
3. What THEY would do in reaction (their responses to your responses)
4. Optionally: Your counter-moves

This helps you choose a response that works across MULTIPLE possible intentions, not just the one you hope is true.

---

## The Process

1. **Layer 0 — The Trigger**
   - The event/message that starts the decision tree

2. **Layer 1 — Their Possible Intentions**
   - What THEY might be thinking/feeling
   - Ordered BEST to WORST (🥇 → 🥈 → 🥉)
   - Examples: Genuine Pause, Unsure, Soft No

3. **Layer 2 — Your Possible Responses**
   - What YOU could do in response
   - Ordered by best total outcomes (#1 → #2 → ...)
   - Each response shows outcome counters: `✓✓:X ✓:Y —:Z !:W ✗:V`

4. **Layer 3 — Their Personality Hypotheses**
   - Self-explanatory names (e.g., "Careful Committer", "Family First", "Always Comparing", "Polite Avoider")
   - Ordered by likelihood (HIGH → MED → LOW)

5. **Layer 4 — Their Possible Reactions**
   - How they respond based on personality × your response
   - Each has editable outcome state (dropdown: ✓✓/✓/—/!/✗)

---

## Three Views Available

1. **📊 Compact View** — Layer-by-layer horizontal columns
2. **🌲 Logic Tree** — Proper horizontal tree (root left → branches right with connecting lines)
3. **🔍 Interactive** — Same as Logic Tree but with expand/collapse buttons (+/−)

---

## Key Rules for Personality Assessment

- **Never assume** — always ask what I don't know
- **Start with foundation** — "Have you met them in person?" before "How do they handle conflict?"
- **One question at a time** — no batching questions
- **Multiple choice format** — easier for you to answer quickly
- **Build on previous answers** — each question should be informed by prior responses
- **Self-explanatory names** — personality types must be instantly understandable (e.g., "People Pleaser", "Always Comparing", "Careful Committer")

---

## Output Format

- The logic tree is generated as an **editable HTML file**
- Use the template at: `Context/LOGIC_TREE_TEMPLATE.html`
- Horizontal layout for easy visualization
- All text is editable directly in the browser
- File location: Same folder as the relevant context
- **Live updates:** The HTML file is updated in real-time as we build the tree together
- **Localhost viewing:** A local server is started so you can view changes live in browser
- **Hyperlink provided:** After EVERY response, I provide the same localhost URL at the end so you can refresh and see changes

---

## 🚨 SERVER MANAGEMENT (CRITICAL)

- **ALWAYS restart server after editing HTML** — no exceptions
- Before providing ANY localhost link, I MUST verify the server is running
- If user reports 404 error, I immediately:
  1. Check if file exists with `ls -la [folder]`
  2. Kill existing server: `pkill -f "python3 -m http.server 8888"`
  3. Restart the server with proper command
  4. Confirm server is active before providing link
- **Restart command (always use this):**
  ```bash
  pkill -f "python3 -m http.server 8888" 2>/dev/null; sleep 1; cd [folder] && python3 -m http.server 8888
  ```
- Server runs in background mode (`isBackground: true`)
- Default port: 8888
- Link format: `http://localhost:8888/[FILENAME].html`

---

## Ordering Rules (Always Applied by Default)

1. **Intentions:** Always ordered from BEST to WORST (🥇 → 🥈 → 🥉)
2. **Responses:** Always ordered from MOST to LEAST recommended (#1 → #2 → ...)
3. **Outcomes within responses:** Also ordered best → worst

---

## View Toggle

The HTML includes a toggle button at the top to switch between two views:

1. **📊 Compact View** (default): Layer-by-layer horizontal flow. Each response shows ALL outcomes for all intentions in a condensed format.

2. **🌲 Pure Logic Tree**: True horizontal tree structure:
   ```
   [Root] ─┬─ [Intention A] ─┬─ [Response #1] ─┬─ [Personality 1]
           │                 │                 ├─ [Personality 2]
           │                 │                 ├─ [Personality 3]
           │                 │                 └─ [Personality 4]
           │                 ├─ [Response #2]
           │                 ├─ [Response #3]
           │                 ├─ [Response #4]
           │                 └─ [Response #5]
           │
           ├─ [Intention C] ─┬─ [Response #1]
           │                 ├─ ...
           │                 └─ [Response #5]
           │
           └─ [Intention B] ─┬─ [Response #1]
                             └─ ...
   ```
   - Root node on far left
   - Each node branches right with connecting lines
   - Proper tree structure with vertical + horizontal connectors

3. **🔍 Interactive Tree**: Same structure as Pure Logic Tree but:
   - Each node with children has an expand/collapse button (+/−)
   - Click to expand or collapse branches
   - Great for focusing on specific paths

---

## HTML Toolbar Features

The HTML includes a fixed toolbar at the top with these buttons:

### Left Section:
| Button | Function |
|--------|----------|
| **↶ Undo** | Undo last change (also Cmd+Z) |
| **↷ Redo** | Redo undone change (also Cmd+Shift+Z) |
| **+ Add Node** | Prompts user to tell me in chat what to add |
| **🔄 Reset** | Resets to original state (requires confirmation) |

### Right Section:
| Button | Function |
|--------|----------|
| **← Return to Previous** | Appears after loading a version; returns to state before load |
| **📂 Load Version** | Opens file picker to load a previously saved HTML version |
| **💾 Save As** | Downloads current state as timestamped HTML file |
| **✓ Save** | Saves + shows changelog modal for user to copy & paste to chat |

### Center:
- Shows tree name
- Shows "● Unsaved changes" indicator when edits are pending

---

## Node Features

Each node (box) in the tree has:

1. **Delete button (✕)**: Appears on hover in top-right corner. Clicking removes the node with animation.
2. **Add branch button (+)**: Appears on hover in right side. Clicking prompts for new branch title/description.
3. **Editable content**: Click any text to edit directly
4. **Rank badges**: Show position (#1, #2, etc.) or quality (🥇 HIGH, 🥈 MED, 🥉 LOW)
5. **Recommended highlight**: Top choice has green glow + badge
6. **Outcome counter**: On Layer 1 response nodes, shows count of each outcome type: `✓✓:X ✓:Y —:Z !:W ✗:V`
7. **Outcome dropdown**: On Layer 3+ nodes, click the outcome icon to change state (✓✓/✓/—/!/✗)

---

## Outcome State Dropdowns

Each outcome in Layer 3+ has a clickable dropdown to change the state:
- Select from: ✓✓ (Best), ✓ (Good), — (Neutral), ! (Risky), ✗ (Bad)
- Color updates automatically based on selection
- Changes are tracked in changelog

---

## Changelog System

When user clicks **✓ Save**:
1. A modal appears showing all tracked changes
2. Format: `[timestamp] ACTION: "old text..." → "new text..."`
3. Actions tracked: EDITED, DELETED, DELETED BRANCH, UNDO, REDO, LOADED VERSION
4. User clicks "📋 Copy to Clipboard" and pastes in chat
5. I can then see what they changed and comment on good/bad choices

---

## CSS Classes Reference

### Personality nodes:
- `.personality-high` — green left border (most likely)
- `.personality-med` — yellow left border (medium likelihood)
- `.personality-low` — red left border (least likely)

### Response nodes:
- `.recommended` — green glow + badge (top choice)
- `.outcome-counter` — shows outcome counts at bottom of node
- Regular nodes have no special class

### Outcome icons/dropdowns:
- `.outcome-select.best` — green (✓✓)
- `.outcome-select.good` — lighter green (✓)
- `.outcome-select.neutral` — gray (—)
- `.outcome-select.risky` — yellow (!)
- `.outcome-select.bad` — red (✗)

### View states:
- `.compact-view` — shows `.tree-container`, hides `.pure-tree-container`
- `.pure-view` — shows `.pure-tree-container`, hides `.tree-container`

---

## HTML Structure Template

```html
<!-- COMPACT VIEW: Layer 1 - Intentions -->
<div class="node intention-best">
    <div class="rank-badge">🥇 BEST</div>
    <div class="node-title" contenteditable="true">[TITLE]</div>
    <div class="node-desc" contenteditable="true">[DESCRIPTION]</div>
</div>

<!-- COMPACT VIEW: Layer 2 - Responses with outcomes -->
<div class="node recommended">
    <div class="rank-badge">#1</div>
    <div class="node-title" contenteditable="true">[RESPONSE]</div>
    <div class="node-desc" contenteditable="true">[DESCRIPTION]</div>
    <div class="outcomes">
        <div class="outcome">
            <div class="outcome-icon best">✓✓</div>
            <span class="outcome-text" contenteditable="true">[INTENTION]: [OUTCOME]</span>
        </div>
    </div>
</div>

<!-- PURE VIEW: Intention branch with all responses -->
<div class="intention-branch">
    <div class="intention-header">
        <div class="node intention-best" style="margin:0;">...</div>
        <span style="color:#4ade80;font-size:24px;">→</span>
    </div>
    <div class="responses-row">
        <div class="response-branch">
            <div class="node recommended">...</div>
            <div class="single-outcome">
                <div class="outcome">...</div>
            </div>
        </div>
        <!-- Repeat for each response -->
    </div>
</div>
```

---

## Rules

- I **do not proceed** to the next layer until you explicitly confirm the current layer
- At each layer, you can ask me to add, remove, or modify branches
- The goal is to help you **see all possible paths** before choosing one
- After EVERY response, I provide the localhost link at the bottom

---

## Current Active Logic Tree

**Subject:** [To be filled when triggered]

**Status:** [Layer 1 / Layer 2 / Layer 3 / Complete]

---
