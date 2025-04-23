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
import builtins
import logging
class bstack11l111lll1_opy_:
    def __init__(self, handler):
        self._11lll11l111_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11lll11ll11_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1ll1l11_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᙙ"), bstack1ll1l11_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩᙚ"), bstack1ll1l11_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬᙛ"), bstack1ll1l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᙜ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11lll11l1ll_opy_
        self._11lll11l11l_opy_()
    def _11lll11l1ll_opy_(self, *args, **kwargs):
        self._11lll11l111_opy_(*args, **kwargs)
        message = bstack1ll1l11_opy_ (u"࠭ࠠࠨᙝ").join(map(str, args)) + bstack1ll1l11_opy_ (u"ࠧ࡝ࡰࠪᙞ")
        self._log_message(bstack1ll1l11_opy_ (u"ࠨࡋࡑࡊࡔ࠭ᙟ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1ll1l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᙠ"): level, bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᙡ"): msg})
    def _11lll11l11l_opy_(self):
        for level, bstack11lll11l1l1_opy_ in self._11lll11ll11_opy_.items():
            setattr(logging, level, self._11lll111lll_opy_(level, bstack11lll11l1l1_opy_))
    def _11lll111lll_opy_(self, level, bstack11lll11l1l1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11lll11l1l1_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11lll11l111_opy_
        for level, bstack11lll11l1l1_opy_ in self._11lll11ll11_opy_.items():
            setattr(logging, level, bstack11lll11l1l1_opy_)