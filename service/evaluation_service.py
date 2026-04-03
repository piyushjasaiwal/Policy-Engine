from service.policy_engine import PolicyEngine
from service.policy_service import PolicyService
from service.audit_service import log_audit_trail

async def run(policy_path: str, content:str):
    engine = PolicyEngine()

    policy_data = PolicyService.load_policy(policy_path)
    
    result = await engine.evaluate_content(policy_data, content)
    
    log_audit_trail(result)

    return result