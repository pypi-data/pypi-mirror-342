from abc import ABC, abstractmethod
from groq import  NotGiven
from typing import Iterable, List, Literal, TypeVar, List

T = TypeVar('T')




class LlmOptions:
    def __init__(self, messages: Iterable[any], model: str, temperature: float | NotGiven | None, max_tokens:  int | NotGiven | None, top_p: float | NotGiven | None, stop: str | List[str] | NotGiven | None, stream: NotGiven | Literal[False] | None):
        self.messages = messages
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.stop = stop
        self.stream = stream

class LlmInterface(ABC):
    def __init__(self, llm_options: LlmOptions):
        self.llm_options = llm_options
    
    @abstractmethod
    def prompt(llm_options, cli: T)-> str:
        ...


class AIAssistantInterface(ABC):
    def __init__(self, cli: T)-> None:
        self.cli = cli
    
    @abstractmethod
    def run_assistant(cli, prompt: str, command: str)-> str:
        ...
