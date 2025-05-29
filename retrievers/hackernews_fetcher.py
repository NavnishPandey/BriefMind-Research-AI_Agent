# research_agent/retrievers/hackernews_fetcher.py

import requests
from datetime import datetime

class HackerNewsFetcher:
    def __init__(self):
        self.base_url = "https://hn.algolia.com/api/v1/search_by_date"

    def fetch(self, keywords, since_date):
        results = []
        for keyword in keywords:
            params = {
                "query": keyword,
                "tags": "story",
                "numericFilters": f"created_at_i>{self._date_to_unix(since_date)}"
            }
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("hits", []):
                    results.append({
                        "title": item.get("title", "No Title"),
                        "url": item.get("url", ""),
                        "summary": item.get("story_text") or item.get("title"),
                        "source": "hackernews"
                    })
            else:
                print(f"[ERROR] HackerNews fetch failed for {keyword} with status code {response.status_code}")
        return results

    def _date_to_unix(self, date_str):
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return int(dt.timestamp())
