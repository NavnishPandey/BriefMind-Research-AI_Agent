# research_agent/retrievers/arxiv_fetcher.py

import arxiv

class ArxivFetcher:
    def fetch(self, keyword: str, since_date: str, max_results=10):
        query = f"{keyword} AND submittedDate:[{since_date}0000 TO *]"
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        results = []
        for result in search.results():
            results.append({
                "title": result.title,
                "summary": result.summary,
                "url": result.entry_id,
                "source": "arxiv"
            })
        return results
