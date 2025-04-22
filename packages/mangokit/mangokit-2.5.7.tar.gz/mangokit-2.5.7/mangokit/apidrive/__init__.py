# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-07-26 上午10:02
# @Author : 毛鹏
from mangokit.apidrive._async_request import AsyncRequests
from mangokit.apidrive._sync_request import Requests

async_requests = AsyncRequests
requests = Requests

__all__ = ['async_requests', 'requests']
