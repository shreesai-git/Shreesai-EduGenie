import json
import re
from gemini_client import generate

def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()

def generate_quiz(passage: str, count: int = 3) -> list[dict]:
    prompt = f"""Create exactly {count} multiple-choice questions from the passage below.
Return ONLY valid JSON with this shape:
{{"questions":[{{"question":"...","options":["A...","B...","C...","D..."],"answer":"A...","explanation":"..."}}]}}
Rules:
- Exactly four options per question.
- Exactly one correct answer.
- The answer must exactly match one option.
- Questions must be answerable from the supplied passage.
- Distractors should be plausible but incorrect.
- No Markdown fences.

Passage:
{passage}
"""
    raw = clean_json_block(generate(prompt, temperature=0.3, max_output_tokens=3000))
    data = json.loads(raw)
    questions = data.get("questions")
    if not isinstance(questions, list) or len(questions) != count:
        raise ValueError("Gemini returned an unexpected quiz structure.")
    for q in questions:
        if not all(k in q for k in ("question", "options", "answer", "explanation")):
            raise ValueError("Each quiz question must contain question, options, answer, and explanation.")
        if len(q["options"]) != 4 or q["answer"] not in q["options"]:
            raise ValueError("Each question must have four options and one matching answer.")
    return questions
