from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path

from app.audio_utils import extract_features
from app.model import predict_voice


app = FastAPI(
    title="Voice AI Detector",
    description="API to detect whether a voice is AI-generated or human",
    version="1.0.0"
)

# 🔐 API KEY
API_KEY = "my-secret-key-123"


# ---------- Serve UI ----------
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    return Path("templates/index.html").read_text()


# ---------- Detection API ----------
@app.post("/detect")
async def detect_voice(
    file: UploadFile = File(...),
    x_api_key: str = Header(None)
):
    # API KEY check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Validate file type
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Upload a valid audio file")

    audio_bytes = await file.read()

    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty audio file")

    try:
        features = extract_features(audio_bytes)
        prediction = predict_voice(features)

        # Support both dict and string output
        if isinstance(prediction, dict):
            result = prediction.get("result", "unknown")
            confidence = prediction.get("confidence", 0)
        else:
            result = prediction
            confidence = 0

        return {
            "prediction": result,
            "confidence": confidence
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {str(e)}")


# ---------- Run locally ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
