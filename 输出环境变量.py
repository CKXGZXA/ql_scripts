"""
name:输出环境变量
cron:0 0 3 * * *
"""

import os

env = os.environ
# 将JD_COOKIE的值输出到日志
print(env.get('JD_COOKIE'))