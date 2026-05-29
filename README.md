# Emergency Call Quality Grader

An AI-powered quality assurance system that automatically grades behavioral-health emergency call transcripts. The system uses a 2-step LLM workflow to extract evidence from transcripts and score call-taker performance against a 9-dimension rubric, then generates professional Word document (`.docx`) grading reports.

Note: This is a personal project built with public resources and synthetic data to explore a behavioral health crisis response use case, and it is not derived from any specific organization’s internal materials.

## How It Works

```
┌──────────────────┐     ┌─────────────────────┐     ┌───────────────────┐
│  Call Transcript  │────▶│  Step 1: Evidence    │────▶│  Step 2: Scoring  │
│  (raw text)       │     │  Extraction (LLM)    │     │  Against Rubric   │
└──────────────────┘     └─────────────────────┘     └────────┬──────────┘
                                                              │
                         ┌─────────────────────┐              │
                         │  Deterministic       │◀─────────────┘
                         │  Standardization     │
                         │  (guardrails)        │
                         └────────┬────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │  .docx Report Generation   │
                    │  (color-coded, templated)  │
                    └────────────────────────────┘
```

**Step 1 — Evidence Extraction**: The LLM analyzes the transcript and extracts structured evidence (location confirmation, medical assessment, naloxone inquiry, pre-arrival instructions, etc.) as JSON.

**Step 2 — Rubric Scoring**: A second LLM call scores the operator across 9 weighted dimensions using the extracted evidence and scoring anchors.

**Deterministic Standardization**: After the LLM scores, Python-based guardrails cap or force scores based on the extracted evidence flags. For example, if the evidence shows naloxone was never asked about during a suspected overdose, the Naloxone Inquiry score is forced to 1/5 regardless of what the LLM returned. This reduces scoring variability.

## Scoring Dimensions

| Dimension | Weight |
|---|---|
| Address & Location | 10% |
| Medical Assessment | 15% |
| Naloxone Inquiry | 15% |
| Pre-Arrival Instructions | 15% |
| Good Samaritan Disclosure | 10% |
| Dispatch Accuracy | 10% |
| Behavioral Health Diversion | 10% |
| Caller Management | 10% |
| Information Completeness | 5% |

## Project Structure

```
911_call_grader/
├── prototype/                  # Core application
│   ├── main.py                 # Entry point — runs demo calls
│   ├── workflow.py             # 2-step LLM grading workflow
│   ├── report_schema.py        # Data models & scoring logic
│   ├── render_docx.py          # Word document generation
│   ├── llm_nvidia.py           # NVIDIA API client
│   ├── sample_transcripts.py   # Demo call transcripts
│   └── template_builder.py     # Extracts single-scenario template from a multi-scenario report
├── templates/                  # Word document template
├── outputs/                    # Generated grading reports (gitignored)
├── dashboard-demo.html         # Standalone analytics dashboard (open in browser)
├── dashboard-demo.jsx          # Archived React reference (not wired/runnable in this repo)
├── call-grading-report.docx    # Source report for template generation
├── requirements.txt
├── .env.example
└── README.md
```

## Tech Stack

- **Python 3.10+** — Core application
- **NVIDIA NIM API** — LLM inference (Llama 3.1 8B Instruct)
- **python-docx** — Word document generation
- **Vanilla HTML/JS + Chart.js** — Analytics dashboard

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/911_call_grader.git
cd 911_call_grader

# 2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your API key
cp .env.example .env
# Edit .env and add your NVIDIA API key
# Get a free key at https://build.nvidia.com/
```

## Usage

### Run the Call Grader

```bash
python prototype/main.py
```

This processes the demo transcripts in `sample_transcripts.py` and generates `.docx` grading reports in the `outputs/` directory.

### View the Dashboard

Open `dashboard-demo.html` directly in your browser. The dashboard uses simulated data to demonstrate:

- Supervisor view with aggregate metrics, trend charts, and dispatch call analysis
- Individual call-taker view with per-dimension scoring
- Drill-down modals for call-level detail

Notes:
- The dashboard is a frontend-only demo with simulated data.
- The Python backend currently generates `.docx` reports; there is no API connection between backend outputs and dashboard data yet.
- Dashboard overall scores are calculated using the same weighted-dimension approach as the backend.
- `dashboard-demo.jsx` is kept only as an archived design reference.

## Output Example

Each generated report includes:
- **Call metadata** (ID, date, call-taker, duration, call type)
- **Overall score** (weighted average, color-coded)
- **Per-dimension scores** with evidence citations from the transcript
- **Critical flags** (e.g., "Naloxone not asked about on suspected overdose")
- **Strengths & areas for improvement**
- **Coaching recommendation**

## Key Design Decisions

1. **Two-step prompting** — Separating evidence extraction from scoring reduces hallucination and makes the scoring more grounded.
2. **Deterministic guardrails** — Post-LLM score standardization ensures consistency (e.g., if the transcript proves naloxone wasn't asked about, the score *must* reflect that, regardless of LLM output).
3. **Weighted scoring** — The overall score is computed deterministically from dimension scores using fixed weights, not taken from the LLM.
4. **Template-based reports** — Using `python-docx` with a real Word template preserves formatting and styling.


## License

This project is for portfolio/demonstration purposes.
