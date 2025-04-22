# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2025-04-04 21:42
# @Author : 毛鹏
import re
import traceback

from playwright._impl._errors import TimeoutError, Error, TargetClosedError
from playwright.sync_api._generated import Locator

from mangokit.assertion import SqlAssertion
from mangokit.enums import ElementExpEnum, ElementOperationEnum, StatusEnum
from mangokit.exceptions import *
from mangokit.mangos import Mango
from mangokit.uidrive._base_data import BaseData
from mangokit.uidrive.web.sync_web._assertion import SyncWebAssertion
from mangokit.uidrive.web.sync_web._browser import SyncWebBrowser
from mangokit.uidrive.web.sync_web._customization import SyncWebCustomization
from mangokit.uidrive.web.sync_web._element import SyncWebElement
from mangokit.uidrive.web.sync_web._input_device import SyncWebDeviceInput
from mangokit.uidrive.web.sync_web._page import SyncWebPage

re = re

__all__ = [
    'SyncWebAssertion',
    'SyncWebBrowser',
    'SyncWebCustomization',
    'SyncWebDeviceInput',
    'SyncWebElement',
    'SyncWebPage',
    'SyncWebDevice',
]


class SyncWebDevice(SyncWebBrowser,
                    SyncWebPage,
                    SyncWebElement,
                    SyncWebDeviceInput,
                    SyncWebCustomization):

    def __init__(self, base_data: BaseData):
        super().__init__(base_data)

    def open_url(self):
        if not self.base_data.is_open_url:
            self.w_goto(self.base_data.url)
            self.base_data.is_open_url = True
        elif self.base_data.switch_step_open_url and self.base_data.page.url != self.base_data.url:
            self.w_wait_for_timeout(1)
            self.w_goto(self.base_data.url)

    def web_action_element(self, name, ope_key, ope_value, ):
        try:
            Mango.s_e(self, ope_key, ope_value)
        except TimeoutError as error:
            self.base_data.log.error(f'WEB自动化失败，类型：{type(error)}，失败详情：{error}')
            raise MangoKitError(*ERROR_MSG_0011, value=(name,))
        except TargetClosedError:
            self.base_data.setup(self.base_data.test_data)
            raise MangoKitError(*ERROR_MSG_0010)
        except Error as error:
            self.base_data.log.error(f'WEB自动化失败，类型：{type(error)}，失败详情：{error}')
            raise MangoKitError(*ERROR_MSG_0032, value=(name,))
        except ValueError as error:
            self.base_data.log.error(f'WEB自动化失败，类型：{type(error)}，失败详情：{error}')
            raise MangoKitError(*ERROR_MSG_0012)

    def web_assertion_element(self, name, ope_key, ope_value):
        from mangokit.assertion import PublicAssertion
        is_method = callable(getattr(SyncWebAssertion, ope_key, None))
        is_method_public = callable(getattr(PublicAssertion, ope_key, None))
        try:
            if is_method or is_method_public:
                if ope_value.get('actual', None) is None:
                    traceback.print_exc()
                    raise MangoKitError(*ERROR_MSG_0031, value=(name,))
                self.base_data.log.debug(f'开始断言，方法：{ope_key}，断言值：{ope_value}')
                getattr(PublicAssertion, ope_key)(**ope_value)
            else:
                if self.base_data.mysql_connect is not None:
                    SqlAssertion.mysql_obj = self.base_data.mysql_connect
                    self.base_data.log.debug(
                        f'开始断言，方法：sql相等端游，实际值：{ope_value}')
                    SqlAssertion.sql_is_equal(**ope_value)
                else:
                    raise MangoKitError(*ERROR_MSG_0019)
        except AssertionError as error:
            self.base_data.log.error(f'WEB自动化失败，类型：{type(error)}，失败详情：{error}')
            raise MangoKitError(*ERROR_MSG_0017)
        except AttributeError as error:
            self.base_data.log.error(f'WEB自动化失败，类型：{type(error)}，失败详情：{error}')
            raise MangoKitError(*ERROR_MSG_0048)
        except ValueError as error:
            self.base_data.log.error(f'WEB自动化失败，类型：{type(error)}，失败详情：{error}')
            raise MangoKitError(*ERROR_MSG_0005)
        except TargetClosedError:
            self.base_data.setup(self.base_data.test_data)
            raise MangoKitError(*ERROR_MSG_0010)
        except Error as error:
            self.base_data.log.error(f'WEB自动化失败，类型：{type(error)}，失败详情：{error}')
            raise MangoKitError(*ERROR_MSG_0052, value=(name,), )

    def web_find_ele(self,
                     name, _type, exp, loc, sub, is_iframe) -> tuple[int, Locator] | tuple[int, list[Locator]]:
        if is_iframe != StatusEnum.SUCCESS.value:
            locator: Locator = self.__find_ele(self.base_data.page, exp, loc)
            try:
                count = locator.count()
                if count < 1 or locator is None and _type == ElementOperationEnum.OPE.value:
                    if _type == ElementOperationEnum.OPE.value:
                        raise MangoKitError(*ERROR_MSG_0029, value=(name, loc))
                return count, locator.nth(sub - 1) if sub else locator
            except Error:
                raise MangoKitError(*ERROR_MSG_0041, )
        else:
            ele_list: list[Locator] = []
            for i in self.base_data.page.frames:
                locator: Locator = self.__find_ele(i, exp, loc)
                try:
                    count = locator.count()
                except Error as error:
                    self.base_data.log.error(f'WEB自动化失败，类型：{type(error)}，失败详情：{error}')
                    raise MangoKitError(*ERROR_MSG_0041, )
                if count > 0:
                    for nth in range(0, count):
                        ele_list.append(locator.nth(nth))
                else:
                    raise MangoKitError(*ERROR_MSG_0023)

            ele_quantity = len(ele_list)
            if not ele_list:
                raise MangoKitError(*ERROR_MSG_0023)
            # 这里需要进行调整
            if not ele_list and _type == ElementOperationEnum.OPE.value:
                raise MangoKitError(*ERROR_MSG_0029, value=(name, loc))
            try:
                return ele_quantity, ele_list[sub - 1] if sub else ele_list[0]
            except IndexError:
                raise MangoKitError(*ERROR_MSG_0025, value=(ele_quantity,))

    def __find_ele(self, page, exp, loc) -> Locator:
        match exp:
            case ElementExpEnum.LOCATOR.value:
                try:
                    return eval(f"page.{loc}")
                except SyntaxError:
                    try:
                        return eval(f"await page.{loc}")
                    except SyntaxError as error:
                        self.base_data.log.error(f'WEB自动化失败，类型：{type(error)}，失败详情：{error}')
                        raise MangoKitError(*ERROR_MSG_0022)
                    except NameError as error:
                        self.base_data.log.error(f'WEB自动化失败，类型：{type(error)}，失败详情：{error}')
                        raise MangoKitError(*ERROR_MSG_0060)
            case ElementExpEnum.XPATH.value:
                return page.locator(f'xpath={loc}')
            case ElementExpEnum.CSS.value:
                return page.locator(loc)
            case ElementExpEnum.TEXT.value:
                return page.get_by_text(loc, exact=True)
            case ElementExpEnum.PLACEHOLDER.value:
                return page.get_by_placeholder(loc)
            case _:
                raise MangoKitError(*ERROR_MSG_0020)
