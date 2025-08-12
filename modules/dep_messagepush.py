import requests, json

def message2pushplus(pushplus_token, content, pushplus_topic=None):
    print("Pushplus 推送开始")
    data = {
        "token": pushplus_token,
        "title": "刷步通知",
        "content": content.replace("\n", "<br>"),
        "template": "json",
    }
    if pushplus_topic:
        data["topic"] = pushplus_topic
    # 重试直到推送成功
    while True:
        try:
            requests.post(url="http://www.pushplus.plus/send", data=json.dumps(data))
            print("Pushplus 推送成功")
            break  # 成功则跳出循环
        except Exception as e:
            # 发生异常时继续重试
            print(f"Pushplus 推送失败，正在重试... 错误: {e}")
            time.sleep(5)  # 等待5秒后重试

    return