# End-to-End MLOps Pipeline (Dockerized)

## Overview

This project implements a **production-style end-to-end MLOps system** covering:

- Batch model training
- Model evaluation and promotion
- Versioned model registry
- Containerized model serving
- Data drift monitoring with retraining signals

The system is fully **Dockerized**, reproducible, and designed to **Airflow-based workflows**, while being implemented in a **cost-free local environment** suitable for students.

The focus of this project is **ML systems engineering and MLOps**, not model complexity.

---

## High-Level Architecture

┌──────────────┐
│ Config YAML │
└──────┬───────┘
↓
┌────────────────────┐
│ Training Pipeline │
│ (Docker container) │
│ │
│ - Data ingestion │
│ - Validation │
│ - Preprocessing │
│ - Training │
│ - Evaluation │
│ - Registry update │
└──────┬─────────────┘
↓
┌──────────────────────────┐
│ Model Registry (Local) │
│ artifacts/registry/ │
│ - versioned runs │
│ - metrics │
│ - config snapshot │
│ - data hash │
│ - PRODUCTION pointer │
└──────┬──────────────────┘
↓
┌────────────────────┐
│ Serving Pipeline │
│ (FastAPI + Docker) │
│ - loads PROD model │
│ - /health │
│ - /predict │
└────────────────────┘

┌────────────────────┐
│ Monitoring Pipeline│
│ - Drift detection │
│ - PSI metric │
│ - Retrain signal │
└────────────────────┘


---

## Project Structure

mlops-studiolab-mvp/
│
├── docker/ # Docker images for training and serving
│ ├── Dockerfile.train
│ └── Dockerfile.serve
│
├── pipelines/ # Pipeline entrypoints (Airflow-ready)
│ ├── run_train_pipeline.py
│ └── run_monitoring.py
│
├── src/ # Core ML & MLOps logic
│ ├── ingestion/ # Data loading and validation
│ ├── features/ # Feature engineering
│ ├── training/ # Model training & evaluation
│ ├── registry/ # Model registry & promotion
│ ├── serving/ # FastAPI inference service
│ ├── monitoring/ # Drift detection
│ └── utils/ # Logging & hashing utilities
│
├── configs/ # Configuration files
│ ├── train.yaml
│ └── monitoring.yaml
│
├── artifacts/ # Persistent outputs
│ ├── registry/ # Model versions + PRODUCTION pointer
│ └── reports/ # Drift reports
│
└── requirements.txt


---

## Key Design Principles

- **Reproducibility first**: models are versioned with config snapshots and data hashes  
- **Separation of concerns**: training, serving, and monitoring are isolated  
- **Promotion gates**: only models that meet quality thresholds are deployed  
- **Container-first execution**: Docker replaces local virtual environments  
- **Orchestrator-ready**: pipelines map directly to Airflow DAG tasks  

---

## Training Pipeline

### What it does
- Loads and validates data
- Computes baseline statistics
- Performs preprocessing (TF-IDF)
- Trains a Logistic Regression model
- Evaluates using F1 score
- Registers a versioned model artifact
- Promotes the model if it passes a threshold

### Run training
```powershell
docker build -f docker/Dockerfile.train -t mlops-train .
docker run --rm -v ${PWD}\artifacts:/app/artifacts mlops-train python -u pipelines/run_train_pipeline.py
Output
artifacts/registry/
 ├── <run_id>/
 │   ├── model.joblib
 │   ├── vectorizer.joblib
 │   ├── metrics.json
 │   ├── baseline.json
 │   ├── config_snapshot.yaml
 │   └── data_hash.txt
 └── PRODUCTION
Model Registry & Promotion
Each training run is stored as a self-contained versioned artifact

A PRODUCTION pointer identifies the approved model

Serving and monitoring never guess which model to load

This mimics AWS SageMaker Model Registry behavior.

Serving Pipeline (Inference)
What it does
Runs a FastAPI service in Docker

Always loads the promoted production model

Applies the same preprocessing used during training

Returns predictions with model version metadata

Run serving
docker build -f docker/Dockerfile.serve -t mlops-serve .
docker run --rm -p 8000:8000 -v ${PWD}\artifacts:/app/artifacts mlops-serve
Test
Invoke-RestMethod `
  -Uri http://localhost:8000/predict `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"text":"NASA launched a new satellite into space"}'
Monitoring & Drift Detection
What it does
Loads the production model

Compares baseline vs new data distributions

Computes Population Stability Index (PSI)

Generates a drift report

Signals whether retraining is needed

Run monitoring
docker run --rm -v ${PWD}\artifacts:/app/artifacts mlops-train python -u pipelines/run_monitoring.py
Output
artifacts/reports/drift_report.json
Orchestration & Airflow Readiness
Airflow is not executed in this project, but the design is DAG-ready.

Each pipeline script in pipelines/ is a task entrypoint

Training, serving, and monitoring are idempotent and decoupled

These scripts can be wrapped directly by Airflow operators

Example mapping
Pipeline Script	Airflow DAG Task
run_train_pipeline.py	training DAG
run_monitoring.py	monitoring DAG
registry promotion	approval gate
AWS SageMaker Mapping
This Project	AWS Equivalent
Docker training container	SageMaker Training Job
Local registry folder	SageMaker Model Registry
PRODUCTION pointer	Model approval stage
FastAPI container	SageMaker Endpoint
Drift monitoring script	SageMaker Model Monitor
Pipelines folder	Airflow DAGs / Step Functions
Why the Model Is Simple
The ML model is intentionally lightweight:

Fast to train

Deterministic

Easy to monitor

This allows the project to focus on production ML systems, not research complexity.

Key Takeaway
This project demonstrates how to build reliable, reproducible, production-ready ML systems with:

clear ownership boundaries

explicit versioning

safe deployment practices

monitoring-driven retraining

The architecture is designed to scale from a local setup to cloud-managed MLOps platforms.

Next Improvements (Future Work)
Train/validation split with offline evaluation

CI/CD for container builds

MLflow or cloud-backed registry

Real-time alerting on drift

Full Airflow deployment
