# AI Quiz & Assessment Platform

Flask-based AI-powered CBT quiz platform with Gemini question generation, validation, evaluation, and analytics.

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

## Features
- Candidate intake and exam configuration
- Gemini-generated structured questions with Pydantic validation
- Timed CBT interface with navigation and review states
- Python-side scoring (single, multiple, true/false + partial scoring)
- Result dashboard with Chart.js visualizations
- Attempt history with access isolation per candidate
