# -*- coding: utf-8 -*-
# @Project: 芒果测试平台# @Description:
# @Time   : 2023/4/6 13:36
# @Author : 毛鹏

from mangokit.assertion._custom_assertion import CustomAssertion
from mangokit.assertion._public_assertion import WhatIsItAssertion, ContainAssertion, MatchingAssertion, \
    WhatIsEqualToAssertion, PublicAssertion
from mangokit.assertion._sql_assertion import SqlAssertion


class Assertion(WhatIsItAssertion, ContainAssertion, MatchingAssertion, WhatIsEqualToAssertion):
    pass


__all__ = [
    'Assertion',
    'CustomAssertion',
    'SqlAssertion',
    'PublicAssertion',
]
