from typing import Dict, Optional


class QuestionEngine:
    """
    Deterministic question selection engine.

    Responsibilities:
    - Decide which topic to ask next
    - Track progress based on session
    - No LLM usage
    """

    def select_next_topic(self, session: Dict) -> Optional[str]:

        plan = session.get("plan", {})
        core_topics = plan.get("core_topics", [])
        asked_count = len(session.get("questions", []))

        if not core_topics:
            return None

        if asked_count < len(core_topics):
            return core_topics[asked_count]

        # If all topics covered, repeat last with deeper focus
        return core_topics[-1]

    def is_interview_complete(self, session: Dict) -> bool:
        plan = session.get("plan", {})
        core_topics = plan.get("core_topics", [])

        asked_count = len(session.get("questions", []))

        return asked_count >= len(core_topics)