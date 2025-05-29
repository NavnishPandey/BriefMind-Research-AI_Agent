from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.pipelines import pipeline  
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import torch

class ResearchSummarizer:
    def __init__(self):
        model_name = "google/gemma-2b-it"

        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            low_cpu_mem_usage=True)

        # Use updated pipeline import
        hf_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=100,
            temperature=0.7,
            do_sample=True,
            return_full_text=False
        )

        # Wrap in LangChain's HuggingFacePipeline
        self.llm = HuggingFacePipeline(pipeline=hf_pipeline)

        self.prompt = PromptTemplate(
            input_variables=["title", "content"],
            template="""
You are a helpful scientific assistant.
Summarize the following research paper content in very easy way in 2–3 sentences.

Title: {title}
Content: {content}

Short Summary:"""
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def summarize(self, title: str, content: str) -> str:
        try:
            result = self.chain.run({"title": title, "content": content})
            return result.strip()
        except Exception as e:
            print(f"[ERROR] Summarization failed: {e}")
            return content[:250] + "..."

            