
import requests

class RedditFetcher:
    def __init__(self):
        self.base_url = "https://www.reddit.com/search.json"
        self.headers = {"User-agent": "Mozilla/5.0"}

    def fetch(self, keyword: str, since_date: str):
        query = f"{keyword} timestamp:{since_date}.."
        params = {
            "q": query,
            "sort": "new",
            "restrict_sr": False,
            "t": "week",
            "limit": 10
        }
        response = requests.get(self.base_url, headers=self.headers, params=params)

        results = []
        if response.status_code == 200:
            data = response.json()
            for post in data["data"]["children"]:
                p = post["data"]
                results.append({
                    "title": p["title"],
                    "summary": p.get("selftext", "No text"),
                    "url": f"https://reddit.com{p['permalink']}",
                    "source": "reddit"
                })
        else:
            print("[ERROR] Reddit fetch failed", response.status_code)
        return results
