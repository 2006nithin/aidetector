def extract_features(audio_bytes: bytes) -> dict:
    energy = sum(audio_bytes) % 100
    return {
        "energy": energy
    }