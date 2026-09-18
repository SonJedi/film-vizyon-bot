import os
import requests
from datetime import datetime

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
TMDB_USERNAME = os.environ.get("TMDB_USERNAME")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

def check_releases():
    today = datetime.now().strftime("%Y-%m-%d")
    
    # TMDb Watchlist Çekme
    watchlist_url = f"https://api.themoviedb.org/3/account/{TMDB_USERNAME}/watchlist/movies?api_key={TMDB_API_KEY}&language=tr-TR"
    res = requests.get(watchlist_url).json()
    
    movies = res.get("results", [])
    for movie in movies:
        movie_id = movie["id"]
        title = movie["title"]
        
        # Türkiye Vizyon Tarihi Sorgulama
        release_url = f"https://api.themoviedb.org/3/movie/{movie_id}/release_dates?api_key={TMDB_API_KEY}"
        rel_data = requests.get(release_url).json()
        
        for country in rel_data.get("results", []):
            if country["iso_3166_1"] == "TR":
                for date_info in country["release_dates"]:
                    # Sinema Vizyon Türü (3 = Theatrical)
                    if date_info.get("type") == 3:
                        release_date = date_info["release_date"].split("T")[0]
                        if release_date == today:
                            msg = f"🎬 *Müjde! İzleme Listendeki Film Bugün Vizyonda!*\n\n🍿 *{title}*\n📅 Bugün Türkiye sinemalarında gösterime girdi. İyi seyirler!"
                            send_telegram(msg)

if __name__ == "__main__":
    check_releases()
