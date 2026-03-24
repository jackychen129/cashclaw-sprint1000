from fastapi import FastAPI, HTTPException

from .schemas import PlanRequest, PlanResponse, RunRequest, RunResponse
from .orchestrator import ModelOrchestrator

app = FastAPI(title="CashClaw Sprint1000 Service", version="0.1.0")
orchestrator = ModelOrchestrator()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/plan", response_model=PlanResponse)
async def create_plan(req: PlanRequest) -> PlanResponse:
    prompt = f"""
You are building a 30-day income sprint plan.
User profile: {req.profile}
Hours/day: {req.hours_per_day}
Target USD: {req.target_usd}
Days: {req.days}

Output:
1) One high-probability micro-offer
2) Day-by-day execution plan
3) Daily outreach quota
4) Delivery checklist
5) Weekly review rubric
Use concise bullet points and practical actions.
""".strip()
    try:
        content, routed = await orchestrator.complete(prompt, quality="high")
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=502, detail=f"Model call failed: {exc}") from exc
    return PlanResponse(plan=content, routed_via=routed)


@app.post("/v1/run", response_model=RunResponse)
async def run_task(req: RunRequest) -> RunResponse:
    prompt = f"""
Objective: {req.objective}
Context: {req.context}

Return a practical output that can be executed today.
""".strip()
    try:
        content, routed = await orchestrator.complete(prompt, quality=req.quality)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=502, detail=f"Model call failed: {exc}") from exc
    return RunResponse(output=content, routed_via=routed)
