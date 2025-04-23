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
class bstack1l1l1ll11_opy_:
    def __init__(self, handler):
        self._111l11l1111_opy_ = None
        self.handler = handler
        self._111l111llll_opy_ = self.bstack111l11l11l1_opy_()
        self.patch()
    def patch(self):
        self._111l11l1111_opy_ = self._111l111llll_opy_.execute
        self._111l111llll_opy_.execute = self.bstack111l11l111l_opy_()
    def bstack111l11l111l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1ll1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࠨᵲ"), driver_command, None, this, args)
            response = self._111l11l1111_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1ll1l11_opy_ (u"ࠢࡢࡨࡷࡩࡷࠨᵳ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._111l111llll_opy_.execute = self._111l11l1111_opy_
    @staticmethod
    def bstack111l11l11l1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver