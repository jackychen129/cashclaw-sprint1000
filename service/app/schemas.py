from pydantic import BaseModel, Field


class PlanRequest(BaseModel):
    profile: str = Field(..., min_length=5)
    hours_per_day: int = Field(..., ge=1, le=12)
    target_usd: int = Field(default=1000, ge=100)
    days: int = Field(default=30, ge=7, le=60)


class RunRequest(BaseModel):
    objective: str = Field(..., min_length=8)
    context: str = Field(default="")
    quality: str = Field(default="balanced")


class ExperimentRequest(BaseModel):
    current_offer: str = Field(..., min_length=6)
    channel: str = Field(..., min_length=3)
    last_metrics: str = Field(..., min_length=5)
    constraint_hours_per_day: int = Field(..., ge=1, le=12)


class LLMResult(BaseModel):
    provider: str
    model: str
    content: str


class PlanResponse(BaseModel):
    plan: str
    routed_via: str


class RunResponse(BaseModel):
    output: str
    routed_via: str


class ExperimentResponse(BaseModel):
    experiment: str
    routed_via: str
