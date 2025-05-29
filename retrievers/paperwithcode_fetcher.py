from paperswithcode import PapersWithCodeClient

def fetch_paperswithcode_papers(keywords, limit=5):
    client = PapersWithCodeClient()
    papers = []
    for keyword in keywords:
        results = client.paper_list(q=keyword, items_per_page=limit)
        for paper in results.results:
            papers.append({
                "title": paper.title,
                "url": paper.url_abs,
                "summary": paper.abstract or "",
                "source": "PapersWithCode"
            })
    return papers
