from __future__ import annotations

from pathlib import Path

import pandas as pd
from catboost import CatBoostClassifier

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "catboost_model.cbm"


class ChurnPredictor:
    def __init__(self, model_path: Path = MODEL_PATH) -> None:
        if not model_path.exists():
            raise FileNotFoundError(f"CatBoost model not found: {model_path}")
        self._model = CatBoostClassifier()
        self._model.load_model(str(model_path))
        self._features = list(self._model.feature_names_)

    def predict(self, payload: dict[str, object]) -> tuple[int, float]:
        prepared_payload = dict(payload)
        if (
            "engagement_score" in self._features
            and "engagement_score" not in prepared_payload
        ):
            # Fallback heuristic when client does not send this feature.
            prepared_payload["engagement_score"] = float(
                prepared_payload.get("visits_per_week", 0.0)
            )

        frame = pd.DataFrame([prepared_payload], columns=self._features)
        prediction = int(self._model.predict(frame)[0])
        probability = float(self._model.predict_proba(frame)[0][1])
        return prediction, probability
