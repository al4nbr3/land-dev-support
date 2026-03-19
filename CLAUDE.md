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

## Main Files
- `land_dev_support.ipynb` — the main notebook (run all cells top to bottom)
- `app.py` — Gradio web portal (question UI + session logging)

## Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Then add your OPENAI_API_KEY to .env

# Launch notebook (optional)
jupyter notebook land_dev_support.ipynb

# Launch web portal (recommended)
source .venv/bin/activate
python app.py

# If you are accessing from another machine, use SSH port forwarding:
# (run this on your local machine, not on the server)
ssh -L 7860:localhost:7860 <user>@<host>
# Then open:
# http://localhost:7860
```

## Scripts
- `scripts/ufw-allow-gradio.sh` — open the Gradio port in UFW (default 7860)

## Key Files
| File | Purpose |
|------|---------|
| `land_dev_support.ipynb` | Main Q&A notebook |
| `app.py` | Web portal UI (Gradio) |
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
