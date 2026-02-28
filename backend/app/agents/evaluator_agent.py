import json
from pathlib import Path
from typing import Dict

from app.models.model_manager import ModelManager
from app.schemas.evaluation_schema import EvaluationSchema


class EvaluatorAgent:

    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.prompt_template = self._load_prompt()

    def _load_prompt(self) -> str:
        prompt_path = Path(__file__).parent.parent / "prompts" / "evaluator.txt"
        return prompt_path.read_text()

    def evaluate(self, question: str, answer: str, plan: Dict) -> Dict:
        prompt = (
            self.prompt_template
            + "\n\nINTERVIEW PLAN:\n"
            + json.dumps(plan)
            + "\n\nQUESTION:\n"
            + question
            + "\n\nCANDIDATE ANSWER:\n"
            + answer
        )

        raw_output = self.model_manager.generate(prompt)

        try:
            parsed = json.loads(raw_output.strip())
        except json.JSONDecodeError:
            raise ValueError("EvaluatorAgent returned invalid JSON")

        # STRICT SCHEMA VALIDATION
        validated = EvaluationSchema(**parsed)

        return validated.model_dump()