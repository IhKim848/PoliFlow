import os
import requests
from dotenv import load_dotenv
import json
from google import genai
from pydantic import BaseModel

# .env 파일에서 인증키 불러오기
load_dotenv()
API_ID = os.getenv("LAW_API_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


# JSON 출력 스키마 정의
class Qualification(BaseModel):
    min_age: int
    must_be_homeless: bool
    notes: str

class CheongyakCategory(BaseModel):
    max_score: int
    base_score: int
    description: str
    score_per_unit: int
    max_unit_limit: int

class CheongyakRules(BaseModel):
    last_updated : str
    max_total_score: int
    qualification: Qualification
    homeless_period: CheongyakCategory
    dependents: CheongyakCategory
    subscription_period: CheongyakCategory

def fetch_and_parse_rules():
    
    # 법령 목록 조회 API 주소
    url = "https://www.law.go.kr/DRF/lawSearch.do"
    
    # 요청 파라미터
    params = {
        "OC": API_ID,             # 인증키
        "target": "eflaw",          # 서비스 대상
        "type": "JSON",           # 출력 형태: JSON
        "query": "주택공급에 관한 규칙"  # 검색을 원하는 질의
    }
    
    try:
        search_res = requests.get(url, params=params)
        search_res.raise_for_status()
        law_id = search_res.json()["LawSearch"]["law"][0]["법령일련번호"]
        
        serv_url = "https://www.law.go.kr/DRF/lawService.do"
        serv_params = {"OC": API_ID, "target": "eflaw", "type": "JSON", "MST": law_id}
        serv_res = requests.get(serv_url, params=serv_params)
        serv_data = serv_res.json()

        article_text = ""
        jo_list = []
        if "Law" in serv_data and "Joa" in serv_data["Law"]:
            jo_list = serv_data["Law"]["Joa"].get("Jo", [])
        elif "조문" in serv_data:
            jo_list = serv_data["조문"].get("조문단위", [])
        elif "법령" in serv_data and "조문" in serv_data["법령"]:
            jo_list = serv_data["법령"]["조문"].get("조문단위", [])

        for jo in jo_list:
            jo_str = str(jo)
            if jo.get("조문번호") == "0004" or "제4조" in jo_str:
                article_text = jo_str
                print("['제4조' 본문 데이터 확보 완료!]")
                break
        if not article_text:
            print("'제4조' 본문 데이터를 얻을 수 없음.")
        
        byl_list = []
        if "Law" in serv_data and "Byls" in serv_data["Law"]:
            byl_list = serv_data["Law"]["Byls"].get("Byl", [])
        elif "별표" in serv_data:
            byl_list = serv_data["별표"].get("별표단위", [])
        elif "법령" in serv_data and "별표" in serv_data["법령"]:
            byl_list = serv_data["법령"]["별표"].get("별표단위", [])
        
        raw_text = ""
        for byl in byl_list:
            byl_str = str(byl)
        
            if "[별표 1]" in byl_str or "별표1" in byl_str or byl.get("별표번호") == "0001":
                raw_text = byl_str
                break
        if not raw_text:
            print("'별표 1' 데이터를 찾을 수 없음.")
            return

        prompt = f"""
        다음은 대한민국 '주택공급에 관한 규칙'의 제4조(자격 요건)와 별표 1(가점 산정표) 원시 데이터입니다.
        1. '제4조'를 읽고 청약 신청의 최소 나이(min_age)와 무주택 필수 여부(must_be_homeless), 기타 요건(notes)을 추출하세요.
        2. '별표 1'의 선(┌, ├, │)으로 그려진 표를 읽고, 무주택기간, 부양가족수, 주택청약종합저축 가입기간의 
        상수(max_score, base_score, score_per_unit, max_unit_limit)와 요약(description)을 추출하세요.
        3. 총점(max_total_score)은 84점입니다.
        4. last_updated 에는 오늘 날짜를 YYYY-MM-DD 형식으로 넣어주세요.

        [제4조 원본 데이터]
        {article_text[:1500]}
    
        [별표 1 원본 데이터]
        {raw_text[:3500]}
        """

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": CheongyakRules,
            },
        )

        parsed_data = json.loads(response.text)
    
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_dir = os.path.join(current_dir, "..", "config")
        os.makedirs(config_dir, exist_ok=True)
        file_path = os.path.join(config_dir, "chengyak.json")
    
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=4)
        
        print("[완료] AI가 성공적으로 법령을 해석하여 JSON 파일로 저장했습니다")
        print(f"위치: {os.path.realpath(file_path)}")
    except Exception as e:
        print(f"API 에러 발생!: {e}")

if __name__ == "__main__":
    fetch_and_parse_rules()