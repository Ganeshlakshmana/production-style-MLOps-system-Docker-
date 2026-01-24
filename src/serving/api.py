from fastapi import FastAPI
from pydantic import BaseModel
from src.registry.load_model import load_production

app = FastAPI()

class Req(BaseModel):
    text: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(req: Req):
    run_id, model, vec = load_production()
    X = vec.transform([req.text])
    proba = float(model.predict_proba(X).max())
    pred = int(model.predict(X)[0])
    return {"label_id": pred, "proba": proba, "model_version": run_id}
