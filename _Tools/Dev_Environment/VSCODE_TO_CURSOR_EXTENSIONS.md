# VS Code Extensions → Cursor Equivalents

**Generated:** February 2026

## Your Current VS Code Extensions

| VS Code Extension                                | Purpose             | Cursor Status   | Notes                                                     |
| ------------------------------------------------ | ------------------- | --------------- | --------------------------------------------------------- |
| **github.copilot**                               | AI code completion  | ❌ **REMOVE**   | Cursor has built-in AI (Claude/GPT-4) — Copilot conflicts |
| **github.copilot-chat**                          | AI chat             | ❌ **REMOVE**   | Cursor Chat is native and better integrated               |
| **google.geminicodeassist**                      | Gemini AI assistant | ❌ **REMOVE**   | Conflicts with Cursor's AI — pick one                     |
| **ms-python.python**                             | Python support      | ✅ **KEEP**     | Works in Cursor, essential                                |
| **ms-python.vscode-pylance**                     | Python IntelliSense | ✅ **KEEP**     | Works in Cursor                                           |
| **ms-python.debugpy**                            | Python debugging    | ✅ **KEEP**     | Works in Cursor                                           |
| **ms-python.vscode-python-envs**                 | Python environments | ✅ **KEEP**     | Works in Cursor                                           |
| **ms-toolsai.jupyter**                           | Jupyter notebooks   | ✅ **KEEP**     | Works in Cursor                                           |
| **ms-toolsai.jupyter-keymap**                    | Jupyter keybindings | ✅ **KEEP**     | Works in Cursor                                           |
| **ms-toolsai.jupyter-renderers**                 | Jupyter output      | ✅ **KEEP**     | Works in Cursor                                           |
| **ms-toolsai.vscode-jupyter-cell-tags**          | Cell tags           | ✅ **KEEP**     | Works in Cursor                                           |
| **ms-toolsai.vscode-jupyter-slideshow**          | Slideshow           | ✅ **KEEP**     | Works in Cursor                                           |
| **esbenp.prettier-vscode**                       | Code formatter      | ✅ **KEEP**     | Works in Cursor                                           |
| **pkief.material-icon-theme**                    | File icons          | ✅ **KEEP**     | Works in Cursor                                           |
| **zhuangtongfa.material-theme**                  | Color theme         | ✅ **KEEP**     | Works in Cursor                                           |
| **ritwickdey.liveserver**                        | Local dev server    | ✅ **KEEP**     | Works in Cursor                                           |
| **mechatroner.rainbow-csv**                      | CSV highlighting    | ✅ **KEEP**     | Works in Cursor                                           |
| **tomoki1207.pdf**                               | PDF viewer          | ✅ **KEEP**     | Works in Cursor                                           |
| **cirlorm.mobileview**                           | Mobile preview      | ✅ **KEEP**     | Works in Cursor                                           |
| **github.codespaces**                            | GitHub Codespaces   | ⚠️ **OPTIONAL** | Only if you use Codespaces                                |
| **github.vscode-github-actions**                 | GitHub Actions      | ✅ **KEEP**     | Works in Cursor                                           |
| **googlecloudtools.cloudcode**                   | Google Cloud        | ⚠️ **OPTIONAL** | Only if using GCP                                         |
| **googlecloudtools.firebase-dataconnect-vscode** | Firebase            | ⚠️ **OPTIONAL** | Only if using Firebase                                    |
| **hasanakg.firebase-snippets**                   | Firebase snippets   | ⚠️ **OPTIONAL** | Only if using Firebase                                    |
| **me-dutour-mathieu.vscode-firebase**            | Firebase tools      | ⚠️ **OPTIONAL** | Only if using Firebase                                    |
| **toba.vsfire**                                  | Firestore rules     | ⚠️ **OPTIONAL** | Only if using Firebase                                    |
| **graphql.vscode-graphql-syntax**                | GraphQL syntax      | ✅ **KEEP**     | Works in Cursor                                           |
| **ms-vscode.vscode-speech**                      | Voice input         | ⚠️ **CHECK**    | May conflict with Cursor voice features                   |

---

## Migration Commands

### Install extensions in Cursor (run in terminal):

```bash
# Essential Python stack
cursor --install-extension ms-python.python
cursor --install-extension ms-python.vscode-pylance
cursor --install-extension ms-python.debugpy
cursor --install-extension ms-python.vscode-python-envs

# Jupyter
cursor --install-extension ms-toolsai.jupyter
cursor --install-extension ms-toolsai.jupyter-keymap
cursor --install-extension ms-toolsai.jupyter-renderers
cursor --install-extension ms-toolsai.vscode-jupyter-cell-tags
cursor --install-extension ms-toolsai.vscode-jupyter-slideshow

# Formatting & themes
cursor --install-extension esbenp.prettier-vscode
cursor --install-extension pkief.material-icon-theme
cursor --install-extension zhuangtongfa.material-theme

# Dev tools
cursor --install-extension ritwickdey.liveserver
cursor --install-extension mechatroner.rainbow-csv
cursor --install-extension tomoki1207.pdf
cursor --install-extension cirlorm.mobileview
cursor --install-extension graphql.vscode-graphql-syntax

# GitHub (optional)
cursor --install-extension github.vscode-github-actions
```

### One-liner (copy-paste this):

```bash
cursor --install-extension ms-python.python && cursor --install-extension ms-python.vscode-pylance && cursor --install-extension ms-python.debugpy && cursor --install-extension ms-toolsai.jupyter && cursor --install-extension esbenp.prettier-vscode && cursor --install-extension pkief.material-icon-theme && cursor --install-extension zhuangtongfa.material-theme && cursor --install-extension ritwickdey.liveserver && cursor --install-extension mechatroner.rainbow-csv
```

---

## Key Differences: VS Code vs Cursor

| Feature           | VS Code                | Cursor                  |
| ----------------- | ---------------------- | ----------------------- |
| AI Assistant      | Copilot (paid extra)   | Built-in Claude/GPT-4   |
| AI Chat           | Copilot Chat extension | Native Cmd+K / Cmd+L    |
| Codebase context  | Limited                | Full repo understanding |
| Price             | Free + $10/mo Copilot  | $20/mo (includes AI)    |
| Extension support | Full                   | 99% compatible          |

---

## DO NOT INSTALL in Cursor

- `github.copilot` — conflicts with Cursor AI
- `github.copilot-chat` — redundant
- `google.geminicodeassist` — conflicts with Cursor AI
- Any other AI coding assistant extensions

---

## Settings to Copy

Your VS Code settings at: `~/Library/Application Support/Code/User/settings.json`
Cursor settings at: `~/Library/Application Support/Cursor/User/settings.json`

To copy settings:

```bash
cp ~/Library/Application\ Support/Code/User/settings.json ~/Library/Application\ Support/Cursor/User/settings.json
```

---

_Note: Cursor is built on VS Code, so most extensions work identically. The main change is removing AI assistants that conflict with Cursor's native AI._
