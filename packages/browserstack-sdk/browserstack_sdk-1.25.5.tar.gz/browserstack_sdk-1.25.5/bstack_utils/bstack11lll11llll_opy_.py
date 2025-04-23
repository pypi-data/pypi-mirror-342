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
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
logger = logging.getLogger(__name__)
class bstack11lll11lll1_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack111l11l1l1l_opy_ = urljoin(builder, bstack1ll1l11_opy_ (u"ࠪ࡭ࡸࡹࡵࡦࡵࠪᵡ"))
        if params:
            bstack111l11l1l1l_opy_ += bstack1ll1l11_opy_ (u"ࠦࡄࢁࡽࠣᵢ").format(urlencode({bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᵣ"): params.get(bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᵤ"))}))
        return bstack11lll11lll1_opy_.bstack111l11l1lll_opy_(bstack111l11l1l1l_opy_)
    @staticmethod
    def bstack11lll1l1l11_opy_(builder,params=None):
        bstack111l11l1l1l_opy_ = urljoin(builder, bstack1ll1l11_opy_ (u"ࠧࡪࡵࡶࡹࡪࡹ࠭ࡴࡷࡰࡱࡦࡸࡹࠨᵥ"))
        if params:
            bstack111l11l1l1l_opy_ += bstack1ll1l11_opy_ (u"ࠣࡁࡾࢁࠧᵦ").format(urlencode({bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᵧ"): params.get(bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᵨ"))}))
        return bstack11lll11lll1_opy_.bstack111l11l1lll_opy_(bstack111l11l1l1l_opy_)
    @staticmethod
    def bstack111l11l1lll_opy_(bstack111l11l1l11_opy_):
        bstack111l11l11ll_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᵩ"), os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᵪ"), bstack1ll1l11_opy_ (u"࠭ࠧᵫ")))
        headers = {bstack1ll1l11_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧᵬ"): bstack1ll1l11_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫᵭ").format(bstack111l11l11ll_opy_)}
        response = requests.get(bstack111l11l1l11_opy_, headers=headers)
        bstack111l11l1ll1_opy_ = {}
        try:
            bstack111l11l1ll1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣᵮ").format(e))
            pass
        if bstack111l11l1ll1_opy_ is not None:
            bstack111l11l1ll1_opy_[bstack1ll1l11_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫᵯ")] = response.headers.get(bstack1ll1l11_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬᵰ"), str(int(datetime.now().timestamp() * 1000)))
            bstack111l11l1ll1_opy_[bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᵱ")] = response.status_code
        return bstack111l11l1ll1_opy_