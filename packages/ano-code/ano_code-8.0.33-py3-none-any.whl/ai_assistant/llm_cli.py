import os
from groq import Groq
from openai import OpenAI

groq_client = Groq(
        api_key= "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",)
    

openai_client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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",
)
