from typing import Dict


class ProbingEngine:

    def should_probe(self, evaluation: Dict) -> bool:
        if evaluation["follow_up_required"]:
            return True

        weak_score = (
            evaluation["technical_depth"] < 5 or
            evaluation["accuracy"] < 5
        )

        return weak_score