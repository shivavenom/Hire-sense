import json
from pathlib import Path
from typing import Dict

from app.models.model_manager import ModelManager


class ConductorAgent:

    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.followup_prompt = self._load_followup_prompt()

    def _load_followup_prompt(self) -> str:
        prompt_path = Path(__file__).parent.parent / "prompts" / "followup.txt"
        return prompt_path.read_text()

    # ----------------------------------
    # Generate Normal Question
    # ----------------------------------

    def generate_question(self, session: Dict) -> str:
        plan = session["plan"]
        questions_asked = len(session["questions"])

        core_topics = plan.get("core_topics", [])

        if questions_asked >= len(core_topics):
            # fallback generic deep question
            topic = core_topics[-1] if core_topics else "core technical concepts"
        else:
            topic = core_topics[questions_asked]

        prompt = (
            "You are a technical interviewer.\n"
            f"Ask one interview question about: {topic}\n"
            "Only output the question.\n"
            "No explanation.\n"
        )

        output = self.model_manager.generate(prompt)

        return output.strip()

    # ----------------------------------
    # Generate Follow-Up Question
    # ----------------------------------

    def generate_followup(self, session: Dict, evaluation: Dict) -> str:

        weaknesses = evaluation.get("weaknesses", [])
        missing = evaluation.get("missing_concepts", [])

        focus_area = weaknesses + missing

        prompt = (
            self.followup_prompt
            + "\n\nWEAKNESSES:\n"
            + json.dumps(weaknesses)
            + "\n\nMISSING CONCEPTS:\n"
            + json.dumps(missing)
        )

        output = self.model_manager.generate(prompt)

        return output.strip()