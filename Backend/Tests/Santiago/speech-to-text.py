import os
from google import genai
from google.genai.errors import APIError

GOOGLE_API_KEY = "AIzaSyCfn7bt5OQAPLkQxfRHQFo6UH4tEbYycNA"

try:
    client = genai.Client(api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"Error al inicializar el cliente de Gemini.")
    print(f"Detalles del error: {e}")
    exit()


FILE_PATH = r'C:\Users\santi\PycharmProjects\deep\output_audio.wav'

TRANSCRIPTION_PROMPT = 'Genera una transcripción del discurso en este audio.'

MODEL_NAME = 'gemini-2.5-flash'


if not os.path.exists(FILE_PATH):
    print(f"Error: El archivo no se encontró en la ruta especificada: {FILE_PATH}")
    print("Asegúrate de reemplazar 'path/to/your/audio.mp3' con la ruta correcta a tu archivo.")
else:
    myfile = None
    try:
        myfile = client.files.upload(file=FILE_PATH)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[TRANSCRIPTION_PROMPT, myfile]
        )
        print(response.text)

    except APIError as e:
        print(f"\nError de la API de Gemini: {e}")
        print("Verifica que tu clave de API sea correcta y que el archivo de audio sea compatible.")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")
    finally:
        if myfile:
            client.files.delete(name=myfile.name)
