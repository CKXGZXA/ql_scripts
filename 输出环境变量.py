"""
name:输出环境变量
cron:0 0 0 * * *
"""

import os

env = os.environ
for key in env:
    print(key, env[key])