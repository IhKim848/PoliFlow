import React, { useState } from 'react';

export default function CalculatorPage() {
  const [userInput, setUserInput] = useState('');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    setIsLoading(true);
    setError('');
    setResult(null);
    
    try {
      const response = await fetch('https://poliflow.onrender.com/api/extract-profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_input: userInput })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setResult(data.data);
      } else {
        setError(data.detail || "분석 중 오류가 발생했습니다.");
      }
    } catch (err) {
      console.error(err);
      setError("서버와 연결할 수 없습니다. 백엔드 서버가 켜져 있는지 확인해주세요.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="bg-white p-6 md:p-10 rounded-2xl shadow-xl w-full max-w-3xl">
        <h1 className="text-3xl font-bold mb-2 text-center text-blue-600">AI 청약 계산기</h1>
        <p className="text-gray-500 text-center mb-8">상황을 이야기하듯 편하게 작성해주세요. AI가 알아서 분석해 드립니다!</p>
        
        {/* 자연어 입력 폼 */}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <textarea 
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="예시: 나는 서울에 사는 96년생이야. 현재 미혼이고 무주택 3년차야. 연봉은 5천만원 정도고 청약통장은 2년 됐어. 부양가족은 없고, 세대원 중에 집을 가진 사람도 없어."
            className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none resize-none h-32"
          />
          <button 
            type="submit" 
            disabled={isLoading}
            className={`py-4 rounded-xl font-bold text-white transition-all ${
              isLoading ? 'bg-blue-300 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 hover:shadow-lg'
            }`}
          >
            {isLoading ? 'AI가 문장을 분석하고 계산하는 중...' : '분석 및 점수 계산하기'}
          </button>
        </form>

        {error && (
          <div className="mt-6 p-4 bg-red-50 text-red-600 rounded-xl font-medium text-center">
            🚨 {error}
          </div>
        )}

        {result && (
          <div className="mt-8 space-y-6 animate-fade-in-up">
            <hr className="border-gray-200" />
            
            {/* 1. AI가 추출한 프로필  */}
            <div className="bg-gray-50 p-6 rounded-xl border border-gray-100">
              <h3 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
                <span>🤖</span> AI가 추출한 나의 프로필
              </h3>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="flex flex-col bg-white p-3 rounded-lg shadow-sm">
                  <span className="text-gray-500 text-xs mb-1">만 나이</span>
                  <span className="font-semibold text-gray-800">{result.profile.age || 0}세</span>
                </div>
                <div className="flex flex-col bg-white p-3 rounded-lg shadow-sm">
                  <span className="text-gray-500 text-xs mb-1">거주 지역</span>
                  <span className="font-semibold text-gray-800">{result.profile.location || '알 수 없음'}</span>
                </div>
                <div className="flex flex-col bg-white p-3 rounded-lg shadow-sm">
                  <span className="text-gray-500 text-xs mb-1">혼인 여부</span>
                  <span className="font-semibold text-gray-800">{result.profile.martial_status || '미혼'}</span>
                </div>
                <div className="flex flex-col bg-white p-3 rounded-lg shadow-sm">
                  <span className="text-gray-500 text-xs mb-1">연소득</span>
                  <span className="font-semibold text-gray-800">
                    {result.profile.annual_income ? `${result.profile.annual_income.toLocaleString()}원` : '0원'}
                  </span>
                </div>
                <div className="flex flex-col bg-white p-3 rounded-lg shadow-sm">
                  <span className="text-gray-500 text-xs mb-1">무주택 기간</span>
                  <span className="font-semibold text-gray-800">{result.profile.homeless_year || 0}년</span>
                </div>
                <div className="flex flex-col bg-white p-3 rounded-lg shadow-sm">
                  <span className="text-gray-500 text-xs mb-1">유주택 세대원</span>
                  <span className="font-semibold text-gray-800">{result.profile.has_house_in_family ? '있음' : '없음'}</span>
                </div>
                <div className="flex flex-col bg-white p-3 rounded-lg shadow-sm">
                  <span className="text-gray-500 text-xs mb-1">청약통장 가입</span>
                  <span className="font-semibold text-gray-800">{result.profile.subscription_years || 0}년</span>
                </div>
                <div className="flex flex-col bg-white p-3 rounded-lg shadow-sm">
                  <span className="text-gray-500 text-xs mb-1">부양가족 수</span>
                  <span className="font-semibold text-gray-800">{result.profile.dependents_count || 0}명</span>
                </div>
              </div>
            </div>

            {/* 2. 자격 요건 및 점수 결과 */}
            {!result.eligibilty.is_eligible ? (
              <div className="p-5 bg-red-50 border border-red-200 text-red-700 rounded-xl">
                <h3 className="font-bold mb-2 flex items-center gap-2">
                  <span>❌</span> 청약 신청 불가
                </h3>
                <p className="text-sm">{result.eligibilty.reasons.join(', ')}</p>
              </div>
            ) : (
              <div className="p-8 bg-blue-50 border border-blue-200 rounded-xl text-center shadow-sm">
                <h3 className="text-xl font-bold text-blue-800 mb-2">청약 신청 가능!</h3>
                <div className="text-5xl font-extrabold text-blue-600 mb-6 drop-shadow-sm">
                  총 {result.score.total_score}점
                </div>
                <div className="flex flex-wrap justify-center gap-4 text-sm font-medium text-blue-800 bg-white inline-flex p-3 rounded-full shadow-sm">
                  <span className="px-3 border-r border-blue-100">무주택: <span className="font-bold">{result.score.breakdown.homeless_score}점</span></span>
                  <span className="px-3 border-r border-blue-100">부양가족: <span className="font-bold">{result.score.breakdown.dependents_score}점</span></span>
                  <span className="px-3">통장가입: <span className="font-bold">{result.score.breakdown.subscription_score}점</span></span>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}