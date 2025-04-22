# -*- coding: utf-8 -*-
# @Project: 芒果测试平台# @Description:
# @Time   : 2023-09-09 23:17
# @Author : 毛鹏
import time

import uiautomator2

from mangokit.decorator import sync_method_callback
from mangokit.exceptions import MangoKitError, ERROR_MSG_0046
from mangokit.models import MethodModel
from mangokit.uidrive._base_data import BaseData
from mangokit.tools import Meta


class AndroidApplication(metaclass=Meta):
    """应用操作"""

    def __init__(self, base_data: BaseData):
        self.base_data = base_data

    @sync_method_callback('android', '应用操作', [
        MethodModel(f='package_name', p='请输入应用名称', d=True)])
    def a_start_app(self, package_name: str):
        """启动应用"""
        if not package_name:
            raise MangoKitError(*ERROR_MSG_0046)
        self.base_data.android.app_start(package_name)
        time.sleep(4)

    @sync_method_callback('android', '应用操作', [
        MethodModel(f='package_name', p='请输入应用名称', d=True)])
    def a_close_app(self, package_name: str):
        """关闭应用"""
        if not package_name:
            raise MangoKitError(*ERROR_MSG_0046)
        try:
            self.base_data.android.app_stop(package_name)
        except uiautomator2.exceptions.BaseError:
            raise MangoKitError(*ERROR_MSG_0046)

    @sync_method_callback('android', '应用操作', [
        MethodModel(f='package_name', p='请输入应用名称', d=True)])
    def a_clear_app(self, package_name: str):
        """清除app数据"""
        if not package_name:
            raise MangoKitError(*ERROR_MSG_0046)

        current_app = self.base_data.android.app_current()
        if current_app.get("package") == package_name:
            try:
                self.base_data.android.app_clear(package_name)
            except uiautomator2.exceptions.BaseError:
                raise MangoKitError(*ERROR_MSG_0046)

    @sync_method_callback('android', '应用操作', )
    def a_app_stop_all(self):
        """停止所有app"""
        self.base_data.android.app_stop_all()

    def a_app_stop_appoint(self, package_name_list: list):
        """停止除指定app外所有app"""
        if package_name_list:
            try:
                self.base_data.android.app_stop_all(excludes=package_name_list)
            except uiautomator2.exceptions.BaseError:
                raise MangoKitError(*ERROR_MSG_0046)
        else:
            raise MangoKitError(*ERROR_MSG_0046)
