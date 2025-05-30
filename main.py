# research_agent/main.py

from schedular.weekly_runner import WeeklyResearchAgent
import os

from huggingface_hub import login
login("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")


def main():
    agent = WeeklyResearchAgent()
    agent.run()

if __name__ == "__main__":
    main()
