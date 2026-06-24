import datetime
from abc import ABC, abstractmethod
from typing import Dict, Any

class basePolicy(ABC):
    """
    추상 부모 클래스 선언하기.
    모듈들은 이 클래스를 바탕으로 해서 구현 필요
    """
    def __init__(self, policy_rule: Dict[str, Any]):
        self.rules = policy_rule

    # 가점, 한도 계산
    @abstractmethod
    def calculate(self, user_profile: Dict[str, Any])->Dict[str,Any]:
        pass

    # 지원 자격 충족 검사
    @abstractmethod
    def valid_eligibility(self, user_profile: Dict[str, Any])->Dict[str, Any]:
        pass

    @staticmethod
    def calculate_age(birth_date_str: str)->int:
        try:
            birth_date = datetime.datetime.strptime(birth_date_str, "%Y-%m-%d").date()
            today = datetime.date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        except ValueError:
            raise ValueError("YYYY-MM-DD 형식으로 입력해주세요.")
    
    # 사용자의 소득이 기준선 제한에 걸리는지 판별
    @staticmethod
    def is_income_cutoff(user_income: int, cutoff_lim: int)-> bool:
        return user_income <= cutoff_lim