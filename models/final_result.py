from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import uuid
from models.rule_result import RuleResult
from models.final_verdict import FinalVerdict

class FinalResult(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    policy_name: str
    policy_version: str
    final_verdict: FinalVerdict
    evaluated_at: datetime
    rule_results: List[RuleResult]
    total_latency_ms: int