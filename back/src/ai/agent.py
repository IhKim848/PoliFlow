import os
import datetime
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
    has_house_in_family: bool | None = Field(description="본인 포함 세대원 중 유주택자의 여부 (true/false)")
    subscription_years: int | None = Field(description="청약통장 가입 기간 (단위: 년)")
    dependents_count: int | None = Field(description="본인을 제외한 부양가족 수 (배우자, 부모, 자녀 등)")

class ProfileExtractorAgent:
    def __init__(self):
        try:
            self.client = genai.Client()
        except Exception as e:
            raise ValueError("Error: Gemini Key 확인 필요함.")
        
        self.model_id = 'gemini-3.5-flash'

    def extract_profile(self, user_text: str)->dict:
        # AI에게 역할 부여 및 지시
        today_str = datetime.date.today().strftime("%Y년 %m월 %d일")
        system_inst = """
        당신의 역할은 금융 정책 자격 요건을 분석해 금융 정책 계산에 필요한 프로필 데이터를 추출하는 역할을 하는 전문가입니다.
        오늘은 {today_str} 입니다.
        만약 사용자가 "96년생", "올해 서른", "작년에 가입" 과 같이 상대적인 시간이나 출생 연도를 말하면,
        반드시 위의 오늘 날짜를 기준으로 하여 정확한 '현재 만 나이' 나 '기간(연수)'을 수학적으로 계산하여 기록해주세요.
        사용자의 입력을 분석하여 제공된 스키마에 맞게 빈칸을 채워주세요.
        """

        full_prompt = f"{system_inst}\n\n 오늘 날짜: {today_str}\n\n 사용자 입력: {user_text}"
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