#API inerta para probar incorporación
#Imports
import logging
from flask import Flask, request, jsonify

#Configuración de los logs
logging.basicConfig(
    filename="api_b.log",
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
#Puerto 7000 en el localhost -> 127.0.0.1:7000
if __name__ == "__main__":
    app.run(port=7000, debug=True)
