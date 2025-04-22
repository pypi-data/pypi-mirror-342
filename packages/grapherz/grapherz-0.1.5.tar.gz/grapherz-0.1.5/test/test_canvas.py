import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import re
import pytest

from grapherz.canvas import Canvas,Color

@pytest.fixture
def canvas():
    canva = Canvas(file_path='/Users/zhaoxuefeng/GitHub/obsidian/工作/工程系统级设计/项目级别/数字人生/模拟资质认证/模拟资质认证.canvas')
    yield canva
    canva.to_file(file_path='test/模拟资质认证output.canvas')



def test_canvas(canvas):

    canvas.select_edges_by_text(key='备案')
    canvas.select_by_color(key=Color.yellow,type='node')[4].color = Color.green.value
