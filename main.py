import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"  # Safe fallback if no GPU

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import uuid

app = FastAPI()
model = MusicGen.get_pretrained('facebook/musicgen-medium')
model.set_generation_params(duration=15)

class Request(BaseModel):
    prompt: str
    duration: int = 15

@app.post("/generate")
async def generate_music(data: Request):
    try:
        model.set_generation_params(duration=data.duration)
        wav = model.generate([data.prompt])
        filename = f"output_{uuid.uuid4().hex[:8]}.wav"
        audio_write(filename, wav[0].cpu(), model.sample_rate, strategy="loudness")
        return {"file_url": f"/files/{filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/{filename}")
def get_file(filename: str):
    filepath = os.path.join(".", filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(filepath)
