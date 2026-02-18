from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

class FAISSService:
    def __init__(self, index_path: str = "./data/faiss_index"):
        self.index_path = index_path

        directory = os.path.dirname(self.index_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        self.embeddings = OpenAIEmbeddings(
            api_key=self.OPENAI_API_KEY,
            model="text-embedding-3-small"
        )
        self.vector_store = self.load_index()
        self.indexed_restaurants = self.get_all_indexed_restaurants()

    def load_index(self):
        """
        서버 시작 시 로컬 저장소에서 FAISS 인덱스를 로드합니다.
        """
        if not os.path.exists(self.index_path):
            return None  # 초기에는 None을 반환하여 add_index에서 생성하도록 유도

        return FAISS.load_local(
            self.index_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
    
    def get_all_indexed_restaurants(self):
        """
        모든 메타데이터를 순회하며 {식당명: 내용} 딕셔너리를 생성합니다.
        """
        if not self.vector_store:
            return {}
        return {
            doc.metadata.get("restaurant"): doc.page_content
            for doc in self.vector_store.docstore._dict.values()
        }
    
    def is_already_indexed(self, restaurant: str):
        return restaurant in self.indexed_restaurants
    
    def get_content(self, restaurant: str):
        """
        딕셔너리 캐시에서 즉시 식당 관련 content를 반환합니다.
        """
        return self.indexed_restaurants.get(restaurant)

    async def add_index(self, processed_data: list):
        new_items = [item for item in processed_data if not self.is_already_indexed(item["restaurant"])]

        if not new_items:
            return

        texts = [item["content"] for item in new_items]

        metadatas = [
            {
                "restaurant": item['restaurant'],
                "content": item["content"]
            } for item in new_items
        ]

        if self.vector_store:
            await self.vector_store.aadd_texts(texts, metadatas=metadatas)
        else:
            self.vector_store = await FAISS.afrom_texts(texts, self.embeddings, metadatas=metadatas)

        for item in new_items:
            self.indexed_restaurants[item["restaurant"]] = item["content"]
        self.save()

    async def search(self, query: str, nearby_restaurants: list, k: int = 20):
        """
        주변 식당 리스트를 기반으로 필터링하여 의미 기반 검색을 수행합니다.
        """
        if not self.vector_store:
            return []
        
        search_filter = {"restaurant": nearby_restaurants}

        docs_and_scores = await self.vector_store.asimilarity_search_with_score(
            query,
            k=k,
            filter=search_filter
        )

        results = []
        for doc, score in docs_and_scores:
            results.append({
                "restaurant": doc.metadata.get("restaurant"),
                "content": doc.page_content,
                "score": float(score)  # 낮을수록 유사함
            })

        return results

    def save(self):
        """
        메모리의 인덱스를 파일로 영구 저장합니다.
        """
        if self.vector_store:
            self.vector_store.save_local(self.index_path)