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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack11llll11_opy_ = {}
        bstack11l11l11ll_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪຣ"), bstack1ll1l11_opy_ (u"ࠪࠫ຤"))
        if not bstack11l11l11ll_opy_:
            return bstack11llll11_opy_
        try:
            bstack11l11l11l1_opy_ = json.loads(bstack11l11l11ll_opy_)
            if bstack1ll1l11_opy_ (u"ࠦࡴࡹࠢລ") in bstack11l11l11l1_opy_:
                bstack11llll11_opy_[bstack1ll1l11_opy_ (u"ࠧࡵࡳࠣ຦")] = bstack11l11l11l1_opy_[bstack1ll1l11_opy_ (u"ࠨ࡯ࡴࠤວ")]
            if bstack1ll1l11_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦຨ") in bstack11l11l11l1_opy_ or bstack1ll1l11_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦຩ") in bstack11l11l11l1_opy_:
                bstack11llll11_opy_[bstack1ll1l11_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧສ")] = bstack11l11l11l1_opy_.get(bstack1ll1l11_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢຫ"), bstack11l11l11l1_opy_.get(bstack1ll1l11_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢຬ")))
            if bstack1ll1l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨອ") in bstack11l11l11l1_opy_ or bstack1ll1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦຮ") in bstack11l11l11l1_opy_:
                bstack11llll11_opy_[bstack1ll1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧຯ")] = bstack11l11l11l1_opy_.get(bstack1ll1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤະ"), bstack11l11l11l1_opy_.get(bstack1ll1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢັ")))
            if bstack1ll1l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧາ") in bstack11l11l11l1_opy_ or bstack1ll1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧຳ") in bstack11l11l11l1_opy_:
                bstack11llll11_opy_[bstack1ll1l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨິ")] = bstack11l11l11l1_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣີ"), bstack11l11l11l1_opy_.get(bstack1ll1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣຶ")))
            if bstack1ll1l11_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣື") in bstack11l11l11l1_opy_ or bstack1ll1l11_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨຸ") in bstack11l11l11l1_opy_:
                bstack11llll11_opy_[bstack1ll1l11_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ູࠢ")] = bstack11l11l11l1_opy_.get(bstack1ll1l11_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨ຺ࠦ"), bstack11l11l11l1_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤົ")))
            if bstack1ll1l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣຼ") in bstack11l11l11l1_opy_ or bstack1ll1l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨຽ") in bstack11l11l11l1_opy_:
                bstack11llll11_opy_[bstack1ll1l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ຾")] = bstack11l11l11l1_opy_.get(bstack1ll1l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ຿"), bstack11l11l11l1_opy_.get(bstack1ll1l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤເ")))
            if bstack1ll1l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢແ") in bstack11l11l11l1_opy_ or bstack1ll1l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢໂ") in bstack11l11l11l1_opy_:
                bstack11llll11_opy_[bstack1ll1l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣໃ")] = bstack11l11l11l1_opy_.get(bstack1ll1l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥໄ"), bstack11l11l11l1_opy_.get(bstack1ll1l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥ໅")))
            if bstack1ll1l11_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦໆ") in bstack11l11l11l1_opy_:
                bstack11llll11_opy_[bstack1ll1l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧ໇")] = bstack11l11l11l1_opy_[bstack1ll1l11_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨ່")]
        except Exception as error:
            logger.error(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩࡧࡴࡢ࠼້ࠣࠦ") +  str(error))
        return bstack11llll11_opy_