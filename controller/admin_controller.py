from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import asyncio
from service.evaluation_service import run
from models.evaluation_request import EvaluationRequest

app = FastAPI(title="Policy Guard API")

@app.get("/evaluate")
async def evaluate_policy(request: EvaluationRequest):
    try:
        result = await run(request.policy_path, request.content)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))