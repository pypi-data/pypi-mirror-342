# -*- coding: utf-8 -*-

"""
@Project : didabox 
@File    : login.py
@Date    : 2023/12/1 11:29:05
@Author  : zhchen
@Desc    : 
"""
from didabox.utils import MidBox


class LoginBox(MidBox):

    def sign_on(self, username, password):
        """账号密码登录接口"""
        json_data = {
            "phone": username,
            "password": password,
        }
        random_id = self.random_string()
        self.req.headers["x-device"] = ('{"platform":"web","os":"Windows 10","device":"Chrome 135.0.0.0","name":"",'
                                        '"version":6260,"id":"' + random_id + '","channel":"website",'
                                                                              '"campaign":"","websocket":""}')
        response = self.req.post("https://api.dida365.com/api/v2/user/signon?wc=true&remember=true", json=json_data)
        self.req.cookies = dict(response.cookies)
        del self.req.headers["x-device"]
        return response
