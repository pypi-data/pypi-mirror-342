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
class RobotHandler():
    def __init__(self, args, logger, bstack1111lll1l1_opy_, bstack111l1111ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111lll1l1_opy_ = bstack1111lll1l1_opy_
        self.bstack111l1111ll_opy_ = bstack111l1111ll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l1l111l_opy_(bstack1111ll11ll_opy_):
        bstack1111ll11l1_opy_ = []
        if bstack1111ll11ll_opy_:
            tokens = str(os.path.basename(bstack1111ll11ll_opy_)).split(bstack11111ll_opy_ (u"ࠨ࡟ࠣဌ"))
            camelcase_name = bstack11111ll_opy_ (u"ࠢࠡࠤဍ").join(t.title() for t in tokens)
            suite_name, bstack1111ll111l_opy_ = os.path.splitext(camelcase_name)
            bstack1111ll11l1_opy_.append(suite_name)
        return bstack1111ll11l1_opy_
    @staticmethod
    def bstack1111ll1l11_opy_(typename):
        if bstack11111ll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦဎ") in typename:
            return bstack11111ll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥဏ")
        return bstack11111ll_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦတ")