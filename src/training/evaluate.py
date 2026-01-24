from sklearn.metrics import f1_score

def evaluate_model(model, X, y):
    pred = model.predict(X)
    return {"f1": float(f1_score(y, pred, average="weighted"))}
