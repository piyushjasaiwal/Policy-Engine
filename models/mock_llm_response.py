from pydantic import BaseModel, Field
from uuid import uuid4
from models.verdict import Verdict

class MockLLMResponse(BaseModel):
    trace_id: str = Field(default_factory=lambda: f"trace_{uuid4().hex}")
    verdict: Verdict
    confidence: float
    latency: float