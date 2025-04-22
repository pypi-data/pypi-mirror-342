# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2025-04-12 17:31
# @Author : 毛鹏
import unittest

from mangokit.data_processor import DataProcessor
from mangokit.models import ElementModel
from mangokit.uidrive import AsyncElement, BaseData, DriverObject, SyncElement

test_data = DataProcessor()
element_model = ElementModel(**{
    "id": 18,
    "type": 0,
    "name": "首页输入框",
    "loc": "//input[@id=\"kw\"]",
    "exp": 0,
    "sleep": 1,
    "sub": None,
    "is_iframe": 0,
    "ope_key": "w_input",
    "ope_value": [{"f": "locating"}, {"f": "input_value", "d": True, "p": "请输入内容", "v": "HAS-1"}],
    "key_list": None,
    "sql": None,
    "key": None,
    "value": None
})


class TestUi(unittest.IsolatedAsyncioTestCase):
    async def test_a(self):
        driver_object = DriverObject(True)
        driver_object.set_web(0, r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        base_data = BaseData(test_data)
        base_data.url = 'https://www.baidu.com/'

        base_data.context, base_data.page = await driver_object.web.new_web_page()
        element = AsyncElement(base_data, element_model, 0)
        await element.open_url()
        await element.element_main()


class TestUi2(unittest.TestCase):

    def test_s(self):
        driver_object = DriverObject()
        driver_object.set_web(0, r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        base_data = BaseData(test_data)
        base_data.url = 'https://www.baidu.com/'
        base_data.context, base_data.page = driver_object.web.new_web_page()
        element = SyncElement(base_data, element_model, 0)
        element.open_url()
        element.element_main()
