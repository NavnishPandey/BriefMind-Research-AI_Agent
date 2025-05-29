import requests

def fetch_openalex_papers(keywords, days_back, limit=5):
    base_url = "https://api.openalex.org/works"
    headers = {"Accept": "application/json"}
    from datetime import datetime, timedelta
    since_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    papers = []

    for keyword in keywords:
        params = {
            "search": keyword,
            "filter": f"from_publication_date:{since_date}",
            "per_page": limit
        }
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            results = response.json().get('results', [])
            for item in results:
                papers.append({
                    "title": item.get("title"),
                    "url": item.get("id"),
                    "summary": item.get("abstract_inverted_index", ""),
                    "source": "OpenAlex"
                })
    return papers
