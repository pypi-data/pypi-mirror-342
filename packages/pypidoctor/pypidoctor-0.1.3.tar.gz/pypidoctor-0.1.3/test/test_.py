import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest


from pypidoctor import build
from pypidoctor import Queryr

def test_build():
    build(
        file_path="/Users/zhaoxuefeng/GitHub/obsidian/工作",
        persist_dir="/Users/zhaoxuefeng/GitHub/test1/obk",
    )

def test_query():
    qr = Queryr(persist_dir="/Users/zhaoxuefeng/GitHub/test1/obk")
    qr.load_query()
    result = qr.ask('hello')
    assert len(result) !=0