import os
from joblib import load

REGISTRY = "artifacts/registry"

def load_production():
    prod_file = os.path.join(REGISTRY, "PRODUCTION")
    if not os.path.exists(prod_file):
        raise RuntimeError("No production model promoted yet.")
    run_id = open(prod_file, "r", encoding="utf-8").read().strip()
    run_dir = os.path.join(REGISTRY, run_id)

    model = load(os.path.join(run_dir, "model.joblib"))
    vectorizer = load(os.path.join(run_dir, "vectorizer.joblib"))
    return run_id, model, vectorizer
