from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from utils.config_handler import chroma_conf
from model.factory import embed_model
from utils.path_tool import get_abs_path
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger


class VectorStoreService():
    # 初始化向量数据库的配置
    def __init__(self):
        # 向量存储实例
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embed_model,
            persist_directory=chroma_conf["persist_directory"]  # 指定存放的文件夹
        )
        # 文本分割器
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            length_function=len,
            separators=chroma_conf["separators"]
        )

    # 获得检索器对象
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

        # 加载文档

    def load_document(self):

        # 验证转换过来的md5字符串是否在文件中存在
        def check_md5_hex(md5_for_check: str):
            md5_path = get_abs_path(chroma_conf["md5_hex_store"])
            # 如果文件还不存在就先创建文件
            if not os.path.exists(md5_path):
                with open(md5_path, "w") as f:
                    pass
                return False

            with open(md5_path, "r") as f:
                for line in f:
                    if md5_for_check == line.strip():
                        return True
            return False

        # 将md5字符串存入文件中
        def save_md5_hex(md5_for_store: str):
            md5_path = get_abs_path(chroma_conf["md5_hex_store"])
            # 使用 with 语句确保文件写入并关闭
            with open(md5_path, "a") as f:
                f.write(md5_for_store + "\n")

        # 得到待传入的知识文档文件
        def get_file_documents(read_path: str):
            if read_path.endswith(".txt"):
                return txt_loader(read_path)
            elif read_path.endswith(".pdf"):
                return pdf_loader(read_path)
            else:
                return []

        # 得到能够被允许读取的文件
        allowed_files_path = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"])
        )

        for path in allowed_files_path:
            # 获取文件的MD5
            md5_hex = get_file_md5_hex(path)
            if not md5_hex:
                logger.warning(f"[加载知识库]无法计算文件 {path} 的MD5，跳过")
                continue

            # 如果对应的MD5已经存在就跳过
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在知识库内，跳过")
                continue

            try:
                # 得到所有已经经过加载后的文档
                documents: list[Document] = get_file_documents(path)

                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效文本内容，跳过")
                    continue

                # 得到所有知识库后进行分片操作
                split_document: list[Document] = self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效文本内容，跳过")
                    continue

                # 【核心修改】手动分批存入向量库，解决 DashScope batch size <= 10 的限制
                batch_size = 10
                total_batches = (len(split_document) + batch_size - 1) // batch_size

                for i in range(0, len(split_document), batch_size):
                    batch_docs = split_document[i:i + batch_size]
                    self.vector_store.add_documents(batch_docs)
                    current_batch = i // batch_size + 1
                    logger.debug(f"[加载知识库]{path} 进度: {current_batch}/{total_batches}")

                # 记录这个已经处理好的文件的md5，避免下次重复加载
                save_md5_hex(md5_hex)

                logger.info(f"[加载知识库]{path} 内容加载成功，共分 {len(split_document)} 片")
            except Exception as e:
                logger.error(f"[加载知识库]{path}加载失败：{str(e)}")


# 测试
if __name__ == '__main__':
    vs = VectorStoreService()

    vs.load_document()
    retriever = vs.get_retriever()
    res = retriever.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("=" * 20)
