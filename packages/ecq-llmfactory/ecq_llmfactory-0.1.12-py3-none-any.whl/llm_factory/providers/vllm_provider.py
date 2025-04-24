from langchain_community.llms import VLLM
from langchain_openai import ChatOpenAI
from llm_factory.factory_llm import AbstractLLMFactory

class vLLMFactory(AbstractLLMFactory):
    """Factory for HuggingFace models"""

    def create_model(self, client_server_mode=True):
        if client_server_mode:
            return ChatOpenAI(
                model=self.config.model_name,
                temperature=self.config.temperature,
                openai_api_key=self.config.api_key,
                openai_api_base=self.config.api_base,
                http_client=self.config.http_client
            )
        llm = VLLM(
            model=self.config.model_name,
            # trust_remote_code=True,  # mandatory for hf models
            tensor_parallel_size=self.config.tensor_parallel_size,
            max_tokens=self.config.max_tokens,
            top_p=self.config.top_p,
            temperature=self.config.temperature,
            vllm_kwargs={'gpu_memory_utilization':self.config.gpu_memory_utilization,
                        'max_model_len': self.config.max_model_len},
        )

        return llm