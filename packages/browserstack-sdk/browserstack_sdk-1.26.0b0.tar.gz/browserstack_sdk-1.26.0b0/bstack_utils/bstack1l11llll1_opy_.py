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
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11llll111ll_opy_, bstack111ll1l1_opy_, get_host_info, bstack11ll11ll1ll_opy_, \
 bstack1lllll1l1l_opy_, bstack1l1llll11l_opy_, bstack111ll1ll11_opy_, bstack11l1lll1lll_opy_, bstack11lllll1l_opy_
import bstack_utils.accessibility as bstack1l1111l1_opy_
from bstack_utils.bstack11l11l11l1_opy_ import bstack11lll1l1_opy_
from bstack_utils.percy import bstack1l111l1l11_opy_
from bstack_utils.config import Config
bstack11l1l1ll_opy_ = Config.bstack11l1ll1ll1_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l111l1l11_opy_()
@bstack111ll1ll11_opy_(class_method=False)
def bstack1111lll11l1_opy_(bs_config, bstack111l111l1_opy_):
  try:
    data = {
        bstack11111ll_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭ụ"): bstack11111ll_opy_ (u"ࠧ࡫ࡵࡲࡲࠬỦ"),
        bstack11111ll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧủ"): bs_config.get(bstack11111ll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧỨ"), bstack11111ll_opy_ (u"ࠪࠫứ")),
        bstack11111ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩỪ"): bs_config.get(bstack11111ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨừ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩỬ"): bs_config.get(bstack11111ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩử")),
        bstack11111ll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭Ữ"): bs_config.get(bstack11111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬữ"), bstack11111ll_opy_ (u"ࠪࠫỰ")),
        bstack11111ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨự"): bstack11lllll1l_opy_(),
        bstack11111ll_opy_ (u"ࠬࡺࡡࡨࡵࠪỲ"): bstack11ll11ll1ll_opy_(bs_config),
        bstack11111ll_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩỳ"): get_host_info(),
        bstack11111ll_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨỴ"): bstack111ll1l1_opy_(),
        bstack11111ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨỵ"): os.environ.get(bstack11111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨỶ")),
        bstack11111ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨỷ"): os.environ.get(bstack11111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩỸ"), False),
        bstack11111ll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧỹ"): bstack11llll111ll_opy_(),
        bstack11111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ỻ"): bstack1111l1l1ll1_opy_(),
        bstack11111ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡨࡪࡺࡡࡪ࡮ࡶࠫỻ"): bstack1111l1l1l1l_opy_(bstack111l111l1_opy_),
        bstack11111ll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭Ỽ"): bstack11ll111l_opy_(bs_config, bstack111l111l1_opy_.get(bstack11111ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪỽ"), bstack11111ll_opy_ (u"ࠪࠫỾ"))),
        bstack11111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ỿ"): bstack1lllll1l1l_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack11111ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡥࡾࡲ࡯ࡢࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨἀ").format(str(error)))
    return None
def bstack1111l1l1l1l_opy_(framework):
  return {
    bstack11111ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ἁ"): framework.get(bstack11111ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨἂ"), bstack11111ll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨἃ")),
    bstack11111ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬἄ"): framework.get(bstack11111ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧἅ")),
    bstack11111ll_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨἆ"): framework.get(bstack11111ll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪἇ")),
    bstack11111ll_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨἈ"): bstack11111ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧἉ"),
    bstack11111ll_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨἊ"): framework.get(bstack11111ll_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩἋ"))
  }
def bstack11ll111l_opy_(bs_config, framework):
  bstack1ll11llll_opy_ = False
  bstack11l1ll1l11_opy_ = False
  bstack1111l1ll11l_opy_ = False
  if bstack11111ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧἌ") in bs_config:
    bstack1111l1ll11l_opy_ = True
  elif bstack11111ll_opy_ (u"ࠫࡦࡶࡰࠨἍ") in bs_config:
    bstack1ll11llll_opy_ = True
  else:
    bstack11l1ll1l11_opy_ = True
  bstack1l11111l1l_opy_ = {
    bstack11111ll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬἎ"): bstack11lll1l1_opy_.bstack1111l1l11ll_opy_(bs_config, framework),
    bstack11111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ἇ"): bstack1l1111l1_opy_.bstack1lll11l1l1_opy_(bs_config),
    bstack11111ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ἐ"): bs_config.get(bstack11111ll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧἑ"), False),
    bstack11111ll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫἒ"): bstack11l1ll1l11_opy_,
    bstack11111ll_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩἓ"): bstack1ll11llll_opy_,
    bstack11111ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨἔ"): bstack1111l1ll11l_opy_
  }
  return bstack1l11111l1l_opy_
@bstack111ll1ll11_opy_(class_method=False)
def bstack1111l1l1ll1_opy_():
  try:
    bstack1111l1ll1ll_opy_ = json.loads(os.getenv(bstack11111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ἕ"), bstack11111ll_opy_ (u"࠭ࡻࡾࠩ἖")))
    return {
        bstack11111ll_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩ἗"): bstack1111l1ll1ll_opy_
    }
  except Exception as error:
    logger.error(bstack11111ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢἘ").format(str(error)))
    return {}
def bstack1111l1lllll_opy_(array, bstack1111l1lll1l_opy_, bstack1111l1l1l11_opy_):
  result = {}
  for o in array:
    key = o[bstack1111l1lll1l_opy_]
    result[key] = o[bstack1111l1l1l11_opy_]
  return result
def bstack1111ll1ll11_opy_(bstack11l11lll1_opy_=bstack11111ll_opy_ (u"ࠩࠪἙ")):
  bstack1111l1l1lll_opy_ = bstack1l1111l1_opy_.on()
  bstack1111l1ll111_opy_ = bstack11lll1l1_opy_.on()
  bstack1111l1lll11_opy_ = percy.bstack11llllllll_opy_()
  if bstack1111l1lll11_opy_ and not bstack1111l1ll111_opy_ and not bstack1111l1l1lll_opy_:
    return bstack11l11lll1_opy_ not in [bstack11111ll_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧἚ"), bstack11111ll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨἛ")]
  elif bstack1111l1l1lll_opy_ and not bstack1111l1ll111_opy_:
    return bstack11l11lll1_opy_ not in [bstack11111ll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭Ἔ"), bstack11111ll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨἝ"), bstack11111ll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ἞")]
  return bstack1111l1l1lll_opy_ or bstack1111l1ll111_opy_ or bstack1111l1lll11_opy_
@bstack111ll1ll11_opy_(class_method=False)
def bstack1111ll111ll_opy_(bstack11l11lll1_opy_, test=None):
  bstack1111l1ll1l1_opy_ = bstack1l1111l1_opy_.on()
  if not bstack1111l1ll1l1_opy_ or bstack11l11lll1_opy_ not in [bstack11111ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ἟")] or test == None:
    return None
  return {
    bstack11111ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩἠ"): bstack1111l1ll1l1_opy_ and bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩἡ"), None) == True and bstack1l1111l1_opy_.bstack11l11ll1l1_opy_(test[bstack11111ll_opy_ (u"ࠫࡹࡧࡧࡴࠩἢ")])
  }