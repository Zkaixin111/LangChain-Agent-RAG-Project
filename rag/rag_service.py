from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from model.factory import chat_model
# 总结服务类：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompts


def print_prompt(prompt):
    print("=" * 20)
    print(prompt)
    print("=" * 20)
    return prompt


class RagSummarizeService(object):
    def __init__(self):
        #         向量数据库
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        # 提示词
        prompt_str = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(prompt_str)
        #         模型
        self.model = chat_model
        self.chain = self._init_chain()

    #     初始化链
    def _init_chain(self):
        chain = self.prompt_template | print_prompt | self.model | StrOutputParser()
        return chain

    def retriever_docs(self, query: str) -> list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str):
        context_docs = self.retriever_docs(query)

        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"【参考资料数量{counter}：参考资料:{doc.page_content}|参考元数据:{doc.metadata}\n"
        return self.chain.invoke(
            {
                "input": query,
                "context": context,
            }
        )


if __name__ == '__main__':
    rag_summarize_service = RagSummarizeService()
    print(rag_summarize_service.rag_summarize("小户型适合什么机器人"))
