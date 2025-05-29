from datetime import datetime, timedelta
from retrievers.arxiv_fetcher import ArxivFetcher
from retrievers.reddit_fetcher import RedditFetcher
from retrievers.hackernews_fetcher import HackerNewsFetcher
from retrievers.paperwithcode_fetcher import fetch_paperswithcode_papers
from retrievers.openalex_fetcher import fetch_openalex_papers
from Summarizer.summarize import ResearchSummarizer
from storage.db import LocalStorage
from notify.email_notifier import EmailNotifier
import os
import yaml
from dotenv import load_dotenv

load_dotenv()

class WeeklyResearchAgent:
    def __init__(self):
        print("[INIT] Loading config and initializing components...")
        try:
            with open("/teamspace/studios/this_studio/Geo-Aware-Rag_System-for-Travelers/config.yaml", "r") as f:
                config = yaml.safe_load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load config.yaml: {e}")
            raise

        self.keywords = config["keywords"]
        self.days_back = config["days_back"]
        self.recipient_email = os.getenv("recipient_email")
        self.sender_email = os.getenv("sender_email")
        self.sender_password = os.getenv("sender_password")

        if not self.sender_email or not self.sender_password:
            print("[WARNING] EMAIL_USER or EMAIL_PASS not set in environment!")

        # Core components
        self.arxiv_fetcher = ArxivFetcher()
        self.reddit_fetcher = RedditFetcher()
        self.hackernews_fetcher = HackerNewsFetcher()
        self.summarizer = ResearchSummarizer()
        self.storage = LocalStorage()
        self.notifier = EmailNotifier(self.sender_email, self.sender_password)
        print("[INIT] Initialization complete.")

    def run(self):
        print("[RUN] Starting weekly digest pipeline...")

        since_date = (datetime.now() - timedelta(days=self.days_back)).strftime("%Y-%m-%d")
        print(f"[INFO] Fetching articles since {since_date} for keywords: {self.keywords}")

        try:
            print(f"[FETCH] Fetching from Arxiv...")
            arxiv_papers = self.arxiv_fetcher.fetch(self.keywords, since_date)
            print(f"[SUCCESS] Arxiv: {len(arxiv_papers)} papers fetched.")
        except Exception as e:
            print(f"[ERROR] Arxiv fetch failed: {e}")
            arxiv_papers = []

        try:
            print(f"[FETCH] Fetching from Reddit...")
            reddit_posts = self.reddit_fetcher.fetch(self.keywords, since_date)
            print(f"[SUCCESS] Reddit: {len(reddit_posts)} posts fetched.")
        except Exception as e:
            print(f"[ERROR] Reddit fetch failed: {e}")
            reddit_posts = []

        try:
            print(f"[FETCH] Fetching from Hacker News...")
            hackernews_posts = self.hackernews_fetcher.fetch(self.keywords, since_date)
            print(f"[SUCCESS] Hacker News: {len(hackernews_posts)} posts fetched.")
        except Exception as e:
            print(f"[ERROR] Hacker News fetch failed: {e}")
            hackernews_posts = []
        
        try:
            print("[FETCH] Fetching from PapersWithCode...")
            pwc_papers = fetch_paperswithcode_papers(self.keywords)
            print(f"[SUCCESS] PapersWithCode: {len(pwc_papers)} papers fetched.")
        except Exception as e:
            print(f"[ERROR] PapersWithCode fetch failed: {e}")
            pwc_papers = []

        try:
            print("[FETCH] Fetching from OpenAlex...")
            openalex_papers = fetch_openalex_papers(self.keywords, self.days_back)
            print(f"[SUCCESS] OpenAlex: {len(openalex_papers)} papers fetched.")
        except Exception as e:
            print(f"[ERROR] OpenAlex fetch failed: {e}")
            openalex_papers = []


        all_items = arxiv_papers + reddit_posts + hackernews_posts + pwc_papers + openalex_papers
        summarized = []

        print(f"[INFO] Total items to process: {len(all_items)}")

        for item in all_items:
            title = item.get('title', 'NO TITLE')
            print(f"\n[PROCESS] Processing: {title}")

            if self.storage.is_duplicate(title):
                print(f"[SKIP] Duplicate found, skipping: {title}")
                continue

            try:
                summary = self.summarizer.summarize(title, item.get('summary', ''))
                item['summary'] = summary
                print(item['summary'])
                summarized.append(item)
                self.storage.add_summary(item)
                print(f"[SUCCESS] Summary added for: {title}")
            except Exception as e:
                print(f"[ERROR] Failed to summarize: {title} | {e}")

        if summarized:
            try:
                print(f"[EMAIL] Sending email to: {self.recipient_email}")
                self.notifier.send_digest(self.recipient_email, summarized)
                self.storage.persist()
                print("[DONE] Digest sent and storage persisted.")
            except Exception as e:
                print(f"[ERROR] Failed to send email or persist storage: {e}")
        else:
            print("[INFO] No new summaries this week. No email sent.")
