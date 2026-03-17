# CLAUDE.md — land-dev-support

## Project Overview
AI-powered bilingual (English/Spanish) customer support Q&A system for a municipal
Land Development Services department. Handles questions about commercial permits,
residential permits, and plot/land verification before permanent construction.

## Purpose
- Answer citizen questions instantly using GPT-4o-mini
- Detect question language (English or Spanish) and respond in the same language
- Track response turnaround time per question
- Collect satisfaction feedback after each answer
- Save full session log to session_log.json for review

## Main File
- `land_dev_support.ipynb` — the main notebook (run all cells top to bottom)

## Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Then add your OPENAI_API_KEY to .env

# Launch notebook
jupyter notebook land_dev_support.ipynb
```

## Scripts
- `scripts/` — reserved for future privileged operations (backups, deploys)

## Key Files
| File | Purpose |
|------|---------|
| `land_dev_support.ipynb` | Main Q&A notebook |
| `faq.md` | Sample FAQ fed to the AI as context |
| `session_log.json` | Auto-generated session history |
| `.env` | API keys (never commit) |
| `.env.example` | Template for API keys |

## API Keys
- `OPENAI_API_KEY` — loaded from `.env` via `python-dotenv`

## Coding Style
- Comments only for non-obvious logic
- Never hardcode credentials — always use `.env`
- Never run sudo manually — always use `scripts/`

## Workflow
1. Always read CHECKLIST.md before making changes
2. Update CHECKLIST.md after EVERY change
3. End every response with a ✅ summary of files changed

## Resume Instructions
1. `cd /home/jbaez120/Projects/land-dev-support`
2. `source .venv/bin/activate`
3. Check CHECKLIST.md for current status
4. Open `land_dev_support.ipynb` in Jupyter
5. Run all cells top to bottom
