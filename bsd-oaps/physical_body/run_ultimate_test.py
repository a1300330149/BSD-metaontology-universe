#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""启动器：运行V5终极测试"""

import sys
import os

# 切换到正确的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

# 运行测试
exec(open('BSD_Go_V5_Ultimate.py').read())