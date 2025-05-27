# research_rag_agent/summarizer/research_summarizer.py

from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class ResearchSummarizer:
    def __init__(self):
        template = (
            "Summarize this research paper concisely:\n\n"
            "Title: {title}\n\n"
            "Abstract: {abstract}\n\n"
            "Summary:"
        )
        self.prompt = PromptTemplate(template=template, input_variables=["title", "abstract"])
        self.llm = HuggingFaceHub(
            repo_id="google/gemma-1.1-2b-it",
            model_kwargs={"temperature": 0.3, "max_new_tokens": 300}
        )
        self.chain = LLMChain(prompt=self.prompt, llm=self.llm)

    def summarize_papers(self, papers):
        summaries = []
        for paper in papers:
            print(f"[INFO] Summarizing: {paper['title']}")
            response = self.chain.run({
                "title": paper["title"],
                "abstract": paper["summary"]
            })
            summaries.append({
                "title": paper["title"],
                "url": paper["url"],
                "published": paper["published"],
                "summary": response.strip()
            })
        return summaries