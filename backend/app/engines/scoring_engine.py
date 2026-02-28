from typing import List, Dict


class ScoringEngine:

    def compute_overall_score(self, evaluations: List[Dict]) -> Dict[str, float]:
        if not evaluations:
            return {
                "technical_score": 0.0,
                "communication_score": 0.0,
                "overall_score": 0.0,
            }

        technical_scores = []
        communication_scores = []

        for eval_data in evaluations:
            technical_component = (
                eval_data["technical_depth"] +
                eval_data["accuracy"]
            ) / 2

            communication_component = (
                eval_data["clarity"] +
                eval_data["confidence"]
            ) / 2

            technical_scores.append(technical_component)
            communication_scores.append(communication_component)

        avg_technical = sum(technical_scores) / len(technical_scores)
        avg_communication = sum(communication_scores) / len(communication_scores)

        overall = (avg_technical * 0.7) + (avg_communication * 0.3)

        return {
            "technical_score": round(avg_technical, 2),
            "communication_score": round(avg_communication, 2),
            "overall_score": round(overall, 2),
        }