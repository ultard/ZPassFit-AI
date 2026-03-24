from __future__ import annotations

from concurrent import futures
import logging
import os
import signal
import threading

import grpc

from app.predictor import ChurnPredictor
from app.proto import prediction_pb2, prediction_pb2_grpc


class PredictionService(prediction_pb2_grpc.PredictionServiceServicer):
    def __init__(self, predictor: ChurnPredictor) -> None:
        self._predictor = predictor

    def Predict(
        self,
        request: prediction_pb2.PredictRequest,
        context: grpc.ServicerContext,
    ) -> prediction_pb2.PredictResponse:
        payload = {
            "gender": request.gender,
            "age": request.age,
            "visits_per_week": request.visits_per_week,
            "visits_last_7d": request.visits_last_7d,
            "visits_last_4w": request.visits_last_4w,
            "visits_prev_4w": request.visits_prev_4w,
            "days_since_last_visit": request.days_since_last_visit,
            "membership_price": request.membership_price,
            "membership_duration_days": request.membership_duration_days,
            "membership_days_to_expire": request.membership_days_to_expire,
        }
        if request.HasField("engagement_score"):
            payload["engagement_score"] = request.engagement_score
        prediction, probability = self._predictor.predict(payload)
        return prediction_pb2.PredictResponse(
            prediction=prediction,
            churn_probability=probability,
        )


def serve() -> None:
    host = os.getenv("GRPC_HOST", "0.0.0.0")
    port = os.getenv("GRPC_PORT", "50051")
    shutdown_grace = float(os.getenv("GRPC_SHUTDOWN_GRACE_SECONDS", "5"))

    predictor = ChurnPredictor()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    prediction_pb2_grpc.add_PredictionServiceServicer_to_server(
        PredictionService(predictor),
        server,
    )
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    logging.info("gRPC server started on %s:%s", host, port)

    shutdown_event = threading.Event()
    stop_lock = threading.Lock()
    stopping = False

    def stop_server(signum: int | None = None, _frame: object | None = None) -> None:
        nonlocal stopping
        with stop_lock:
            if stopping:
                return
            stopping = True
        signal_name = signal.Signals(signum).name if signum is not None else "UNKNOWN"
        logging.info(
            "Shutdown signal received (%s). Stopping gRPC server with %.1fs grace.",
            signal_name,
            shutdown_grace,
        )
        server.stop(grace=shutdown_grace)
        shutdown_event.set()

    signal.signal(signal.SIGINT, stop_server)
    signal.signal(signal.SIGTERM, stop_server)

    try:
        shutdown_event.wait()
    except KeyboardInterrupt:
        stop_server(signal.SIGINT, None)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
