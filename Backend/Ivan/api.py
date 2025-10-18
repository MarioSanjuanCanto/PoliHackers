# api.py
import os, json, hmac, hashlib, uuid, requests, subprocess, pathlib, tempfile
from flask import Flask, request, jsonify

# --- Modo de integración con API A ---
API_A_MODE       = os.getenv("API_A_MODE", "process")  # "process" | "http"

# --- Integración API A por HTTP (opcional) ---
API_A_URL_SYNC   = os.getenv("API_A_URL_SYNC")         # ej: http://127.0.0.1:9000/asr/sync
API_A_URL_ASYNC  = os.getenv("API_A_URL_ASYNC")        # ej: http://127.0.0.1:9000/asr/async
USE_WEBHOOK      = bool(int(os.getenv("USE_WEBHOOK", "0")))
API_A_SECRET     = os.getenv("API_A_SECRET", "")       # para HMAC firmas entrantes

# --- Integración API A por proceso (tu script original) ---
API_A_PYTHON     = os.getenv("API_A_PYTHON", "python")     # ruta a python.exe si hace falta
API_A_SCRIPT     = os.getenv("API_A_SCRIPT", r"C:\ruta\a\speech-to-text.py")

# --- API B ---
API_B_URL        = os.getenv("API_B_URL")               # ej: http://127.0.0.1:7000/intent
TIMEOUT_S        = float(os.getenv("TIMEOUT_S", "90"))

# (opcional) si tu script te hace push al router:
ROUTER_HMAC_SECRET = os.getenv("ROUTER_HMAC_SECRET", "")  # para verificar /from-api-a

app = Flask(__name__)

def verify_hmac(sig_header: str, raw_body: bytes, secret: str) -> bool:
    if not secret:
        return True
    try:
        method, sig = sig_header.split("=", 1)
        if method.lower() != "sha256":
            return False
        mac = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(mac, sig)
    except Exception:
        return False

def call_api_b(text: str, meta: dict):
    if not API_B_URL:
        return {"ok": False, "error": "API_B_URL_NOT_SET"}
    payload = {"text": text, "meta": meta}
    r = requests.post(API_B_URL, json=payload, timeout=TIMEOUT_S)
    r.raise_for_status()
    return r.json()

def run_api_a_process_get_text(file_path: str) -> str:
    """Ejecuta speech-to-text.py con --file y devuelve la transcripción (stdout)."""
    cmd = [API_A_PYTHON, API_A_SCRIPT, "--file", file_path]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_S)
    out = (proc.stdout or "").strip()
    if not out:
        err = (proc.stderr or "").strip()
        raise RuntimeError(f"API A no devolvió texto. stderr: {err[:500]}")
    # Se toma la última línea no vacía como transcripción
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    return lines[-1] if lines else ""

