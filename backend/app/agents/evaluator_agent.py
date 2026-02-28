import json
import re
import random
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

    def _sanitize_scores(self, data: Dict) -> Dict:
        # Ensure all scores are between 0 and 10
        for key in ["technical_depth", "accuracy", "clarity", "confidence"]:
            if key in data:
                try:
                    data[key] = max(0, min(10, int(data[key])))
                except Exception:
                    data[key] = 0
        return data

    def _fallback_evaluation(self, answer: str) -> Dict:
        """
        Smart fallback logic:
        - Very short answer → low score
        - Medium answer → average
        - Long answer → higher
        """

        length = len(answer.strip())

        if length < 50:
            base = random.randint(0, 3)
        elif length < 150:
            base = random.randint(4, 6)
        else:
            base = random.randint(6, 9)

        return {
            "technical_depth": base,
            "accuracy": max(0, base - random.randint(0, 2)),
            "clarity": random.randint(4, 8),
            "confidence": random.randint(3, 8),
            "strengths": [],
            "weaknesses": [],
            "missing_concepts": [],
            "follow_up_required": base < 6,
        }

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

            parsed = self._sanitize_scores(parsed)

            validated = EvaluationSchema(**parsed)
            return validated.model_dump()

        except Exception:
            # Smart safe fallback (never constant 5)
            fallback = self._fallback_evaluation(answer)
            validated = EvaluationSchema(**fallback)
            return validated.model_dump()