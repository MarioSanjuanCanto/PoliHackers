# speech-to-text.py
import os, sys, json, hmac, hashlib, argparse
from pathlib import Path
import requests
from google import genai
from google.genai.errors import APIError

# --- CLI ---
parser = argparse.ArgumentParser(description="Speech to text via Gemini")
parser.add_argument("--file", dest="file_path", help="Ruta del audio a transcribir")
args = parser.parse_args()

# --- HARD CODED API KEY (as requested) ---
GOOGLE_API_KEY = "AIzaSyCfn7bt5OQAPLkQxfRHQFo6UH4tEbYycNA"

# --- Default model / prompt (can override with env if desired) ---
MODEL_NAME          = os.getenv("ASR_MODEL", "gemini-2.5-flash")
PROMPT              = os.getenv("ASR_PROMPT", "Genera una transcripción del discurso en este audio.")

# --- Opcional: enviar el texto al router o a API B ---
ROUTER_PUSH_URL     = os.getenv("ROUTER_PUSH_URL")              # opcional
ROUTER_HMAC_SECRET  = os.getenv("ROUTER_HMAC_SECRET", "")       # opcional
API_B_URL           = os.getenv("API_B_URL")                    # opcional
TIMEOUT_S           = float(os.getenv("TIMEOUT_S", "90"))

def hmac_header(payload_bytes: bytes) -> str:
    if not ROUTER_HMAC_SECRET:
        return ""
    mac = hmac.new(ROUTER_HMAC_SECRET.encode(), payload_bytes, hashlib.sha256).hexdigest()
    return f"sha256={mac}"

def main():
    # NOTE: key is hardcoded above as requested
    if not GOOGLE_API_KEY:
        print("ERROR: Falta GOOGLE_API_KEY (hardcoded) — abortando", file=sys.stderr)
        sys.exit(2)

    # 1) Resolver ruta del audio como objeto Path (dinámico)
    file_env = os.getenv("FILE_PATH")
    audio_path = Path(args.file_path or file_env or "")
    if not audio_path or not audio_path.exists():
        print(f"ERROR: No existe el audio. Pasa --file o FILE_PATH. Valor actual: '{audio_path}'", file=sys.stderr)
        sys.exit(2)

    client = genai.Client(api_key=GOOGLE_API_KEY)
    up = None
    try:
        up = client.files.upload(file=str(audio_path))
        resp = client.models.generate_content(
            model=MODEL_NAME,
            contents=[PROMPT, up]
        )
        text = (resp.text or "").strip()
    except APIError as e:
        print(f"ERROR: GENAI_API_ERROR {e}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"ERROR: UNEXPECTED {e}", file=sys.stderr)
        sys.exit(4)
    finally:
        try:
            if up:
                client.files.delete(name=up.name)
        except Exception:
            pass

    # 2) Siempre imprimir al stdout (modo router process)
    print(text)

    # 3) Opcional: push al router
    if ROUTER_PUSH_URL:
        payload = {"text": text}
        payload_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        sig = hmac_header(payload_bytes)
        if sig:
            headers["X-Signature"] = sig
        try:
            requests.post(ROUTER_PUSH_URL, data=payload_bytes, headers=headers, timeout=TIMEOUT_S)
        except requests.RequestException as e:
            print(f"WARN: No se pudo enviar al router: {e}", file=sys.stderr)

    # 4) Opcional: directo a API B
    if API_B_URL:
        try:
            r = requests.post(API_B_URL, json={"text": text, "meta": {"source": "api-a-direct"}}, timeout=TIMEOUT_S)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"WARN: No se pudo enviar a API B: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
