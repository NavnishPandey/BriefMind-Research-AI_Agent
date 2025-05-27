# research_rag_agent/main.py

from scheduler.weekly_runner import WeeklyRunner
from retrievers.research_retriever import ResearchRetriever
from summarizer.research_summarizer import ResearchSummarizer
from notify.email_notifier import EmailNotifier
from storage.local_storage import LocalStorage


def main():
    print("[INFO] Starting Research Agent...")

    # Setup modules
    retriever = ResearchRetriever()
    summarizer = ResearchSummarizer()
    storage = LocalStorage()
    notifier = EmailNotifier()

    # Runner will handle the flow
    runner = WeeklyRunner(retriever, summarizer, storage, notifier)
    runner.run()


if __name__ == "__main__":
    main()
