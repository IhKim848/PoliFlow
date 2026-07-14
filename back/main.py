from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.ai.agent import ProfileExtractorAgent
from dotenv import load_dotenv
from src.ai.agent import ProfileExtractorAgent
from src.module.cy import CheongyakPolicy

# .env 로드
load_dotenv()

app = FastAPI(
    title = "금융 정책 통합 계산기 API",
    description= "Fast API를 이용한 back-end server",
    version = "1.0.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# react에서 받아올 데이터 형태 정의
class ProfileRequest(BaseModel):
    user_input: str

agent = ProfileExtractorAgent()
cy_calculate = CheongyakPolicy()

@app.get("/")
def read_root():
    """서버 health check"""
    return {"message" : "Fast API 정상 작동 중"}

@app.post("/api/extract-profile")
def extract_profile(request: ProfileRequest):
    try:
        profile_data = agent.extract_profile(request.user_input)

        if not profile_data:
            raise HTTPException(
                status_code=400,
                detail = "분석에 실패하였습니다. 상황을 더 자세히 적어주세요."
            )
        eligibility_result = cy_calculate.valid_eligibility(profile_data)
        score_result = cy_calculate.calculate(profile_data)

        return {
            "status" : "success",
            "message" : "AI가 성공적으로 프로필을 추출하여 계산을 완료하였습니다.",
            "data": {
                "profile" : profile_data,
                "eligibilty" : eligibility_result,
                "score" : score_result
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"오류 발생! : {str(e)}")