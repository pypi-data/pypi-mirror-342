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
import builtins
import logging
class bstack11l111ll11_opy_:
    def __init__(self, handler):
        self._11lll11ll1l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11lll11ll11_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11111ll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᙙ"), bstack11111ll_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩᙚ"), bstack11111ll_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬᙛ"), bstack11111ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᙜ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11lll11l11l_opy_
        self._11lll11l1ll_opy_()
    def _11lll11l11l_opy_(self, *args, **kwargs):
        self._11lll11ll1l_opy_(*args, **kwargs)
        message = bstack11111ll_opy_ (u"࠭ࠠࠨᙝ").join(map(str, args)) + bstack11111ll_opy_ (u"ࠧ࡝ࡰࠪᙞ")
        self._log_message(bstack11111ll_opy_ (u"ࠨࡋࡑࡊࡔ࠭ᙟ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11111ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᙠ"): level, bstack11111ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᙡ"): msg})
    def _11lll11l1ll_opy_(self):
        for level, bstack11lll11l1l1_opy_ in self._11lll11ll11_opy_.items():
            setattr(logging, level, self._11lll11l111_opy_(level, bstack11lll11l1l1_opy_))
    def _11lll11l111_opy_(self, level, bstack11lll11l1l1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11lll11l1l1_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11lll11ll1l_opy_
        for level, bstack11lll11l1l1_opy_ in self._11lll11ll11_opy_.items():
            setattr(logging, level, bstack11lll11l1l1_opy_)