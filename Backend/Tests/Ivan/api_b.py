import logging
from flask import Flask, request, jsonify

# --- Configuración de logs persistentes ---
logging.basicConfig(
    filename="api_b.log",       # Nombre del archivo de log
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

app = Flask(__name__)

@app.post("/intent")
def intent():
    data = request.get_json(force=True)
    logging.info(f"POST /intent - texto: {data.get('text')} meta: {data.get('meta')}")
    return jsonify({"ok": True, "received_text": data.get("text"), "meta": data.get("meta", {})})

if __name__ == "__main__":
    app.run(port=7000, debug=True)
