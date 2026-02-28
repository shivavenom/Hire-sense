from typing import Dict, List, Optional


class IdealAnswerStore:
    """
    In-memory ideal answer reference store.

    Responsibilities:
    - Provide expected concepts per topic
    - No LLM usage
    - No business logic
    - Pure data provider
    """

    def __init__(self):
        self._store: Dict[str, List[str]] = self._load_defaults()

    # -------------------------------------
    # Public API
    # -------------------------------------

    def get_expected_concepts(self, topic: str) -> Optional[List[str]]:
        return self._store.get(topic.lower())

    def add_topic(self, topic: str, concepts: List[str]) -> None:
        self._store[topic.lower()] = concepts

    def list_topics(self) -> List[str]:
        return list(self._store.keys())

    # -------------------------------------
    # Internal Defaults
    # -------------------------------------

    def _load_defaults(self) -> Dict[str, List[str]]:
        """
        Default static ideal answers.
        Expand as needed.
        """

        return {
            "data structures": [
                "array",
                "linked list",
                "stack",
                "queue",
                "hash map",
                "tree",
                "graph",
                "time complexity",
                "space complexity"
            ],
            "oop": [
                "encapsulation",
                "abstraction",
                "inheritance",
                "polymorphism",
                "class",
                "object"
            ],
            "system design": [
                "scalability",
                "load balancing",
                "database",
                "caching",
                "consistency",
                "availability",
                "microservices"
            ]
        }