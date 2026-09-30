from gemini_client import generate

def summarize_text(text: str) -> str:
    prompt = f"""Summarize the educational passage below for a student.
Keep the central ideas, important facts, definitions, and relationships. Remove repetition.
Use clear headings or bullet points when helpful. Do not add information that is not supported by the passage.

Passage:
{text}
"""
    return generate(prompt, temperature=0.2, max_output_tokens=1800)
