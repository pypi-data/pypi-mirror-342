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
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11lll1l11l1_opy_ import bstack11lll1l1l11_opy_
from bstack_utils.constants import *
import json
class bstack11l111l11_opy_:
    def __init__(self, bstack1l1111l11l_opy_, bstack11lll1l1l1l_opy_):
        self.bstack1l1111l11l_opy_ = bstack1l1111l11l_opy_
        self.bstack11lll1l1l1l_opy_ = bstack11lll1l1l1l_opy_
        self.bstack11lll1l11ll_opy_ = None
    def __call__(self):
        bstack11lll11llll_opy_ = {}
        while True:
            self.bstack11lll1l11ll_opy_ = bstack11lll11llll_opy_.get(
                bstack11111ll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬᙆ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11lll11lll1_opy_ = self.bstack11lll1l11ll_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11lll11lll1_opy_ > 0:
                sleep(bstack11lll11lll1_opy_ / 1000)
            params = {
                bstack11111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᙇ"): self.bstack1l1111l11l_opy_,
                bstack11111ll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᙈ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11lll1l1111_opy_ = bstack11111ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᙉ") + bstack11lll1l1ll1_opy_ + bstack11111ll_opy_ (u"ࠣ࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࠧᙊ")
            if self.bstack11lll1l1l1l_opy_.lower() == bstack11111ll_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡵࠥᙋ"):
                bstack11lll11llll_opy_ = bstack11lll1l1l11_opy_.results(bstack11lll1l1111_opy_, params)
            else:
                bstack11lll11llll_opy_ = bstack11lll1l1l11_opy_.bstack11lll1l111l_opy_(bstack11lll1l1111_opy_, params)
            if str(bstack11lll11llll_opy_.get(bstack11111ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᙌ"), bstack11111ll_opy_ (u"ࠫ࠷࠶࠰ࠨᙍ"))) != bstack11111ll_opy_ (u"ࠬ࠺࠰࠵ࠩᙎ"):
                break
        return bstack11lll11llll_opy_.get(bstack11111ll_opy_ (u"࠭ࡤࡢࡶࡤࠫᙏ"), bstack11lll11llll_opy_)