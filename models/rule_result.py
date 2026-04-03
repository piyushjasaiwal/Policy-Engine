from pydantic import BaseModel, Field
from models.verdict import Verdict

class RuleResult(BaseModel):
    rule_id: str
    verdict: Verdict
    confidence: float
    reasoning: str
    action: str
    latency_ms: float
    raw_prompt: str
    raw_response: str