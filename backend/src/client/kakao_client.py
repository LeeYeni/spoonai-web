from dotenv import load_dotenv
import os, httpx, asyncio

load_dotenv()

class KakaoClient:
    def __init__(self):
        self.KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")
        self.headers = {
            "Authorization": f"KakaoAK {self.KAKAO_API_KEY}"
        }
        # 한 번에 최대 5개 페이지만 동시에 요청하도록 제한
        self.semaphore = asyncio.Semaphore(5)

    async def search_restaurants(self, client: httpx.AsyncClient, x: float, y: float, radius: int = 500, page: int = 1, size: int = 15):
        base_url = "https://dapi.kakao.com/v2/local/search/category.json"

        # FD6: 음식점 | CE7: 카페
        params = {
            "category_group_code": "FD6",
            "x": str(x),
            "y": str(y),
            "radius": radius,
            "sort": "distance",
            "page": page,
            "size": size
        }

        async with self.semaphore:
            response = await client.get(base_url, headers=self.headers, params=params)
            
            data = response.json()
            documents = data.get("documents", [])

            results = []
            for doc in documents:
                # 식당명 가져오기
                place_name = doc["place_name"]
                place_name_lst = place_name.split()

                # 지점명 제거 로직
                if len(place_name_lst) > 1 and place_name_lst[-1].endswith("점"):
                    restaurant = " ".join(place_name_lst[:-1])
                else:
                    restaurant = place_name

                results.append({
                    "restaurant": restaurant,
                    "category_name": doc["category_name"],
                    "place_url": doc["place_url"]
                })

            return results
        
    async def search_restaurants_concurrently(self, x: float, y: float, max_pages: int = 4):
        """
        search_restaurants를 page 1부터 max_pages까지 병렬로 호출합니다.
        """
        points = [
            (x, y),                # 중심
            (x + 0.005, y),        # 동
            (x - 0.005, y),        # 서
            (x, y + 0.005),        # 남
            (x, y - 0.005)         # 북
        ]
        
        # Task 리스트 생성
        async with httpx.AsyncClient() as client:
            tasks = []
            for px, py in points:
                for page in range(1, max_pages + 1):
                    tasks.append(
                        self.search_restaurants(
                            client=client,
                            x=px,
                            y=py,
                            page=page
                        )
                    )

            # 병렬 실행
            results = await asyncio.gather(*tasks)

            # Flatten
            final_results = []
            seen_restaurants = set()

            for r_lst in results:
                for r in r_lst:
                    if r["restaurant"] not in seen_restaurants:
                        final_results.append(r)
                        seen_restaurants.add(r["restaurant"])

            return final_results