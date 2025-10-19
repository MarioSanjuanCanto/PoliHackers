import requests
import os

SERVER_URL = "http://127.0.0.1:8000"
UPLOAD_ENDPOINT = "/uploadfile/"
DOWNLOAD_ENDPOINT = "/download/"


def upload_audio(file_path: str):

    if not os.path.exists(file_path):
        print(f"Error: El archivo no se encontró en la ruta: {file_path}")
        print("Por favor, verifica y actualiza la variable FILE_PATH_TO_UPLOAD.")
        return

    try:
        with open(file_path, 'rb') as f:
            files = {'audio_file': (os.path.basename(file_path), f, 'audio/mp3')}

            print(
                f"Intentando subir el archivo: {os.path.basename(file_path)} a {SERVER_URL}{UPLOAD_ENDPOINT}")

            response = requests.post(f"{SERVER_URL}{UPLOAD_ENDPOINT}", files=files)

            response.raise_for_status()

            print("Subida exitosa.")
            print("Respuesta del servidor:")
            print(response.json())

    except requests.exceptions.HTTPError as errh:
        print(f"Error HTTP al subir (código {response.status_code}): {response.json()}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error de Conexión: Asegúrate de que tu servidor FastAPI está corriendo en {SERVER_URL}.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


def download_file(filename: str, save_path: str):

    download_url = f"{SERVER_URL}{DOWNLOAD_ENDPOINT}{filename}"

    try:
        print(f"Intentando descargar el archivo '{filename}' desde {download_url}")

        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Descarga exitosa. Archivo guardado en: {save_path}")

    except requests.exceptions.HTTPError as errh:
        print(
            f"Error HTTP al descargar (código {response.status_code}): El archivo no existe o hubo un error en el servidor.")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error de Conexión: Asegúrate de que tu servidor FastAPI está corriendo en {SERVER_URL}.")
    except Exception as e:
        print(f"Ocurrió un error inesperado durante la descarga: {e}")

