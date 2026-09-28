# AI Quiz & Assessment Platform

Flask-based AI-powered CBT quiz platform with Gemini question generation, validation, evaluation, and analytics.

## Current Version Notes

- This version is **session-based** and **does not use a database**.
- Active exam state is kept in Flask session + server-side in-memory application state.
- Persistent exam history is intentionally not included in this prototype.

## Setup

```bash
cd quiz_platform
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

Open `http://127.0.0.1:5000`.

## Candidate Flow

1. Home
2. Candidate details (Name, Roll Number, Section)
3. Roll number validation + decoded details confirmation
4. Exam configuration
5. AI question generation
6. Exam
7. Submit
8. Results
9. Review

## Features

- Gemini-generated structured questions with Pydantic validation
- NBKRIST roll-number parser/decoder with user-friendly validation errors
- Timed CBT interface with navigation and review states
- Python-side scoring (single, multiple, true/false + partial scoring + negative marking)
- Result dashboard with Chart.js visualizations
- Review filtering (all/correct/incorrect/partial/unanswered)
