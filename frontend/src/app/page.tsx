"use client";

import { recommend } from "@/api/search";
import { SearchResponse, SearchRequest } from "@/schema/search";

import { useState } from "react";
import SearchBar from "@/component/searchBar";
import SearchResultList from "@/component/searchResultList";
import { useLocation } from "@/client/useLocation";

export default function Home() {
  const [results, setResults] = useState<SearchResponse[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  
  // 분리된 훅에서 좌표와 에러 상태를 가져옴
  const { coords, error: locationError } = useLocation();

  const handleSearch = async (query: string) => {
    setIsLoading(true);

    const x = coords?.x || 126.832633;
    const y = coords?.y || 37.634643;

    const request: SearchRequest = { x, y, query}
    const data = await recommend(request);

    setResults(data);
  };

  return (
    <div className="flex flex-col w-full min-h-screen bg-white">
      {/* 위치 정보 권한 거부 시 안내 배너 */}
      {locationError && (
        <div className="bg-orange-50 text-orange-600 text-xs text-center py-2 font-medium">
          ⚠️ {locationError} (기본 위치로 검색됩니다)
        </div>
      )}

      {/* 검색창 섹션 */}
      <SearchBar onSearch={handleSearch} />

      {/* 결과 리스트 섹션 */}
      <SearchResultList results={results} isLoading={isLoading} />
    </div>
  );
}