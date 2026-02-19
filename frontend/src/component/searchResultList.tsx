import SearchResultItem from "./searchResultItem";
import { SearchResponse } from "@/schema/search";

interface SearchResultListProps {
  results: SearchResponse[];
  isLoading: boolean;
}

export default function SearchResultList({ results, isLoading }: SearchResultListProps) {
  // 로딩 중일 때 보여줄 스켈레톤 UI (사용자 경험 향상)
  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map((n) => (
            <div key={n} className="h-48 rounded-2xl bg-gray-100 animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  // 검색 결과가 없을 때
  if (results.length === 0) {
    return (
      <div className="container mx-auto px-4 py-20 text-center">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gray-50 text-4xl mb-6">
          🥄
        </div>
        <h3 className="text-xl font-bold text-gray-900">아직 스푼이 비어있어요</h3>
        <p className="text-gray-500 mt-2">
          먹고 싶은 메뉴나 분위기를 입력해 취향을 찾아보세요!
        </p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-10">
      {/* 검색 결과 요약 */}
      <div className="flex items-center gap-2 mb-8">
        <h3 className="text-lg font-bold text-gray-900">검색 결과</h3>
        <span className="px-2.5 py-0.5 rounded-full bg-orange-100 text-orange-600 text-sm font-bold">
          {results.length}
        </span>
      </div>

      {/* 카드 그리드 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {results.map((item, index) => (
          <SearchResultItem
            key={`${item.restaurant}-${index}`}
            restaurant={item.restaurant}
            place_url={item.place_url}
          />
        ))}
      </div>
    </div>
  );
}