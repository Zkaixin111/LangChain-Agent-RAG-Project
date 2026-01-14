from abc import ABC, abstractmethod
import os
from typing import Optional

from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.language_models import BaseChatModel
from openai.types import Embedding
from utils.config_handler import agent_conf, rag_conf


class BaseModelFactory():
    @abstractmethod
    def create_model(self) -> Optional[Embedding | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def create_model(self) -> Optional[BaseChatModel]:
        api_key = os.getenv("DASHSCOPE_API_KEY") or rag_conf.get("dashscope_api_key")
        if not api_key:
            raise ValueError(
                "未找到 DASHSCOPE_API_KEY。请设置环境变量 DASHSCOPE_API_KEY "
                "或在 config/rag.yaml 中配置 dashscope_api_key"
            )

        model_name = rag_conf.get("chat_model_name", "qwen-max")

        return ChatTongyi(
            model_name=model_name,
            temperature=0,
            dashscope_api_key=api_key.strip()
        )


class EmbeddingModelFactory(BaseModelFactory):
    def create_model(self) -> Optional[Embedding]:
        api_key = os.getenv("DASHSCOPE_API_KEY") or rag_conf.get("dashscope_api_key")
        if not api_key:
            raise ValueError(
                "未找到 DASHSCOPE_API_KEY。请设置环境变量 DASHSCOPE_API_KEY "
                "或在 config/rag.yaml 中配置 dashscope_api_key"
            )

        model_name = rag_conf.get("embedding_model_name", "text-embedding-v1")

        return DashScopeEmbeddings(
            model=model_name,
            dashscope_api_key=api_key.strip()
        )


chat_model = ChatModelFactory().create_model()
embed_model = EmbeddingModelFactory().create_model()
