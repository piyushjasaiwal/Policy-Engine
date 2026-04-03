from llm_judges.hate_speech_judge import HateSpeechJudge
from llm_judges.pii_judge import PIIJudge
from llm_judges.professional_tone_judge import ProfessionalToneJudge

class JudgeFactoryService:

    """
    Service factory responsible for instantiating and retrieving specialized 
    judge objects based on policy rule identifiers.

    Currently, this factory acts as a hardcoded router to local judge 
    implementations (e.g., HateSpeech, PII, Professional Tone).

    This factory is a structural placeholder. Once a real LLM is 
    fully integrated, this manual routing logic can be replaced by a 
    'Tool Call' or 'Function Calling' mechanism, allowing the LLM to 
    dynamically select the appropriate validation tool based on the rule context.
    """

    def __init__(self):
        self.hate_speech_judge = HateSpeechJudge()
        self.pii_judge = PIIJudge()
        self.professional_tone_judge = ProfessionalToneJudge()

    def judge_factory(self, rule_id:str):
        if rule_id == "no_hate_speech":
            return self.hate_speech_judge
        
        elif rule_id == "no_pii":
            return self.pii_judge
        
        elif rule_id == "professional_tone":
            return self.professional_tone_judge
        
        else:
            raise RuntimeError("No Judge available for the rule mentioned") 