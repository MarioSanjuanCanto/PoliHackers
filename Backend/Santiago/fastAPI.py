from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import uvicorn
import os
import shutil
import stt

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/uploadfile/")
async def upload_file(audio_file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, audio_file.filename)

    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)

        print(f"DEBUG: Archivo guardado localmente en: {file_location}")

        transcription_result = stt.translate(file_location)

        return {
            "message": f"Archivo '{audio_file.filename}' procesado exitosamente.",
            "filename": audio_file.filename,
            "transcription": transcription_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el procesamiento del archivo: {e}")


@app.get("/download/{filename}")
async def download_file(filename: str):

    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado.")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=filename
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)