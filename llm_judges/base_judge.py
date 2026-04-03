from models.rule_result import RuleResult
from abc import ABC, abstractmethod
from common.circuit_breaker import CircuitBreaker
import asyncio
import logging
from llm_judges.mock_llm_judge import MockLLMJudge
from models.verdict import Verdict
from models.mock_llm_response import MockLLMResponse

class BaseJudge(ABC):

    """Abstract interface for all Judges."""
    @abstractmethod
    async def evaluate(self, rule_id: str, prompt: str, content: str, action: str) -> RuleResult:
        pass
    

    def create_raw_prompt(self, gaudrail:str, prompt:str, content:str):
        return f"{gaudrail}\nUSER CONTEXT: {prompt}\nCONTENT: {content}"

    async def call_llm_with_resilience(self, rule_id: str, llm_judge: MockLLMJudge, raw_prompt: str, breaker:CircuitBreaker, max_retries:int) -> MockLLMResponse:
        if not breaker.can_proceed():
            raise Exception("Circuit Breaker is OPEN. LLM service is currently unavailable.")
        

        try:
            for attempt in range(max_retries):
                try:
                    # 1. Handle Timeouts (e.g., 10 second limit)
                    return await asyncio.wait_for(
                        llm_judge.generate(raw_prompt), 
                        timeout=10.0
                    )

                except (asyncio.TimeoutError, Exception) as e:
                    wait_time = (2 ** attempt)
                    
                    logging.warning(f"LLM call failed (Attempt {attempt+1}): {e}. Retrying in {wait_time}s...")
                    
                    if attempt == max_retries - 1:
                        breaker.record_failure()
                        raise e
                    
                    await asyncio.sleep(wait_time)
            
            breaker.record_success()
        except Exception as e:
            # Graceful Fallback if LLM is dead or timing out
            return MockLLMResponse(
                verdict=Verdict.UNCERTAIN,
                confidence=0.0,
                latency=0.0
            )
        
        return MockLLMResponse(verdict=Verdict.UNCERTAIN, confidence=0.0, latency=0.0)