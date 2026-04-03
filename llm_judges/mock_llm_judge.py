import random
import time
import asyncio
from models.mock_llm_response import MockLLMResponse
from models.verdict import Verdict

class MockLLMJudge:
    async def generate(self, prompt) -> MockLLMResponse:
        """
        Generates a mock response with random verdict and confidence.
        Note: We pass values into the constructor, not define them inside.
        """
        
        start_time = time.time()

        # Simulate real time LLM call latency
        await asyncio.sleep(random.uniform(0.1, 0.3)) 

        end_time = time.time()

        latency = int((end_time - start_time) * 1000)

        confidence = round(random.uniform(0.49, 0.99), 2)

        if confidence < 0.5:
            verdict = Verdict.UNCERTAIN
        else:
            verdict = random.choice([Verdict.PASS, Verdict.FAIL])

        return MockLLMResponse(
            verdict=verdict,
            confidence=confidence,
            latency=latency
        )
