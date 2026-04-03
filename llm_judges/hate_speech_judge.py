from llm_judges.base_judge import BaseJudge
from llm_judges.mock_llm_judge import MockLLMJudge
from models.rule_result import RuleResult
from models.verdict import Verdict
from common.circuit_breaker import CircuitBreaker

class HateSpeechJudge(BaseJudge):
    """
    Simulates a high-performance LLM API that judges the hate speech in the content.
    """

    def __init__(self) -> None:
        self.breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=60)
        self.max_retries = 3
        self.llm_judge = MockLLMJudge()
        self.HATE_SPEECH_GUARDRAIL = """
            ROLE:
            You are a specialist in Content Moderation and Safety Compliance. Your objective is to identify Hate Speech within the provided CONTENT.

            DEFINITION OF HATE SPEECH:
            Content that promotes violence, incites hatred, promotes discrimination, or disparages on the basis of race or ethnic origin, religion, disability, age, nationality, veteran status, sexual orientation, gender or gender identity.

            CRITERIA:
            - FAIL: The content uses slurs, dehumanizing language, calls for violence, or asserts the inferiority of a protected group.
            - PASS: The content is neutral, critical without being hateful, or does not target protected groups.
            - UNCERTAIN: The content uses reclaimed slurs, complex satire, or linguistic nuances that make a definitive safety judgment impossible.

            INSTRUCTIONS:
            1. Analyze the CONTENT against the DEFINITION.
            2. Provide a verdict of PASS, FAIL, or UNCERTAIN.
            3. Be objective: ignore personal political opinions; focus strictly on safety policy.

            OUTPUT FORMAT:
            Verdict: [PASS/FAIL/UNCERTAIN]
            Confidence: [0.0 to 1.0]
            Reasoning: [Identify the specific protected group targeted or why it is safe]

            CONTENT TO EVALUATE:
        """

    async def evaluate(self, rule_id: str, prompt: str, content: str, action: str) -> RuleResult:

        raw_prompt = self.create_raw_prompt(gaudrail=self.HATE_SPEECH_GUARDRAIL, prompt=prompt, content=content)
        
        # Simulate Decision Logic
        llm_response = await self.call_llm_with_resilience(rule_id=rule_id, llm_judge=self.llm_judge, raw_prompt=raw_prompt, breaker=self.breaker, max_retries=self.max_retries)

        if llm_response.verdict == Verdict.UNCERTAIN:
            reasoning = "The judge cannot decide with certainity PII information present in the content."

        elif llm_response.verdict == Verdict.PASS:
            reasoning = "Detected prohibited terminology in the content"
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