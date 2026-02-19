import { SearchResponse } from "@/schema/search";

export default function SearchResultItem({ restaurant, place_url }: SearchResponse) {
  return (
    <div className="group relative flex flex-col p-6 rounded-2xl border border-gray-100 bg-white shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
      {/* 장식용 아이콘 영역 (식당 아이콘) */}
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-orange-50 text-2xl group-hover:bg-orange-500 group-hover:scale-110 transition-all duration-300">
        <span className="group-hover:filter group-hover:brightness-0 group-hover:invert">
          📍
        </span>
      </div>

      {/* 식당 이름 */}
      <h3 className="text-xl font-bold text-gray-900 group-hover:text-orange-600 transition-colors">
        {restaurant}
      </h3>

      {/* 하단 버튼 영역 */}
      <div className="mt-6 flex items-center justify-between">
        {place_url ? (
          <a
            href={place_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center text-sm font-semibold text-orange-500 hover:text-orange-700 transition-colors"
          >
            카카오맵 상세보기
            <svg 
              className="ml-1 w-4 h-4 transition-transform group-hover:translate-x-1" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </a>
        ) : (
          <span className="text-sm text-gray-300">위치 정보 준비 중</span>
        )}
      </div>
    </div>
  );
}