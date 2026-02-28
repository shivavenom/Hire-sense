# app/agents/conductor_agent.py

from typing import Dict, Any
from app.models.model_manager import ModelManager


class ConductorAgent:
    """
    Conversational Interview Conductor

    Responsibilities:
    - Maintain human-like interview flow
    - Greet candidate properly
    - Gradually move into technical depth
    - Use conversation history
    - Never evaluate (evaluation is separate agent)
    """

    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager

    # ==========================================================
    # MAIN QUESTION GENERATION
    # ==========================================================

    def generate_question(self, session: Dict[str, Any]) -> str:
        candidate_name = session.get("candidate_name", "Candidate")
        plan = session.get("plan", {})
        conversation = session.get("conversation", [])
        questions = session.get("questions", [])

        is_first_message = len(questions) == 0

        history_text = self._format_conversation(conversation)

        if is_first_message:
            prompt = f"""
You are a calm, professional technical interviewer.

Candidate Name: {candidate_name}

Start the interview naturally.

1. Greet the candidate by name.
2. Make them feel comfortable.
3. Briefly acknowledge their background.
4. Then smoothly transition into the first light technical discussion.

Do NOT sound robotic.
Do NOT number questions.
Do NOT behave like an exam paper.
Keep it conversational and human.

Interview plan (internal guidance):
{plan}

Conversation so far:
{history_text}

Now continue the interview.
"""
        else:
            prompt = f"""
You are continuing a live technical interview.

Candidate Name: {candidate_name}

Keep the tone conversational and natural.

Gradually increase technical depth.
Ask follow-up questions naturally.
Do NOT sound like an exam sheet.
Avoid abrupt transitions.

Interview plan (internal guidance):
{plan}

Conversation so far:
{history_text}

Now continue the interview.
"""

        response = self.model_manager.generate(prompt)

        # Store in conversation
        conversation.append({"role": "assistant", "content": response})
        session["conversation"] = conversation

        return response.strip()

    # ==========================================================
    # FOLLOW-UP GENERATION (After Evaluation)
    # ==========================================================

    def generate_followup(
        self,
        session: Dict[str, Any],
        evaluation: Dict[str, Any]
    ) -> str:

        candidate_name = session.get("candidate_name", "Candidate")
        conversation = session.get("conversation", [])
        history_text = self._format_conversation(conversation)

        weaknesses = evaluation.get("weaknesses", [])
        missing = evaluation.get("missing_concepts", [])

        prompt = f"""
You are a professional technical interviewer.

Candidate Name: {candidate_name}

You noticed some gaps in the candidate's previous answer.

Weak areas:
{weaknesses}

Missing concepts:
{missing}

Ask a natural follow-up question to clarify or probe deeper.
Do NOT mention evaluation or scoring.
Keep tone supportive and calm.
Sound like a real interviewer.

Conversation so far:
{history_text}

Continue the interview naturally.
"""

        response = self.model_manager.generate(prompt)

        conversation.append({"role": "assistant", "content": response})
        session["conversation"] = conversation

        return response.strip()

    # ==========================================================
    # HELPER
    # ==========================================================

    def _format_conversation(self, conversation):
        if not conversation:
            return "No prior conversation."

        formatted = ""
        for turn in conversation:
            role = turn.get("role", "assistant")
            content = turn.get("content", "")
            formatted += f"{role.upper()}: {content}\n"

        return formatted