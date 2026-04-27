from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
def get_model_status():
    return {
        "modelName": "Random Forest Classifier",
        "version": "v1.0.0",
        "dataset": "UGRansom",
        "accuracy": 94.6,
        "precision": 93.8,
        "recall": 95.1,
        "f1Score": 94.4,
        "lastTrained": "2026-04-25",
        "status": "Loaded",
        "predictionMode": "Mock / Integration Ready",
    }