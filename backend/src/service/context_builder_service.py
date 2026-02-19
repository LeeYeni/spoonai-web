import asyncio, httpx
from typing import Tuple
# import time

from src.client.kakao_client import KakaoClient
from src.client.naver_client import NaverClient
from src.service.faiss_service import FAISSService

class ContextBuilderService:
    def __init__(self, faiss_service: FAISSService):
        self.kakao_client = KakaoClient()
        self.naver_client = NaverClient()

        self.faiss_service = faiss_service

        # 동시에 실행할 요청 수를 10개로 제한
        self.semaphore = asyncio.Semaphore(10)

    async def get_review(self, client: httpx.AsyncClient, restaurant: str) -> Tuple[bool, str]:
        """
        세마포어를 통과하는 경우만 API를 사용해서 리뷰 데이터를 반환합니다.
        """
        # faiss_store에 저장되어 있는지 확인
        if self.faiss_service.is_already_indexed(restaurant):
            content = self.faiss_service.get_content(restaurant)
            return True, content
        
        # 저장되어 있지 않다면, 리뷰 데이터를 새로 가져오기
        async with self.semaphore:
            review = await self.naver_client.search_blog_reviews(client, restaurant)
            return False, review
        
    def compose_results(self, kakao_results, reviews):
        docs = []
        
        for k, (is_stored, text) in zip(kakao_results, reviews):
            if text == "리뷰가 존재하지 않습니다.":
                continue

            restaurant = k["restaurant"]
            content = text if is_stored else f"Restaurant: {restaurant}\n\nCategory: {k['category_name']}\n\nReview: {text}"

            docs.append({
                "restaurant": restaurant,
                "place_url": k["place_url"],
                "content": content
            })

        return docs

    async def build_search_context(self, x: float, y: float):
        async with httpx.AsyncClient() as client:
            # 카카오 식당 리스트 가져오기
            # start_time = time.time()
            kakao_results = await self.kakao_client.search_restaurants_concurrently(client, x, y)
            # print("500m 반경 내 식당 정보를 모두 가져옵니다.:", time.time() - start_time)

            if not kakao_results:
                return []
        
            # 병렬 처리 태스크 생성
            tasks = [
                self.get_review(client, r["restaurant"])
                for r in kakao_results
            ]

            # 병렬 처리
            # start_time = time.time()
            reviews = await asyncio.gather(*tasks)
            # print("500m 반경 내 식당 리뷰를 모두 가져옵니다.:", time.time() - start_time)

        return self.compose_results(kakao_results, reviews)