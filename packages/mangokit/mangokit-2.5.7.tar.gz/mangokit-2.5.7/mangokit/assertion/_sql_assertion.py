# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2023-11-20 9:47
# @Author : 毛鹏
import asyncio

from mangokit.database import MysqlConnect


class SqlAssertion:
    """sql断言"""
    mysql_connect: MysqlConnect = None

    @staticmethod
    async def sql_is_equal(sql: str, expect: list[dict]):
        """值相等"""

        result = SqlAssertion.mysql_connect.condition_execute(sql)
        assert all(dict2 in result for dict2 in expect), "列表不相等"


if __name__ == '__main__':
    _sql = "SELECT id,`name`,`status` FROM `project`;"
    _expect = [{'id': 2, 'name': '1CDXP', 'status': 1}, {'id': 5, 'name': 'AIGC', 'status': 1},
               {'id': 10, 'name': 'DESK', 'status': 1}, {'id': 11, 'name': 'AIGC-SaaS', 'status': 1}]
