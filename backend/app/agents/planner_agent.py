import json
from pathlib import Path
from typing import Dict

from app.models.model_manager import ModelManager


class PlannerAgent:
    """
    Responsible for generating structured interview plans.

    Constraints:
    - Must return STRICT JSON
    - Must not modify session state
    - Must not access database
    - Must not contain prompt text inline
    """

    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.prompt_template = self._load_prompt()

    # -----------------------------------
    # Prompt Loader
    # -----------------------------------

    def _load_prompt(self) -> str:
        prompt_path = Path(__file__).parent.parent / "prompts" / "planner.txt"

        if not prompt_path.exists():
            raise FileNotFoundError("planner.txt prompt file not found")

        return prompt_path.read_text(encoding="utf-8")

    # -----------------------------------
    # Public API
    # -----------------------------------

    def create_plan(self, resume: str, job_description: str) -> Dict:
        """
        Generate structured interview plan.
        Returns validated JSON dictionary.
        """

        if not resume.strip():
            raise ValueError("Resume cannot be empty")

        if not job_description.strip():
            raise ValueError("Job description cannot be empty")

        prompt = (
            self.prompt_template
            + "\n\nRESUME:\n"
            + resume
            + "\n\nJOB DESCRIPTION:\n"
            + job_description
        )

        raw_output = self.model_manager.generate(prompt)

        cleaned_output = self._clean_json_output(raw_output)

        try:
            parsed = json.loads(cleaned_output)
        except json.JSONDecodeError:
            raise ValueError("PlannerAgent returned invalid JSON")

        self._validate_structure(parsed)

        return parsed

    # -----------------------------------
    # Internal Utilities
    # -----------------------------------

    def _clean_json_output(self, text: str) -> str:
        """
        Removes markdown fences if LLM accidentally adds them.
        """
        text = text.strip()

        if text.startswith("```"):
            text = text.split("```")[1]

        return text.strip()

    def _validate_structure(self, plan: Dict):
        """
        Minimal structure validation before returning.
        Full validation can be added later if needed.
        """

        required_keys = ["rounds", "core_topics", "estimated_duration_minutes"]

        for key in required_keys:
            if key not in plan:
                raise ValueError(f"Planner output missing required key: {key}")

        if not isinstance(plan["rounds"], list):
            raise ValueError("Planner output 'rounds' must be a list")

        if not isinstance(plan["core_topics"], list):
            raise ValueError("Planner output 'core_topics' must be a list")

        if not isinstance(plan["estimated_duration_minutes"], int):
            raise ValueError(
                "Planner output 'estimated_duration_minutes' must be int"
            )