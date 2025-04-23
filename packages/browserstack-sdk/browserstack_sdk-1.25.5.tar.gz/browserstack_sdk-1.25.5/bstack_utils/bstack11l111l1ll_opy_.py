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
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11lllll1ll1_opy_, bstack11llll1lll1_opy_, bstack11lllll1ll_opy_, bstack111l11lll1_opy_, bstack11l11lllll1_opy_, bstack11l1l11lll1_opy_, bstack11l1llllll1_opy_, bstack1lllllll11_opy_, bstack11ll111l1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111l11llll1_opy_ import bstack111l1l11111_opy_
import bstack_utils.bstack11l1l11l1l_opy_ as bstack11l11l1ll1_opy_
from bstack_utils.bstack11l1111l1l_opy_ import bstack1lll111111_opy_
import bstack_utils.accessibility as bstack1ll1lll1l_opy_
from bstack_utils.bstack1l11l111_opy_ import bstack1l11l111_opy_
from bstack_utils.bstack111llll111_opy_ import bstack111lll1l1l_opy_
bstack1111ll1l111_opy_ = bstack1ll1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫᷧ")
logger = logging.getLogger(__name__)
class bstack1ll1l11l1l_opy_:
    bstack111l11llll1_opy_ = None
    bs_config = None
    bstack111l11l11_opy_ = None
    @classmethod
    @bstack111l11lll1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11lll1111ll_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def launch(cls, bs_config, bstack111l11l11_opy_):
        cls.bs_config = bs_config
        cls.bstack111l11l11_opy_ = bstack111l11l11_opy_
        try:
            cls.bstack1111ll1llll_opy_()
            bstack11llllll1l1_opy_ = bstack11lllll1ll1_opy_(bs_config)
            bstack11llllll11l_opy_ = bstack11llll1lll1_opy_(bs_config)
            data = bstack11l11l1ll1_opy_.bstack1111lll111l_opy_(bs_config, bstack111l11l11_opy_)
            config = {
                bstack1ll1l11_opy_ (u"ࠬࡧࡵࡵࡪࠪᷨ"): (bstack11llllll1l1_opy_, bstack11llllll11l_opy_),
                bstack1ll1l11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᷩ"): cls.default_headers()
            }
            response = bstack11lllll1ll_opy_(bstack1ll1l11_opy_ (u"ࠧࡑࡑࡖࡘࠬᷪ"), cls.request_url(bstack1ll1l11_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠲࠰ࡤࡸ࡭ࡱࡪࡳࠨᷫ")), data, config)
            if response.status_code != 200:
                bstack1l11ll1l1l1_opy_ = response.json()
                if bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᷬ")] == False:
                    cls.bstack1111ll1l1l1_opy_(bstack1l11ll1l1l1_opy_)
                    return
                cls.bstack1111ll1l1ll_opy_(bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᷭ")])
                cls.bstack1111lll11ll_opy_(bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᷮ")])
                return None
            bstack1111ll11l11_opy_ = cls.bstack1111ll111ll_opy_(response)
            return bstack1111ll11l11_opy_
        except Exception as error:
            logger.error(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡼࡿࠥᷯ").format(str(error)))
            return None
    @classmethod
    @bstack111l11lll1_opy_(class_method=True)
    def stop(cls, bstack1111ll11ll1_opy_=None):
        if not bstack1lll111111_opy_.on() and not bstack1ll1lll1l_opy_.on():
            return
        if os.environ.get(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᷰ")) == bstack1ll1l11_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᷱ") or os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᷲ")) == bstack1ll1l11_opy_ (u"ࠤࡱࡹࡱࡲࠢᷳ"):
            logger.error(bstack1ll1l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭ᷴ"))
            return {
                bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ᷵"): bstack1ll1l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ᷶"),
                bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫᷷ࠧ"): bstack1ll1l11_opy_ (u"ࠧࡕࡱ࡮ࡩࡳ࠵ࡢࡶ࡫࡯ࡨࡎࡊࠠࡪࡵࠣࡹࡳࡪࡥࡧ࡫ࡱࡩࡩ࠲ࠠࡣࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡ࡯࡬࡫࡭ࡺࠠࡩࡣࡹࡩࠥ࡬ࡡࡪ࡮ࡨࡨ᷸ࠬ")
            }
        try:
            cls.bstack111l11llll1_opy_.shutdown()
            data = {
                bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ᷹࠭"): bstack1lllllll11_opy_()
            }
            if not bstack1111ll11ll1_opy_ is None:
                data[bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡲ࡫ࡴࡢࡦࡤࡸࡦ᷺࠭")] = [{
                    bstack1ll1l11_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ᷻"): bstack1ll1l11_opy_ (u"ࠫࡺࡹࡥࡳࡡ࡮࡭ࡱࡲࡥࡥࠩ᷼"),
                    bstack1ll1l11_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰ᷽ࠬ"): bstack1111ll11ll1_opy_
                }]
            config = {
                bstack1ll1l11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ᷾"): cls.default_headers()
            }
            bstack11l1l1l1111_opy_ = bstack1ll1l11_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨ᷿").format(os.environ[bstack1ll1l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨḀ")])
            bstack1111lll1l1l_opy_ = cls.request_url(bstack11l1l1l1111_opy_)
            response = bstack11lllll1ll_opy_(bstack1ll1l11_opy_ (u"ࠩࡓ࡙࡙࠭ḁ"), bstack1111lll1l1l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1ll1l11_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤḂ"))
        except Exception as error:
            logger.error(bstack1ll1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࡀࠠࠣḃ") + str(error))
            return {
                bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬḄ"): bstack1ll1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬḅ"),
                bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨḆ"): str(error)
            }
    @classmethod
    @bstack111l11lll1_opy_(class_method=True)
    def bstack1111ll111ll_opy_(cls, response):
        bstack1l11ll1l1l1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1111ll11l11_opy_ = {}
        if bstack1l11ll1l1l1_opy_.get(bstack1ll1l11_opy_ (u"ࠨ࡬ࡺࡸࠬḇ")) is None:
            os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ḉ")] = bstack1ll1l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨḉ")
        else:
            os.environ[bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨḊ")] = bstack1l11ll1l1l1_opy_.get(bstack1ll1l11_opy_ (u"ࠬࡰࡷࡵࠩḋ"), bstack1ll1l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫḌ"))
        os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬḍ")] = bstack1l11ll1l1l1_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪḎ"), bstack1ll1l11_opy_ (u"ࠩࡱࡹࡱࡲࠧḏ"))
        logger.info(bstack1ll1l11_opy_ (u"ࠪࡘࡪࡹࡴࡩࡷࡥࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨḐ") + os.getenv(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩḑ")));
        if bstack1lll111111_opy_.bstack1111ll1111l_opy_(cls.bs_config, cls.bstack111l11l11_opy_.get(bstack1ll1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭Ḓ"), bstack1ll1l11_opy_ (u"࠭ࠧḓ"))) is True:
            bstack111l11l11ll_opy_, build_hashed_id, bstack1111ll11l1l_opy_ = cls.bstack1111ll11lll_opy_(bstack1l11ll1l1l1_opy_)
            if bstack111l11l11ll_opy_ != None and build_hashed_id != None:
                bstack1111ll11l11_opy_[bstack1ll1l11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧḔ")] = {
                    bstack1ll1l11_opy_ (u"ࠨ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠫḕ"): bstack111l11l11ll_opy_,
                    bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫḖ"): build_hashed_id,
                    bstack1ll1l11_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧḗ"): bstack1111ll11l1l_opy_
                }
            else:
                bstack1111ll11l11_opy_[bstack1ll1l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫḘ")] = {}
        else:
            bstack1111ll11l11_opy_[bstack1ll1l11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬḙ")] = {}
        if bstack1ll1lll1l_opy_.bstack1l11l1lll_opy_(cls.bs_config) is True:
            bstack1111l1llll1_opy_, build_hashed_id = cls.bstack1111llll111_opy_(bstack1l11ll1l1l1_opy_)
            if bstack1111l1llll1_opy_ != None and build_hashed_id != None:
                bstack1111ll11l11_opy_[bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ḛ")] = {
                    bstack1ll1l11_opy_ (u"ࠧࡢࡷࡷ࡬ࡤࡺ࡯࡬ࡧࡱࠫḛ"): bstack1111l1llll1_opy_,
                    bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪḜ"): build_hashed_id,
                }
            else:
                bstack1111ll11l11_opy_[bstack1ll1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩḝ")] = {}
        else:
            bstack1111ll11l11_opy_[bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪḞ")] = {}
        if bstack1111ll11l11_opy_[bstack1ll1l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫḟ")].get(bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧḠ")) != None or bstack1111ll11l11_opy_[bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ḡ")].get(bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩḢ")) != None:
            cls.bstack1111ll1l11l_opy_(bstack1l11ll1l1l1_opy_.get(bstack1ll1l11_opy_ (u"ࠨ࡬ࡺࡸࠬḣ")), bstack1l11ll1l1l1_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫḤ")))
        return bstack1111ll11l11_opy_
    @classmethod
    def bstack1111ll11lll_opy_(cls, bstack1l11ll1l1l1_opy_):
        if bstack1l11ll1l1l1_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪḥ")) == None:
            cls.bstack1111ll1l1ll_opy_()
            return [None, None, None]
        if bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫḦ")][bstack1ll1l11_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ḧ")] != True:
            cls.bstack1111ll1l1ll_opy_(bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭Ḩ")])
            return [None, None, None]
        logger.debug(bstack1ll1l11_opy_ (u"ࠧࡕࡧࡶࡸࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫḩ"))
        os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧḪ")] = bstack1ll1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧḫ")
        if bstack1l11ll1l1l1_opy_.get(bstack1ll1l11_opy_ (u"ࠪ࡮ࡼࡺࠧḬ")):
            os.environ[bstack1ll1l11_opy_ (u"ࠫࡈࡘࡅࡅࡇࡑࡘࡎࡇࡌࡔࡡࡉࡓࡗࡥࡃࡓࡃࡖࡌࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨḭ")] = json.dumps({
                bstack1ll1l11_opy_ (u"ࠬࡻࡳࡦࡴࡱࡥࡲ࡫ࠧḮ"): bstack11lllll1ll1_opy_(cls.bs_config),
                bstack1ll1l11_opy_ (u"࠭ࡰࡢࡵࡶࡻࡴࡸࡤࠨḯ"): bstack11llll1lll1_opy_(cls.bs_config)
            })
        if bstack1l11ll1l1l1_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩḰ")):
            os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧḱ")] = bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫḲ")]
        if bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪḳ")].get(bstack1ll1l11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬḴ"), {}).get(bstack1ll1l11_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩḵ")):
            os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧḶ")] = str(bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧḷ")][bstack1ll1l11_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩḸ")][bstack1ll1l11_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ḹ")])
        else:
            os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫḺ")] = bstack1ll1l11_opy_ (u"ࠦࡳࡻ࡬࡭ࠤḻ")
        return [bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠬࡰࡷࡵࠩḼ")], bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨḽ")], os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨḾ")]]
    @classmethod
    def bstack1111llll111_opy_(cls, bstack1l11ll1l1l1_opy_):
        if bstack1l11ll1l1l1_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨḿ")) == None:
            cls.bstack1111lll11ll_opy_()
            return [None, None]
        if bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṀ")][bstack1ll1l11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫṁ")] != True:
            cls.bstack1111lll11ll_opy_(bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫṂ")])
            return [None, None]
        if bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬṃ")].get(bstack1ll1l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧṄ")):
            logger.debug(bstack1ll1l11_opy_ (u"ࠧࡕࡧࡶࡸࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫṅ"))
            parsed = json.loads(os.getenv(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩṆ"), bstack1ll1l11_opy_ (u"ࠩࡾࢁࠬṇ")))
            capabilities = bstack11l11l1ll1_opy_.bstack1111lll1l11_opy_(bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪṈ")][bstack1ll1l11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬṉ")][bstack1ll1l11_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫṊ")], bstack1ll1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫṋ"), bstack1ll1l11_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭Ṍ"))
            bstack1111l1llll1_opy_ = capabilities[bstack1ll1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭ṍ")]
            os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧṎ")] = bstack1111l1llll1_opy_
            if bstack1ll1l11_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧṏ") in bstack1l11ll1l1l1_opy_ and bstack1l11ll1l1l1_opy_.get(bstack1ll1l11_opy_ (u"ࠦࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠥṐ")) is None:
                parsed[bstack1ll1l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ṑ")] = capabilities[bstack1ll1l11_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧṒ")]
            os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨṓ")] = json.dumps(parsed)
            scripts = bstack11l11l1ll1_opy_.bstack1111lll1l11_opy_(bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨṔ")][bstack1ll1l11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪṕ")][bstack1ll1l11_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫṖ")], bstack1ll1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩṗ"), bstack1ll1l11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࠭Ṙ"))
            bstack1l11l111_opy_.bstack1l1l11ll_opy_(scripts)
            commands = bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ṙ")][bstack1ll1l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨṚ")][bstack1ll1l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠩṛ")].get(bstack1ll1l11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫṜ"))
            bstack1l11l111_opy_.bstack11llll111l1_opy_(commands)
            bstack1l11l111_opy_.store()
        return [bstack1111l1llll1_opy_, bstack1l11ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬṝ")]]
    @classmethod
    def bstack1111ll1l1ll_opy_(cls, response=None):
        os.environ[bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩṞ")] = bstack1ll1l11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪṟ")
        os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪṠ")] = bstack1ll1l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬṡ")
        os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧṢ")] = bstack1ll1l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨṣ")
        os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩṤ")] = bstack1ll1l11_opy_ (u"ࠦࡳࡻ࡬࡭ࠤṥ")
        os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭Ṧ")] = bstack1ll1l11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦṧ")
        cls.bstack1111ll1l1l1_opy_(response, bstack1ll1l11_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢṨ"))
        return [None, None, None]
    @classmethod
    def bstack1111lll11ll_opy_(cls, response=None):
        os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ṩ")] = bstack1ll1l11_opy_ (u"ࠩࡱࡹࡱࡲࠧṪ")
        os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨṫ")] = bstack1ll1l11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩṬ")
        os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩṭ")] = bstack1ll1l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫṮ")
        cls.bstack1111ll1l1l1_opy_(response, bstack1ll1l11_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢṯ"))
        return [None, None, None]
    @classmethod
    def bstack1111ll1l11l_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬṰ")] = jwt
        os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧṱ")] = build_hashed_id
    @classmethod
    def bstack1111ll1l1l1_opy_(cls, response=None, product=bstack1ll1l11_opy_ (u"ࠥࠦṲ")):
        if response == None:
            logger.error(product + bstack1ll1l11_opy_ (u"ࠦࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠨṳ"))
        for error in response[bstack1ll1l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬṴ")]:
            bstack11ll111llll_opy_ = error[bstack1ll1l11_opy_ (u"࠭࡫ࡦࡻࠪṵ")]
            error_message = error[bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨṶ")]
            if error_message:
                if bstack11ll111llll_opy_ == bstack1ll1l11_opy_ (u"ࠣࡇࡕࡖࡔࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡅࡇࡑࡍࡊࡊࠢṷ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1ll1l11_opy_ (u"ࠤࡇࡥࡹࡧࠠࡶࡲ࡯ࡳࡦࡪࠠࡵࡱࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࠥṸ") + product + bstack1ll1l11_opy_ (u"ࠥࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡩࡻࡥࠡࡶࡲࠤࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣṹ"))
    @classmethod
    def bstack1111ll1llll_opy_(cls):
        if cls.bstack111l11llll1_opy_ is not None:
            return
        cls.bstack111l11llll1_opy_ = bstack111l1l11111_opy_(cls.bstack1111ll11111_opy_)
        cls.bstack111l11llll1_opy_.start()
    @classmethod
    def bstack111l1llll1_opy_(cls):
        if cls.bstack111l11llll1_opy_ is None:
            return
        cls.bstack111l11llll1_opy_.shutdown()
    @classmethod
    @bstack111l11lll1_opy_(class_method=True)
    def bstack1111ll11111_opy_(cls, bstack111ll1l1ll_opy_, event_url=bstack1ll1l11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪṺ")):
        config = {
            bstack1ll1l11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ṻ"): cls.default_headers()
        }
        logger.debug(bstack1ll1l11_opy_ (u"ࠨࡰࡰࡵࡷࡣࡩࡧࡴࡢ࠼ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡷࡳࠥࡺࡥࡴࡶ࡫ࡹࡧࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࡵࠣࡿࢂࠨṼ").format(bstack1ll1l11_opy_ (u"ࠧ࠭ࠢࠪṽ").join([event[bstack1ll1l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬṾ")] for event in bstack111ll1l1ll_opy_])))
        response = bstack11lllll1ll_opy_(bstack1ll1l11_opy_ (u"ࠩࡓࡓࡘ࡚ࠧṿ"), cls.request_url(event_url), bstack111ll1l1ll_opy_, config)
        bstack11llll1ll11_opy_ = response.json()
    @classmethod
    def bstack11l1lll111_opy_(cls, bstack111ll1l1ll_opy_, event_url=bstack1ll1l11_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩẀ")):
        logger.debug(bstack1ll1l11_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡣࡧࡨࠥࡪࡡࡵࡣࠣࡸࡴࠦࡢࡢࡶࡦ࡬ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦẁ").format(bstack111ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩẂ")]))
        if not bstack11l11l1ll1_opy_.bstack1111ll1ll1l_opy_(bstack111ll1l1ll_opy_[bstack1ll1l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪẃ")]):
            logger.debug(bstack1ll1l11_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡓࡵࡴࠡࡣࡧࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧẄ").format(bstack111ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬẅ")]))
            return
        bstack1l111111l1_opy_ = bstack11l11l1ll1_opy_.bstack1111ll111l1_opy_(bstack111ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭Ẇ")], bstack111ll1l1ll_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬẇ")))
        if bstack1l111111l1_opy_ != None:
            if bstack111ll1l1ll_opy_.get(bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭Ẉ")) != None:
                bstack111ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧẉ")][bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫẊ")] = bstack1l111111l1_opy_
            else:
                bstack111ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬẋ")] = bstack1l111111l1_opy_
        if event_url == bstack1ll1l11_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧẌ"):
            cls.bstack1111ll1llll_opy_()
            logger.debug(bstack1ll1l11_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡁࡥࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡹࡵࠠࡣࡣࡷࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧẍ").format(bstack111ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧẎ")]))
            cls.bstack111l11llll1_opy_.add(bstack111ll1l1ll_opy_)
        elif event_url == bstack1ll1l11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩẏ"):
            cls.bstack1111ll11111_opy_([bstack111ll1l1ll_opy_], event_url)
    @classmethod
    @bstack111l11lll1_opy_(class_method=True)
    def bstack1l1l11l1l_opy_(cls, logs):
        bstack1111lll1111_opy_ = []
        for log in logs:
            bstack1111ll1lll1_opy_ = {
                bstack1ll1l11_opy_ (u"ࠬࡱࡩ࡯ࡦࠪẐ"): bstack1ll1l11_opy_ (u"࠭ࡔࡆࡕࡗࡣࡑࡕࡇࠨẑ"),
                bstack1ll1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭Ẓ"): log[bstack1ll1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧẓ")],
                bstack1ll1l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬẔ"): log[bstack1ll1l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ẕ")],
                bstack1ll1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࠫẖ"): {},
                bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ẗ"): log[bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧẘ")],
            }
            if bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧẙ") in log:
                bstack1111ll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨẚ")] = log[bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẛ")]
            elif bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪẜ") in log:
                bstack1111ll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫẝ")] = log[bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬẞ")]
            bstack1111lll1111_opy_.append(bstack1111ll1lll1_opy_)
        cls.bstack11l1lll111_opy_({
            bstack1ll1l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪẟ"): bstack1ll1l11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫẠ"),
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ạ"): bstack1111lll1111_opy_
        })
    @classmethod
    @bstack111l11lll1_opy_(class_method=True)
    def bstack1111l1lllll_opy_(cls, steps):
        bstack1111lll11l1_opy_ = []
        for step in steps:
            bstack1111lll1lll_opy_ = {
                bstack1ll1l11_opy_ (u"ࠩ࡮࡭ࡳࡪࠧẢ"): bstack1ll1l11_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡗࡉࡕ࠭ả"),
                bstack1ll1l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪẤ"): step[bstack1ll1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫấ")],
                bstack1ll1l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩẦ"): step[bstack1ll1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪầ")],
                bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩẨ"): step[bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪẩ")],
                bstack1ll1l11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬẪ"): step[bstack1ll1l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ẫ")]
            }
            if bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬẬ") in step:
                bstack1111lll1lll_opy_[bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ậ")] = step[bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧẮ")]
            elif bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨắ") in step:
                bstack1111lll1lll_opy_[bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẰ")] = step[bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪằ")]
            bstack1111lll11l1_opy_.append(bstack1111lll1lll_opy_)
        cls.bstack11l1lll111_opy_({
            bstack1ll1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨẲ"): bstack1ll1l11_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩẳ"),
            bstack1ll1l11_opy_ (u"࠭࡬ࡰࡩࡶࠫẴ"): bstack1111lll11l1_opy_
        })
    @classmethod
    @bstack111l11lll1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1l111lll1_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def bstack1ll1llll11_opy_(cls, screenshot):
        cls.bstack11l1lll111_opy_({
            bstack1ll1l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫẵ"): bstack1ll1l11_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬẶ"),
            bstack1ll1l11_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧặ"): [{
                bstack1ll1l11_opy_ (u"ࠪ࡯࡮ࡴࡤࠨẸ"): bstack1ll1l11_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࠭ẹ"),
                bstack1ll1l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨẺ"): datetime.datetime.utcnow().isoformat() + bstack1ll1l11_opy_ (u"࡚࠭ࠨẻ"),
                bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨẼ"): screenshot[bstack1ll1l11_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧẽ")],
                bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẾ"): screenshot[bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪế")]
            }]
        }, event_url=bstack1ll1l11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩỀ"))
    @classmethod
    @bstack111l11lll1_opy_(class_method=True)
    def bstack1ll11ll11_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11l1lll111_opy_({
            bstack1ll1l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩề"): bstack1ll1l11_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪỂ"),
            bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩể"): {
                bstack1ll1l11_opy_ (u"ࠣࡷࡸ࡭ࡩࠨỄ"): cls.current_test_uuid(),
                bstack1ll1l11_opy_ (u"ࠤ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠣễ"): cls.bstack11l111ll11_opy_(driver)
            }
        })
    @classmethod
    def bstack111lllll1l_opy_(cls, event: str, bstack111ll1l1ll_opy_: bstack111lll1l1l_opy_):
        bstack111ll1l1l1_opy_ = {
            bstack1ll1l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧỆ"): event,
            bstack111ll1l1ll_opy_.bstack111l11l111_opy_(): bstack111ll1l1ll_opy_.bstack111ll1l11l_opy_(event)
        }
        cls.bstack11l1lll111_opy_(bstack111ll1l1l1_opy_)
        result = getattr(bstack111ll1l1ll_opy_, bstack1ll1l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫệ"), None)
        if event == bstack1ll1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭Ỉ"):
            threading.current_thread().bstackTestMeta = {bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ỉ"): bstack1ll1l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨỊ")}
        elif event == bstack1ll1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪị"):
            threading.current_thread().bstackTestMeta = {bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩỌ"): getattr(result, bstack1ll1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪọ"), bstack1ll1l11_opy_ (u"ࠫࠬỎ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩỏ"), None) is None or os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪỐ")] == bstack1ll1l11_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧố")) and (os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭Ồ"), None) is None or os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧồ")] == bstack1ll1l11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣỔ")):
            return False
        return True
    @staticmethod
    def bstack1111lll1ll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll1l11l1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1ll1l11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪổ"): bstack1ll1l11_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨỖ"),
            bstack1ll1l11_opy_ (u"࠭ࡘ࠮ࡄࡖࡘࡆࡉࡋ࠮ࡖࡈࡗ࡙ࡕࡐࡔࠩỗ"): bstack1ll1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬỘ")
        }
        if os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬộ"), None):
            headers[bstack1ll1l11_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩỚ")] = bstack1ll1l11_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ớ").format(os.environ[bstack1ll1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠣỜ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1ll1l11_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫờ").format(bstack1111ll1l111_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪỞ"), None)
    @staticmethod
    def bstack11l111ll11_opy_(driver):
        return {
            bstack11l11lllll1_opy_(): bstack11l1l11lll1_opy_(driver)
        }
    @staticmethod
    def bstack1111ll1ll11_opy_(exception_info, report):
        return [{bstack1ll1l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪở"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111ll1111_opy_(typename):
        if bstack1ll1l11_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦỠ") in typename:
            return bstack1ll1l11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥỡ")
        return bstack1ll1l11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦỢ")