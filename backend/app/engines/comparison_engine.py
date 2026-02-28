from typing import List, Dict


class ComparisonEngine:
    """
    Deterministic comparison engine.

    Responsibilities:
    - Compare expected concepts with candidate answer
    - Identify missing keywords
    - Compute basic coverage score
    - No LLM usage
    """

    def normalize_text(self, text: str) -> str:
        return text.lower()

    def extract_missing_concepts(
        self,
        expected_concepts: List[str],
        answer: str
    ) -> List[str]:

        answer_text = self.normalize_text(answer)

        missing = []

        for concept in expected_concepts:
            if concept.lower() not in answer_text:
                missing.append(concept)

        return missing

    def compute_coverage_score(
        self,
        expected_concepts: List[str],
        answer: str
    ) -> float:

        if not expected_concepts:
            return 1.0

        missing = self.extract_missing_concepts(expected_concepts, answer)

        covered = len(expected_concepts) - len(missing)

        return round(covered / len(expected_concepts), 2)

    def compare(
        self,
        expected_concepts: List[str],
        answer: str
    ) -> Dict:

        missing = self.extract_missing_concepts(expected_concepts, answer)
        coverage = self.compute_coverage_score(expected_concepts, answer)

        return {
            "missing_concepts_detected": missing,
            "coverage_score": coverage
        }