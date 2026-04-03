from models.final_result import FinalResult
import time
import asyncio
from service.aggregation_service import Aggregator
from datetime import datetime
from service.judge_factory_service import JudgeFactoryService

class PolicyEngine:
    def __init__(self):
        self.judge_factory_service = JudgeFactoryService()

    async def evaluate_content(self, policy_config: dict, content: str) -> FinalResult:
        start_time = time.time()

        tasks = []

        for rule in policy_config["rules"]:
            judge = self.judge_factory_service.judge_factory(rule["id"])
            tasks.append(
                judge.evaluate(
                    rule["id"], 
                    rule["judge_prompt"], 
                    content, 
                    rule["on_fail"]
                )
            )
        
        rule_results = (await asyncio.gather(*tasks))
        
        final_verdict = Aggregator.resolve(
            rule_results, 
            policy_config.get("evaluation_strategy", "all"),
            policy_config.get("threshold", 0.7)
        )

        return FinalResult(
            policy_name=policy_config["name"],
            policy_version=policy_config["version"],
            final_verdict=final_verdict,
            evaluated_at= datetime.now(),
            rule_results=rule_results,
            total_latency_ms=int((time.time() - start_time) * 1000)
        )