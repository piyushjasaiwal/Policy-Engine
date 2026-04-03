import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Literal

# Set up logging for production visibility
logger = logging.getLogger(__name__)

# Define custom types for better IDE support and safety
Verdict = Literal["PASS", "FAIL", "UNCERTAIN"]

class PolicyService:
    """
    Service to handle loading and sanitizing policy configurations.
    """

    @staticmethod
    def load_policy(file_path: str) -> Dict[str, Any]:
        path = Path(file_path)
        
        try:
            with path.open('r', encoding='utf-8') as file:
                raw_data = yaml.safe_load(file) or {}
                
            policy = raw_data.get('policy', {})
            if not policy:
                logger.error(f"Policy object missing in {file_path}")
                return {}

            # Process rules with list comprehension and basic sanitization
            formatted_rules = [
                {
                    "id": rule.get("id"),
                    # Clean up multi-line prompts for consistent processing
                    "judge_prompt": " ".join(rule.get("judge_prompt", "").split()),
                    "on_fail": rule.get("on_fail")  # This maps to our Literal type
                }
                for rule in policy.get('rules', [])
            ]

            return {
                "name": policy.get("name"),
                "version": policy.get("version"),
                "evaluation_strategy": policy.get("evaluation_strategy"),
                "threshold": policy.get("threshold"),
                "rules": formatted_rules
            }

        except FileNotFoundError:
            logger.error(f"Policy file not found: {file_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML in {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading policy {file_path}: {e}")
            raise
