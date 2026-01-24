import numpy as np

def psi(expected, actual, bins=10, eps=1e-6):
    q = np.linspace(0, 1, bins + 1)
    cuts = np.quantile(expected, q)
    cuts[0], cuts[-1] = -np.inf, np.inf

    e_hist, _ = np.histogram(expected, bins=cuts)
    a_hist, _ = np.histogram(actual, bins=cuts)

    e = e_hist / max(1, e_hist.sum())
    a = a_hist / max(1, a_hist.sum())

    e = np.clip(e, eps, 1.0)
    a = np.clip(a, eps, 1.0)

    return float(np.sum((a - e) * np.log(a / e)))
