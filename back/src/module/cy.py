import os
import json
from typing import Dict, Any
from core.policy_base import basePolicy

class CheongyakPolicy(basePolicy):
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "..", "..", "config", "chengyak.json")

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                rules = json.load(f)
        except FileNotFoundError:
            raise Exception("청약 기준 데이터 파일이 없음.")
        
        super().__init__(policy_rule=rules)

    def _calculate_linear_score(self, category_key: str, unit: int)->int:
        rule = self.rules["categories"][category_key]
        unit_count = max(0, min(unit, rule["max_unit_limit"]))
        calculated_score = rule["base_score"] + (unit_count * rule["score_per_unit"])
        return min(calculated_score, rule["max_score"])
    
    def calculate(self, user_profile: Dict[str, Any])->Dict[str, Any]:
        homeless_score = 0
        if not user_profile.get("has_house_in_family", False):
            homeless_score = self._calculate_linear_score(
                "homeless_period", user_profile.get("homeless_years", 0)
            )

        dependents_score = self._calculate_linear_score(
            "dependents", user_profile.get("dependents_count", 0)
        )

        subscription_score = self._calculate_linear_score(
            "subscription_period", user_profile.get("subscription_years", 0)
        )

        return {
            "breakdown": {
                "homeless_score": homeless_score,
                "dependents_score": dependents_score,
                "subscription_score": subscription_score
            },
            "total_score": homeless_score + dependents_score + subscription_score,
            "max_possible_score": self.rules["max_total_score"]
        }
    
    def valid_eligibility(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        is_eligible = True
        reasons = []

        min_age = self.rules.get("qualification", {}).get("min_age", 19)
        
        user_age = user_profile.get("age", 0)
        if user_age < min_age:
            is_eligible = False
            reasons.append(f"만 {min_age}세 이상만 청약이 가능합니다. (현재 {user_age}세)")

        return {
            "is_eligible": is_eligible,
            "reasons": reasons
        }
    