import os
import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL_VERSION = os.getenv("MODEL_VERSION", "v0.9.9")
MODEL_TYPE = os.getenv("MODEL_TYPE", "stable")
MODEL_PATH = os.getenv("MODEL_PATH", "models/stable_model.pkl")

model = None

def load_model():
    global model
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Файл модели не найден: {MODEL_PATH}")
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print(f"Загружена модель: {MODEL_TYPE} версия {MODEL_VERSION}")

load_model()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "version": MODEL_VERSION,
        "model_type": MODEL_TYPE
    })

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True) or {}
        features = data.get("x", [5.1, 3.5, 1.4, 0.2])
        
        if len(features) != 4:
            return jsonify({"error": "Нужно 4 признака"}), 400
        
        prediction = model.predict([features])[0]
        
        species = {0: "setosa", 1: "versicolor", 2: "virginica"}
        
        return jsonify({
            "status": "ok",
            "version": MODEL_VERSION,
            "model_type": MODEL_TYPE,
            "prediction": int(prediction),
            "species": species.get(prediction, "unknown")
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
