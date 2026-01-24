import sys
sys.path.append('.')

import os
import json
import yaml
from src.ingestion.load_data import load_dataset
from src.registry.load_model import load_production
from src.monitoring.drift import psi

def main():
    with open('configs/train.yaml', 'r', encoding='utf-8') as f:
        train_cfg = yaml.safe_load(f)
    with open('configs/monitoring.yaml', 'r', encoding='utf-8') as f:
        mon_cfg = yaml.safe_load(f)

    texts, y, _ = load_dataset(train_cfg['data']['categories'])
    run_id, model, vec = load_production()

    expected = vec.transform(texts[:200]).mean(axis=0).A1
    actual = vec.transform(texts[200:400]).mean(axis=0).A1

    drift_score = psi(expected, actual, bins=10)
    threshold = mon_cfg['drift']['threshold']

    report = {
        'model_version': run_id,
        'drift_method': 'psi',
        'drift_score': drift_score,
        'threshold': threshold,
        'retrain_recommended': drift_score > threshold,
    }

    os.makedirs('artifacts/reports', exist_ok=True)
    with open('artifacts/reports/drift_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(report)
    if report['retrain_recommended']:
        print('DRIFT ALERT: retraining should be triggered.')

if __name__ == '__main__':
    main()
