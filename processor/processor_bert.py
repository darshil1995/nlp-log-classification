import os

# These are loaded lazily (inside the function) so that importing this module
# does NOT crash the server if the model file is missing or packages are absent.
_model_embedding = None
_model_classification = None


def _load_models():
    global _model_embedding, _model_classification
    if _model_embedding is None or _model_classification is None:
        import joblib
        from sentence_transformers import SentenceTransformer

        current_dir = os.path.dirname(__file__)
        model_path = os.path.join(current_dir, "..", "models", "log_classifier.joblib")

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Trained model not found at: {os.path.abspath(model_path)}\n"
                "Please run the training notebook first:\n"
                "  training/training_log_classification.ipynb"
            )

        _model_embedding = SentenceTransformer('all-MiniLM-L6-v2')
        _model_classification = joblib.load(model_path)


def classify_with_bert(log_message):
    _load_models()

    # 1. Encode the single message
    embeddings = _model_embedding.encode([log_message])

    # 2. Get probabilities
    probabilities = _model_classification.predict_proba(embeddings)[0]

    # 3. Threshold check
    if max(probabilities) < 0.5:
        return "Unknown"

    # 4. Predict label
    return _model_classification.predict(embeddings)[0]


if __name__ == "__main__":
    logs = [
        "alpha.osapi_compute.wsgi.server - 12.10.11.1 - API returned 404 not found error",
        "GET /v2/3454/servers/detail HTTP/1.1 RCODE   404 len: 1583 time: 0.1878400",
        "System crashed due to drivers errors when restarting the server",
        "Hey bro, chill ya!",
        "Multiple login failures occurred on user 6454 account",
        "Server A790 was restarted unexpectedly during the process of data transfer",
        "IP 192.168.133.114 blocked due to potential attack"
    ]
    results = [classify_with_bert(log) for log in logs]
    for log, label in zip(logs, results):
        print(f"[{label}] -> {log}")
