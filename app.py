"""Simple web portal for Land Development Services AI support.

Run this script and open http://127.0.0.1:7860 in your browser.

It provides:
- A searchable FAQ table (loaded from faq.md)
- A text box to ask questions (English/Spanish)
- A session log saved to session_log.json

Dependencies are listed in requirements.txt.
"""

from __future__ import annotations

import json
import os
import time
import traceback
from pathlib import Path

import openai
import gradio as gr
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=False)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# Paths
ROOT = Path(__file__).resolve().parent
FAQ_PATH = ROOT / "faq.md"
SESSION_LOG_PATH = ROOT / "session_log.json"

# In-memory session log
session_log: list[dict] = []


def load_faq(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()

    entries: list[dict[str, str]] = []
    question = None
    answer_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("**Q:") and stripped.endswith("**"):
            if question is not None:
                entries.append({"question": question, "answer": " ".join(answer_lines).strip()})
                answer_lines = []
            question = stripped[4:-2].strip()
        elif question is not None:
            answer_lines.append(line.rstrip())
    if question is not None:
        entries.append({"question": question, "answer": " ".join(answer_lines).strip()})
    return entries


def faq_markdown(entries: list[dict[str, str]]) -> str:
    if not entries:
        return "**No FAQ entries found. Make sure `faq.md` exists.**"
    md_lines = ["# FAQ", "", "| Question | Answer |", "|---|---|"]
    for e in entries:
        q = e["question"].replace("|", "\\|")
        a = e["answer"].replace("|", "\\|")
        md_lines.append(f"| {q} | {a} |")
    md_lines.append("")
    md_lines.append(f"*Showing {len(entries)} FAQ entries.*")
    return "\n".join(md_lines)


def _detect_language(question: str) -> str:
    spanish_indicators = [
        "¿",
        "¡",
        " cómo ",
        " qué ",
        " permiso",
        "permiso",
        "remodel",
        "requisitos",
        "zona",
        "zonificación",
    ]
    lower = question.lower()
    for token in spanish_indicators:
        if token in lower:
            return "spanish"
    return "english"


def ask_land_support(question: str) -> str:
    question = question.strip()
    if not question:
        return "Please enter a question."

    if not OPENAI_API_KEY:
        mock_answer = (
            "OPENAI_API_KEY is missing. To get real AI responses, copy `.env.example` to `.env` and set your key.\n\n"
            "Meanwhile, use the FAQ table on the left for common questions."
        )
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "question": question,
            "language": "unknown",
            "answer": mock_answer,
            "response_time_seconds": 0.0,
        }
        session_log.append(entry)
        _save_session_log()
        return mock_answer

    language = _detect_language(question)
    system_prompt = (
        "You are an AI assistant for a municipal Land Development Services department. "
        "Answer the question in the same language that the user asked it (English or Spanish). "
        "Use the provided FAQ context when possible."
    )

    start = time.time()
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.2,
        )
        elapsed = time.time() - start

        answer = response.choices[0].message.content.strip()

    except Exception as e:
        # Log the full traceback to the console for debugging
        traceback.print_exc()
        answer = f"Error: {type(e).__name__}: {e}"
        elapsed = 0.0

    entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "question": question,
        "language": language,
        "answer": answer,
        "response_time_seconds": round(elapsed, 3),
    }
    session_log.append(entry)
    _save_session_log()
    return answer


def _save_session_log() -> None:
    try:
        SESSION_LOG_PATH.write_text(json.dumps(session_log, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def get_session_log_md() -> str:
    if not session_log:
        return "**No session entries yet. Ask a question to get started.**"

    md_lines = ["# Session Log", "", "| # | Question | Answer | Time (s) |", "|---|---|---|---|"]
    for idx, e in enumerate(session_log, start=1):
        q = e["question"].replace("|", "\\|")
        a = e["answer"].replace("|", "\\|")
        t = e.get("response_time_seconds", "")
        md_lines.append(f"| {idx} | {q} | {a} | {t} |")
    return "\n".join(md_lines)


def main() -> None:
    faq_entries = load_faq(FAQ_PATH)
    faq_md = faq_markdown(faq_entries)

    with gr.Blocks(title="Land Development Services — AI Support") as demo:
        gr.Markdown("## Land Development Services — AI Support")
        gr.Markdown(
            "Ask a question in English or Spanish and get an answer based on the FAQ and AI. "
            "Your session will be logged to `session_log.json`."
        )

        with gr.Row():
            with gr.Column(scale=2):
                faq_display = gr.Markdown(faq_md)

            with gr.Column(scale=1):
                question_input = gr.Textbox(
                    label="Your question",
                    placeholder="What permits do I need to build a new home?",
                    lines=3,
                )
                answer_output = gr.Textbox(label="Answer", interactive=False)
                submit = gr.Button("Ask")
                session_log_md = gr.Markdown(get_session_log_md())

                def on_submit(question: str):
                    answer = ask_land_support(question)
                    return answer, get_session_log_md()

                submit.click(on_submit, inputs=[question_input], outputs=[answer_output, session_log_md])

    # Bind to 0.0.0.0 so the app is reachable from other machines on the network
    # (e.g., when connected via SSH to a server).
    # You can override the port by setting GRADIO_PORT in your environment.
    port = int(os.getenv("GRADIO_PORT", "7860"))
    host = "0.0.0.0"

    print(f"🚀 Starting web portal on http://{host}:{port} (open from your browser)")
    print("   (use SSH port forwarding if you want to access it locally: ssh -L 7860:localhost:7860 <user>@<host>)")

    demo.launch(server_name=host, server_port=port)


if __name__ == "__main__":
    main()
