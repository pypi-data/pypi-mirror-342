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
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
logger = logging.getLogger(__name__)
class bstack11lll1l1l11_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack111l11l1lll_opy_ = urljoin(builder, bstack11111ll_opy_ (u"ࠬ࡯ࡳࡴࡷࡨࡷࠬᵣ"))
        if params:
            bstack111l11l1lll_opy_ += bstack11111ll_opy_ (u"ࠨ࠿ࡼࡿࠥᵤ").format(urlencode({bstack11111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᵥ"): params.get(bstack11111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᵦ"))}))
        return bstack11lll1l1l11_opy_.bstack111l11l1l1l_opy_(bstack111l11l1lll_opy_)
    @staticmethod
    def bstack11lll1l111l_opy_(builder,params=None):
        bstack111l11l1lll_opy_ = urljoin(builder, bstack11111ll_opy_ (u"ࠩ࡬ࡷࡸࡻࡥࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠪᵧ"))
        if params:
            bstack111l11l1lll_opy_ += bstack11111ll_opy_ (u"ࠥࡃࢀࢃࠢᵨ").format(urlencode({bstack11111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᵩ"): params.get(bstack11111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᵪ"))}))
        return bstack11lll1l1l11_opy_.bstack111l11l1l1l_opy_(bstack111l11l1lll_opy_)
    @staticmethod
    def bstack111l11l1l1l_opy_(bstack111l11l11ll_opy_):
        bstack111l11l1ll1_opy_ = os.environ.get(bstack11111ll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᵫ"), os.environ.get(bstack11111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᵬ"), bstack11111ll_opy_ (u"ࠨࠩᵭ")))
        headers = {bstack11111ll_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᵮ"): bstack11111ll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ᵯ").format(bstack111l11l1ll1_opy_)}
        response = requests.get(bstack111l11l11ll_opy_, headers=headers)
        bstack111l11l1l11_opy_ = {}
        try:
            bstack111l11l1l11_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11111ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥᵰ").format(e))
            pass
        if bstack111l11l1l11_opy_ is not None:
            bstack111l11l1l11_opy_[bstack11111ll_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ᵱ")] = response.headers.get(bstack11111ll_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧᵲ"), str(int(datetime.now().timestamp() * 1000)))
            bstack111l11l1l11_opy_[bstack11111ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᵳ")] = response.status_code
        return bstack111l11l1l11_opy_