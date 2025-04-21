# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2025-04-12 15:53
# @Author : 毛鹏
import os
import traceback

from playwright._impl._errors import TargetClosedError, Error, TimeoutError

from mangokit.decorator import async_retry
from mangokit.enums import StatusEnum, ElementOperationEnum, DriveTypeEnum
from mangokit.exceptions import MangoKitError, ERROR_MSG_0015, ERROR_MSG_0010, ERROR_MSG_0048, ERROR_MSG_0051, \
    ERROR_MSG_0054, ERROR_MSG_0027, ERROR_MSG_0053, ERROR_MSG_0038, ERROR_MSG_0036
from mangokit.models import ElementResultModel, ElementModel
from mangokit.uidrive.android import AndroidDriver
from mangokit.uidrive.web.async_web import AsyncWebDevice, AsyncWebAssertion


class AsyncElement(AsyncWebDevice, AndroidDriver):

    def __init__(self, base_data, element_model: ElementModel, drive_type: int, element_data: dict | None = None):
        super().__init__(base_data)
        self.element_data = element_data
        self.element_model = element_model
        self.drive_type = drive_type
        self.ope_name = element_model.name if element_model.name else element_model.ope_key
        self.element_test_result = ElementResultModel(
            id=self.element_model.id,
            name=self.element_model.name,
            loc=self.element_model.loc,
            exp=self.element_model.exp,
            sub=self.element_model.sub,
            sleep=self.element_model.sleep,

            type=self.element_model.type,
            ope_key=self.element_model.ope_key,
            sql=self.element_model.sql,
            key_list=self.element_model.key_list,
            key=self.element_model.key,
            value=self.element_model.value,

            status=StatusEnum.FAIL.value,
        )

    async def open_device(self):
        if self.drive_type == DriveTypeEnum.WEB.value:
            await self.open_url()
        elif self.drive_type == DriveTypeEnum.ANDROID.value:
            self.open_app()
        elif self.drive_type == DriveTypeEnum.DESKTOP.value:
            pass
        else:
            raise Exception('不存在的设备类型')

    @async_retry(10, 0.2)
    async def element_main(self) -> ElementResultModel:
        try:
            for field_name, field_value in self.element_model:
                if field_value is None:
                    continue
                if field_name == "ope_value":
                    for method_model in field_value:
                        for method_field, method_val in method_model:
                            if isinstance(method_val, str):
                                setattr(method_model, method_field, self.base_data.test_data.replace(method_val))
                elif isinstance(field_value, str):
                    setattr(self.element_model, field_name, self.base_data.test_data.replace(field_value))
        except MangoKitError as error:
            raise MangoKitError(error.code, error.msg)

        try:
            if self.element_model.type == ElementOperationEnum.OPE.value:
                await self.__ope()
            elif self.element_model.type == ElementOperationEnum.ASS.value:
                await self.__ass()
            elif self.element_model.type == ElementOperationEnum.SQL.value:
                await self.__sql()
            elif self.element_model.type == ElementOperationEnum.CUSTOM.value:
                await self.__custom()
            else:
                raise MangoKitError(*ERROR_MSG_0015)
            if self.element_model.sleep:
                await self.w_wait_for_timeout(self.element_model.sleep)
            self.element_test_result.status = StatusEnum.SUCCESS.value
            return self.element_test_result
        except TargetClosedError as error:
            self.base_data.setup(self.base_data.test_data)
            self.base_data.log.warning(f'浏览器对象关闭异常：{error}')
            self.element_test_result.status = StatusEnum.FAIL.value
            self.element_test_result.error_message = '浏览器对象被关闭，请检查是人为关闭还是异常关闭，异常关闭请发送error日志联系管理员！'
            raise MangoKitError(*ERROR_MSG_0010)
        except MangoKitError as error:
            await self.__error(error)
            raise error
        except Error as error:
            self.base_data.log.warning(f'浏览器对象关闭异常：{error}')
            self.element_test_result.status = StatusEnum.FAIL.value
            self.element_test_result.error_message = f'未捕获的异常，可以联系管理来添加异常提示。或者你可以根据异常提示进行修改测试内容。异常内容：{error}'
            raise error
        except Exception as error:
            self.element_test_result.status = StatusEnum.FAIL.value
            self.element_test_result.error_message = f'未知异常，可以联系管理来添加异常提示。或者你可以根据异常提示进行修改测试内容。异常内容：{error}'
            raise error

    async def __ope(self):
        try:
            getattr(self, self.element_model.ope_key).__doc__
        except AttributeError:
            raise MangoKitError(*ERROR_MSG_0048)
        except TypeError:
            raise MangoKitError(*ERROR_MSG_0051)
        if self.element_model.ope_value is None:
            raise MangoKitError(*ERROR_MSG_0054)
        await self.__ope_value()
        if self.drive_type == DriveTypeEnum.WEB.value:
            await self.web_action_element(
                self.element_model.name,
                self.element_model.ope_key,
                {i.f: i.v for i in self.element_model.ope_value}
            )
        elif self.drive_type == DriveTypeEnum.ANDROID.value:
            self.a_action_element(
                self.element_model.name,
                self.element_model.ope_key,
                {i.f: i.v for i in self.element_model.ope_value}
            )
        else:
            pass
        for i in self.element_model.ope_value:
            if i.d:
                self.element_test_result.ope_value[i.p] = i.v

    async def __ass(self):
        if self.element_model.ope_value is None:
            raise MangoKitError(*ERROR_MSG_0053)
        await self.__ope_value(True)
        if self.drive_type == DriveTypeEnum.WEB.value:
            await self.web_assertion_element(self.element_model.name, self.element_model.ope_key,
                                             {i.f: i.v for i in self.element_model.ope_value})
        elif self.drive_type == DriveTypeEnum.ANDROID.value:
            self.a_assertion_element()
        else:
            pass
        for i in self.element_model.ope_value:
            if i.d:
                self.element_test_result.ope_value[i.p] = i.v

    async def __sql(self):
        if not self.element_data:
            sql = self.element_model.sql
            key_list = self.element_model.key_list
        else:
            sql = self.element_data.get('sql')
            key_list = self.element_data.get('key_list')
        if self.base_data.mysql_connect:
            result_list: list[dict] = self.base_data.mysql_connect.condition_execute(sql)
            if isinstance(result_list, list):
                for result in result_list:
                    try:
                        for value, key in zip(result, key_list):
                            self.base_data.test_data.set_cache(key, result.get(value))
                    except SyntaxError:
                        raise MangoKitError(*ERROR_MSG_0038)

                if not result_list:
                    raise MangoKitError(*ERROR_MSG_0036, value=(self.element_model.sql,))

    async def __custom(self):
        if not self.element_data:
            key = self.element_model.key
            value = self.element_model.value
        else:
            key = self.element_data.get('key')
            value = self.element_data.get('value')
        self.base_data.test_data.set_cache(key, value)

    async def __element_preset_processing(self):
        count, loc, text = 0, None, None
        if self.drive_type == DriveTypeEnum.WEB.value:
            count, loc = await self.web_find_ele(
                self.element_model.name,
                self.element_model.type,
                self.element_model.exp,
                self.element_model.loc,
                self.element_model.sub,
                self.element_model.is_iframe
            )
            try:
                text = await self.w_get_text(loc)
            except Exception:
                text = None
        elif self.drive_type == DriveTypeEnum.ANDROID.value:
            count, loc = self.a_find_ele()
            try:
                text = await self.a_get_text(loc)
            except Exception:
                text = None
        else:
            try:
                count, loc = 0, 0
                text = None
            except Exception:
                text = None
        if text:
            self.element_test_result.ope_value.update({'元素文本': text})
        return count, loc, text

    async def __ope_value(self, is_ass: bool = False):
        try:
            ope_key = 'actual' if is_ass else 'locating'
            for i in self.element_model.ope_value:
                if i.f == ope_key and self.element_model.loc:
                    count, loc, text = await self.__element_preset_processing()
                    if is_ass:
                        from mangokit.assertion import PublicAssertion
                        is_method = callable(getattr(AsyncWebAssertion, ope_key, None))
                        is_method_public = callable(getattr(PublicAssertion, ope_key, None))
                        if is_method:
                            i.v = loc
                        elif is_method_public:
                            i.v = text
                    else:
                        i.v = loc
                else:
                    if self.element_data:
                        for ele_name, case_data in self.element_data.items():
                            if ele_name == i.f:
                                value = case_data
                                i.v = self.base_data.test_data.replace(value)

        except AttributeError:
            traceback.print_exc()
            raise MangoKitError(*ERROR_MSG_0027)

    async def __error(self, error: MangoKitError):
        self.element_test_result.status = StatusEnum.FAIL.value
        self.element_test_result.error_message = error.msg
        self.base_data.log.debug(
            f"""
            元素操作失败----->
            元 素 对 象：{self.element_model.model_dump() if self.element_model else self.element_model}
            元素测试结果：{
            self.element_test_result.model_dump() if self.element_test_result else self.element_test_result}
            报 错 信 息：{error.msg}
            """
        )
        if self.element_test_result:
            file_name = f'失败截图-{self.element_model.name}{self.base_data.test_data.get_time_for_min()}.jpg'
            file_path = os.path.join(self.base_data.screenshot_path, file_name)
            self.element_test_result.picture_path = file_path
            self.element_test_result.picture_name = file_name
            await self.__error_screenshot(file_path)

    async def __error_screenshot(self, file_path):
        if self.drive_type == DriveTypeEnum.WEB.value:
            try:
                await self.w_screenshot(file_path)
            except (TargetClosedError, TimeoutError):
                self.base_data.setup(self.base_data.test_data)
                raise MangoKitError(*ERROR_MSG_0010)
            except AttributeError:
                self.base_data.setup(self.base_data.test_data)
                raise MangoKitError(*ERROR_MSG_0010)
        elif self.drive_type == DriveTypeEnum.ANDROID.value:
            self.a_screenshot(file_path)
        else:
            pass
