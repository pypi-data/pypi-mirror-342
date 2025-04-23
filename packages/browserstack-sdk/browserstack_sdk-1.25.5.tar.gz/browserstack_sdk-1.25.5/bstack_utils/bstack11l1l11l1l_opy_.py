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
import datetime
import threading
from bstack_utils.helper import bstack11llll11ll1_opy_, bstack1l1l11l1ll_opy_, get_host_info, bstack11l1lll11ll_opy_, \
 bstack1l1l1lll1_opy_, bstack11ll111l1_opy_, bstack111l11lll1_opy_, bstack11l1llllll1_opy_, bstack1lllllll11_opy_
import bstack_utils.accessibility as bstack1ll1lll1l_opy_
from bstack_utils.bstack11l1111l1l_opy_ import bstack1lll111111_opy_
from bstack_utils.percy import bstack111l111l_opy_
from bstack_utils.config import Config
bstack11lll1111_opy_ = Config.bstack11111l1l1_opy_()
logger = logging.getLogger(__name__)
percy = bstack111l111l_opy_()
@bstack111l11lll1_opy_(class_method=False)
def bstack1111lll111l_opy_(bs_config, bstack111l11l11_opy_):
  try:
    data = {
        bstack1ll1l11_opy_ (u"ࠫ࡫ࡵࡲ࡮ࡣࡷࠫợ"): bstack1ll1l11_opy_ (u"ࠬࡰࡳࡰࡰࠪỤ"),
        bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺ࡟࡯ࡣࡰࡩࠬụ"): bs_config.get(bstack1ll1l11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬỦ"), bstack1ll1l11_opy_ (u"ࠨࠩủ")),
        bstack1ll1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧỨ"): bs_config.get(bstack1ll1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ứ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧỪ"): bs_config.get(bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧừ")),
        bstack1ll1l11_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫỬ"): bs_config.get(bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪử"), bstack1ll1l11_opy_ (u"ࠨࠩỮ")),
        bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ữ"): bstack1lllllll11_opy_(),
        bstack1ll1l11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨỰ"): bstack11l1lll11ll_opy_(bs_config),
        bstack1ll1l11_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧự"): get_host_info(),
        bstack1ll1l11_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭Ỳ"): bstack1l1l11l1ll_opy_(),
        bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ỳ"): os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭Ỵ")),
        bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ࠭ỵ"): os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧỶ"), False),
        bstack1ll1l11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬỷ"): bstack11llll11ll1_opy_(),
        bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫỸ"): bstack1111l1ll11l_opy_(),
        bstack1ll1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡦࡨࡸࡦ࡯࡬ࡴࠩỹ"): bstack1111l1l1lll_opy_(bstack111l11l11_opy_),
        bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫỺ"): bstack1l1ll11l_opy_(bs_config, bstack111l11l11_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨỻ"), bstack1ll1l11_opy_ (u"ࠨࠩỼ"))),
        bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫỽ"): bstack1l1l1lll1_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1ll1l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡣࡼࡰࡴࡧࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦỾ").format(str(error)))
    return None
def bstack1111l1l1lll_opy_(framework):
  return {
    bstack1ll1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫỿ"): framework.get(bstack1ll1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭ἀ"), bstack1ll1l11_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ἁ")),
    bstack1ll1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪἂ"): framework.get(bstack1ll1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬἃ")),
    bstack1ll1l11_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ἄ"): framework.get(bstack1ll1l11_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨἅ")),
    bstack1ll1l11_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ἆ"): bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬἇ"),
    bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭Ἀ"): framework.get(bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧἉ"))
  }
def bstack1l1ll11l_opy_(bs_config, framework):
  bstack1l11l1lll1_opy_ = False
  bstack1l1l11ll11_opy_ = False
  bstack1111l1ll1ll_opy_ = False
  if bstack1ll1l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬἊ") in bs_config:
    bstack1111l1ll1ll_opy_ = True
  elif bstack1ll1l11_opy_ (u"ࠩࡤࡴࡵ࠭Ἃ") in bs_config:
    bstack1l11l1lll1_opy_ = True
  else:
    bstack1l1l11ll11_opy_ = True
  bstack1l111111l1_opy_ = {
    bstack1ll1l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪἌ"): bstack1lll111111_opy_.bstack1111l1l1ll1_opy_(bs_config, framework),
    bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫἍ"): bstack1ll1lll1l_opy_.bstack1l11l1lll_opy_(bs_config),
    bstack1ll1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫἎ"): bs_config.get(bstack1ll1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬἏ"), False),
    bstack1ll1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩἐ"): bstack1l1l11ll11_opy_,
    bstack1ll1l11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧἑ"): bstack1l11l1lll1_opy_,
    bstack1ll1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ἒ"): bstack1111l1ll1ll_opy_
  }
  return bstack1l111111l1_opy_
@bstack111l11lll1_opy_(class_method=False)
def bstack1111l1ll11l_opy_():
  try:
    bstack1111l1ll1l1_opy_ = json.loads(os.getenv(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫἓ"), bstack1ll1l11_opy_ (u"ࠫࢀࢃࠧἔ")))
    return {
        bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧἕ"): bstack1111l1ll1l1_opy_
    }
  except Exception as error:
    logger.error(bstack1ll1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧ἖").format(str(error)))
    return {}
def bstack1111lll1l11_opy_(array, bstack1111l1lll11_opy_, bstack1111l1lll1l_opy_):
  result = {}
  for o in array:
    key = o[bstack1111l1lll11_opy_]
    result[key] = o[bstack1111l1lll1l_opy_]
  return result
def bstack1111ll1ll1l_opy_(bstack1l11l1ll1l_opy_=bstack1ll1l11_opy_ (u"ࠧࠨ἗")):
  bstack1111l1ll111_opy_ = bstack1ll1lll1l_opy_.on()
  bstack1111l1l1l1l_opy_ = bstack1lll111111_opy_.on()
  bstack1111l1l11ll_opy_ = percy.bstack11l1ll1lll_opy_()
  if bstack1111l1l11ll_opy_ and not bstack1111l1l1l1l_opy_ and not bstack1111l1ll111_opy_:
    return bstack1l11l1ll1l_opy_ not in [bstack1ll1l11_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬἘ"), bstack1ll1l11_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭Ἑ")]
  elif bstack1111l1ll111_opy_ and not bstack1111l1l1l1l_opy_:
    return bstack1l11l1ll1l_opy_ not in [bstack1ll1l11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫἚ"), bstack1ll1l11_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭Ἓ"), bstack1ll1l11_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩἜ")]
  return bstack1111l1ll111_opy_ or bstack1111l1l1l1l_opy_ or bstack1111l1l11ll_opy_
@bstack111l11lll1_opy_(class_method=False)
def bstack1111ll111l1_opy_(bstack1l11l1ll1l_opy_, test=None):
  bstack1111l1l1l11_opy_ = bstack1ll1lll1l_opy_.on()
  if not bstack1111l1l1l11_opy_ or bstack1l11l1ll1l_opy_ not in [bstack1ll1l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨἝ")] or test == None:
    return None
  return {
    bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ἞"): bstack1111l1l1l11_opy_ and bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ἟"), None) == True and bstack1ll1lll1l_opy_.bstack11ll1ll1l1_opy_(test[bstack1ll1l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧἠ")])
  }