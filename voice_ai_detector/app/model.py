def predict_voice(features: dict) -> dict:
    ai_score = features["energy"]
    human_score = 100 - ai_score

    if ai_score > human_score:
        return {
            "result": "AI_GENERATED",
            "confidence": round(ai_score / 100, 2)
        }
    else:
        return {
            "result": "HUMAN",
            "confidence": round(human_score / 100, 2)
        }
