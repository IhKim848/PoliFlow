import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# 환경변수 불러오기
load_dotenv()

# 추출 스키마 정의
class UserProfile(BaseModel):
    age : int | None = Field(description="만 나이")
    location: str | None = Field(description="거주 지역")
    martial_status: str | None = Field(description="'미혼' 또는 '기혼'")
    annual_income: int | None = Field(description="연소득")
    homeless_year: int | None = Field(description="무주택 기간")

class ProfileExtractorAgent:
    def __init__(self):
        try:
            self.client = genai.Client()
        except Exception as e:
            raise ValueError("Error: Gemini Key 확인 필요함.")
        
        self.model_id = 'gemini-3.5-flash'

    def extract_profile(self, user_text: str)->dict:
        # AI에게 역할 부여 및 지시
        system_inst = """
        당신의 역할은 금융 정책 자격 요건을 분석하는 데이터 추출 전문가입니다.
        사용자의 입력을 분석하여 제공된 스키마에 맞게 빈칸을 채워주세요.
        """

        full_prompt = f"{system_inst}\n\n 사용자 입력: {user_text}"
        try:
            response = self.client.models.generate_content(
                model = self.model_id,
                contents = full_prompt,
                config = types.GenerateContentConfig(
                    response_mime_type = "application/json",
                    response_schema = UserProfile,
                )
            )
            return json.loads(response.text)
        except json.JSONDecodeError:
            print("Error: JSON 파싱 실패")
            return {}
        except Exception as e:
            print(f"Error: API 호출 오류-{e}")
            return {}