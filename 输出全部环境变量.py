"""
name:输出全部环境变量
cron:0 0 6 * * *
"""

import os

env = os.environ

for key in env:
    print(key, env[key])