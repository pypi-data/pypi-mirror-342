from enum import Enum
from typing import List, Any

from .reader import CustObsidianReader

class Reader(Enum):
    CustObsidianReader = 'CustObsidianReader'
    _Reader = '_Reader'
    # 添加更多选项

class ReaderFactory:
    def __new__(cls, reader_type: Reader) -> Any:
        assert reader_type.value in [i.value for i in Reader]
        reader = None

        if reader_type.value == 'CustObsidianReader':
            reader = CustObsidianReader()

        elif reader_type.value == '_Reader':
            # 配置 _Reader 的实例
            # 例如：
            # reader = AnotherClass(param1=value1, param2=value2)
            pass


        else:
            raise Exception('Unknown reader_type')

        return reader