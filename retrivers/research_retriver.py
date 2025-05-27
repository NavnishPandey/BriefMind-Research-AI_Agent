# research_rag_agent/retrievers/research_retriever.py

import arxiv
from datetime import datetime, timedelta

class ResearchRetriever:
    def __init__(self, query="AI alignment", days_back=7, max_results=10):
        self.query = query
        self.days_back = days_back
        self.max_results = max_results

    def fetch_papers(self):
        print(f"[INFO] Fetching latest papers for query: {self.query}")
        search = arxiv.Search(
            query=self.query,
            max_results=self.max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        one_week_ago = datetime.now() - timedelta(days=self.days_back)
        recent_papers = []

        for result in search.results():
            if result.published >= one_week_ago:
                recent_papers.append({
                    "title": result.title,
                    "summary": result.summary,
                    "url": result.entry_id,
                    "published": result.published.isoformat()
                })

        print(f"[INFO] Retrieved {len(recent_papers)} new papers.")
        return recent_papers
