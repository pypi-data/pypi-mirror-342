# -*- coding: utf-8 -*-

"""
@Project : didabox 
@File    : main.py
@Date    : 2023/12/1 10:16:44
@Author  : zhchen
@Desc    : 
"""
import copy

from requests import Response

from didabox.check import CheckBox
from didabox.info import InfoBox
from didabox.pomodoros import PomodorosBox
from didabox.request import Request
from didabox.task import TaskBox
from didabox.login import LoginBox


class DidaBox:
    def __init__(self, cookies: dict, headers=None):
        self.req = Request(cookies=cookies, tz='Asia/Shanghai', headers=headers)
        self.check_box = CheckBox(self)
        self.task_box = TaskBox(self)
        self.login_box = LoginBox(self)
        self.info_box = InfoBox(self)
        self.pomodoros_Box = PomodorosBox(self)

    # == 账号维度 ==
    def check_cookie(self) -> Response:
        """检测cookie是否过期"""
        return self.check_box.check_cookie()

    def sign_on(self, username, password) -> Response:
        """
        账号密码登录, 登录完成后自动更新cookie
        :param username: 账号
        :param password: 密码
        :return:
        """
        return self.login_box.sign_on(username, password)

    # -- 账号维度 --

    # == 清单任务维度 ==
    def base_info(self):
        """清单的基本信息"""
        return self.info_box.base_info()

    def column_info(self):
        """清单的分组/看板信息"""
        return self.info_box.column_info()

    def add_simple_task(self, project_id: str, title: str, content: str, trigger_time: str) -> Response:
        """
        添加简单的任务
        :param project_id: 清单id
        :param title: 任务标题
        :param content: 任务内容
        :param trigger_time: 触发时间, 准时触发. 格式: %Y-%m-%d %H:%M:%S
        :return:
        """
        return self.task_box.add_reminders_task(project_id, title, content, trigger_time)

    def get_completed_tasks(self, to_date, from_date: str = '', limit: int = 50) -> Response:
        """
        获取已完成的任务
        :param to_date: 格式 2024-03-28 00:57:26
        :param from_date:
        :param limit:
        """
        return self.task_box.all_completed(from_date=from_date, to_date=to_date, limit=limit)

    def update_content(self, title: str, content: str):
        """
        根据title查询到未完成的任务，将任务内容修改为content
        """
        # 获取所有清单信息
        all_dida_info_res = self.base_info()
        all_dida_info = all_dida_info_res.json()
        result = []
        for row in all_dida_info['syncTaskBean']['update']:
            if row['title'] == title:
                task_info = copy.deepcopy(row)
                task_info['content'] = content
                update_res = self.task_box.update_task(task_info)
                result.append(update_res.json())
        return result

    def search(self, keywords: str) -> Response:
        """根据关键词查询相关任务"""
        return self.task_box.search_all(keywords)
    # -- 清单任务维度 --

    # -- 番茄专注维度 --
    def pomodoros_overview(self) -> Response:
        """获取番茄概览(今天番茄、今天专注时长、总番茄、总专注时长……)"""
        return self.pomodoros_Box.general_for_desktop()

    # -- 番茄专注维度 --
