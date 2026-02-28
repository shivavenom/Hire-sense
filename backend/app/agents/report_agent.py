import json
from pathlib import Path
from typing import Dict

from app.models.model_manager import ModelManager
from app.schemas.report_schema import ReportSchema
from app.engines.scoring_engine import ScoringEngine


class ReportAgent:

    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.scoring_engine = ScoringEngine()
        self.prompt_template = self._load_prompt()

    def _load_prompt(self) -> str:
        prompt_path = Path(__file__).parent.parent / "prompts" / "report.txt"
        return prompt_path.read_text()

    def generate_report(self, session: Dict) -> Dict:
        evaluations = session.get("evaluations", [])

        scores = self.scoring_engine.compute_overall_score(evaluations)

        prompt = (
            self.prompt_template
            + "\n\nCOMPUTED SCORES:\n"
            + json.dumps(scores)
            + "\n\nEVALUATIONS:\n"
            + json.dumps(evaluations)
        )

        raw_output = self.model_manager.generate(prompt)

        try:
            parsed = json.loads(raw_output.strip())
        except json.JSONDecodeError:
            raise ValueError("ReportAgent returned invalid JSON")

        validated = ReportSchema(**parsed)

        return validated.model_dump()