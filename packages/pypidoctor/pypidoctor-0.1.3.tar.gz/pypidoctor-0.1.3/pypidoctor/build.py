import os
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
import shutil
from .reader import ReaderFactory, Reader
from .utils import get_llm


def build(
    file_path: str,
    persist_dir="./obsidian_kb",
    readertype=Reader.CustObsidianReader,
    debug=True,
):
    get_llm()
    file_extractor = {".md": ReaderFactory(readertype)}  # 使用自定义Reader
    reader = SimpleDirectoryReader(
        input_dir=file_path,
        file_extractor=file_extractor,
        recursive=True,
    )
    documents = reader.load_data()
    if debug:
        documents = documents[:10]
    index = VectorStoreIndex.from_documents(documents)
    # 如果路径存在,则删除
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    index.storage_context.persist(persist_dir=persist_dir)
    return len(documents)

