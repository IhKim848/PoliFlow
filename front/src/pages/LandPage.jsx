import React from 'react';

export default function LandingPage() {
  return (
    <div className="relative w-full h-screen overflow-hidden bg-[var(--color-obsidian)] text-[var(--color-paper)] font-[var(--font-roobert)]">
      
      {/*background*/}
      <div className="absolute inset-0 z-0">
        <div className="w-full h-full bg-gradient-to-br from-[var(--color-inkstone)] to-[var(--color-obsidian)] opacity-80" />
        {/* 비디오 배경은 여기에 추가 (monopo saigon 처럼 물 흐르는 듯한 느낌) */}
      </div>

      {/*좌 상단 poliflow 로고 */}
      <div className="absolute z-20 top-[var(--spacing-28)] left-[var(--spacing-28)] md:top-[var(--spacing-40)] md:left-[var(--spacing-40)]">
        <h2 className="font-bold tracking-tight text-[var(--text-subheading)] md:text-[var(--text-subheading-lg)]">
          PoliFlow
        </h2>
      </div>

      {/*설명 + 시작 버튼 */}
      <div className="relative z-10 flex flex-col items-center justify-center w-full h-full px-[var(--spacing-28)]">
        
        {/* 설명 타이틀: 기존 서브 텍스트에서 메인 헤딩(text-heading)급으로 사이즈 업! */}
        <h1 className="max-w-5xl mb-[var(--spacing-48)] font-bold tracking-tight text-center text-[var(--text-display)] md:text-[var(--text-display)] leading-[var(--leading-heading)]">
          복잡한 청약 계산과 다양한 정책의 계산을<br />
          물 흐르듯 자연스럽게 해결합니다.
        </h1>

        {/* 시작하기 버튼 */}
        <button className="px-[var(--spacing-40)] py-[var(--spacing-12)] font-semibold text-black transition-transform duration-300 transform rounded-[var(--radius-full)] bg-[var(--color-paper)] hover:scale-105 hover:bg-[var(--color-ash-mist)]">
          시작하기
        </button>
        
      </div>
    </div>
  );
}