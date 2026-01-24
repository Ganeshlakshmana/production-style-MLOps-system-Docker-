import hashlib

def sha256_texts(texts) -> str:
    h = hashlib.sha256()
    for t in texts:
        h.update(t.encode("utf-8", errors="ignore"))
    return h.hexdigest()
