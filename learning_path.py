from gemini_client import generate

def get_learning_recommendations(topic: str, level: str = "Beginner") -> str:
    prompt = f"""Create a personalized learning path for the topic: {topic}
Learner level: {level}

Structure it from foundational to advanced learning. Include:
1. Prerequisites
2. Ordered topics/modules
3. Suggested practice for each stage
4. A realistic suggested timeline
5. Project or self-check ideas
6. Types of resources to look for (videos, documentation, books, practice sites)

Keep it practical and concise. Clearly label suggestions as suggestions rather than guaranteed facts.
"""
    return generate(prompt, temperature=0.5, max_output_tokens=2400)
