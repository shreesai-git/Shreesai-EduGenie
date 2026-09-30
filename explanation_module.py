import os
from functools import lru_cache

# The project documentation specifies LaMini-Flan-T5 for local concept explanation.
# Loading is lazy so the web app can start even when the optional local model is not installed.
MODEL_NAME = os.getenv("LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M")

@lru_cache(maxsize=1)
def _load_local_model():
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    return tokenizer, model

def _local_explain(topic: str) -> str:
    import torch
    tokenizer, model = _load_local_model()
    prompt = f"Explain the following educational topic simply for a beginner: {topic}"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=220, num_beams=4, early_stopping=True)
    return tokenizer.decode(output[0], skip_special_tokens=True).strip()

def explain_topic(topic: str) -> str:
    if os.getenv("USE_LOCAL_EXPLANATION", "false").lower() == "true":
        try:
            return _local_explain(topic)
        except Exception as exc:
            # Fall back to Gemini so a missing local model does not break the feature.
            from gemini_client import generate
            return generate(
                f"Explain this topic simply for a beginner. Mention the key idea, a simple example, and a short recap.\n\nTopic: {topic}\n\nLocal model fallback reason: {type(exc).__name__}",
                temperature=0.3,
                max_output_tokens=1200,
            )
    from gemini_client import generate
    return generate(
        f"Explain this educational topic simply for a beginner. Use a short definition, key points, an easy example, and a recap.\n\nTopic: {topic}",
        temperature=0.3,
        max_output_tokens=1200,
    )
