from models.final_result import RuleResult
from typing import List
from models.final_verdict import FinalVerdict
from models.verdict import Verdict

class Aggregator:
    @staticmethod
    def resolve(results: List[RuleResult], strategy: str, threshold: float = 0.7) -> FinalVerdict:
        if strategy == "all":
            # [cite: 104]
            return FinalVerdict.BLOCK if any(r.verdict == Verdict.FAIL for r in results) else FinalVerdict.ALLOW
        
        if strategy == "weighted_threshold":
            total_weight = len(results)
            score = sum(1 for r in results if r.verdict == Verdict.FAIL) / total_weight
            return FinalVerdict.ALLOW if score >= threshold else FinalVerdict.BLOCK
            
        return FinalVerdict.BLOCK