export interface SearchRequest {
    x: number;
    y: number;
    query: string;
}

export interface SearchResponse {
    restaurant: string;
    place_url: string;
}