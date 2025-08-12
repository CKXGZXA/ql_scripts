#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务名称
name: 刷步数
定时规则
cron: 0 20 * * *
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.brush_step import BrushStepManager

def parse_step_range(step_range):
    """
    解析STEP环境变量，格式为 "最小步数#最大步数"
    
    :param step_range: STEP环境变量值
    :return: (min_steps, max_steps) 元组
    """
    if step_range and '#' in step_range:
        try:
            parts = step_range.split('#')
            min_val = int(parts[0])
            max_val = int(parts[1])
            if min_val > max_val:
                min_val, max_val = max_val, min_val
            return min_val, max_val
        except ValueError:
            # 格式不正确时使用默认值
            pass
    
    # 默认值
    return 15000, 16000

if __name__ == "__main__":
    print("开始执行华米运动刷步数任务...")
    
    # 解析STEP环境变量
    step_env = os.environ.get('STEP')
    min_steps, max_steps = parse_step_range(step_env)
    print(f"设置步数范围: {min_steps} - {max_steps}")
    
    try:
        # 创建刷步管理器实例
        manager = BrushStepManager()
        # 执行刷步任务
        manager.run_and_push(min_steps, max_steps)
        print("华米运动刷步数任务执行完毕")
    except Exception as e:
        print(f"执行过程中发生错误: {e}")
        raise