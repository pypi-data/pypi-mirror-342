from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import Document
from llama_index.core.agent import ReActAgent
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.core import Settings
from llama_index.core import get_response_synthesizer
from llama_index.llms.openai import OpenAI
from llama_index.core import PromptTemplate
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.base.response.schema import Response
from llama_index.core.base.response.schema import StreamingResponse
from llama_index.core import SimpleDirectoryReader
from llama_index.core.extractors import BaseExtractor
from llama_index.core.readers.base import BaseReader
from typing import List, Dict,Optional
from enum import Enum
import os
import random
import shutil
import re
# 定义提示模板字符串
template_str = """
Take a deep breath and work on this problem step-by-step

您是一个Python工程师, 我会提供给您一些已验证可用的代码(防止出现包版本过旧,或者环境不支持的情况),
在代码编写中,如果被验证代码块中存在相关内容,您应该尽可能的使用被验证的代码, 而非经验.
基于用户的需求和提供的已验证代码, 结合自己的经验,编写代码.
您编写的代码应该封装成函数或者类


已验证代码:
---
```python
{safe_code}
```
---

用户的诉求:
{prompt}

输出函数:
"""

# 创建PromptTemplate实例
qa_prompt = PromptTemplate(template=template_str)


class PythonQueryEngine(CustomQueryEngine):
    """RAG String Query Engine."""

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer
    llm: OpenAI
    qa_prompt: PromptTemplate
    stream:bool

    def custom_query(self, query_str: str):
        # custom_query(query_str: str) -> STR_OR_RESPONSE_TYPE
        # acustom_query(query_str: str) -> STR_OR_RESPONSE_TYPE

        queries = query_str.split('&')
        nodes = []
        for query_str in queries:
            nodes += self.retriever.retrieve(query_str)
        # nodes = self.retriever.retrieve(query_str)
        print(query_str,'query_str')
        context_str = "\n\n".join([n.node.get_metadata_str() for n in nodes])
        if self.stream:
            response = self.llm.stream_complete(
                qa_prompt.format(safe_code=context_str, prompt=query_str)
            )

            def response_gen():
                i = [0]
                for r in response:
                    i.append(len(str(r)))
                    yield str(r)[i[-2]:]

            return StreamingResponse(response_gen=response_gen(),source_nodes=nodes)
        else:
            response = self.llm.complete(qa_prompt.format(safe_code=context_str, prompt=query_str))
    
            response_obj = self.response_synthesizer.synthesize(response.text, nodes)
            return Response(response=response.text,source_nodes=nodes) # TODO 增加metadata


