# PoliFlow 

![PoliFlow 메인 화면](<img width="1943" height="1577" alt="image" src="https://github.com/user-attachments/assets/e1f27dd2-db69-4c1b-9057-b7fcf68dee82" />)

## 프로젝트 소개 (About the Project)
* 청약 점수를 계산하는 계산기는 많습니다.
* 그러나 대화형으로 작성하면 알아서 AI가 분석해서 최종적으로 점수를 제공하는 계산기는 없습니다.
* Poliflow는 어려운 전문 용어나 복잡한 입력 폼 대신, 상황을 입력하면, AI가 이를 분석하여 정확한 청약 가점과 신청 가능 여부를 즉시 계산해 줍니다.

## 핵심 기능
* **자연어 기반 프로필 추출 (AI 문맥 분석):** 장문의 텍스트에서 사용자의 나이, 혼인 여부, 무주택 기간, 연소득, 부양가족 수 등을 정확하게 추출합니다.
* **맞춤형 청약 점수 계산:** 추출된 프로필 데이터를 바탕으로 무주택 기간, 부양가족 수, 청약통장 가입 기간에 따른 청약 가점을 계산하여 제공합니다.
* **직관적인 UI/UX:** 복잡한 입력창 대신 단일 텍스트 박스 디자인을 채택했습니다.

## 기술 스택

### Frontend
* **Framework:** React
* **Styling:** Tailwind CSS
* **Deployment:** Vercel

### Backend
* **Framework:** FastAPI (Python)
* **API & Data:** RESTful API 설계, 공공데이터포털(국가법령정보 등) 규칙 적용
* **Deployment:** Render

## Architecture
1. **User Input:** 사용자가 프론트엔드(React)에서 자신의 상황을 자연어로 입력합니다.
2. **Data Processing:** 백엔드(FastAPI) 서버로 데이터가 전송되며, AI 모듈이 텍스트 내에서 청약 계산에 필요한 핵심 프로필 정보(JSON)를 추출해 냅니다.
3. **Calculation:** 추출된 데이터를 기반으로 주택공급 규칙에 맞추어 항목별 가점을 계산합니다.
4. **Result:** 계산된 총점과 자격 여부, 항목별 점수 내역을 프론트엔드로 반환하여 시각적으로 보여줍니다.

이 프로젝트는 2026 000 오픈소스 소프트웨어 대회 출품작입니다.
