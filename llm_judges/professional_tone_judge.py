from common.circuit_breaker import CircuitBreaker
from llm_judges.base_judge import BaseJudge
from models.rule_result import RuleResult
from llm_judges.mock_llm_judge import MockLLMJudge

class ProfessionalToneJudge(BaseJudge):
    """
    Simulates a high-performance LLM API that judges the professional tone of the content.
    Right now for mocking purpose all the judges have the same evaluation logic.
    This logic can be later changed according to requirements when actual LLM is integrated in the project.
    """

    def __init__(self) -> None:
        self.breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=60)
        self.max_retries = 3
        self.llm_judge = MockLLMJudge()
        self.PROFESSIONAL_TONE_GUARDRAIL = """
            ROLE:
            You are an expert Corporate Communications Consultant and Linguist. Your task is to evaluate the provided CONTENT for professional tone, clarity, and workplace appropriateness.

            CRITERIA FOR "PASS":
            - Language is respectful, objective, and constructive.
            - Clear and concise structure.
            - Free of excessive slang, aggressive language, or unprofessional emotional outbursts.

            CRITERIA FOR "FAIL":
            - Contains insults, profanity, or passive-aggressive remarks.
            - Use of overly casual "text-speak" in a formal context (e.g., "u r late lol").
            - Hostile or discriminatory language.
            - Highly incoherent or disorganized thought patterns.

            INSTRUCTIONS:
            1. Review the CONTENT against the CRITERIA.
            2. Return 'PASS' if the tone is professional.
            3. Return 'FAIL' if the tone is unprofessional or offensive.
            4. Return 'UNCERTAIN' if the text is too short to judge or contains mixed tones that are hard to categorize.

            OUTPUT FORMAT:
            Verdict: [PASS/FAIL/UNCERTAIN]
            Confidence: [0.0 to 1.0]
            Reasoning: [1-sentence explanation of the tone detected]

            CONTENT TO EVALUATE:
        """

    async def evaluate(self, rule_id: str, prompt: str, content: str, action: str) -> RuleResult:

        raw_prompt = self.create_raw_prompt(gaudrail=self.PROFESSIONAL_TONE_GUARDRAIL, prompt=prompt, content=content)
        
        # Simulate Decision Logic
        llm_response = await self.call_llm_with_resilience(rule_id=rule_id, llm_judge=self.llm_judge, raw_prompt=raw_prompt, breaker=self.breaker, max_retries=self.max_retries)

        if llm_response.verdict == "UNCERTAIN":
            reasoning = "The judge cannot decide with certainity about the tone of the content."

        elif llm_response.verdict == "FAIL":
            reasoning = "Detected prohibited terminology in the content"
        else:
            reasoning = "No policy violations detected. Content appears safe."
        
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