@app.post("/ingest")
def ingest():
    """
    - Si JSON con 'text' => lo manda a API B.
    - Si audio => según API_A_MODE:
        * process: guarda audio en TMP y ejecuta speech-to-text.py --file <tmp>
        * http:    reenvía audio a API A HTTP (sync/async)
    """
    ct = (request.headers.get("Content-Type") or "").lower()
    ui_session_id = request.args.get("ui_session_id")
    meta = {"ui_session_id": ui_session_id}

    # --- TEXTO directo ---
    if "application/json" in ct:
        body = request.get_json(force=True)
        text = (body.get("text") or "").strip()
        if not text:
            return jsonify({"ok": False, "error": "TEXT_REQUIRED"}), 400
        try:
            b_resp = call_api_b(text, meta)
        except requests.RequestException as e:
            return jsonify({"ok": False, "error": "API_B_FAILED", "details": str(e)}), 502
        return jsonify({"ok": True, "mode": "text->B", "text": text, "b_result": b_resp}), 200

    # --- AUDIO ---
    if ("multipart/form-data" in ct) or ct.startswith("audio/") or ("application/octet-stream" in ct):
        # Leer bytes del audio
        if "file" in request.files:
            audio_file = request.files["file"]
            audio_bytes = audio_file.read()
            # intenta preservar extensión
            ext = pathlib.Path(audio_file.filename).suffix or ".bin"
        else:
            audio_bytes = request.get_data() or b""
            ext = ".bin"

        if API_A_MODE == "process":
            # Guardar a un archivo temporal para pasarlo al script
            fd, tmp_name = tempfile.mkstemp(prefix="asr_", suffix=ext)
            os.close(fd)
            try:
                with open(tmp_name, "wb") as w:
                    w.write(audio_bytes)

                try:
                    text = run_api_a_process_get_text(tmp_name).strip()
                except Exception as e:
                    return jsonify({"ok": False, "error": "API_A_PROCESS_FAILED", "details": str(e)}), 502

                if not text:
                    return jsonify({"ok": False, "error": "ASR_EMPTY"}), 502

                try:
                    b_resp = call_api_b(text, meta)
                except requests.RequestException as e:
                    return jsonify({"ok": False, "error": "API_B_FAILED", "details": str(e)}), 502

                return jsonify({"ok": True, "mode": "audio->A(process)->B", "text": text, "b_result": b_resp}), 200
            finally:
                try:
                    os.remove(tmp_name)
                except Exception:
                    pass

        elif API_A_MODE == "http":
            headers = {"X-API-KEY": API_A_SECRET} if API_A_SECRET else {}
            if USE_WEBHOOK:
                if not API_A_URL_ASYNC:
                    return jsonify({"ok": False, "error": "API_A_URL_ASYNC_NOT_SET"}), 500
                callback_id = "cbk_" + uuid.uuid4().hex[:10]
                callback_url = request.url_root.rstrip("/") + f"/from-api-a?callback_id={callback_id}&ui_session_id={ui_session_id}"
                files = {"file": ("audio", audio_bytes, "application/octet-stream")}
                data = {"callback_url": callback_url}
                r = requests.post(API_A_URL_ASYNC, data=data, files=files, headers=headers, timeout=TIMEOUT_S)
                r.raise_for_status()
                return jsonify({"ok": True, "mode": "audio->A(async)", "callback_id": callback_id, "status": "forwarded"}), 202
            else:
                if not API_A_URL_SYNC:
                    return jsonify({"ok": False, "error": "API_A_URL_SYNC_NOT_SET"}), 500
                files = {"file": ("audio", audio_bytes, "application/octet-stream")}
                r = requests.post(API_A_URL_SYNC, files=files, headers=headers, timeout=TIMEOUT_S)
                r.raise_for_status()
                a_resp = r.json()
                text = (a_resp.get("text") or "").strip()
                if not text:
                    return jsonify({"ok": False, "error": "ASR_EMPTY"}), 502
                try:
                    b_resp = call_api_b(text, meta)
                except requests.RequestException as e:
                    return jsonify({"ok": False, "error": "API_B_FAILED", "details": str(e)}), 502
                return jsonify({"ok": True, "mode": "audio->A(sync)->B", "text": text, "a_result": a_resp, "b_result": b_resp}), 200

        else:
            return jsonify({"ok": False, "error": "INVALID_API_A_MODE"}), 500

    return jsonify({"ok": False, "error": "UNSUPPORTED_CONTENT_TYPE"}), 415

@app.post("/from-api-a")
def from_api_a():
    """
    Permite que speech-to-text.py (si algún día hace push) mande el texto al router,
    y el router lo reenvía a API B.
    """
    raw = request.get_data()
    if not verify_hmac(request.headers.get("X-Signature", ""), raw, ROUTER_HMAC_SECRET):
        return jsonify({"ok": False, "error": "INVALID_SIGNATURE"}), 401

    payload = request.get_json(force=True)
    text = (payload.get("text") or "").strip()
    ui_session_id = request.args.get("ui_session_id")
    meta = {"ui_session_id": ui_session_id, "from": "api-a-push"}

    if not text:
        return jsonify({"ok": False, "error": "TEXT_REQUIRED"}), 400

    try:
        b_resp = call_api_b(text, meta)
    except requests.RequestException as e:
        return jsonify({"ok": False, "error": "API_B_FAILED", "details": str(e)}), 502

    return jsonify({"ok": True, "routed": "A->Router->B", "text": text, "b_result": b_resp}), 200

@app.get("/healthz")
def health():
    ok_core = bool(API_B_URL)
    if API_A_MODE == "process":
        ok_core &= os.path.isfile(API_A_SCRIPT)
    else:
        ok_core &= bool(API_A_URL_SYNC or (API_A_URL_ASYNC and USE_WEBHOOK))
    return jsonify({"status": "ok" if ok_core else "misconfigured", "mode": API_A_MODE})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
