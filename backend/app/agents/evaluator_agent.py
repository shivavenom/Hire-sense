import json
import re
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

    def _extract_json(self, text: str) -> str:
        text = text.replace("```json", "").replace("```", "")
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON found")
        return match.group(0)

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

        try:
            raw_output = self.model_manager.generate(prompt)
            json_str = self._extract_json(raw_output)
            parsed = json.loads(json_str)

            validated = EvaluationSchema(**parsed)
            return validated.model_dump()

        except Exception:
            # Absolute safe fallback
            return {
                "technical_depth": 5,
                "accuracy": 5,
                "clarity": 5,
                "confidence": 5,
                "strengths": [],
                "weaknesses": [],
                "missing_concepts": [],
                "follow_up_required": False,
            }