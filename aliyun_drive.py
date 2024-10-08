# -*- coding: utf-8 -*-
"""
name:阿里云盘每日签到
cron: 10 9 * * *
new Env('阿里云盘');
"""

import requests, time, re, json, sys, traceback, os
from io import StringIO
from messagepush import message2pushplus

class ALiYun:
    def __init__(self, cookie):
        self.sio = StringIO()
        # self.Cookies = cookie
        # self.cookie = ''
        self.cookie = cookie

    def _get_access_token(self, token: str) -> "tuple[bool, str, str, str]":
        url = 'https://auth.aliyundrive.com/v2/account/token'
        data = {'grant_type': 'refresh_token', 'refresh_token': token}
        res = requests.post(url, json=data, timeout=5).json()
        if 'code' in res and res['code'] in ['RefreshTokenExpired', 'InvalidParameter.RefreshToken', 'InvalidParameterMissing.RefreshToken']:
            return False, '', '', res['message']
        nick_name, user_name = res['nick_name'], res['user_name']
        name = nick_name if nick_name else user_name
        access_token = res['access_token']
        return True, name, access_token, '成功获取access_token'
    
    def _check_in(self, access_token: str) -> "tuple[bool, int, str]":
        url = 'https://member.aliyundrive.com/v1/activity/sign_in_list'
        payload = {'isReward': False}
        params = {'_rx-s': 'mobile'}
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.post(url, json=payload, params=params, headers=headers, timeout=5)
        data = response.json()
        if 'success' not in data:
            return False, -1, data['message']
        success = data['success']
        signin_count = data['result']['signInCount']
        return success, signin_count, '签到成功'

    def _get_reward(self, access_token: str, sign_day: int) -> "tuple[bool, str]":
        url = 'https://member.aliyundrive.com/v1/activity/sign_in_reward'
        payload = {'signInDay': sign_day}
        params = {'_rx-s': 'mobile'}
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.post(url, json=payload, params=params, headers=headers, timeout=5)
        data = response.json()
        if 'result' not in data:
            return False, data['message']
        success = data['success']
        notice = data['result']['notice']
        return success, notice

    def SignIn(self):
        print("【阿里云盘 日志】")
        self.sio.write("【阿里云盘】\n")
        # for cookie in self.Cookies:
        # cookie = cookie.get("user")
        # print(f"{cookie.get('name')} 开始签到...")
        print(f"开始签到...")
        # self.sio.write(f"{cookie.get('name')}: ")
        # self.cookie = cookie.get('cookie')
        try:
            flag, user_name, access_token, message = self._get_access_token(self.cookie)
            if not flag:
                print('token 已失效, ' + message)
                self.sio.write('token 已失效\n')
            else:
                flag, signin_count, message = self._check_in(access_token)
                if not flag:
                    print('签到失败, ' + message)
                    self.sio.write('签到失败\n')
                else:
                    print(f'本月已签到{signin_count}次')
                    self.sio.write(f'本月已签到{signin_count}次\n')
                    flag, message = self._get_reward(access_token, signin_count)
                    if not flag:
                        print('领取失败, ' + message)
                    else:
                        print('领取成功: ' + message)
                        self.sio.write('领取成功: ' + message + '\n')
        except:
            print(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
            if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    # 从环境变量中获取ALI_REFRESH_TOKEN
    env = os.environ
    Cookies = env.get('ALI_REFRESH_TOKEN')
    pushplus_token = env.get('PUSH_PLUS_TOKEN')
    if Cookies != None:
        aly = ALiYun(Cookies)
        sio = aly.SignIn()
        print(f'\n{sio.getvalue()}')
        message2pushplus(pushplus_token, sio.getvalue())
    else:
        print('未配置阿里云盘环境变量')