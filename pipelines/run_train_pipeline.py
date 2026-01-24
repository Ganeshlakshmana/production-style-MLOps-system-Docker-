import sys
sys.path.append('.')

import os
import time
import yaml
from joblib import dump

from src.utils.logger import get_logger
from src.ingestion.load_data import load_dataset
from src.ingestion.validate_data import validate_and_baseline
from src.features.preprocess import fit_transform
from src.training.train import train_model
from src.training.evaluate import evaluate_model
from src.registry.register import register_run, maybe_promote

logger = get_logger('train_pipeline')

def main():
    with open('configs/train.yaml', 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)

    run_id = time.strftime('%Y%m%d-%H%M%S')

    texts, y, label_names = load_dataset(cfg['data']['categories'])
    baseline = validate_and_baseline(texts, y, label_names)

    X, vectorizer = fit_transform(texts)
    model = train_model(X, y, cfg)
    metrics = evaluate_model(model, X, y)

    run_dir = register_run(run_id, cfg, baseline, metrics)
    dump(model, os.path.join(run_dir, 'model.joblib'))
    dump(vectorizer, os.path.join(run_dir, 'vectorizer.joblib'))
    maybe_promote(run_id, metrics, cfg)

    logger.info(f'Run saved: {run_dir}')
    logger.info(f'Metrics: {metrics}')
    logger.info('If promoted, artifacts/registry/PRODUCTION points to this run_id.')

if __name__ == '__main__':
    main()
