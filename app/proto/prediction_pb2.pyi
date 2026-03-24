from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PredictRequest(_message.Message):
    __slots__ = ("gender", "age", "visits_per_week", "visits_last_7d", "visits_last_4w", "visits_prev_4w", "days_since_last_visit", "membership_price", "membership_duration_days", "membership_days_to_expire", "engagement_score")
    GENDER_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    VISITS_PER_WEEK_FIELD_NUMBER: _ClassVar[int]
    VISITS_LAST_7D_FIELD_NUMBER: _ClassVar[int]
    VISITS_LAST_4W_FIELD_NUMBER: _ClassVar[int]
    VISITS_PREV_4W_FIELD_NUMBER: _ClassVar[int]
    DAYS_SINCE_LAST_VISIT_FIELD_NUMBER: _ClassVar[int]
    MEMBERSHIP_PRICE_FIELD_NUMBER: _ClassVar[int]
    MEMBERSHIP_DURATION_DAYS_FIELD_NUMBER: _ClassVar[int]
    MEMBERSHIP_DAYS_TO_EXPIRE_FIELD_NUMBER: _ClassVar[int]
    ENGAGEMENT_SCORE_FIELD_NUMBER: _ClassVar[int]
    gender: str
    age: int
    visits_per_week: float
    visits_last_7d: int
    visits_last_4w: int
    visits_prev_4w: int
    days_since_last_visit: int
    membership_price: float
    membership_duration_days: int
    membership_days_to_expire: int
    engagement_score: float
    def __init__(self, gender: _Optional[str] = ..., age: _Optional[int] = ..., visits_per_week: _Optional[float] = ..., visits_last_7d: _Optional[int] = ..., visits_last_4w: _Optional[int] = ..., visits_prev_4w: _Optional[int] = ..., days_since_last_visit: _Optional[int] = ..., membership_price: _Optional[float] = ..., membership_duration_days: _Optional[int] = ..., membership_days_to_expire: _Optional[int] = ..., engagement_score: _Optional[float] = ...) -> None: ...

class PredictResponse(_message.Message):
    __slots__ = ("prediction", "churn_probability")
    PREDICTION_FIELD_NUMBER: _ClassVar[int]
    CHURN_PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    prediction: int
    churn_probability: float
    def __init__(self, prediction: _Optional[int] = ..., churn_probability: _Optional[float] = ...) -> None: ...
