"use client";

import { useState } from "react";

interface SearchBarProps {
  onSearch: (query: string) => void;
}

export default function SearchBar({ onSearch }: SearchBarProps) {
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    if (!query.trim()) return;
    onSearch(query);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") handleSearch();
  };

  return (
    <section className="flex flex-col items-center justify-center py-20 px-4 w-full bg-linear-to-b from-orange-50/50 to-white">
      <div className="max-w-3xl w-full text-center space-y-6">
        {/* 타이틀 영역 */}
        <h2 className="text-2xl sm:text-4xl md:text-5xl lg:text-5xl font-black text-gray-900 tracking-tight">
          오늘 당신의 <span className="text-orange-500">취향</span>은 무엇인가요?
        </h2>
        <p className="text-gray-500 text-sm sm:text-lg md:text-lg lg:text-lg font-medium">
          "매콤달달한 떡볶이 맛집 알려줘"와 같이 구체적으로 물어보세요.
        </p>

        {/* 검색창 영역 */}
        <div className="relative mt-8 group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            className="w-full px-8 pr-32 py-5 text-lg rounded-full border-2 border-gray-100 bg-white shadow-xl focus:border-orange-500 focus:outline-none transition-all duration-300 group-hover:shadow-2xl text-gray-500"
          />
          <button
            onClick={handleSearch}
            className="absolute right-3 top-2.5 bottom-2.5 px-8 bg-orange-500 text-white font-bold rounded-full hover:bg-orange-600 active:scale-95 transition-all shadow-lg shadow-orange-200"
          >
            찾기
          </button>
        </div>
      </div>
    </section>
  );
}