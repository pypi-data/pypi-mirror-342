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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack11llll1lll1_opy_ as bstack11llll11ll1_opy_, EVENTS
from bstack_utils.bstack1l11l1l11l_opy_ import bstack1l11l1l11l_opy_
from bstack_utils.helper import bstack11lllll1l_opy_, bstack111l1ll11l_opy_, bstack1lllll1l1l_opy_, bstack11lllll11l1_opy_, \
  bstack11llll1l1l1_opy_, bstack111ll1l1_opy_, get_host_info, bstack11llll111ll_opy_, bstack1l1lllll1l_opy_, bstack111ll1ll11_opy_, bstack1l1llll11l_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack11ll11llll_opy_ import get_logger
from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll111l1l_opy_
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1ll11l1lll_opy_ = bstack1llll111l1l_opy_()
@bstack111ll1ll11_opy_(class_method=False)
def _11llll1ll1l_opy_(driver, bstack111l111lll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11111ll_opy_ (u"ࠩࡲࡷࡤࡴࡡ࡮ࡧࠪᕏ"): caps.get(bstack11111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᕐ"), None),
        bstack11111ll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᕑ"): bstack111l111lll_opy_.get(bstack11111ll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᕒ"), None),
        bstack11111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬᕓ"): caps.get(bstack11111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᕔ"), None),
        bstack11111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᕕ"): caps.get(bstack11111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᕖ"), None)
    }
  except Exception as error:
    logger.debug(bstack11111ll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧᕗ") + str(error))
  return response
def on():
    if os.environ.get(bstack11111ll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᕘ"), None) is None or os.environ[bstack11111ll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᕙ")] == bstack11111ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᕚ"):
        return False
    return True
