from flask import Flask, request, jsonify
app = Flask(__name__)

@app.post("/intent")
def intent():
    data = request.get_json(force=True)
    # Solo mostramos lo que recibimos para verificar el flujo
    return jsonify({
        "ok": True,
        "received_text": data.get("text"),
        "meta": data.get("meta", {})
    }), 200

@app.get("/healthz")
def health():
    return jsonify({"status":"ok"})

if __name__ == "__main__":
    app.run(port=7000, debug=True)
