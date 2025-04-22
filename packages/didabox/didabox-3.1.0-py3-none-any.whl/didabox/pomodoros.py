# -*- coding: utf-8 -*-

"""
@Project : didabox 
@File    : pomodoros.py
@Date    : 2025/3/12 16:38:12
@Author  : luke
@Desc    : 
"""
from didabox.utils import MidBox


class PomodorosBox(MidBox):
    def general_for_desktop(self):
        """番茄专注-概览"""
        response = self.req.get(
            'https://api.dida365.com/api/v2/pomodoros/statistics/generalForDesktop',
            params={}
        )
        return response
