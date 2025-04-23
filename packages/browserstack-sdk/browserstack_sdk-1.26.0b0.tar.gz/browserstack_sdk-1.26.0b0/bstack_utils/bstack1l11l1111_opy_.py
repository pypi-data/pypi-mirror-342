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
class bstack1lll111ll1_opy_:
    def __init__(self, handler):
        self._111l11l111l_opy_ = None
        self.handler = handler
        self._111l11l11l1_opy_ = self.bstack111l111llll_opy_()
        self.patch()
    def patch(self):
        self._111l11l111l_opy_ = self._111l11l11l1_opy_.execute
        self._111l11l11l1_opy_.execute = self.bstack111l11l1111_opy_()
    def bstack111l11l1111_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11111ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࠣᵴ"), driver_command, None, this, args)
            response = self._111l11l111l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11111ll_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣᵵ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._111l11l11l1_opy_.execute = self._111l11l111l_opy_
    @staticmethod
    def bstack111l111llll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver