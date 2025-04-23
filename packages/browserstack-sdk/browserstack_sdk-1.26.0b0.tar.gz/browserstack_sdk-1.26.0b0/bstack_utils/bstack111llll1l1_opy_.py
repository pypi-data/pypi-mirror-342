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
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11lllll11l1_opy_, bstack11llll1l1l1_opy_, bstack1l1lllll1l_opy_, bstack111ll1ll11_opy_, bstack11l11llllll_opy_, bstack11ll11l11ll_opy_, bstack11l1lll1lll_opy_, bstack11lllll1l_opy_, bstack1l1llll11l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111l11lll11_opy_ import bstack111l11llll1_opy_
import bstack_utils.bstack1l11llll1_opy_ as bstack111l11lll_opy_
from bstack_utils.bstack11l11l11l1_opy_ import bstack11lll1l1_opy_
import bstack_utils.accessibility as bstack1l1111l1_opy_
from bstack_utils.bstack1l11l1l11l_opy_ import bstack1l11l1l11l_opy_
from bstack_utils.bstack111llll11l_opy_ import bstack111l11ll1l_opy_
bstack1111ll1l11l_opy_ = bstack11111ll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡤࡱ࡯ࡰࡪࡩࡴࡰࡴ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᷩ")
logger = logging.getLogger(__name__)
class bstack1l1l1l1111_opy_:
    bstack111l11lll11_opy_ = None
    bs_config = None
    bstack111l111l1_opy_ = None
    @classmethod
    @bstack111ll1ll11_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11ll1ll1111_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def launch(cls, bs_config, bstack111l111l1_opy_):
        cls.bs_config = bs_config
        cls.bstack111l111l1_opy_ = bstack111l111l1_opy_
        try:
            cls.bstack1111lll1l11_opy_()
            bstack11llll11111_opy_ = bstack11lllll11l1_opy_(bs_config)
            bstack11llllll111_opy_ = bstack11llll1l1l1_opy_(bs_config)
            data = bstack111l11lll_opy_.bstack1111lll11l1_opy_(bs_config, bstack111l111l1_opy_)
            config = {
                bstack11111ll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᷪ"): (bstack11llll11111_opy_, bstack11llllll111_opy_),
                bstack11111ll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᷫ"): cls.default_headers()
            }
            response = bstack1l1lllll1l_opy_(bstack11111ll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᷬ"), cls.request_url(bstack11111ll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠴࠲ࡦࡺ࡯࡬ࡥࡵࠪᷭ")), data, config)
            if response.status_code != 200:
                bstack1llll111lll_opy_ = response.json()
                if bstack1llll111lll_opy_[bstack11111ll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᷮ")] == False:
                    cls.bstack1111ll1lll1_opy_(bstack1llll111lll_opy_)
                    return
                cls.bstack1111lll1l1l_opy_(bstack1llll111lll_opy_[bstack11111ll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᷯ")])
                cls.bstack1111ll1llll_opy_(bstack1llll111lll_opy_[bstack11111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᷰ")])
                return None
            bstack1111ll1l111_opy_ = cls.bstack1111lll11ll_opy_(response)
            return bstack1111ll1l111_opy_
        except Exception as error:
            logger.error(bstack11111ll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡾࢁࠧᷱ").format(str(error)))
            return None
    @classmethod
    @bstack111ll1ll11_opy_(class_method=True)
    def stop(cls, bstack1111lll1ll1_opy_=None):
        if not bstack11lll1l1_opy_.on() and not bstack1l1111l1_opy_.on():
            return
        if os.environ.get(bstack11111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᷲ")) == bstack11111ll_opy_ (u"ࠤࡱࡹࡱࡲࠢᷳ") or os.environ.get(bstack11111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᷴ")) == bstack11111ll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ᷵"):
            logger.error(bstack11111ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨ᷶"))
            return {
                bstack11111ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ᷷࠭"): bstack11111ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ᷸࠭"),
                bstack11111ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦ᷹ࠩ"): bstack11111ll_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪ᷺ࠧ")
            }
        try:
            cls.bstack111l11lll11_opy_.shutdown()
            data = {
                bstack11111ll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ᷻"): bstack11lllll1l_opy_()
            }
            if not bstack1111lll1ll1_opy_ is None:
                data[bstack11111ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠨ᷼")] = [{
                    bstack11111ll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲ᷽ࠬ"): bstack11111ll_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫ᷾"),
                    bstack11111ll_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲ᷿ࠧ"): bstack1111lll1ll1_opy_
                }]
            config = {
                bstack11111ll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩḀ"): cls.default_headers()
            }
            bstack11l1l11l1ll_opy_ = bstack11111ll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡴࡰࡲࠪḁ").format(os.environ[bstack11111ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣḂ")])
            bstack1111ll1l1ll_opy_ = cls.request_url(bstack11l1l11l1ll_opy_)
            response = bstack1l1lllll1l_opy_(bstack11111ll_opy_ (u"ࠫࡕ࡛ࡔࠨḃ"), bstack1111ll1l1ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11111ll_opy_ (u"࡙ࠧࡴࡰࡲࠣࡶࡪࡷࡵࡦࡵࡷࠤࡳࡵࡴࠡࡱ࡮ࠦḄ"))
        except Exception as error:
            logger.error(bstack11111ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺࠻ࠢࠥḅ") + str(error))
            return {
                bstack11111ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧḆ"): bstack11111ll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧḇ"),
                bstack11111ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪḈ"): str(error)
            }
    @classmethod
    @bstack111ll1ll11_opy_(class_method=True)
    def bstack1111lll11ll_opy_(cls, response):
        bstack1llll111lll_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1111ll1l111_opy_ = {}
        if bstack1llll111lll_opy_.get(bstack11111ll_opy_ (u"ࠪ࡮ࡼࡺࠧḉ")) is None:
            os.environ[bstack11111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨḊ")] = bstack11111ll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪḋ")
        else:
            os.environ[bstack11111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪḌ")] = bstack1llll111lll_opy_.get(bstack11111ll_opy_ (u"ࠧ࡫ࡹࡷࠫḍ"), bstack11111ll_opy_ (u"ࠨࡰࡸࡰࡱ࠭Ḏ"))
        os.environ[bstack11111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧḏ")] = bstack1llll111lll_opy_.get(bstack11111ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬḐ"), bstack11111ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩḑ"))
        logger.info(bstack11111ll_opy_ (u"࡚ࠬࡥࡴࡶ࡫ࡹࡧࠦࡳࡵࡣࡵࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥ࡯ࡤ࠻ࠢࠪḒ") + os.getenv(bstack11111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫḓ")));
        if bstack11lll1l1_opy_.bstack1111ll11ll1_opy_(cls.bs_config, cls.bstack111l111l1_opy_.get(bstack11111ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨḔ"), bstack11111ll_opy_ (u"ࠨࠩḕ"))) is True:
            bstack111l11l1ll1_opy_, build_hashed_id, bstack1111ll1ll1l_opy_ = cls.bstack1111ll1l1l1_opy_(bstack1llll111lll_opy_)
            if bstack111l11l1ll1_opy_ != None and build_hashed_id != None:
                bstack1111ll1l111_opy_[bstack11111ll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩḖ")] = {
                    bstack11111ll_opy_ (u"ࠪ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳ࠭ḗ"): bstack111l11l1ll1_opy_,
                    bstack11111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭Ḙ"): build_hashed_id,
                    bstack11111ll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩḙ"): bstack1111ll1ll1l_opy_
                }
            else:
                bstack1111ll1l111_opy_[bstack11111ll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭Ḛ")] = {}
        else:
            bstack1111ll1l111_opy_[bstack11111ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧḛ")] = {}
        if bstack1l1111l1_opy_.bstack1lll11l1l1_opy_(cls.bs_config) is True:
            bstack1111l1llll1_opy_, build_hashed_id = cls.bstack1111ll11l1l_opy_(bstack1llll111lll_opy_)
            if bstack1111l1llll1_opy_ != None and build_hashed_id != None:
                bstack1111ll1l111_opy_[bstack11111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨḜ")] = {
                    bstack11111ll_opy_ (u"ࠩࡤࡹࡹ࡮࡟ࡵࡱ࡮ࡩࡳ࠭ḝ"): bstack1111l1llll1_opy_,
                    bstack11111ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬḞ"): build_hashed_id,
                }
            else:
                bstack1111ll1l111_opy_[bstack11111ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫḟ")] = {}
        else:
            bstack1111ll1l111_opy_[bstack11111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬḠ")] = {}
        if bstack1111ll1l111_opy_[bstack11111ll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ḡ")].get(bstack11111ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩḢ")) != None or bstack1111ll1l111_opy_[bstack11111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨḣ")].get(bstack11111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫḤ")) != None:
            cls.bstack1111lll1111_opy_(bstack1llll111lll_opy_.get(bstack11111ll_opy_ (u"ࠪ࡮ࡼࡺࠧḥ")), bstack1llll111lll_opy_.get(bstack11111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭Ḧ")))
        return bstack1111ll1l111_opy_
    @classmethod
    def bstack1111ll1l1l1_opy_(cls, bstack1llll111lll_opy_):
        if bstack1llll111lll_opy_.get(bstack11111ll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬḧ")) == None:
            cls.bstack1111lll1l1l_opy_()
            return [None, None, None]
        if bstack1llll111lll_opy_[bstack11111ll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭Ḩ")][bstack11111ll_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨḩ")] != True:
            cls.bstack1111lll1l1l_opy_(bstack1llll111lll_opy_[bstack11111ll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨḪ")])
            return [None, None, None]
        logger.debug(bstack11111ll_opy_ (u"ࠩࡗࡩࡸࡺࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭ḫ"))
        os.environ[bstack11111ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩḬ")] = bstack11111ll_opy_ (u"ࠫࡹࡸࡵࡦࠩḭ")
        if bstack1llll111lll_opy_.get(bstack11111ll_opy_ (u"ࠬࡰࡷࡵࠩḮ")):
            os.environ[bstack11111ll_opy_ (u"࠭ࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࡣࡋࡕࡒࡠࡅࡕࡅࡘࡎ࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪḯ")] = json.dumps({
                bstack11111ll_opy_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩḰ"): bstack11lllll11l1_opy_(cls.bs_config),
                bstack11111ll_opy_ (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪḱ"): bstack11llll1l1l1_opy_(cls.bs_config)
            })
        if bstack1llll111lll_opy_.get(bstack11111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫḲ")):
            os.environ[bstack11111ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩḳ")] = bstack1llll111lll_opy_[bstack11111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭Ḵ")]
        if bstack1llll111lll_opy_[bstack11111ll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬḵ")].get(bstack11111ll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧḶ"), {}).get(bstack11111ll_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫḷ")):
            os.environ[bstack11111ll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩḸ")] = str(bstack1llll111lll_opy_[bstack11111ll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩḹ")][bstack11111ll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫḺ")][bstack11111ll_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨḻ")])
        else:
            os.environ[bstack11111ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭Ḽ")] = bstack11111ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦḽ")
        return [bstack1llll111lll_opy_[bstack11111ll_opy_ (u"ࠧ࡫ࡹࡷࠫḾ")], bstack1llll111lll_opy_[bstack11111ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪḿ")], os.environ[bstack11111ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪṀ")]]
    @classmethod
    def bstack1111ll11l1l_opy_(cls, bstack1llll111lll_opy_):
        if bstack1llll111lll_opy_.get(bstack11111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪṁ")) == None:
            cls.bstack1111ll1llll_opy_()
            return [None, None]
        if bstack1llll111lll_opy_[bstack11111ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫṂ")][bstack11111ll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ṃ")] != True:
            cls.bstack1111ll1llll_opy_(bstack1llll111lll_opy_[bstack11111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ṅ")])
            return [None, None]
        if bstack1llll111lll_opy_[bstack11111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧṅ")].get(bstack11111ll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩṆ")):
            logger.debug(bstack11111ll_opy_ (u"ࠩࡗࡩࡸࡺࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭ṇ"))
            parsed = json.loads(os.getenv(bstack11111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫṈ"), bstack11111ll_opy_ (u"ࠫࢀࢃࠧṉ")))
            capabilities = bstack111l11lll_opy_.bstack1111l1lllll_opy_(bstack1llll111lll_opy_[bstack11111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬṊ")][bstack11111ll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧṋ")][bstack11111ll_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭Ṍ")], bstack11111ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ṍ"), bstack11111ll_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨṎ"))
            bstack1111l1llll1_opy_ = capabilities[bstack11111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨṏ")]
            os.environ[bstack11111ll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩṐ")] = bstack1111l1llll1_opy_
            if bstack11111ll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢṑ") in bstack1llll111lll_opy_ and bstack1llll111lll_opy_.get(bstack11111ll_opy_ (u"ࠨࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠧṒ")) is None:
                parsed[bstack11111ll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨṓ")] = capabilities[bstack11111ll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩṔ")]
            os.environ[bstack11111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪṕ")] = json.dumps(parsed)
            scripts = bstack111l11lll_opy_.bstack1111l1lllll_opy_(bstack1llll111lll_opy_[bstack11111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪṖ")][bstack11111ll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬṗ")][bstack11111ll_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭Ṙ")], bstack11111ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫṙ"), bstack11111ll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࠨṚ"))
            bstack1l11l1l11l_opy_.bstack1l1111111l_opy_(scripts)
            commands = bstack1llll111lll_opy_[bstack11111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨṛ")][bstack11111ll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪṜ")][bstack11111ll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠫṝ")].get(bstack11111ll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭Ṟ"))
            bstack1l11l1l11l_opy_.bstack11lll1llll1_opy_(commands)
            bstack1l11l1l11l_opy_.store()
        return [bstack1111l1llll1_opy_, bstack1llll111lll_opy_[bstack11111ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧṟ")]]
    @classmethod
    def bstack1111lll1l1l_opy_(cls, response=None):
        os.environ[bstack11111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫṠ")] = bstack11111ll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬṡ")
        os.environ[bstack11111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬṢ")] = bstack11111ll_opy_ (u"ࠩࡱࡹࡱࡲࠧṣ")
        os.environ[bstack11111ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩṤ")] = bstack11111ll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪṥ")
        os.environ[bstack11111ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫṦ")] = bstack11111ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦṧ")
        os.environ[bstack11111ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨṨ")] = bstack11111ll_opy_ (u"ࠣࡰࡸࡰࡱࠨṩ")
        cls.bstack1111ll1lll1_opy_(response, bstack11111ll_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤṪ"))
        return [None, None, None]
    @classmethod
    def bstack1111ll1llll_opy_(cls, response=None):
        os.environ[bstack11111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨṫ")] = bstack11111ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩṬ")
        os.environ[bstack11111ll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪṭ")] = bstack11111ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫṮ")
        os.environ[bstack11111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫṯ")] = bstack11111ll_opy_ (u"ࠨࡰࡸࡰࡱ࠭Ṱ")
        cls.bstack1111ll1lll1_opy_(response, bstack11111ll_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤṱ"))
        return [None, None, None]
    @classmethod
    def bstack1111lll1111_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack11111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧṲ")] = jwt
        os.environ[bstack11111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩṳ")] = build_hashed_id
    @classmethod
    def bstack1111ll1lll1_opy_(cls, response=None, product=bstack11111ll_opy_ (u"ࠧࠨṴ")):
        if response == None:
            logger.error(product + bstack11111ll_opy_ (u"ࠨࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠣṵ"))
        for error in response[bstack11111ll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧṶ")]:
            bstack11l1l111l11_opy_ = error[bstack11111ll_opy_ (u"ࠨ࡭ࡨࡽࠬṷ")]
            error_message = error[bstack11111ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪṸ")]
            if error_message:
                if bstack11l1l111l11_opy_ == bstack11111ll_opy_ (u"ࠥࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠤṹ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11111ll_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࠧṺ") + product + bstack11111ll_opy_ (u"ࠧࠦࡦࡢ࡫࡯ࡩࡩࠦࡤࡶࡧࠣࡸࡴࠦࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥṻ"))
    @classmethod
    def bstack1111lll1l11_opy_(cls):
        if cls.bstack111l11lll11_opy_ is not None:
            return
        cls.bstack111l11lll11_opy_ = bstack111l11llll1_opy_(cls.bstack1111ll11lll_opy_)
        cls.bstack111l11lll11_opy_.start()
    @classmethod
    def bstack111l1lll11_opy_(cls):
        if cls.bstack111l11lll11_opy_ is None:
            return
        cls.bstack111l11lll11_opy_.shutdown()
    @classmethod
    @bstack111ll1ll11_opy_(class_method=True)
    def bstack1111ll11lll_opy_(cls, bstack111ll1ll1l_opy_, event_url=bstack11111ll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬṼ")):
        config = {
            bstack11111ll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨṽ"): cls.default_headers()
        }
        logger.debug(bstack11111ll_opy_ (u"ࠣࡲࡲࡷࡹࡥࡤࡢࡶࡤ࠾࡙ࠥࡥ࡯ࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡹࡵࠠࡵࡧࡶࡸ࡭ࡻࡢࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࡷࠥࢁࡽࠣṾ").format(bstack11111ll_opy_ (u"ࠩ࠯ࠤࠬṿ").join([event[bstack11111ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧẀ")] for event in bstack111ll1ll1l_opy_])))
        response = bstack1l1lllll1l_opy_(bstack11111ll_opy_ (u"ࠫࡕࡕࡓࡕࠩẁ"), cls.request_url(event_url), bstack111ll1ll1l_opy_, config)
        bstack11lllll1l1l_opy_ = response.json()
    @classmethod
    def bstack1111l11l_opy_(cls, bstack111ll1ll1l_opy_, event_url=bstack11111ll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫẂ")):
        logger.debug(bstack11111ll_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡥࡩࡪࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨẃ").format(bstack111ll1ll1l_opy_[bstack11111ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫẄ")]))
        if not bstack111l11lll_opy_.bstack1111ll1ll11_opy_(bstack111ll1ll1l_opy_[bstack11111ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬẅ")]):
            logger.debug(bstack11111ll_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡎࡰࡶࠣࡥࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢẆ").format(bstack111ll1ll1l_opy_[bstack11111ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧẇ")]))
            return
        bstack1l11111l1l_opy_ = bstack111l11lll_opy_.bstack1111ll111ll_opy_(bstack111ll1ll1l_opy_[bstack11111ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨẈ")], bstack111ll1ll1l_opy_.get(bstack11111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧẉ")))
        if bstack1l11111l1l_opy_ != None:
            if bstack111ll1ll1l_opy_.get(bstack11111ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨẊ")) != None:
                bstack111ll1ll1l_opy_[bstack11111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩẋ")][bstack11111ll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭Ẍ")] = bstack1l11111l1l_opy_
            else:
                bstack111ll1ll1l_opy_[bstack11111ll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧẍ")] = bstack1l11111l1l_opy_
        if event_url == bstack11111ll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩẎ"):
            cls.bstack1111lll1l11_opy_()
            logger.debug(bstack11111ll_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡃࡧࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢẏ").format(bstack111ll1ll1l_opy_[bstack11111ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩẐ")]))
            cls.bstack111l11lll11_opy_.add(bstack111ll1ll1l_opy_)
        elif event_url == bstack11111ll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫẑ"):
            cls.bstack1111ll11lll_opy_([bstack111ll1ll1l_opy_], event_url)
    @classmethod
    @bstack111ll1ll11_opy_(class_method=True)
    def bstack1llllll1l_opy_(cls, logs):
        bstack1111ll11l11_opy_ = []
        for log in logs:
            bstack1111ll11111_opy_ = {
                bstack11111ll_opy_ (u"ࠧ࡬࡫ࡱࡨࠬẒ"): bstack11111ll_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡌࡐࡉࠪẓ"),
                bstack11111ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨẔ"): log[bstack11111ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩẕ")],
                bstack11111ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧẖ"): log[bstack11111ll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨẗ")],
                bstack11111ll_opy_ (u"࠭ࡨࡵࡶࡳࡣࡷ࡫ࡳࡱࡱࡱࡷࡪ࠭ẘ"): {},
                bstack11111ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨẙ"): log[bstack11111ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩẚ")],
            }
            if bstack11111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẛ") in log:
                bstack1111ll11111_opy_[bstack11111ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪẜ")] = log[bstack11111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫẝ")]
            elif bstack11111ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬẞ") in log:
                bstack1111ll11111_opy_[bstack11111ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ẟ")] = log[bstack11111ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧẠ")]
            bstack1111ll11l11_opy_.append(bstack1111ll11111_opy_)
        cls.bstack1111l11l_opy_({
            bstack11111ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬạ"): bstack11111ll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭Ả"),
            bstack11111ll_opy_ (u"ࠪࡰࡴ࡭ࡳࠨả"): bstack1111ll11l11_opy_
        })
    @classmethod
    @bstack111ll1ll11_opy_(class_method=True)
    def bstack1111lll111l_opy_(cls, steps):
        bstack1111ll111l1_opy_ = []
        for step in steps:
            bstack1111lll1lll_opy_ = {
                bstack11111ll_opy_ (u"ࠫࡰ࡯࡮ࡥࠩẤ"): bstack11111ll_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨấ"),
                bstack11111ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬẦ"): step[bstack11111ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ầ")],
                bstack11111ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫẨ"): step[bstack11111ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬẩ")],
                bstack11111ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫẪ"): step[bstack11111ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬẫ")],
                bstack11111ll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧẬ"): step[bstack11111ll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨậ")]
            }
            if bstack11111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧẮ") in step:
                bstack1111lll1lll_opy_[bstack11111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨắ")] = step[bstack11111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẰ")]
            elif bstack11111ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪằ") in step:
                bstack1111lll1lll_opy_[bstack11111ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫẲ")] = step[bstack11111ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬẳ")]
            bstack1111ll111l1_opy_.append(bstack1111lll1lll_opy_)
        cls.bstack1111l11l_opy_({
            bstack11111ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪẴ"): bstack11111ll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫẵ"),
            bstack11111ll_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭Ặ"): bstack1111ll111l1_opy_
        })
    @classmethod
    @bstack111ll1ll11_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1lll111l1l_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def bstack1l111l1ll1_opy_(cls, screenshot):
        cls.bstack1111l11l_opy_({
            bstack11111ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ặ"): bstack11111ll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧẸ"),
            bstack11111ll_opy_ (u"ࠫࡱࡵࡧࡴࠩẹ"): [{
                bstack11111ll_opy_ (u"ࠬࡱࡩ࡯ࡦࠪẺ"): bstack11111ll_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨẻ"),
                bstack11111ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪẼ"): datetime.datetime.utcnow().isoformat() + bstack11111ll_opy_ (u"ࠨ࡜ࠪẽ"),
                bstack11111ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪẾ"): screenshot[bstack11111ll_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩế")],
                bstack11111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫỀ"): screenshot[bstack11111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬề")]
            }]
        }, event_url=bstack11111ll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫỂ"))
    @classmethod
    @bstack111ll1ll11_opy_(class_method=True)
    def bstack1lll11l111_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1111l11l_opy_({
            bstack11111ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫể"): bstack11111ll_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬỄ"),
            bstack11111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫễ"): {
                bstack11111ll_opy_ (u"ࠥࡹࡺ࡯ࡤࠣỆ"): cls.current_test_uuid(),
                bstack11111ll_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥệ"): cls.bstack111llllll1_opy_(driver)
            }
        })
    @classmethod
    def bstack11l11l1111_opy_(cls, event: str, bstack111ll1ll1l_opy_: bstack111l11ll1l_opy_):
        bstack111ll1llll_opy_ = {
            bstack11111ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩỈ"): event,
            bstack111ll1ll1l_opy_.bstack111lll1lll_opy_(): bstack111ll1ll1l_opy_.bstack111ll1l1l1_opy_(event)
        }
        cls.bstack1111l11l_opy_(bstack111ll1llll_opy_)
        result = getattr(bstack111ll1ll1l_opy_, bstack11111ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ỉ"), None)
        if event == bstack11111ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨỊ"):
            threading.current_thread().bstackTestMeta = {bstack11111ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨị"): bstack11111ll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪỌ")}
        elif event == bstack11111ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬọ"):
            threading.current_thread().bstackTestMeta = {bstack11111ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫỎ"): getattr(result, bstack11111ll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬỏ"), bstack11111ll_opy_ (u"࠭ࠧỐ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫố"), None) is None or os.environ[bstack11111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬỒ")] == bstack11111ll_opy_ (u"ࠤࡱࡹࡱࡲࠢồ")) and (os.environ.get(bstack11111ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨỔ"), None) is None or os.environ[bstack11111ll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩổ")] == bstack11111ll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥỖ")):
            return False
        return True
    @staticmethod
    def bstack1111ll1111l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1l1l1111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11111ll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬỗ"): bstack11111ll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪỘ"),
            bstack11111ll_opy_ (u"ࠨ࡚࠰ࡆࡘ࡚ࡁࡄࡍ࠰ࡘࡊ࡙ࡔࡐࡒࡖࠫộ"): bstack11111ll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧỚ")
        }
        if os.environ.get(bstack11111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧớ"), None):
            headers[bstack11111ll_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫỜ")] = bstack11111ll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨờ").format(os.environ[bstack11111ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠥỞ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11111ll_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ở").format(bstack1111ll1l11l_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11111ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬỠ"), None)
    @staticmethod
    def bstack111llllll1_opy_(driver):
        return {
            bstack11l11llllll_opy_(): bstack11ll11l11ll_opy_(driver)
        }
    @staticmethod
    def bstack1111llll111_opy_(exception_info, report):
        return [{bstack11111ll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬỡ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111ll1l11_opy_(typename):
        if bstack11111ll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨỢ") in typename:
            return bstack11111ll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧợ")
        return bstack11111ll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨỤ")