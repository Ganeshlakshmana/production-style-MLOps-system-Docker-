from sklearn.linear_model import LogisticRegression

def train_model(X, y, cfg):
    max_iter = cfg["model"].get("max_iter", 200)
    model = LogisticRegression(max_iter=max_iter)
    model.fit(X, y)
    return model
