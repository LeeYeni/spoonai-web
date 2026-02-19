import { BASE_URL } from "./base";
import { SearchRequest, SearchResponse } from "@/schema/search";

export const recommend = async (request: SearchRequest): Promise<SearchResponse[]> => {
    const response = await fetch(`${BASE_URL}/api/search/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(request)
    });
    return response.json() as Promise<SearchResponse[]>;
}