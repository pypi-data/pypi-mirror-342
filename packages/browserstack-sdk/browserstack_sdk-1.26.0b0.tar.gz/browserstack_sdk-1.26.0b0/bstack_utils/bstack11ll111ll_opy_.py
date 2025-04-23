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
from collections import deque
from bstack_utils.constants import *
class bstack1111l11l1_opy_:
    def __init__(self):
        self._111ll111lll_opy_ = deque()
        self._111ll11l1l1_opy_ = {}
        self._111ll1111l1_opy_ = False
    def bstack111ll1111ll_opy_(self, test_name, bstack111ll11ll1l_opy_):
        bstack111ll11lll1_opy_ = self._111ll11l1l1_opy_.get(test_name, {})
        return bstack111ll11lll1_opy_.get(bstack111ll11ll1l_opy_, 0)
    def bstack111ll111l11_opy_(self, test_name, bstack111ll11ll1l_opy_):
        bstack111ll11ll11_opy_ = self.bstack111ll1111ll_opy_(test_name, bstack111ll11ll1l_opy_)
        self.bstack111ll11l111_opy_(test_name, bstack111ll11ll1l_opy_)
        return bstack111ll11ll11_opy_
    def bstack111ll11l111_opy_(self, test_name, bstack111ll11ll1l_opy_):
        if test_name not in self._111ll11l1l1_opy_:
            self._111ll11l1l1_opy_[test_name] = {}
        bstack111ll11lll1_opy_ = self._111ll11l1l1_opy_[test_name]
        bstack111ll11ll11_opy_ = bstack111ll11lll1_opy_.get(bstack111ll11ll1l_opy_, 0)
        bstack111ll11lll1_opy_[bstack111ll11ll1l_opy_] = bstack111ll11ll11_opy_ + 1
    def bstack11l1llll1_opy_(self, bstack111ll11l11l_opy_, bstack111ll111ll1_opy_):
        bstack111ll111l1l_opy_ = self.bstack111ll111l11_opy_(bstack111ll11l11l_opy_, bstack111ll111ll1_opy_)
        event_name = bstack11ll1llllll_opy_[bstack111ll111ll1_opy_]
        bstack1l1ll1l11ll_opy_ = bstack11111ll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨᳫ").format(bstack111ll11l11l_opy_, event_name, bstack111ll111l1l_opy_)
        self._111ll111lll_opy_.append(bstack1l1ll1l11ll_opy_)
    def bstack11l1ll11l1_opy_(self):
        return len(self._111ll111lll_opy_) == 0
    def bstack1llll11lll_opy_(self):
        bstack111ll11l1ll_opy_ = self._111ll111lll_opy_.popleft()
        return bstack111ll11l1ll_opy_
    def capturing(self):
        return self._111ll1111l1_opy_
    def bstack11l111ll_opy_(self):
        self._111ll1111l1_opy_ = True
    def bstack11l1lllll1_opy_(self):
        self._111ll1111l1_opy_ = False