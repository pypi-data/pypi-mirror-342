from enum import Enum
from typing import List, Any

from .querys import PythonQueryEngine, get_response_synthesizer,Settings,qa_prompt

class QueryType(Enum):
    Query1 = 'Query1'
    Query2 = 'Query2'
    Query3 = 'Query3'
    # 添加更多选项

class QueryClass:
    def __new__(cls, querytype: QueryType,index,similarity_top_k=3) -> Any:
        assert querytype.value in [i.value for i in QueryType]
        instance = None

        if querytype.value == 'Query1':
            # 配置 Query1 的实例
            # 例如：
            # instance = SomeClass(param1=value1, param2=value2)
            query_engine = index.as_query_engine(similarity_top_k=similarity_top_k)
            instance = query_engine

        elif querytype.value == 'Query2':
            # 配置 Query2 的实例
            # 例如：
            # instance = AnotherClass(param1=value1, param2=value2)
            retriever = index.as_retriever(similarity_top_k=similarity_top_k)
            query_engine = PythonQueryEngine(
                retriever=retriever,
                response_synthesizer=get_response_synthesizer(response_mode="compact"),
                llm=Settings.llm,
                qa_prompt=qa_prompt,
                stream = True,
            )
            instance = query_engine


        elif querytype.value == 'Query3':
            # 配置 Query3 的实例
            # 例如：
            # instance = YetAnotherClass(param1=value1, param2=value2)
            pass

        else:
            raise Exception('Unknown querytype')

        return instance
    


