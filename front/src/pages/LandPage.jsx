import React from 'react';
import {Link} from 'react-router-dom';

export default function LandPage() {
  return (
    <div className="relative w-full h-screen overflow-hidden bg-[var(--color-obsidian)] text-[var(--color-paper)] font-[var(--font-roobert)]">
      
      {/*background*/}
      <div className="absolute inset-0 z-0 bg-[var(--color-obsidian)]">
        <video
          autoPlay
          loop
          muted
          playsInline
          className = "object-cover w-full h-full opacity-80"
        >
          <source src="/assets/fluid-background.mp4" type="video/mp4" />
        </video>
        <div className="absolute inset-0 bg-balck/30" />
      </div>

      {/*좌 상단 poliflow 로고 */}
      <div className="absolute z-20 top-[var(--spacing-28)] left-[var(--spacing-28)] md:top-[var(--spacing-40)] md:left-[var(--spacing-40)]">
        <Link to ="/">
          <h2 className="font-bold tracking-tight text-3l md:text-3l lg:text-1xl text-white-600 hover:text-gray-700 transition-colors">
            PoliFlow
          </h2>
        </Link>
      </div>

      {/*설명 + 시작 버튼 */}
      <div className="relative z-10 flex flex-col items-center justify-center w-full h-full px-[var(--spacing-28)]">
        
        <h1 className="w-full mb-[100px] font-bold tracking-tight text-center text-[40px] md:text-[50px] lg:text-[60px] leading-tight font-sans">
          복잡한 청약 계산과 다양한 정책의 계산을<br />
          물 흐르듯 자연스럽게 해결.
        </h1>

        {/* 시작하기 버튼 */}
        <Link to="/calculator">
          <button className="px-[var(--spacing-40)] py-[var(--spacing-12)] font-semibold text-black transition-transform duration-300 transform rounded-[var(--radius-full)] bg-[var(--color-paper)] hover:scale-105 hover:bg-[var(--color-ash-mist)]">
            시작하기
          </button>
        </Link>
        
        
      </div>
    </div>
  );
}