def bstack1lll11l1l1_opy_(config):
  return config.get(bstack11111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᕛ"), False) or any([p.get(bstack11111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᕜ"), False) == True for p in config.get(bstack11111ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᕝ"), [])])
def bstack11l11lllll_opy_(config, bstack1ll11l1111_opy_):
  try:
    if not bstack1lllll1l1l_opy_(config):
      return False
    bstack11llll111l1_opy_ = config.get(bstack11111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᕞ"), False)
    if int(bstack1ll11l1111_opy_) < len(config.get(bstack11111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᕟ"), [])) and config[bstack11111ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᕠ")][bstack1ll11l1111_opy_]:
      bstack11llll1l11l_opy_ = config[bstack11111ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᕡ")][bstack1ll11l1111_opy_].get(bstack11111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᕢ"), None)
    else:
      bstack11llll1l11l_opy_ = config.get(bstack11111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᕣ"), None)
    if bstack11llll1l11l_opy_ != None:
      bstack11llll111l1_opy_ = bstack11llll1l11l_opy_
    bstack11lllll11ll_opy_ = os.getenv(bstack11111ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᕤ")) is not None and len(os.getenv(bstack11111ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᕥ"))) > 0 and os.getenv(bstack11111ll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᕦ")) != bstack11111ll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᕧ")
    return bstack11llll111l1_opy_ and bstack11lllll11ll_opy_
  except Exception as error:
    logger.debug(bstack11111ll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡥࡳ࡫ࡩࡽ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ᕨ") + str(error))
  return False
def bstack11l11ll1l1_opy_(test_tags):
  bstack1ll1l11llll_opy_ = os.getenv(bstack11111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᕩ"))
  if bstack1ll1l11llll_opy_ is None:
    return True
  bstack1ll1l11llll_opy_ = json.loads(bstack1ll1l11llll_opy_)
  try:
    include_tags = bstack1ll1l11llll_opy_[bstack11111ll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᕪ")] if bstack11111ll_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᕫ") in bstack1ll1l11llll_opy_ and isinstance(bstack1ll1l11llll_opy_[bstack11111ll_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᕬ")], list) else []
    exclude_tags = bstack1ll1l11llll_opy_[bstack11111ll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᕭ")] if bstack11111ll_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᕮ") in bstack1ll1l11llll_opy_ and isinstance(bstack1ll1l11llll_opy_[bstack11111ll_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᕯ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11111ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢᕰ") + str(error))
  return False
def bstack11lllll1lll_opy_(config, bstack11llll1l1ll_opy_, bstack11llll11l1l_opy_, bstack11lllll111l_opy_):
  bstack11llll11111_opy_ = bstack11lllll11l1_opy_(config)
  bstack11llllll111_opy_ = bstack11llll1l1l1_opy_(config)
  if bstack11llll11111_opy_ is None or bstack11llllll111_opy_ is None:
    logger.error(bstack11111ll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩᕱ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᕲ"), bstack11111ll_opy_ (u"ࠪࡿࢂ࠭ᕳ")))
    data = {
        bstack11111ll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᕴ"): config[bstack11111ll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᕵ")],
        bstack11111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᕶ"): config.get(bstack11111ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᕷ"), os.path.basename(os.getcwd())),
        bstack11111ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡔࡪ࡯ࡨࠫᕸ"): bstack11lllll1l_opy_(),
        bstack11111ll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᕹ"): config.get(bstack11111ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᕺ"), bstack11111ll_opy_ (u"ࠫࠬᕻ")),
        bstack11111ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬᕼ"): {
            bstack11111ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ᕽ"): bstack11llll1l1ll_opy_,
            bstack11111ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᕾ"): bstack11llll11l1l_opy_,
            bstack11111ll_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᕿ"): __version__,
            bstack11111ll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫᖀ"): bstack11111ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᖁ"),
            bstack11111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᖂ"): bstack11111ll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧᖃ"),
            bstack11111ll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᖄ"): bstack11lllll111l_opy_
        },
        bstack11111ll_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩᖅ"): settings,
        bstack11111ll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡅࡲࡲࡹࡸ࡯࡭ࠩᖆ"): bstack11llll111ll_opy_(),
        bstack11111ll_opy_ (u"ࠩࡦ࡭ࡎࡴࡦࡰࠩᖇ"): bstack111ll1l1_opy_(),
        bstack11111ll_opy_ (u"ࠪ࡬ࡴࡹࡴࡊࡰࡩࡳࠬᖈ"): get_host_info(),
        bstack11111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᖉ"): bstack1lllll1l1l_opy_(config)
    }
    headers = {
        bstack11111ll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᖊ"): bstack11111ll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᖋ"),
    }
    config = {
        bstack11111ll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᖌ"): (bstack11llll11111_opy_, bstack11llllll111_opy_),
        bstack11111ll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᖍ"): headers
    }
    response = bstack1l1lllll1l_opy_(bstack11111ll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᖎ"), bstack11llll11ll1_opy_ + bstack11111ll_opy_ (u"ࠪ࠳ࡻ࠸࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵࠪᖏ"), data, config)
    bstack11lllll1l1l_opy_ = response.json()
    if bstack11lllll1l1l_opy_[bstack11111ll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᖐ")]:
      parsed = json.loads(os.getenv(bstack11111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᖑ"), bstack11111ll_opy_ (u"࠭ࡻࡾࠩᖒ")))
      parsed[bstack11111ll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᖓ")] = bstack11lllll1l1l_opy_[bstack11111ll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᖔ")][bstack11111ll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᖕ")]
      os.environ[bstack11111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᖖ")] = json.dumps(parsed)
      bstack1l11l1l11l_opy_.bstack1l1111111l_opy_(bstack11lllll1l1l_opy_[bstack11111ll_opy_ (u"ࠫࡩࡧࡴࡢࠩᖗ")][bstack11111ll_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ᖘ")])
      bstack1l11l1l11l_opy_.bstack11lll1llll1_opy_(bstack11lllll1l1l_opy_[bstack11111ll_opy_ (u"࠭ࡤࡢࡶࡤࠫᖙ")][bstack11111ll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᖚ")])
      bstack1l11l1l11l_opy_.store()
      return bstack11lllll1l1l_opy_[bstack11111ll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᖛ")][bstack11111ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧᖜ")], bstack11lllll1l1l_opy_[bstack11111ll_opy_ (u"ࠪࡨࡦࡺࡡࠨᖝ")][bstack11111ll_opy_ (u"ࠫ࡮ࡪࠧᖞ")]
    else:
      logger.error(bstack11111ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࠭ᖟ") + bstack11lllll1l1l_opy_[bstack11111ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᖠ")])
      if bstack11lllll1l1l_opy_[bstack11111ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᖡ")] == bstack11111ll_opy_ (u"ࠨࡋࡱࡺࡦࡲࡩࡥࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡸࡹࡥࡥ࠰ࠪᖢ"):
        for bstack11lll1lllll_opy_ in bstack11lllll1l1l_opy_[bstack11111ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩᖣ")]:
          logger.error(bstack11lll1lllll_opy_[bstack11111ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᖤ")])
      return None, None
  except Exception as error:
    logger.error(bstack11111ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠧᖥ") +  str(error))
    return None, None
def bstack11llll1l111_opy_():
  if os.getenv(bstack11111ll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᖦ")) is None:
    return {
        bstack11111ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᖧ"): bstack11111ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᖨ"),
        bstack11111ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᖩ"): bstack11111ll_opy_ (u"ࠩࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣ࡬ࡦࡪࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠨᖪ")
    }
  data = {bstack11111ll_opy_ (u"ࠪࡩࡳࡪࡔࡪ࡯ࡨࠫᖫ"): bstack11lllll1l_opy_()}
  headers = {
      bstack11111ll_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫᖬ"): bstack11111ll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥ࠭ᖭ") + os.getenv(bstack11111ll_opy_ (u"ࠨࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠦᖮ")),
      bstack11111ll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᖯ"): bstack11111ll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᖰ")
  }
  response = bstack1l1lllll1l_opy_(bstack11111ll_opy_ (u"ࠩࡓ࡙࡙࠭ᖱ"), bstack11llll11ll1_opy_ + bstack11111ll_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹ࠯ࡴࡶࡲࡴࠬᖲ"), data, { bstack11111ll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᖳ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11111ll_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰࠣࡱࡦࡸ࡫ࡦࡦࠣࡥࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡤࡸࠥࠨᖴ") + bstack111l1ll11l_opy_().isoformat() + bstack11111ll_opy_ (u"࡚࠭ࠨᖵ"))
      return {bstack11111ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᖶ"): bstack11111ll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᖷ"), bstack11111ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᖸ"): bstack11111ll_opy_ (u"ࠪࠫᖹ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11111ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠤࡴ࡬ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲ࠿ࠦࠢᖺ") + str(error))
    return {
        bstack11111ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᖻ"): bstack11111ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᖼ"),
        bstack11111ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᖽ"): str(error)
    }
def bstack11lll1lll1l_opy_(bstack11lllll1111_opy_):
    return re.match(bstack11111ll_opy_ (u"ࡳࠩࡡࡠࡩ࠱ࠨ࡝࠰࡟ࡨ࠰࠯࠿ࠥࠩᖾ"), bstack11lllll1111_opy_.strip()) is not None
def bstack1lll11111l_opy_(caps, options, desired_capabilities={}):
    try:
        if options:
          bstack11llllll1ll_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11llllll1ll_opy_ = desired_capabilities
        else:
          bstack11llllll1ll_opy_ = {}
        bstack11llllll11l_opy_ = (bstack11llllll1ll_opy_.get(bstack11111ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᖿ"), bstack11111ll_opy_ (u"ࠪࠫᗀ")).lower() or caps.get(bstack11111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᗁ"), bstack11111ll_opy_ (u"ࠬ࠭ᗂ")).lower())
        if bstack11llllll11l_opy_ == bstack11111ll_opy_ (u"࠭ࡩࡰࡵࠪᗃ"):
            return True
        if bstack11llllll11l_opy_ == bstack11111ll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࠨᗄ"):
            bstack11llll11lll_opy_ = str(float(caps.get(bstack11111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᗅ")) or bstack11llllll1ll_opy_.get(bstack11111ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᗆ"), {}).get(bstack11111ll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᗇ"),bstack11111ll_opy_ (u"ࠫࠬᗈ"))))
            if bstack11llllll11l_opy_ == bstack11111ll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᗉ") and int(bstack11llll11lll_opy_.split(bstack11111ll_opy_ (u"࠭࠮ࠨᗊ"))[0]) < float(bstack11llllll1l1_opy_):
                logger.warning(str(bstack11lll1lll11_opy_))
                return False
            return True
        bstack1ll1l1ll111_opy_ = caps.get(bstack11111ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗋ"), {}).get(bstack11111ll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᗌ"), caps.get(bstack11111ll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᗍ"), bstack11111ll_opy_ (u"ࠪࠫᗎ")))
        if bstack1ll1l1ll111_opy_:
            logger.warn(bstack11111ll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᗏ"))
            return False
        browser = caps.get(bstack11111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᗐ"), bstack11111ll_opy_ (u"࠭ࠧᗑ")).lower() or bstack11llllll1ll_opy_.get(bstack11111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᗒ"), bstack11111ll_opy_ (u"ࠨࠩᗓ")).lower()
        if browser != bstack11111ll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᗔ"):
            logger.warning(bstack11111ll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᗕ"))
            return False
        browser_version = caps.get(bstack11111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᗖ")) or caps.get(bstack11111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᗗ")) or bstack11llllll1ll_opy_.get(bstack11111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᗘ")) or bstack11llllll1ll_opy_.get(bstack11111ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗙ"), {}).get(bstack11111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᗚ")) or bstack11llllll1ll_opy_.get(bstack11111ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᗛ"), {}).get(bstack11111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᗜ"))
        if browser_version and browser_version != bstack11111ll_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫᗝ") and int(browser_version.split(bstack11111ll_opy_ (u"ࠬ࠴ࠧᗞ"))[0]) <= 98:
            logger.warning(bstack11111ll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠ࠺࠺࠱ࠦᗟ"))
            return False
        if not options:
            bstack1ll1l1111l1_opy_ = caps.get(bstack11111ll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᗠ")) or bstack11llllll1ll_opy_.get(bstack11111ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᗡ"), {})
            if bstack11111ll_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ᗢ") in bstack1ll1l1111l1_opy_.get(bstack11111ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᗣ"), []):
                logger.warn(bstack11111ll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨᗤ"))
                return False
        return True
    except Exception as error:
        logger.debug(bstack11111ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢᗥ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lll111111l_opy_ = config.get(bstack11111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᗦ"), {})
    bstack1lll111111l_opy_[bstack11111ll_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪᗧ")] = os.getenv(bstack11111ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᗨ"))
    bstack11llll11l11_opy_ = json.loads(os.getenv(bstack11111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᗩ"), bstack11111ll_opy_ (u"ࠪࡿࢂ࠭ᗪ"))).get(bstack11111ll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᗫ"))
    caps[bstack11111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᗬ")] = True
    if not config[bstack11111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᗭ")].get(bstack11111ll_opy_ (u"ࠢࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪࠨᗮ")):
      if bstack11111ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᗯ") in caps:
        caps[bstack11111ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᗰ")][bstack11111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᗱ")] = bstack1lll111111l_opy_
        caps[bstack11111ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᗲ")][bstack11111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᗳ")][bstack11111ll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᗴ")] = bstack11llll11l11_opy_
      else:
        caps[bstack11111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᗵ")] = bstack1lll111111l_opy_
        caps[bstack11111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᗶ")][bstack11111ll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᗷ")] = bstack11llll11l11_opy_
  except Exception as error:
    logger.debug(bstack11111ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࠦᗸ") +  str(error))
def bstack1l11l1l11_opy_(driver, bstack11lll1ll1ll_opy_):
  try:
    setattr(driver, bstack11111ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫᗹ"), True)
    session = driver.session_id
    if session:
      bstack11lllll1ll1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lllll1ll1_opy_ = False
      bstack11lllll1ll1_opy_ = url.scheme in [bstack11111ll_opy_ (u"ࠧ࡮ࡴࡵࡲࠥᗺ"), bstack11111ll_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᗻ")]
      if bstack11lllll1ll1_opy_:
        if bstack11lll1ll1ll_opy_:
          logger.info(bstack11111ll_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡦࡰࡴࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰ࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡥࡩ࡬࡯࡮ࠡ࡯ࡲࡱࡪࡴࡴࡢࡴ࡬ࡰࡾ࠴ࠢᗼ"))
      return bstack11lll1ll1ll_opy_
  except Exception as e:
    logger.error(bstack11111ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡤࡶࡹ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦᗽ") + str(e))
    return False
def bstack11ll11l1l_opy_(driver, name, path):
  try:
    bstack1ll1ll111l1_opy_ = {
        bstack11111ll_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩᗾ"): threading.current_thread().current_test_uuid,
        bstack11111ll_opy_ (u"ࠪࡸ࡭ࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᗿ"): os.environ.get(bstack11111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᘀ"), bstack11111ll_opy_ (u"ࠬ࠭ᘁ")),
        bstack11111ll_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪᘂ"): os.environ.get(bstack11111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᘃ"), bstack11111ll_opy_ (u"ࠨࠩᘄ"))
    }
    bstack1ll1ll1l1ll_opy_ = bstack1ll11l1lll_opy_.bstack1ll1l111lll_opy_(EVENTS.bstack1l11ll1l1_opy_.value)
    logger.debug(bstack11111ll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡧࡶࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬᘅ"))
    try:
      if (bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᘆ"), None) and bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᘇ"), None)):
        scripts = {bstack11111ll_opy_ (u"ࠬࡹࡣࡢࡰࠪᘈ"): bstack1l11l1l11l_opy_.perform_scan}
        bstack11llll1llll_opy_ = json.loads(scripts[bstack11111ll_opy_ (u"ࠨࡳࡤࡣࡱࠦᘉ")].replace(bstack11111ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᘊ"), bstack11111ll_opy_ (u"ࠣࠤᘋ")))
        bstack11llll1llll_opy_[bstack11111ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᘌ")][bstack11111ll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪᘍ")] = None
        scripts[bstack11111ll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᘎ")] = bstack11111ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᘏ") + json.dumps(bstack11llll1llll_opy_)
        bstack1l11l1l11l_opy_.bstack1l1111111l_opy_(scripts)
        bstack1l11l1l11l_opy_.store()
        logger.debug(driver.execute_script(bstack1l11l1l11l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l11l1l11l_opy_.perform_scan, {bstack11111ll_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨᘐ"): name}))
      bstack1ll11l1lll_opy_.end(EVENTS.bstack1l11ll1l1_opy_.value, bstack1ll1ll1l1ll_opy_ + bstack11111ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᘑ"), bstack1ll1ll1l1ll_opy_ + bstack11111ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᘒ"), True, None)
    except Exception as error:
      bstack1ll11l1lll_opy_.end(EVENTS.bstack1l11ll1l1_opy_.value, bstack1ll1ll1l1ll_opy_ + bstack11111ll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᘓ"), bstack1ll1ll1l1ll_opy_ + bstack11111ll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᘔ"), False, str(error))
    bstack1ll1ll1l1ll_opy_ = bstack1ll11l1lll_opy_.bstack11lllll1l11_opy_(EVENTS.bstack1ll1l11111l_opy_.value)
    bstack1ll11l1lll_opy_.mark(bstack1ll1ll1l1ll_opy_ + bstack11111ll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᘕ"))
    try:
      if (bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬᘖ"), None) and bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᘗ"), None)):
        scripts = {bstack11111ll_opy_ (u"ࠧࡴࡥࡤࡲࠬᘘ"): bstack1l11l1l11l_opy_.perform_scan}
        bstack11llll1llll_opy_ = json.loads(scripts[bstack11111ll_opy_ (u"ࠣࡵࡦࡥࡳࠨᘙ")].replace(bstack11111ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᘚ"), bstack11111ll_opy_ (u"ࠥࠦᘛ")))
        bstack11llll1llll_opy_[bstack11111ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᘜ")][bstack11111ll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬᘝ")] = None
        scripts[bstack11111ll_opy_ (u"ࠨࡳࡤࡣࡱࠦᘞ")] = bstack11111ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᘟ") + json.dumps(bstack11llll1llll_opy_)
        bstack1l11l1l11l_opy_.bstack1l1111111l_opy_(scripts)
        bstack1l11l1l11l_opy_.store()
        logger.debug(driver.execute_script(bstack1l11l1l11l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l11l1l11l_opy_.bstack11llll1111l_opy_, bstack1ll1ll111l1_opy_))
      bstack1ll11l1lll_opy_.end(bstack1ll1ll1l1ll_opy_, bstack1ll1ll1l1ll_opy_ + bstack11111ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᘠ"), bstack1ll1ll1l1ll_opy_ + bstack11111ll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᘡ"),True, None)
    except Exception as error:
      bstack1ll11l1lll_opy_.end(bstack1ll1ll1l1ll_opy_, bstack1ll1ll1l1ll_opy_ + bstack11111ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᘢ"), bstack1ll1ll1l1ll_opy_ + bstack11111ll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᘣ"),False, str(error))
    logger.info(bstack11111ll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᘤ"))
  except Exception as bstack1ll1ll11ll1_opy_:
    logger.error(bstack11111ll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣᘥ") + str(path) + bstack11111ll_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤᘦ") + str(bstack1ll1ll11ll1_opy_))
def bstack11llll1ll11_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11111ll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᘧ")) and str(caps.get(bstack11111ll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣᘨ"))).lower() == bstack11111ll_opy_ (u"ࠥࡥࡳࡪࡲࡰ࡫ࡧࠦᘩ"):
        bstack11llll11lll_opy_ = caps.get(bstack11111ll_opy_ (u"ࠦࡦࡶࡰࡪࡷࡰ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᘪ")) or caps.get(bstack11111ll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᘫ"))
        if bstack11llll11lll_opy_ and int(str(bstack11llll11lll_opy_)) < bstack11llllll1l1_opy_:
            return False
    return True