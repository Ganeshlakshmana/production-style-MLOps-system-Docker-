from collections import Counter
from src.utils.hashing import sha256_texts

def validate_and_baseline(texts, y, label_names):
    assert len(texts) > 0, "No data loaded"
    assert len(texts) == len(y), "Texts and labels length mismatch"

    label_counts = Counter(y)
    baseline = {
        "n": len(texts),
        "label_counts": {label_names[int(k)]: int(v) for k, v in label_counts.items()},
        "avg_text_len": sum(len(t) for t in texts) / max(1, len(texts)),
        "data_hash": sha256_texts(texts[:200]),  # MVP: hash subset for speed
    }
    return baseline
