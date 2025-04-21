import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest


from promptlibz.lib import TemplateFactory,TemplateType

def test_promptLib():
    assert type(TemplateFactory(TemplateType.GITHUB)) == str


