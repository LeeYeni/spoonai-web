import { useState, useEffect } from "react";

export const useLocation = () => {
  const [coords, setCoords] = useState<{ x: number; y: number } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!("geolocation" in navigator)) {
      setError("이 브라우저는 위치 정보를 지원하지 않습니다.");
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setCoords({
          x: position.coords.longitude, // 경도
          y: position.coords.latitude,  // 위도
        });
      },
      (err) => {
        setError("위치 정보를 가져오지 못했습니다: " + err.message);
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
    );
  }, []);

  return { coords, error };
};