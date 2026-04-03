from pydantic import BaseModel

class EvaluationRequest(BaseModel):
    content: str
    policy_path: str 