import os
import time
from modules.messagepush import message2pushplus
from modules.huamimotion import huamiBrushStep


class BrushStepManager:
    """
    刷步管理器类，用于处理多账户刷步任务
    """

    def __init__(self):
        """
        初始化刷步管理器
        """
        self.env = os.environ
        self.pushplus_token = self.env.get('PUSH_PLUS_TOKEN')
        self.accounts = self._parse_accounts()

    def _parse_accounts(self):
        """
        解析环境变量中的账户信息
        
        环境变量BRUSH_STEP_ACCOUNT格式: "账户名1 账号1 密码1 账户名2 账号2 密码2 ..."
        每3个元素为一组创建账户信息（账户名、账号、密码）
        
        :return: 账户字典
        """
        accounts_env = self.env.get('BRUSH_STEP_ACCOUNT')
        account_list = accounts_env.split() if accounts_env else []
        
        # 按每3个元素一组进行分组，生成账户字典
        accounts = {account_list[i]: {"账号": account_list[i+1], "密码": account_list[i+2]}
                   for i in range(0, len(account_list), 3) if i+2 < len(account_list)}
        
        return accounts

    def run_brush_step_task(self, min_steps=15000, max_steps=16000):
        """
        执行刷步任务
        
        :param min_steps: 最小步数
        :param max_steps: 最大步数
        :return: 执行结果字符串
        """
        result = ""
        
        for account_name, account_info in self.accounts.items():
            result += f"{account_name}:\n"
            
            while True:
                try:
                    step_result = huamiBrushStep(
                        account_info['账号'], 
                        account_info['密码'], 
                        min_steps, 
                        max_steps
                    )
                    result += step_result
                    break  # 成功则跳出循环
                    
                except Exception as e:
                    # 发生异常时继续重试
                    print(f"{account_name} 刷步失败，正在重试... 错误: {e}")
                    time.sleep(5)  # 等待5秒后重试
            
            result += "\n"
            
        return result

    def run_and_push(self, min_steps=15000, max_steps=16000, push_topic="步数提醒群"):
        """
        执行刷步任务并将结果推送到PushPlus
        
        :param min_steps: 最小步数
        :param max_steps: 最大步数
        :param push_topic: 推送主题
        """
        result = self.run_brush_step_task(min_steps, max_steps)
        message2pushplus(self.pushplus_token, result, push_topic)
        return result


def run_brush_step(min_steps=15000, max_steps=16000):
    """
    运行刷步任务的便捷函数
    
    :param min_steps: 最小步数
    :param max_steps: 最大步数
    :return: 执行结果
    """
    manager = BrushStepManager()
    return manager.run_and_push(min_steps, max_steps)


if __name__ == "__main__":
    # 主程序入口
    run_brush_step()