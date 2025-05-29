# research_agent/main.py

from schedular.weekly_runner import WeeklyResearchAgent
import os


os.environ["HUGGINGFACE_TOKEN"] = "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"

def main():
    agent = WeeklyResearchAgent()
    agent.run()

if __name__ == "__main__":
    main()
