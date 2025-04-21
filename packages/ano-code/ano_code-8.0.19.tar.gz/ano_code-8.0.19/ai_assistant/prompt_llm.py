from groq import Groq
from openai import OpenAI
import openai
from ai_assistant.interfaces import LlmOptions, LlmInterface, AIAssistantInterface
from ai_assistant.consts import UserRole, AIModel
from typing import TypeVar
T = TypeVar('T')





class PromptLlm(LlmInterface):
    def __init__(self, llm_options: LlmOptions)-> None:
        super().__init__(llm_options)

    def prompt(self, cli: T) -> str:
        opt = self.llm_options
        chat_completion = cli.chat.completions.create(
                messages=opt.messages,
                model=AIModel.GEMMA_2_9_IT.value,
                temperature=0.5,
                max_tokens=30,
                top_p=1,
                stop=None,
                stream=False,
            )
        
        prompt_result = chat_completion.choices[0].message.content
        return prompt_result



class AIAssistant(AIAssistantInterface):
    def __init__(self, cli: Groq) -> None:
        super().__init__(cli)


    def run_assistant(self, prompt: str, command: str)-> str:
        llm_opt = LlmOptions(
        messages=[
            {
                "role": UserRole.SYSTEM_ROLE.value,
                "content": command
            },
            {
                "role": UserRole.USER_ROLE.value,
                "content": prompt,
            }
        ],
        model=AIModel.LLAMA_3_70B_VERSATILE.value,
        temperature=0.5,
        max_tokens=30,
        top_p=1,
        stop=None,
        stream=False,
        )
        promptLlm = PromptLlm(llm_opt)
        prompt_result = promptLlm.prompt(self.cli)
        return prompt_result
