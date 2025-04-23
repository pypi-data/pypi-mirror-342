# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1lll1l_opy_ = 7
def bstack1ll1l11_opy_ (bstack111llll_opy_):
    global bstack11lll1_opy_
    bstack11l1l1_opy_ = ord (bstack111llll_opy_ [-1])
    bstack11l1_opy_ = bstack111llll_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack11l1l1_opy_ % len (bstack11l1_opy_)
    bstack1111111_opy_ = bstack11l1_opy_ [:bstack1l1lll1_opy_] + bstack11l1_opy_ [bstack1l1lll1_opy_:]
    if bstack1lll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l11l_opy_ + bstack11l1l1_opy_) % bstack1lll1l_opy_) for bstack1l11l_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l11l_opy_ + bstack11l1l1_opy_) % bstack1lll1l_opy_) for bstack1l11l_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1llll11_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack1ll111111_opy_:
    def __init__(self):
        self._111ll11l1l1_opy_ = deque()
        self._111ll11l1ll_opy_ = {}
        self._111ll111ll1_opy_ = False
    def bstack111ll11l11l_opy_(self, test_name, bstack111ll11ll11_opy_):
        bstack111ll11lll1_opy_ = self._111ll11l1ll_opy_.get(test_name, {})
        return bstack111ll11lll1_opy_.get(bstack111ll11ll11_opy_, 0)
    def bstack111ll11l111_opy_(self, test_name, bstack111ll11ll11_opy_):
        bstack111ll11ll1l_opy_ = self.bstack111ll11l11l_opy_(test_name, bstack111ll11ll11_opy_)
        self.bstack111ll111lll_opy_(test_name, bstack111ll11ll11_opy_)
        return bstack111ll11ll1l_opy_
    def bstack111ll111lll_opy_(self, test_name, bstack111ll11ll11_opy_):
        if test_name not in self._111ll11l1ll_opy_:
            self._111ll11l1ll_opy_[test_name] = {}
        bstack111ll11lll1_opy_ = self._111ll11l1ll_opy_[test_name]
        bstack111ll11ll1l_opy_ = bstack111ll11lll1_opy_.get(bstack111ll11ll11_opy_, 0)
        bstack111ll11lll1_opy_[bstack111ll11ll11_opy_] = bstack111ll11ll1l_opy_ + 1
    def bstack111111111_opy_(self, bstack111ll111l11_opy_, bstack111ll1111l1_opy_):
        bstack111ll111l1l_opy_ = self.bstack111ll11l111_opy_(bstack111ll111l11_opy_, bstack111ll1111l1_opy_)
        event_name = bstack11ll1l111ll_opy_[bstack111ll1111l1_opy_]
        bstack1111l11l1l_opy_ = bstack1ll1l11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦᳩ").format(bstack111ll111l11_opy_, event_name, bstack111ll111l1l_opy_)
        self._111ll11l1l1_opy_.append(bstack1111l11l1l_opy_)
    def bstack11l1l1lll1_opy_(self):
        return len(self._111ll11l1l1_opy_) == 0
    def bstack11l1lll11_opy_(self):
        bstack111ll1111ll_opy_ = self._111ll11l1l1_opy_.popleft()
        return bstack111ll1111ll_opy_
    def capturing(self):
        return self._111ll111ll1_opy_
    def bstack1lll1l1l1_opy_(self):
        self._111ll111ll1_opy_ = True
    def bstack1llllll11l_opy_(self):
        self._111ll111ll1_opy_ = False