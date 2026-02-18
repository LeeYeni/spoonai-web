from dotenv import load_dotenv
import os, httpx, html, re

load_dotenv()

class NaverClient:
    def __init__(self):
        self.NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
        self.NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
        self.base_url = "https://openapi.naver.com/v1/search/blog.json"

        self.headers = {
            "X-Naver-Client-Id": self.NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": self.NAVER_CLIENT_SECRET
        }

    def clean_text(self, text):
        # html 엔티티를 일반 문자로 변환
        text = html.unescape(text)

        # 모든 html 태그 제거
        text = re.sub(r"<[^>]+>", "", text)

        # *점, *역 노이즈 제거
        text = re.sub(r"\w{2,}(점|역)\b", " ", text)

        # 공백 축소
        text = re.sub(r"\s+", " ", text).strip()

        return text

    async def search_blog_reviews(self, restaurant: str, display: int = 100) -> str:
        """
        특정 검색어로 블로그 리뷰 요약을 가져옵니다.
        임베딩하기 좋게 하나의 문자열로 합쳐서 반환합니다.
        """
        restaurant = restaurant.replace(" ", "")

        query = f'"{restaurant}" 리뷰'

        params = {
            "query": query,
            "display": display,
            "sort": "sim"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, headers=self.headers, params=params)
            
            items = response.json().get("items", [])

            results = ""
            for item in items:
                title = self.clean_text(item["title"])

                if restaurant not in title.replace(" ", ""):
                    continue

                desc = self.clean_text(item["description"])
                results = results + f"\n[{title}] {desc}"

                if len(results) >= 500:
                    break

            if results == "":
                results = "리뷰가 존재하지 않습니다."

            return results
