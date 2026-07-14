from .prompts import Profile_extract_prompt
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
        
        self.model_id = 'gemini-2.5-flash'

    def extract_profile(self, user_text: str)->dict:
        # AI에게 역할 부여 및 지시
        today_str = datetime.date.today().strftime("%Y년 %m월 %d일")
        system_inst = Profile_extract_prompt.format(today_str = today_str)

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