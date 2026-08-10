#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 公有部件: 棋盘管理器
==============================

来源引擎: go
来源文件: bsd_go_engine.py
部件类型: manager
描述: GoBoard 棋盘管理，支持9/13/19路

理论依据:
    - 部件引擎与组件引擎的二分法
    - 虚拟宇宙数字可公有，不需要重复制造
    - 六系立系引擎论
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


# ============================================================
# 部件元信息
# ============================================================

PART_METADATA = {
    'part_id': 'go_board_manager',
    'part_name': '棋盘管理器',
    'source_engine': 'go',
    'part_type': 'manager',
    'description': 'GoBoard 棋盘管理，支持9/13/19路',
    'can_be_shared': True,
    'created_at': datetime.now().isoformat(),
}


def get_part_metadata() -> Dict[str, Any]:
    """获取部件元信息"""
    return PART_METADATA.copy()


def register_part(registry: Dict[str, Any]) -> bool:
    """注册部件到公有注册表"""
    part_id = PART_METADATA['part_id']
    if part_id not in registry:
        registry[part_id] = {
            'name': PART_METADATA['part_name'],
            'type': PART_METADATA['part_type'],
            'source': PART_METADATA['source_engine'],
            'status': 'registered',
        }
        return True
    return False


def acquire_part(registry: Dict[str, Any]) -> Optional[Any]:
    """获取部件（公有，不消耗）"""
    part_id = PART_METADATA['part_id']
    if part_id in registry:
        registry[part_id]['usage_count'] = registry[part_id].get('usage_count', 0) + 1
        return {
            'part_id': part_id,
            'name': PART_METADATA['part_name'],
            'status': 'active',
        }
    return None
