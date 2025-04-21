# -*- coding: utf-8 -*-
# @Project: 芒果测试平台# @Description:
# @Time   : 2023-09-09 23:17
# @Author : 毛鹏
from uiautomator2 import UiObject

from mangokit.decorator import sync_method_callback
from mangokit.models import MethodModel
from mangokit.tools import Meta
from mangokit.uidrive._base_data import BaseData


class AndroidAssertion(metaclass=Meta):
    """元素断言"""

    def __init__(self, base_data: BaseData):
        self.base_data = base_data

    @sync_method_callback('ass_android', '元素断言', [
        MethodModel(f='actual')])
    def a_assert_ele_exists(self, actual: UiObject):
        """元素是否存在"""
        assert actual.count

    @sync_method_callback('ass_android', '元素断言', [
        MethodModel(f='actual'),
        MethodModel(f='expect', p='请输入预期内容', d=True)])
    def a_assert_ele_count(self, actual: UiObject, expect):
        """元素个数"""
        assert actual.count == expect
