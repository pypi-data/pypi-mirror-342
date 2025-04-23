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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1111lllll1_opy_, bstack111l111ll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111lllll1_opy_ = bstack1111lllll1_opy_
        self.bstack111l111ll1_opy_ = bstack111l111ll1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111ll11ll1_opy_(bstack1111ll11l1_opy_):
        bstack1111ll111l_opy_ = []
        if bstack1111ll11l1_opy_:
            tokens = str(os.path.basename(bstack1111ll11l1_opy_)).split(bstack1ll1l11_opy_ (u"ࠢࡠࠤဍ"))
            camelcase_name = bstack1ll1l11_opy_ (u"ࠣࠢࠥဎ").join(t.title() for t in tokens)
            suite_name, bstack1111ll11ll_opy_ = os.path.splitext(camelcase_name)
            bstack1111ll111l_opy_.append(suite_name)
        return bstack1111ll111l_opy_
    @staticmethod
    def bstack1111ll1111_opy_(typename):
        if bstack1ll1l11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧဏ") in typename:
            return bstack1ll1l11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦတ")
        return bstack1ll1l11_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧထ")