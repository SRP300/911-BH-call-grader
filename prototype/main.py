from __future__ import annotations

import sys
import os
from pathlib import Path

if __package__ is None or __package__ == "":
    # Allow `python prototype/main.py` to work (adds repo root to sys.path).
    _repo_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(_repo_root))

from prototype.render_docx import write_call_grading_docx  # noqa: E402
from prototype.sample_transcripts import DEMO_CALLS  # noqa: E402
from prototype.template_builder import build_single_scenario_template  # noqa: E402
from prototype.workflow import grade_call_from_transcript  # noqa: E402


def _load_env_file(env_path: Path) -> None:
    """Load KEY=VALUE lines from .env if present (no extra dependency)."""
    if not env_path.is_file():
        return
    try:
        text = env_path.read_text(encoding="utf-8")
    except OSError:
        return
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def main() -> None:
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    repo_root = Path(__file__).resolve().parent.parent
    if not os.getenv("NVIDIA_API_KEY", "").strip():
        _load_env_file(repo_root / ".env")

    template_path = repo_root / "templates" / "call-grading-template.docx"
    if not template_path.exists():
        # Build the template from the multi-scenario source report.
        input_docx = repo_root / "call-grading-report.docx"
        if not input_docx.exists():
            raise SystemExit(
                f"Missing template and input docx. Expected input at {input_docx}. "
                "Place the source Word report in the repo root."
            )
        build_single_scenario_template(
            input_docx=str(input_docx),
            output_docx=str(template_path),
            scenario_index=1,
        )

    api_key = os.getenv("NVIDIA_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("Missing env var NVIDIA_API_KEY")

    model = os.getenv("NVIDIA_MODEL", "meta/llama-3.1-8b-instruct")

    for call in DEMO_CALLS:
        assessed = grade_call_from_transcript(
            transcript_text=call["transcript_text"],
            call_metadata=call["metadata"],
            nvidia_api_key=api_key,
            model=model,
        )

        filename = f"{call['metadata']['call_id']}_{call['metadata']['call_type'].replace(' ', '_').replace('/', '_')}.docx"
        out_path = out_dir / filename
        write_call_grading_docx(assessed=assessed, out_path=str(out_path))
        print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()

