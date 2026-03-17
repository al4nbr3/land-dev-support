# Land Development Services — AI Customer Support

Bilingual (English / Spanish) AI-powered Q&A assistant for a municipal Land Development Services department.

## What it does

- Answers citizen questions about **commercial permits**, **residential permits**, and **plot/land verification**
- Detects question language (English or Spanish) and responds in the same language
- Tracks **response turnaround time** per question
- Collects **satisfaction feedback** after every answer
- Asks if the citizen needs a **human agent** if unsatisfied
- Saves full **session log** to `session_log.json`
- Prints a **session summary report** at the end

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/al4nbr3/land-dev-support.git
cd land-dev-support
```

**2. Create virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**3. Configure API key**
```bash
cp .env.example .env
nano .env   # add your OPENAI_API_KEY
```

**4. Launch the notebook**
```bash
jupyter notebook land_dev_support.ipynb
```

## How to use

1. Run all cells top to bottom (Shift+Enter)
2. In **Cell 7**, change the `question` variable to what a citizen would ask
3. The AI responds in the same language as the question
4. Answer the satisfaction prompts after each response
5. Run **Cell 10** at the end to save the log and see the summary report

## Sample questions

**English:**
- `"What permits do I need to build a new home?"`
- `"How do I verify if my land is approved for construction?"`
- `"How long does a commercial permit take to be approved?"`

**Spanish:**
- `"¿Qué permisos necesito para construir una casa?"`
- `"¿Cómo verifico si mi terreno está aprobado para construcción permanente?"`
- `"¿Cuánto tiempo tarda un permiso comercial?"`

## Session Log

Every interaction is saved to `session_log.json` with:
- Timestamp
- Question asked
- AI response
- Response time (seconds)
- Satisfaction (yes/no)
- Needed human agent (yes/no)

## Replacing the FAQ

The AI's knowledge comes from `faq.md`. To use real department content:
1. Replace the content of `faq.md` with your actual department FAQ
2. Restart the notebook kernel and re-run all cells

## Roadmap
- [ ] Gradio web UI (after Week 2)
- [ ] Multi-turn conversation memory (after Week 3)
- [ ] Connect to real permit database
- [ ] Ollama/local model fallback
