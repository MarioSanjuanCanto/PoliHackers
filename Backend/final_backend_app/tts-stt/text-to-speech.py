import wave
import contextlib

from google import genai

# Get API key from environment variable
GOOGLE_API_KEY = "AIzaSyCfn7bt5OQAPLkQxfRHQFo6UH4tEbYycNA"

if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY environment variable not set.")
else:
    client = genai.Client(api_key=GOOGLE_API_KEY)

    MODEL_ID = "gemini-2.5-flash-preview-tts"

    @contextlib.contextmanager
    def wave_file(filename, channels=1, rate=24000, sample_width=2):
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            yield wf

    response = client.models.generate_content(
      model=MODEL_ID,
      contents="Di '¿Quieres que realice la tranferencia usando tus datos?' en español de España",
      config={"response_modalities": ['Audio']},
    )

    blob = response.candidates[0].content.parts[0].inline_data
    print(blob.mime_type)

    fname = 'output_audio.wav'
    with wave_file(fname) as wav:
        wav.writeframes(blob.data)

    print(f"Audio saved to {fname}")
