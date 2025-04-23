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
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11lll11llll_opy_ import bstack11lll11lll1_opy_
from bstack_utils.constants import *
import json
class bstack1llllllll1_opy_:
    def __init__(self, bstack111l1l111_opy_, bstack11lll1l1l1l_opy_):
        self.bstack111l1l111_opy_ = bstack111l1l111_opy_
        self.bstack11lll1l1l1l_opy_ = bstack11lll1l1l1l_opy_
        self.bstack11lll11ll1l_opy_ = None
    def __call__(self):
        bstack11lll1l111l_opy_ = {}
        while True:
            self.bstack11lll11ll1l_opy_ = bstack11lll1l111l_opy_.get(
                bstack1ll1l11_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬᙆ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11lll1l11l1_opy_ = self.bstack11lll11ll1l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11lll1l11l1_opy_ > 0:
                sleep(bstack11lll1l11l1_opy_ / 1000)
            params = {
                bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᙇ"): self.bstack111l1l111_opy_,
                bstack1ll1l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᙈ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11lll1l11ll_opy_ = bstack1ll1l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᙉ") + bstack11lll1l1111_opy_ + bstack1ll1l11_opy_ (u"ࠣ࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࠧᙊ")
            if self.bstack11lll1l1l1l_opy_.lower() == bstack1ll1l11_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡵࠥᙋ"):
                bstack11lll1l111l_opy_ = bstack11lll11lll1_opy_.results(bstack11lll1l11ll_opy_, params)
            else:
                bstack11lll1l111l_opy_ = bstack11lll11lll1_opy_.bstack11lll1l1l11_opy_(bstack11lll1l11ll_opy_, params)
            if str(bstack11lll1l111l_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᙌ"), bstack1ll1l11_opy_ (u"ࠫ࠷࠶࠰ࠨᙍ"))) != bstack1ll1l11_opy_ (u"ࠬ࠺࠰࠵ࠩᙎ"):
                break
        return bstack11lll1l111l_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡤࡢࡶࡤࠫᙏ"), bstack11lll1l111l_opy_)