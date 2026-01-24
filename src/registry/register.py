import os
import json
import yaml

REGISTRY = "artifacts/registry"

def register_run(run_id, cfg, baseline, metrics):
    run_dir = os.path.join(REGISTRY, run_id)
    os.makedirs(run_dir, exist_ok=True)

    with open(os.path.join(run_dir, "config_snapshot.yaml"), "w") as f:
        yaml.safe_dump(cfg, f)

    with open(os.path.join(run_dir, "baseline.json"), "w") as f:
        json.dump(baseline, f, indent=2)

    with open(os.path.join(run_dir, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    with open(os.path.join(run_dir, "data_hash.txt"), "w") as f:
        f.write(baseline["data_hash"])

    return run_dir

def maybe_promote(run_id, metrics, cfg):
    threshold = cfg["registry"].get("promote_threshold_f1", 0.0)
    if metrics.get("f1", 0.0) >= threshold:
        with open(os.path.join(REGISTRY, "PRODUCTION"), "w") as f:
            f.write(run_id)
