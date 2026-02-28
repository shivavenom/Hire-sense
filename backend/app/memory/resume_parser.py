import re
from typing import Dict, List


class ResumeParser:
    """
    Deterministic resume parser.

    Responsibilities:
    - Extract skills
    - Extract technologies
    - Extract experience indicators
    - No LLM usage
    - No external dependencies
    """

    COMMON_SKILLS = [
        "python", "java", "c++", "javascript", "react", "node",
        "sql", "mongodb", "aws", "docker", "kubernetes",
        "data structures", "algorithms", "system design",
        "machine learning", "deep learning"
    ]

    EDUCATION_KEYWORDS = [
        "b.tech", "bachelor", "master", "m.tech",
        "phd", "engineering", "computer science"
    ]

    def parse(self, resume_text: str) -> Dict:
        if not resume_text or not resume_text.strip():
            raise ValueError("Resume text cannot be empty")

        normalized = resume_text.lower()

        skills = self._extract_skills(normalized)
        education = self._extract_education(normalized)
        experience_years = self._extract_experience_years(normalized)

        return {
            "skills_detected": skills,
            "education_detected": education,
            "estimated_experience_years": experience_years
        }

    # ---------------------------------------
    # Internal Extractors
    # ---------------------------------------

    def _extract_skills(self, text: str) -> List[str]:
        detected = []

        for skill in self.COMMON_SKILLS:
            if skill in text:
                detected.append(skill)

        return detected

    def _extract_education(self, text: str) -> List[str]:
        detected = []

        for keyword in self.EDUCATION_KEYWORDS:
            if keyword in text:
                detected.append(keyword)

        return detected

    def _extract_experience_years(self, text: str) -> int:
        """
        Very simple heuristic:
        Looks for patterns like:
        - 3 years
        - 5+ years
        - 2 yrs
        """

        patterns = [
            r"(\d+)\+?\s+years",
            r"(\d+)\+?\s+yrs"
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return int(match.group(1))

        return 0