import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest


from pypidoctor.utils import get_llm

def test_llm():
    llm = get_llm()
    result = llm.complete('hello')

    assert type(result) == str
    assert len(result) != 0
    print(result)
