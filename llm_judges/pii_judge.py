from common.circuit_breaker import CircuitBreaker
from llm_judges.base_judge import BaseJudge
from llm_judges.base_judge import BaseJudge
from models.rule_result import RuleResult
from llm_judges.mock_llm_judge import MockLLMJudge

class PIIJudge(BaseJudge):
    """
    Simulates a high-performance LLM API that judges the professional tone of the content.
    """

    def __init__(self):
        self.breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=60)
        self.max_retries = 3
        self.llm_judge = MockLLMJudge()
        self.PII_GUARDRAIL = """
            ROLE:
            You are an expert Privacy Compliance Auditor. Your task is to analyze the provided CONTENT for Personally Identifiable Information (PII).

            CRITERIA:
            PII includes, but is not limited to:
            - Full Names, Phone Numbers, Home Addresses.
            - Government IDs (SSN, Passport, Driver's License).
            - Financial info (Credit Card numbers, Bank Accounts).
            - Digital identifiers (Email addresses, IP addresses, private URLs).
            - Biometric data or health records.

            INSTRUCTIONS:
            1. Review the CONTENT against the CRITERIA.
            2. If ANY clear PII is found, return: FAIL.
            3. If no PII is found, return: PASS.
            4. If the content is highly ambiguous or you are unsure, return: UNCERTAIN.

            OUTPUT FORMAT:
            Your response must follow this strict format:
            Verdict: [PASS/FAIL/UNCERTAIN]
            Confidence: [0.0 to 1.0]
            Reasoning: [Brief explanation of what was found or why it is safe]

            CONTENT TO EVALUATE:
        """

    async def evaluate(self, rule_id: str, prompt: str, content: str, action: str) -> RuleResult:

        raw_prompt = self.create_raw_prompt(gaudrail=self.PII_GUARDRAIL, prompt=prompt, content=content)
        
        # Simulate Decision Logic
        llm_response = await self.call_llm_with_resilience(rule_id=rule_id, llm_judge=self.llm_judge, raw_prompt=raw_prompt, breaker=self.breaker, max_retries=self.max_retries)

        if llm_response.verdict == "UNCERTAIN":
            reasoning = "The judge cannot decide with certainity PII information present in the content."

        elif llm_response.verdict == "FAIL":
            reasoning = "Detected pii information in the content"
        else:
            reasoning = "No policy violations detected. Content appears to be PII free."
        
        return RuleResult(
            rule_id=rule_id,
            verdict=llm_response.verdict,
            confidence=llm_response.confidence,
            reasoning=reasoning,
            action=action,
            latency_ms=llm_response.latency,
            raw_prompt=raw_prompt,
            raw_response=f"Raw result: trace_id {llm_response.trace_id}. {llm_response.verdict} at {llm_response.confidence} confidence with {llm_response.latency} latency."
        )