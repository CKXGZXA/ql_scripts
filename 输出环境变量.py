"""
name:输出环境变量
cron:0 0 3 * * *
"""

import os

env = os.environ
# 有多个名为JD_COOKIE的值, 全部输出
for key, value in env.items():
    if key == 'JD_COOKIE':
        print(key, value)