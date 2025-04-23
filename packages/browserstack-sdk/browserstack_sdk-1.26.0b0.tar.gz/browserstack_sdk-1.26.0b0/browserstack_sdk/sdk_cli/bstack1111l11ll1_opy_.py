# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack111ll1l_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack11111ll_opy_ (bstack1l1111_opy_):
    global bstack111111_opy_
    bstack11l1l1l_opy_ = ord (bstack1l1111_opy_ [-1])
    bstack1ll11l1_opy_ = bstack1l1111_opy_ [:-1]
    bstack1l1l1l1_opy_ = bstack11l1l1l_opy_ % len (bstack1ll11l1_opy_)
    bstack11111_opy_ = bstack1ll11l1_opy_ [:bstack1l1l1l1_opy_] + bstack1ll11l1_opy_ [bstack1l1l1l1_opy_:]
    if bstack1111l11_opy_:
        bstack11ll111_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1l_opy_ - (bstack11l1lll_opy_ + bstack11l1l1l_opy_) % bstack11l1l1_opy_) for bstack11l1lll_opy_, char in enumerate (bstack11111_opy_)])
    else:
        bstack11ll111_opy_ = str () .join ([chr (ord (char) - bstack111ll1l_opy_ - (bstack11l1lll_opy_ + bstack11l1l1l_opy_) % bstack11l1l1_opy_) for bstack11l1lll_opy_, char in enumerate (bstack11111_opy_)])
    return eval (bstack11ll111_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack111111l1ll_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack11111l1l11_opy_:
    bstack1l1111ll111_opy_ = bstack11111ll_opy_ (u"ࠥࡦࡪࡴࡣࡩ࡯ࡤࡶࡰࠨᔘ")
    context: bstack111111l1ll_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack111111l1ll_opy_):
        self.context = context
        self.data = dict({bstack11111l1l11_opy_.bstack1l1111ll111_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack11111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᔙ"), bstack11111ll_opy_ (u"ࠬ࠶ࠧᔚ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1111l11111_opy_(self, target: object):
        return bstack11111l1l11_opy_.create_context(target) == self.context
    def bstack1ll11l11l1l_opy_(self, context: bstack111111l1ll_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1l1ll11ll_opy_(self, key: str, value: timedelta):
        self.data[bstack11111l1l11_opy_.bstack1l1111ll111_opy_][key] += value
    def bstack1lll1111l11_opy_(self) -> dict:
        return self.data[bstack11111l1l11_opy_.bstack1l1111ll111_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack111111l1ll_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )