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
import atexit
import signal
import yaml
import socket
import datetime
import string
import random
import collections.abc
import traceback
import copy
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import json
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack11lllll111_opy_ import bstack11lll1l1ll_opy_
from browserstack_sdk.bstack1l1l1lll1l_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack1ll111111l_opy_():
  global CONFIG
  headers = {
        bstack1ll1l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1ll1l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1ll1l1111_opy_(CONFIG, bstack1l1lll1ll_opy_)
  try:
    response = requests.get(bstack1l1lll1ll_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l1l11llll_opy_ = response.json()[bstack1ll1l11_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l1l1ll1l1_opy_.format(response.json()))
      return bstack1l1l11llll_opy_
    else:
      logger.debug(bstack1l1l11l11l_opy_.format(bstack1ll1l11_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1l1l11l11l_opy_.format(e))
def bstack1l1lll11l_opy_(hub_url):
  global CONFIG
  url = bstack1ll1l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1ll1l11_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1ll1l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1ll1l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1ll1l1111_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l11llll1l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll1lll111_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack11ll11ll1_opy_, stage=STAGE.bstack1l11lll1l_opy_)
def bstack11l1l11ll_opy_():
  try:
    global bstack1l11ll1lll_opy_
    bstack1l1l11llll_opy_ = bstack1ll111111l_opy_()
    bstack111111l1l_opy_ = []
    results = []
    for bstack1l1lllll_opy_ in bstack1l1l11llll_opy_:
      bstack111111l1l_opy_.append(bstack1ll11111l_opy_(target=bstack1l1lll11l_opy_,args=(bstack1l1lllll_opy_,)))
    for t in bstack111111l1l_opy_:
      t.start()
    for t in bstack111111l1l_opy_:
      results.append(t.join())
    bstack1l1111lll_opy_ = {}
    for item in results:
      hub_url = item[bstack1ll1l11_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1ll1l11_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1l1111lll_opy_[hub_url] = latency
    bstack11l1l111l1_opy_ = min(bstack1l1111lll_opy_, key= lambda x: bstack1l1111lll_opy_[x])
    bstack1l11ll1lll_opy_ = bstack11l1l111l1_opy_
    logger.debug(bstack1ll1111l1_opy_.format(bstack11l1l111l1_opy_))
  except Exception as e:
    logger.debug(bstack1l11l11l1l_opy_.format(e))
from browserstack_sdk.bstack1l111llll1_opy_ import *
from browserstack_sdk.bstack1lllll1ll_opy_ import *
from browserstack_sdk.bstack11111ll1l_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack1ll1lllll_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack11111ll11_opy_, stage=STAGE.bstack1l11lll1l_opy_)
def bstack11l1ll111_opy_():
    global bstack1l11ll1lll_opy_
    try:
        bstack111l1ll1l_opy_ = bstack1llll1l1l_opy_()
        bstack1l11llllll_opy_(bstack111l1ll1l_opy_)
        hub_url = bstack111l1ll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack1ll1l11_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack1ll1l11_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack1ll1l11_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack1ll1l11_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1ll1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack1l11ll1lll_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1llll1l1l_opy_():
    global CONFIG
    bstack11lll11ll1_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack1ll1l11_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack1ll1l11_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack11lll11ll1_opy_, str):
        raise ValueError(bstack1ll1l11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack111l1ll1l_opy_ = bstack1lllll11_opy_(bstack11lll11ll1_opy_)
        return bstack111l1ll1l_opy_
    except Exception as e:
        logger.error(bstack1ll1l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack1lllll11_opy_(bstack11lll11ll1_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1ll1l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack1ll1l11_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack111lll1ll_opy_ + bstack11lll11ll1_opy_
        auth = (CONFIG[bstack1ll1l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1ll111lll_opy_ = json.loads(response.text)
            return bstack1ll111lll_opy_
    except ValueError as ve:
        logger.error(bstack1ll1l11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1ll1l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1l11llllll_opy_(bstack11ll1ll111_opy_):
    global CONFIG
    if bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack1ll1l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack1ll1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack1ll1l11_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack11ll1ll111_opy_:
        bstack11l11l1lll_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack1ll1l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack11l11l1lll_opy_)
        bstack1l11l1ll11_opy_ = bstack11ll1ll111_opy_.get(bstack1ll1l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack1l1l11ll1_opy_ = bstack1ll1l11_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack1l11l1ll11_opy_)
        logger.debug(bstack1ll1l11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack1l1l11ll1_opy_)
        bstack1lll11l111_opy_ = {
            bstack1ll1l11_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack1ll1l11_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack1ll1l11_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack1ll1l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack1ll1l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack1l1l11ll1_opy_
        }
        bstack11l11l1lll_opy_.update(bstack1lll11l111_opy_)
        logger.debug(bstack1ll1l11_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack11l11l1lll_opy_)
        CONFIG[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack11l11l1lll_opy_
        logger.debug(bstack1ll1l11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack1l1111lll1_opy_():
    bstack111l1ll1l_opy_ = bstack1llll1l1l_opy_()
    if not bstack111l1ll1l_opy_[bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack1ll1l11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack111l1ll1l_opy_[bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack1ll1l11_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack1ll111ll_opy_, stage=STAGE.bstack1l11lll1l_opy_)
def bstack1ll111l1_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1ll1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack111lll11_opy_
        logger.debug(bstack1ll1l11_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1ll1l11_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack1ll1l11_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack1llll1l1l1_opy_ = json.loads(response.text)
                bstack1lllll1ll1_opy_ = bstack1llll1l1l1_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack1lllll1ll1_opy_:
                    bstack11llll11l_opy_ = bstack1lllll1ll1_opy_[0]
                    build_hashed_id = bstack11llll11l_opy_.get(bstack1ll1l11_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack1lll111ll_opy_ = bstack1l11lll11_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1lll111ll_opy_])
                    logger.info(bstack11ll11l1l1_opy_.format(bstack1lll111ll_opy_))
                    bstack1l1l1l1111_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack1l1l1l1111_opy_ += bstack1ll1l11_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack1l1l1l1111_opy_ != bstack11llll11l_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack11llll11l1_opy_.format(bstack11llll11l_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack1l1l1l1111_opy_))
                    return result
                else:
                    logger.debug(bstack1ll1l11_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack1ll1l11_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack1ll1l11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack1ll1l11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11ll11111l_opy_ import bstack11ll11111l_opy_, bstack11lll1l1l1_opy_, bstack111lll1l1_opy_, bstack1l1ll1l1ll_opy_
from bstack_utils.measure import bstack1ll11l1lll_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1lll1l1ll_opy_ import bstack1ll111111_opy_
from bstack_utils.messages import *
from bstack_utils import bstack1ll1lllll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1lll11llll_opy_, bstack11lllll1ll_opy_, bstack1ll1l11l11_opy_, bstack11ll111l1_opy_, \
  bstack1l1l1lll1_opy_, \
  Notset, bstack1ll1ll1ll_opy_, \
  bstack111l1ll1_opy_, bstack1lll111l_opy_, bstack1l1l1l11l_opy_, bstack1l1l11l1ll_opy_, bstack1l1l1ll1l_opy_, bstack1l1ll11lll_opy_, \
  bstack11l11lll1l_opy_, \
  bstack1l1l11l1_opy_, bstack1llll1l1_opy_, bstack1111l11l_opy_, bstack11lll111l_opy_, \
  bstack1l111lll_opy_, bstack1111111l1_opy_, bstack11l1llllll_opy_, bstack1ll1111ll1_opy_
from bstack_utils.bstack1ll111l111_opy_ import bstack1l1lll111l_opy_, bstack1l1l1l1l1_opy_
from bstack_utils.bstack1l11lll1l1_opy_ import bstack1l1l1ll11_opy_
from bstack_utils.bstack11111l11_opy_ import bstack11lll1l11_opy_, bstack11llllll1_opy_
from bstack_utils.bstack1l11l111_opy_ import bstack1l11l111_opy_
from bstack_utils.bstack1ll11l1l_opy_ import bstack1llllllll1_opy_
from bstack_utils.proxy import bstack1llll1l11l_opy_, bstack1ll1l1111_opy_, bstack11l11ll11_opy_, bstack1ll11l1ll_opy_
from bstack_utils.bstack1l1l1lll_opy_ import bstack1l1lll1l1l_opy_
import bstack_utils.bstack11l1l11l1l_opy_ as bstack11l11l1ll1_opy_
import bstack_utils.bstack11ll1lll_opy_ as bstack111llllll_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1l1111l1l1_opy_ import bstack11l1ll11l_opy_
if os.getenv(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡌࡔࡕࡋࡔࠩࢹ")):
  cli.bstack11l11ll1ll_opy_()
else:
  os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪࢺ")] = bstack1ll1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢻ")
bstack1lll1111l1_opy_ = bstack1ll1l11_opy_ (u"ࠪࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠣࠤ࡮࡬ࠨࡱࡣࡪࡩࠥࡃ࠽࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠣࡿࡡࡴࠠࠡࠢࡷࡶࡾࢁ࡜࡯ࠢࡦࡳࡳࡹࡴࠡࡨࡶࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨ࡝ࠩࡩࡷࡡ࠭ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࡨࡶ࠲ࡦࡶࡰࡦࡰࡧࡊ࡮ࡲࡥࡔࡻࡱࡧ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪ࠯ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡶ࡟ࡪࡰࡧࡩࡽ࠯ࠠࠬࠢࠥ࠾ࠧࠦࠫࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࠨࡢࡹࡤ࡭ࡹࠦ࡮ࡦࡹࡓࡥ࡬࡫࠲࠯ࡧࡹࡥࡱࡻࡡࡵࡧࠫࠦ࠭࠯ࠠ࠾ࡀࠣࡿࢂࠨࠬࠡ࡞ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢࡾ࡞ࠪ࠭࠮࠯࡛ࠣࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠦࡢ࠯ࠠࠬࠢࠥ࠰ࡡࡢ࡮ࠣࠫ࡟ࡲࠥࠦࠠࠡࡿࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࢀࡠࡳࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠪࢼ")
bstack1lll11ll11_opy_ = bstack1ll1l11_opy_ (u"ࠫࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࡜࡯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸࠯࡜࡯ࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼࡞ࡱ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࡷࡶࡾࠦࡻ࡝ࡰࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡡࡴࠠࠡࡿࠣࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠪࢽ")
from ._version import __version__
bstack1ll1ll1l_opy_ = None
CONFIG = {}
bstack11l1l1lll_opy_ = {}
bstack1l11l1l11l_opy_ = {}
bstack1lllllll1l_opy_ = None
bstack11l1ll1ll1_opy_ = None
bstack11l111111_opy_ = None
bstack1ll1ll11l_opy_ = -1
bstack1l11lllll1_opy_ = 0
bstack111l1lll_opy_ = bstack1l1llll1_opy_
bstack1ll111l11_opy_ = 1
bstack1l1l11l1l1_opy_ = False
bstack11ll11l1ll_opy_ = False
bstack1l111111ll_opy_ = bstack1ll1l11_opy_ (u"ࠬ࠭ࢾ")
bstack11l1111ll_opy_ = bstack1ll1l11_opy_ (u"࠭ࠧࢿ")
bstack11l1llll1l_opy_ = False
bstack1lll111ll1_opy_ = True
bstack1lllll11l_opy_ = bstack1ll1l11_opy_ (u"ࠧࠨࣀ")
bstack1lll11111_opy_ = []
bstack1l11ll1lll_opy_ = bstack1ll1l11_opy_ (u"ࠨࠩࣁ")
bstack1l1ll1lll_opy_ = False
bstack1llll1lll_opy_ = None
bstack11l1l11111_opy_ = None
bstack1l1l1l11l1_opy_ = None
bstack11lll11l1_opy_ = -1
bstack1ll1111l1l_opy_ = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠩࢁࠫࣂ")), bstack1ll1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪࣃ"), bstack1ll1l11_opy_ (u"ࠫ࠳ࡸ࡯ࡣࡱࡷ࠱ࡷ࡫ࡰࡰࡴࡷ࠱࡭࡫࡬ࡱࡧࡵ࠲࡯ࡹ࡯࡯ࠩࣄ"))
bstack11lllll11l_opy_ = 0
bstack11l111l1l_opy_ = 0
bstack1ll111ll11_opy_ = []
bstack1lll1111_opy_ = []
bstack1l11111lll_opy_ = []
bstack1l1lllllll_opy_ = []
bstack111ll1ll1_opy_ = bstack1ll1l11_opy_ (u"ࠬ࠭ࣅ")
bstack11l1l11lll_opy_ = bstack1ll1l11_opy_ (u"࠭ࠧࣆ")
bstack11l11ll111_opy_ = False
bstack11llllllll_opy_ = False
bstack11ll11ll11_opy_ = {}
bstack111llll1l_opy_ = None
bstack1l1lll11ll_opy_ = None
bstack1l1111ll1_opy_ = None
bstack11ll111lll_opy_ = None
bstack1ll1l1ll1l_opy_ = None
bstack11ll1ll11_opy_ = None
bstack1111ll1ll_opy_ = None
bstack1lllllll1_opy_ = None
bstack1llll1llll_opy_ = None
bstack1ll1l1l1ll_opy_ = None
bstack1l111lll1l_opy_ = None
bstack1l111l1l1l_opy_ = None
bstack11l111lll_opy_ = None
bstack1ll1l11l1_opy_ = None
bstack11l11ll1_opy_ = None
bstack11ll11l1_opy_ = None
bstack1l11ll111_opy_ = None
bstack11ll111ll1_opy_ = None
bstack1l11l1l1l_opy_ = None
bstack1ll1ll111_opy_ = None
bstack1l1l1lll11_opy_ = None
bstack1l111llll_opy_ = None
bstack11llll1lll_opy_ = None
thread_local = threading.local()
bstack1l1ll111l_opy_ = False
bstack1llll111l_opy_ = bstack1ll1l11_opy_ (u"ࠢࠣࣇ")
logger = bstack1ll1lllll_opy_.get_logger(__name__, bstack111l1lll_opy_)
bstack11lll1111_opy_ = Config.bstack11111l1l1_opy_()
percy = bstack111l111l_opy_()
bstack111ll1l1l_opy_ = bstack1ll111111_opy_()
bstack11l1ll1l11_opy_ = bstack11111ll1l_opy_()
def bstack1ll1l11ll1_opy_():
  global CONFIG
  global bstack11l11ll111_opy_
  global bstack11lll1111_opy_
  bstack11llllll1l_opy_ = bstack1lllll1l1_opy_(CONFIG)
  if bstack1l1l1lll1_opy_(CONFIG):
    if (bstack1ll1l11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࣈ") in bstack11llllll1l_opy_ and str(bstack11llllll1l_opy_[bstack1ll1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫࣉ")]).lower() == bstack1ll1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊")):
      bstack11l11ll111_opy_ = True
    bstack11lll1111_opy_.bstack1llll111l1_opy_(bstack11llllll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࣋"), False))
  else:
    bstack11l11ll111_opy_ = True
    bstack11lll1111_opy_.bstack1llll111l1_opy_(True)
def bstack11ll1111_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1llll11ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11111ll1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1ll1l11_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࣌") == args[i].lower() or bstack1ll1l11_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࣍") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1lllll11l_opy_
      bstack1lllll11l_opy_ += bstack1ll1l11_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࣎") + path
      return path
  return None
bstack1111lll1_opy_ = re.compile(bstack1ll1l11_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂ࣏ࠦ"))
def bstack1ll11ll11l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1111lll1_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1ll1l11_opy_ (u"ࠤࠧࡿ࣐ࠧ") + group + bstack1ll1l11_opy_ (u"ࠥࢁ࣑ࠧ"), os.environ.get(group))
  return value
def bstack1ll1ll1l1l_opy_():
  global bstack11llll1lll_opy_
  if bstack11llll1lll_opy_ is None:
        bstack11llll1lll_opy_ = bstack11111ll1_opy_()
  bstack1l1ll11111_opy_ = bstack11llll1lll_opy_
  if bstack1l1ll11111_opy_ and os.path.exists(os.path.abspath(bstack1l1ll11111_opy_)):
    fileName = bstack1l1ll11111_opy_
  if bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࣓ࠩ")])) and not bstack1ll1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨࣔ") in locals():
    fileName = os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫࣕ")]
  if bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪࣖ") in locals():
    bstack11l1ll1_opy_ = os.path.abspath(fileName)
  else:
    bstack11l1ll1_opy_ = bstack1ll1l11_opy_ (u"ࠩࠪࣗ")
  bstack11lll1l1l_opy_ = os.getcwd()
  bstack11ll1l11ll_opy_ = bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࣘ")
  bstack111111lll_opy_ = bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࣙ")
  while (not os.path.exists(bstack11l1ll1_opy_)) and bstack11lll1l1l_opy_ != bstack1ll1l11_opy_ (u"ࠧࠨࣚ"):
    bstack11l1ll1_opy_ = os.path.join(bstack11lll1l1l_opy_, bstack11ll1l11ll_opy_)
    if not os.path.exists(bstack11l1ll1_opy_):
      bstack11l1ll1_opy_ = os.path.join(bstack11lll1l1l_opy_, bstack111111lll_opy_)
    if bstack11lll1l1l_opy_ != os.path.dirname(bstack11lll1l1l_opy_):
      bstack11lll1l1l_opy_ = os.path.dirname(bstack11lll1l1l_opy_)
    else:
      bstack11lll1l1l_opy_ = bstack1ll1l11_opy_ (u"ࠨࠢࣛ")
  bstack11llll1lll_opy_ = bstack11l1ll1_opy_ if os.path.exists(bstack11l1ll1_opy_) else None
  return bstack11llll1lll_opy_
def bstack1lll111l1_opy_():
  bstack11l1ll1_opy_ = bstack1ll1ll1l1l_opy_()
  if not os.path.exists(bstack11l1ll1_opy_):
    bstack1ll1ll1lll_opy_(
      bstack1l1llll11_opy_.format(os.getcwd()))
  try:
    with open(bstack11l1ll1_opy_, bstack1ll1l11_opy_ (u"ࠧࡳࠩࣜ")) as stream:
      yaml.add_implicit_resolver(bstack1ll1l11_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࣝ"), bstack1111lll1_opy_)
      yaml.add_constructor(bstack1ll1l11_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࣞ"), bstack1ll11ll11l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack11l1ll1_opy_, bstack1ll1l11_opy_ (u"ࠪࡶࠬࣟ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1ll1ll1lll_opy_(bstack1lll11l11_opy_.format(str(exc)))
def bstack1lllll1l1l_opy_(config):
  bstack1l11ll11l_opy_ = bstack111lll11l_opy_(config)
  for option in list(bstack1l11ll11l_opy_):
    if option.lower() in bstack1lll1ll11_opy_ and option != bstack1lll1ll11_opy_[option.lower()]:
      bstack1l11ll11l_opy_[bstack1lll1ll11_opy_[option.lower()]] = bstack1l11ll11l_opy_[option]
      del bstack1l11ll11l_opy_[option]
  return config
def bstack1lll1llll_opy_():
  global bstack1l11l1l11l_opy_
  for key, bstack11llll1l1l_opy_ in bstack1l11ll11ll_opy_.items():
    if isinstance(bstack11llll1l1l_opy_, list):
      for var in bstack11llll1l1l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1l11l1l11l_opy_[key] = os.environ[var]
          break
    elif bstack11llll1l1l_opy_ in os.environ and os.environ[bstack11llll1l1l_opy_] and str(os.environ[bstack11llll1l1l_opy_]).strip():
      bstack1l11l1l11l_opy_[key] = os.environ[bstack11llll1l1l_opy_]
  if bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭࣠") in os.environ:
    bstack1l11l1l11l_opy_[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ࣡")] = {}
    bstack1l11l1l11l_opy_[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ࣢")][bstack1ll1l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")] = os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࣤ")]
def bstack11l11l111_opy_():
  global bstack11l1l1lll_opy_
  global bstack1lllll11l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1ll1l11_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣥ").lower() == val.lower():
      bstack11l1l1lll_opy_[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࣦࠧ")] = {}
      bstack11l1l1lll_opy_[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣧ")][bstack1ll1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣨ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11ll11lll_opy_ in bstack1l1ll1l1l1_opy_.items():
    if isinstance(bstack11ll11lll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11ll11lll_opy_:
          if idx < len(sys.argv) and bstack1ll1l11_opy_ (u"࠭࠭࠮ࣩࠩ") + var.lower() == val.lower() and not key in bstack11l1l1lll_opy_:
            bstack11l1l1lll_opy_[key] = sys.argv[idx + 1]
            bstack1lllll11l_opy_ += bstack1ll1l11_opy_ (u"ࠧࠡ࠯࠰ࠫ࣪") + var + bstack1ll1l11_opy_ (u"ࠨࠢࠪ࣫") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1ll1l11_opy_ (u"ࠩ࠰࠱ࠬ࣬") + bstack11ll11lll_opy_.lower() == val.lower() and not key in bstack11l1l1lll_opy_:
          bstack11l1l1lll_opy_[key] = sys.argv[idx + 1]
          bstack1lllll11l_opy_ += bstack1ll1l11_opy_ (u"ࠪࠤ࠲࠳࣭ࠧ") + bstack11ll11lll_opy_ + bstack1ll1l11_opy_ (u"࣮ࠫࠥ࠭") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1111l1l11_opy_(config):
  bstack1l1ll11l1_opy_ = config.keys()
  for bstack111111l11_opy_, bstack1llll11lll_opy_ in bstack1ll1llll1l_opy_.items():
    if bstack1llll11lll_opy_ in bstack1l1ll11l1_opy_:
      config[bstack111111l11_opy_] = config[bstack1llll11lll_opy_]
      del config[bstack1llll11lll_opy_]
  for bstack111111l11_opy_, bstack1llll11lll_opy_ in bstack1111llll_opy_.items():
    if isinstance(bstack1llll11lll_opy_, list):
      for bstack1l1ll11l1l_opy_ in bstack1llll11lll_opy_:
        if bstack1l1ll11l1l_opy_ in bstack1l1ll11l1_opy_:
          config[bstack111111l11_opy_] = config[bstack1l1ll11l1l_opy_]
          del config[bstack1l1ll11l1l_opy_]
          break
    elif bstack1llll11lll_opy_ in bstack1l1ll11l1_opy_:
      config[bstack111111l11_opy_] = config[bstack1llll11lll_opy_]
      del config[bstack1llll11lll_opy_]
  for bstack1l1ll11l1l_opy_ in list(config):
    for bstack1ll11l11l_opy_ in bstack11l1lllll_opy_:
      if bstack1l1ll11l1l_opy_.lower() == bstack1ll11l11l_opy_.lower() and bstack1l1ll11l1l_opy_ != bstack1ll11l11l_opy_:
        config[bstack1ll11l11l_opy_] = config[bstack1l1ll11l1l_opy_]
        del config[bstack1l1ll11l1l_opy_]
  bstack1lll1l11_opy_ = [{}]
  if not config.get(bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")):
    config[bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ")] = [{}]
  bstack1lll1l11_opy_ = config[bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")]
  for platform in bstack1lll1l11_opy_:
    for bstack1l1ll11l1l_opy_ in list(platform):
      for bstack1ll11l11l_opy_ in bstack11l1lllll_opy_:
        if bstack1l1ll11l1l_opy_.lower() == bstack1ll11l11l_opy_.lower() and bstack1l1ll11l1l_opy_ != bstack1ll11l11l_opy_:
          platform[bstack1ll11l11l_opy_] = platform[bstack1l1ll11l1l_opy_]
          del platform[bstack1l1ll11l1l_opy_]
  for bstack111111l11_opy_, bstack1llll11lll_opy_ in bstack1111llll_opy_.items():
    for platform in bstack1lll1l11_opy_:
      if isinstance(bstack1llll11lll_opy_, list):
        for bstack1l1ll11l1l_opy_ in bstack1llll11lll_opy_:
          if bstack1l1ll11l1l_opy_ in platform:
            platform[bstack111111l11_opy_] = platform[bstack1l1ll11l1l_opy_]
            del platform[bstack1l1ll11l1l_opy_]
            break
      elif bstack1llll11lll_opy_ in platform:
        platform[bstack111111l11_opy_] = platform[bstack1llll11lll_opy_]
        del platform[bstack1llll11lll_opy_]
  for bstack1lll1lll_opy_ in bstack1ll1lll11_opy_:
    if bstack1lll1lll_opy_ in config:
      if not bstack1ll1lll11_opy_[bstack1lll1lll_opy_] in config:
        config[bstack1ll1lll11_opy_[bstack1lll1lll_opy_]] = {}
      config[bstack1ll1lll11_opy_[bstack1lll1lll_opy_]].update(config[bstack1lll1lll_opy_])
      del config[bstack1lll1lll_opy_]
  for platform in bstack1lll1l11_opy_:
    for bstack1lll1lll_opy_ in bstack1ll1lll11_opy_:
      if bstack1lll1lll_opy_ in list(platform):
        if not bstack1ll1lll11_opy_[bstack1lll1lll_opy_] in platform:
          platform[bstack1ll1lll11_opy_[bstack1lll1lll_opy_]] = {}
        platform[bstack1ll1lll11_opy_[bstack1lll1lll_opy_]].update(platform[bstack1lll1lll_opy_])
        del platform[bstack1lll1lll_opy_]
  config = bstack1lllll1l1l_opy_(config)
  return config
def bstack111111ll_opy_(config):
  global bstack11l1111ll_opy_
  bstack1111l1ll_opy_ = False
  if bstack1ll1l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࣲࠬ") in config and str(config[bstack1ll1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ࣳ")]).lower() != bstack1ll1l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣴ"):
    if bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࣵ") not in config or str(config[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࣶࠩ")]).lower() == bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣷ"):
      config[bstack1ll1l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ࣸ")] = False
    else:
      bstack111l1ll1l_opy_ = bstack1llll1l1l_opy_()
      if bstack1ll1l11_opy_ (u"ࠨ࡫ࡶࡘࡷ࡯ࡡ࡭ࡉࡵ࡭ࡩࣹ࠭") in bstack111l1ll1l_opy_:
        if not bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸࣺ࠭") in config:
          config[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣻ")] = {}
        config[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")][bstack1ll1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣽ")] = bstack1ll1l11_opy_ (u"࠭ࡡࡵࡵ࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠬࣾ")
        bstack1111l1ll_opy_ = True
        bstack11l1111ll_opy_ = config[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࣿ")].get(bstack1ll1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऀ"))
  if bstack1l1l1lll1_opy_(config) and bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ँ") in config and str(config[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं")]).lower() != bstack1ll1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪः") and not bstack1111l1ll_opy_:
    if not bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
      config[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
    if not config[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")].get(bstack1ll1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠬइ")) and not bstack1ll1l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫई") in config[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")]:
      bstack1lllllll11_opy_ = datetime.datetime.now()
      bstack1ll11l1111_opy_ = bstack1lllllll11_opy_.strftime(bstack1ll1l11_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨऊ"))
      hostname = socket.gethostname()
      bstack1ll1l1llll_opy_ = bstack1ll1l11_opy_ (u"ࠬ࠭ऋ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1ll1l11_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨऌ").format(bstack1ll11l1111_opy_, hostname, bstack1ll1l1llll_opy_)
      config[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫऍ")][bstack1ll1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऎ")] = identifier
    bstack11l1111ll_opy_ = config[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")].get(bstack1ll1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऐ"))
  return config
def bstack11lll11ll_opy_():
  bstack1l11111l11_opy_ =  bstack1l1l11l1ll_opy_()[bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠪऑ")]
  return bstack1l11111l11_opy_ if bstack1l11111l11_opy_ else -1
def bstack1lll111lll_opy_(bstack1l11111l11_opy_):
  global CONFIG
  if not bstack1ll1l11_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧऒ") in CONFIG[bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨओ")]:
    return
  CONFIG[bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ")] = CONFIG[bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")].replace(
    bstack1ll1l11_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫख"),
    str(bstack1l11111l11_opy_)
  )
def bstack1l1ll111_opy_():
  global CONFIG
  if not bstack1ll1l11_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩग") in CONFIG[bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")]:
    return
  bstack1lllllll11_opy_ = datetime.datetime.now()
  bstack1ll11l1111_opy_ = bstack1lllllll11_opy_.strftime(bstack1ll1l11_opy_ (u"ࠬࠫࡤ࠮ࠧࡥ࠱ࠪࡎ࠺ࠦࡏࠪङ"))
  CONFIG[bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = CONFIG[bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")].replace(
    bstack1ll1l11_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧज"),
    bstack1ll11l1111_opy_
  )
def bstack11lll11l_opy_():
  global CONFIG
  if bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ") in CONFIG and not bool(CONFIG[bstack1ll1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")]):
    del CONFIG[bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]
    return
  if not bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ") in CONFIG:
    CONFIG[bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")] = bstack1ll1l11_opy_ (u"ࠧࠤࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪढ")
  if bstack1ll1l11_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧण") in CONFIG[bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")]:
    bstack1l1ll111_opy_()
    os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧथ")] = CONFIG[bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")]
  if not bstack1ll1l11_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧध") in CONFIG[bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]:
    return
  bstack1l11111l11_opy_ = bstack1ll1l11_opy_ (u"ࠧࠨऩ")
  bstack111l11111_opy_ = bstack11lll11ll_opy_()
  if bstack111l11111_opy_ != -1:
    bstack1l11111l11_opy_ = bstack1ll1l11_opy_ (u"ࠨࡅࡌࠤࠬप") + str(bstack111l11111_opy_)
  if bstack1l11111l11_opy_ == bstack1ll1l11_opy_ (u"ࠩࠪफ"):
    bstack1ll111l1l1_opy_ = bstack11ll1l1l11_opy_(CONFIG[bstack1ll1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ब")])
    if bstack1ll111l1l1_opy_ != -1:
      bstack1l11111l11_opy_ = str(bstack1ll111l1l1_opy_)
  if bstack1l11111l11_opy_:
    bstack1lll111lll_opy_(bstack1l11111l11_opy_)
    os.environ[bstack1ll1l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨभ")] = CONFIG[bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]
def bstack1l1l111l1_opy_(bstack1l111ll1ll_opy_, bstack1l1ll1ll1_opy_, path):
  bstack1llllll1l_opy_ = {
    bstack1ll1l11_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪय"): bstack1l1ll1ll1_opy_
  }
  if os.path.exists(path):
    bstack11l1ll11_opy_ = json.load(open(path, bstack1ll1l11_opy_ (u"ࠧࡳࡤࠪर")))
  else:
    bstack11l1ll11_opy_ = {}
  bstack11l1ll11_opy_[bstack1l111ll1ll_opy_] = bstack1llllll1l_opy_
  with open(path, bstack1ll1l11_opy_ (u"ࠣࡹ࠮ࠦऱ")) as outfile:
    json.dump(bstack11l1ll11_opy_, outfile)
def bstack11ll1l1l11_opy_(bstack1l111ll1ll_opy_):
  bstack1l111ll1ll_opy_ = str(bstack1l111ll1ll_opy_)
  bstack11l11lll11_opy_ = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠩࢁࠫल")), bstack1ll1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪळ"))
  try:
    if not os.path.exists(bstack11l11lll11_opy_):
      os.makedirs(bstack11l11lll11_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠫࢃ࠭ऴ")), bstack1ll1l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬव"), bstack1ll1l11_opy_ (u"࠭࠮ࡣࡷ࡬ࡰࡩ࠳࡮ࡢ࡯ࡨ࠱ࡨࡧࡣࡩࡧ࠱࡮ࡸࡵ࡮ࠨश"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1ll1l11_opy_ (u"ࠧࡸࠩष")):
        pass
      with open(file_path, bstack1ll1l11_opy_ (u"ࠣࡹ࠮ࠦस")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1ll1l11_opy_ (u"ࠩࡵࠫह")) as bstack11ll1ll1_opy_:
      bstack11l1ll1l1_opy_ = json.load(bstack11ll1ll1_opy_)
    if bstack1l111ll1ll_opy_ in bstack11l1ll1l1_opy_:
      bstack1l1lll1l11_opy_ = bstack11l1ll1l1_opy_[bstack1l111ll1ll_opy_][bstack1ll1l11_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऺ")]
      bstack1l1l1111ll_opy_ = int(bstack1l1lll1l11_opy_) + 1
      bstack1l1l111l1_opy_(bstack1l111ll1ll_opy_, bstack1l1l1111ll_opy_, file_path)
      return bstack1l1l1111ll_opy_
    else:
      bstack1l1l111l1_opy_(bstack1l111ll1ll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1ll1llll_opy_.format(str(e)))
    return -1
def bstack11lll1l111_opy_(config):
  if not config[bstack1ll1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ऻ")] or not config[bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ़")]:
    return True
  else:
    return False
def bstack11l1ll11ll_opy_(config, index=0):
  global bstack11l1llll1l_opy_
  bstack1l11llll11_opy_ = {}
  caps = bstack11ll1lllll_opy_ + bstack11111l1l_opy_
  if config.get(bstack1ll1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪऽ"), False):
    bstack1l11llll11_opy_[bstack1ll1l11_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫा")] = True
    bstack1l11llll11_opy_[bstack1ll1l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬि")] = config.get(bstack1ll1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ी"), {})
  if bstack11l1llll1l_opy_:
    caps += bstack1l11111111_opy_
  for key in config:
    if key in caps + [bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ु")]:
      continue
    bstack1l11llll11_opy_[key] = config[key]
  if bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧू") in config:
    for bstack1lll1l1l11_opy_ in config[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨृ")][index]:
      if bstack1lll1l1l11_opy_ in caps:
        continue
      bstack1l11llll11_opy_[bstack1lll1l1l11_opy_] = config[bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॄ")][index][bstack1lll1l1l11_opy_]
  bstack1l11llll11_opy_[bstack1ll1l11_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩॅ")] = socket.gethostname()
  if bstack1ll1l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩॆ") in bstack1l11llll11_opy_:
    del (bstack1l11llll11_opy_[bstack1ll1l11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪे")])
  return bstack1l11llll11_opy_
def bstack1ll1ll1l11_opy_(config):
  global bstack11l1llll1l_opy_
  bstack1l11l11l1_opy_ = {}
  caps = bstack11111l1l_opy_
  if bstack11l1llll1l_opy_:
    caps += bstack1l11111111_opy_
  for key in caps:
    if key in config:
      bstack1l11l11l1_opy_[key] = config[key]
  return bstack1l11l11l1_opy_
def bstack11lll11l1l_opy_(bstack1l11llll11_opy_, bstack1l11l11l1_opy_):
  bstack11l111ll1_opy_ = {}
  for key in bstack1l11llll11_opy_.keys():
    if key in bstack1ll1llll1l_opy_:
      bstack11l111ll1_opy_[bstack1ll1llll1l_opy_[key]] = bstack1l11llll11_opy_[key]
    else:
      bstack11l111ll1_opy_[key] = bstack1l11llll11_opy_[key]
  for key in bstack1l11l11l1_opy_:
    if key in bstack1ll1llll1l_opy_:
      bstack11l111ll1_opy_[bstack1ll1llll1l_opy_[key]] = bstack1l11l11l1_opy_[key]
    else:
      bstack11l111ll1_opy_[key] = bstack1l11l11l1_opy_[key]
  return bstack11l111ll1_opy_
def bstack1ll1l1ll_opy_(config, index=0):
  global bstack11l1llll1l_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1ll1l111ll_opy_ = bstack1lll11llll_opy_(bstack1l111l1lll_opy_, config, logger)
  bstack1l11l11l1_opy_ = bstack1ll1ll1l11_opy_(config)
  bstack1l11ll11_opy_ = bstack11111l1l_opy_
  bstack1l11ll11_opy_ += bstack1ll1ll1l1_opy_
  bstack1l11l11l1_opy_ = update(bstack1l11l11l1_opy_, bstack1ll1l111ll_opy_)
  if bstack11l1llll1l_opy_:
    bstack1l11ll11_opy_ += bstack1l11111111_opy_
  if bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ै") in config:
    if bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॉ") in config[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨॊ")][index]:
      caps[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")] = config[bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ")][index][bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ्࠭")]
    if bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॎ") in config[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॏ")][index]:
      caps[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬॐ")] = str(config[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ॑")][index][bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴ॒ࠧ")])
    bstack1lll1111ll_opy_ = bstack1lll11llll_opy_(bstack1l111l1lll_opy_, config[bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ॓")][index], logger)
    bstack1l11ll11_opy_ += list(bstack1lll1111ll_opy_.keys())
    for bstack1l11ll111l_opy_ in bstack1l11ll11_opy_:
      if bstack1l11ll111l_opy_ in config[bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
        if bstack1l11ll111l_opy_ == bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫॕ"):
          try:
            bstack1lll1111ll_opy_[bstack1l11ll111l_opy_] = str(config[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack1l11ll111l_opy_] * 1.0)
          except:
            bstack1lll1111ll_opy_[bstack1l11ll111l_opy_] = str(config[bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ")][index][bstack1l11ll111l_opy_])
        else:
          bstack1lll1111ll_opy_[bstack1l11ll111l_opy_] = config[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack1l11ll111l_opy_]
        del (config[bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index][bstack1l11ll111l_opy_])
    bstack1l11l11l1_opy_ = update(bstack1l11l11l1_opy_, bstack1lll1111ll_opy_)
  bstack1l11llll11_opy_ = bstack11l1ll11ll_opy_(config, index)
  for bstack1l1ll11l1l_opy_ in bstack11111l1l_opy_ + list(bstack1ll1l111ll_opy_.keys()):
    if bstack1l1ll11l1l_opy_ in bstack1l11llll11_opy_:
      bstack1l11l11l1_opy_[bstack1l1ll11l1l_opy_] = bstack1l11llll11_opy_[bstack1l1ll11l1l_opy_]
      del (bstack1l11llll11_opy_[bstack1l1ll11l1l_opy_])
  if bstack1ll1ll1ll_opy_(config):
    bstack1l11llll11_opy_[bstack1ll1l11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧग़")] = True
    caps.update(bstack1l11l11l1_opy_)
    caps[bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩज़")] = bstack1l11llll11_opy_
  else:
    bstack1l11llll11_opy_[bstack1ll1l11_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩड़")] = False
    caps.update(bstack11lll11l1l_opy_(bstack1l11llll11_opy_, bstack1l11l11l1_opy_))
    if bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़") in caps:
      caps[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬफ़")] = caps[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")]
      del (caps[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")])
    if bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॡ") in caps:
      caps[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪॢ")] = caps[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॣ")]
      del (caps[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ।")])
  return caps
def bstack11l1ll1111_opy_():
  global bstack1l11ll1lll_opy_
  global CONFIG
  if bstack1llll11ll_opy_() <= version.parse(bstack1ll1l11_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ॥")):
    if bstack1l11ll1lll_opy_ != bstack1ll1l11_opy_ (u"ࠬ࠭०"):
      return bstack1ll1l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ१") + bstack1l11ll1lll_opy_ + bstack1ll1l11_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ२")
    return bstack1111lllll_opy_
  if bstack1l11ll1lll_opy_ != bstack1ll1l11_opy_ (u"ࠨࠩ३"):
    return bstack1ll1l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ४") + bstack1l11ll1lll_opy_ + bstack1ll1l11_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ५")
  return bstack1lll11lll_opy_
def bstack111lllll_opy_(options):
  return hasattr(options, bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ६"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l1ll11ll1_opy_(options, bstack1l1111l11_opy_):
  for bstack1l1l1111l1_opy_ in bstack1l1111l11_opy_:
    if bstack1l1l1111l1_opy_ in [bstack1ll1l11_opy_ (u"ࠬࡧࡲࡨࡵࠪ७"), bstack1ll1l11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ८")]:
      continue
    if bstack1l1l1111l1_opy_ in options._experimental_options:
      options._experimental_options[bstack1l1l1111l1_opy_] = update(options._experimental_options[bstack1l1l1111l1_opy_],
                                                         bstack1l1111l11_opy_[bstack1l1l1111l1_opy_])
    else:
      options.add_experimental_option(bstack1l1l1111l1_opy_, bstack1l1111l11_opy_[bstack1l1l1111l1_opy_])
  if bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡷࠬ९") in bstack1l1111l11_opy_:
    for arg in bstack1l1111l11_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭॰")]:
      options.add_argument(arg)
    del (bstack1l1111l11_opy_[bstack1ll1l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॱ")])
  if bstack1ll1l11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧॲ") in bstack1l1111l11_opy_:
    for ext in bstack1l1111l11_opy_[bstack1ll1l11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॳ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1l1111l11_opy_[bstack1ll1l11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॴ")])
def bstack11l1l1l1_opy_(options, bstack1ll111l11l_opy_):
  if bstack1ll1l11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॵ") in bstack1ll111l11l_opy_:
    for bstack1lllll111_opy_ in bstack1ll111l11l_opy_[bstack1ll1l11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ॶ")]:
      if bstack1lllll111_opy_ in options._preferences:
        options._preferences[bstack1lllll111_opy_] = update(options._preferences[bstack1lllll111_opy_], bstack1ll111l11l_opy_[bstack1ll1l11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧॷ")][bstack1lllll111_opy_])
      else:
        options.set_preference(bstack1lllll111_opy_, bstack1ll111l11l_opy_[bstack1ll1l11_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॸ")][bstack1lllll111_opy_])
  if bstack1ll1l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॹ") in bstack1ll111l11l_opy_:
    for arg in bstack1ll111l11l_opy_[bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ")]:
      options.add_argument(arg)
def bstack1l11l1l111_opy_(options, bstack11l11l1l1_opy_):
  if bstack1ll1l11_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭ॻ") in bstack11l11l1l1_opy_:
    options.use_webview(bool(bstack11l11l1l1_opy_[bstack1ll1l11_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧॼ")]))
  bstack1l1ll11ll1_opy_(options, bstack11l11l1l1_opy_)
def bstack1111l1ll1_opy_(options, bstack1l1111llll_opy_):
  for bstack1ll1l1lll_opy_ in bstack1l1111llll_opy_:
    if bstack1ll1l1lll_opy_ in [bstack1ll1l11_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫॽ"), bstack1ll1l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ")]:
      continue
    options.set_capability(bstack1ll1l1lll_opy_, bstack1l1111llll_opy_[bstack1ll1l1lll_opy_])
  if bstack1ll1l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ") in bstack1l1111llll_opy_:
    for arg in bstack1l1111llll_opy_[bstack1ll1l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ")]:
      options.add_argument(arg)
  if bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨঁ") in bstack1l1111llll_opy_:
    options.bstack11ll1l1l1l_opy_(bool(bstack1l1111llll_opy_[bstack1ll1l11_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩং")]))
def bstack1l1l111lll_opy_(options, bstack11lll1llll_opy_):
  for bstack11l1l1ll11_opy_ in bstack11lll1llll_opy_:
    if bstack11l1l1ll11_opy_ in [bstack1ll1l11_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঃ"), bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡷࠬ঄")]:
      continue
    options._options[bstack11l1l1ll11_opy_] = bstack11lll1llll_opy_[bstack11l1l1ll11_opy_]
  if bstack1ll1l11_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬঅ") in bstack11lll1llll_opy_:
    for bstack1111ll1l_opy_ in bstack11lll1llll_opy_[bstack1ll1l11_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭আ")]:
      options.bstack1l1111ll11_opy_(
        bstack1111ll1l_opy_, bstack11lll1llll_opy_[bstack1ll1l11_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧই")][bstack1111ll1l_opy_])
  if bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩঈ") in bstack11lll1llll_opy_:
    for arg in bstack11lll1llll_opy_[bstack1ll1l11_opy_ (u"ࠬࡧࡲࡨࡵࠪউ")]:
      options.add_argument(arg)
def bstack1l11l11l_opy_(options, caps):
  if not hasattr(options, bstack1ll1l11_opy_ (u"࠭ࡋࡆ࡛ࠪঊ")):
    return
  if options.KEY == bstack1ll1l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঋ") and options.KEY in caps:
    bstack1l1ll11ll1_opy_(options, caps[bstack1ll1l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ঌ")])
  elif options.KEY == bstack1ll1l11_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ঍") and options.KEY in caps:
    bstack11l1l1l1_opy_(options, caps[bstack1ll1l11_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ঎")])
  elif options.KEY == bstack1ll1l11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬএ") and options.KEY in caps:
    bstack1111l1ll1_opy_(options, caps[bstack1ll1l11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ঐ")])
  elif options.KEY == bstack1ll1l11_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ঑") and options.KEY in caps:
    bstack1l11l1l111_opy_(options, caps[bstack1ll1l11_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ঒")])
  elif options.KEY == bstack1ll1l11_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧও") and options.KEY in caps:
    bstack1l1l111lll_opy_(options, caps[bstack1ll1l11_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨঔ")])
def bstack11l11111l_opy_(caps):
  global bstack11l1llll1l_opy_
  if isinstance(os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫক")), str):
    bstack11l1llll1l_opy_ = eval(os.getenv(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬখ")))
  if bstack11l1llll1l_opy_:
    if bstack11ll1111_opy_() < version.parse(bstack1ll1l11_opy_ (u"ࠬ࠸࠮࠴࠰࠳ࠫগ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1ll1l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ঘ")
    if bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬঙ") in caps:
      browser = caps[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭চ")]
    elif bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪছ") in caps:
      browser = caps[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫজ")]
    browser = str(browser).lower()
    if browser == bstack1ll1l11_opy_ (u"ࠫ࡮ࡶࡨࡰࡰࡨࠫঝ") or browser == bstack1ll1l11_opy_ (u"ࠬ࡯ࡰࡢࡦࠪঞ"):
      browser = bstack1ll1l11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ট")
    if browser == bstack1ll1l11_opy_ (u"ࠧࡴࡣࡰࡷࡺࡴࡧࠨঠ"):
      browser = bstack1ll1l11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨড")
    if browser not in [bstack1ll1l11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩঢ"), bstack1ll1l11_opy_ (u"ࠪࡩࡩ࡭ࡥࠨণ"), bstack1ll1l11_opy_ (u"ࠫ࡮࡫ࠧত"), bstack1ll1l11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬথ"), bstack1ll1l11_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧদ")]:
      return None
    try:
      package = bstack1ll1l11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࢁࡽ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩধ").format(browser)
      name = bstack1ll1l11_opy_ (u"ࠨࡑࡳࡸ࡮ࡵ࡮ࡴࠩন")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack111lllll_opy_(options):
        return None
      for bstack1l1ll11l1l_opy_ in caps.keys():
        options.set_capability(bstack1l1ll11l1l_opy_, caps[bstack1l1ll11l1l_opy_])
      bstack1l11l11l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11ll1l111l_opy_(options, bstack11ll1111ll_opy_):
  if not bstack111lllll_opy_(options):
    return
  for bstack1l1ll11l1l_opy_ in bstack11ll1111ll_opy_.keys():
    if bstack1l1ll11l1l_opy_ in bstack1ll1ll1l1_opy_:
      continue
    if bstack1l1ll11l1l_opy_ in options._caps and type(options._caps[bstack1l1ll11l1l_opy_]) in [dict, list]:
      options._caps[bstack1l1ll11l1l_opy_] = update(options._caps[bstack1l1ll11l1l_opy_], bstack11ll1111ll_opy_[bstack1l1ll11l1l_opy_])
    else:
      options.set_capability(bstack1l1ll11l1l_opy_, bstack11ll1111ll_opy_[bstack1l1ll11l1l_opy_])
  bstack1l11l11l_opy_(options, bstack11ll1111ll_opy_)
  if bstack1ll1l11_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨ঩") in options._caps:
    if options._caps[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨপ")] and options._caps[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩফ")].lower() != bstack1ll1l11_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ব"):
      del options._caps[bstack1ll1l11_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬভ")]
def bstack11l1l111_opy_(proxy_config):
  if bstack1ll1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫম") in proxy_config:
    proxy_config[bstack1ll1l11_opy_ (u"ࠨࡵࡶࡰࡕࡸ࡯ࡹࡻࠪয")] = proxy_config[bstack1ll1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭র")]
    del (proxy_config[bstack1ll1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ঱")])
  if bstack1ll1l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧল") in proxy_config and proxy_config[bstack1ll1l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ঳")].lower() != bstack1ll1l11_opy_ (u"࠭ࡤࡪࡴࡨࡧࡹ࠭঴"):
    proxy_config[bstack1ll1l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ঵")] = bstack1ll1l11_opy_ (u"ࠨ࡯ࡤࡲࡺࡧ࡬ࠨশ")
  if bstack1ll1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡂࡷࡷࡳࡨࡵ࡮ࡧ࡫ࡪ࡙ࡷࡲࠧষ") in proxy_config:
    proxy_config[bstack1ll1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭স")] = bstack1ll1l11_opy_ (u"ࠫࡵࡧࡣࠨহ")
  return proxy_config
def bstack1ll1l11l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1ll1l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ঺") in config:
    return proxy
  config[bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ঻")] = bstack11l1l111_opy_(config[bstack1ll1l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ়࠭")])
  if proxy == None:
    proxy = Proxy(config[bstack1ll1l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧঽ")])
  return proxy
def bstack1l1l1l1ll1_opy_(self):
  global CONFIG
  global bstack1l111l1l1l_opy_
  try:
    proxy = bstack11l11ll11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1ll1l11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧা")):
        proxies = bstack1llll1l11l_opy_(proxy, bstack11l1ll1111_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll11ll111_opy_ = proxies.popitem()
          if bstack1ll1l11_opy_ (u"ࠥ࠾࠴࠵ࠢি") in bstack1ll11ll111_opy_:
            return bstack1ll11ll111_opy_
          else:
            return bstack1ll1l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧী") + bstack1ll11ll111_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1ll1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤু").format(str(e)))
  return bstack1l111l1l1l_opy_(self)
def bstack11l1lll11l_opy_():
  global CONFIG
  return bstack1ll11l1ll_opy_(CONFIG) and bstack1l1ll11lll_opy_() and bstack1llll11ll_opy_() >= version.parse(bstack1l1llll11l_opy_)
def bstack1ll1l1lll1_opy_():
  global CONFIG
  return (bstack1ll1l11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩূ") in CONFIG or bstack1ll1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫৃ") in CONFIG) and bstack11l11lll1l_opy_()
def bstack111lll11l_opy_(config):
  bstack1l11ll11l_opy_ = {}
  if bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬৄ") in config:
    bstack1l11ll11l_opy_ = config[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৅")]
  if bstack1ll1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৆") in config:
    bstack1l11ll11l_opy_ = config[bstack1ll1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪে")]
  proxy = bstack11l11ll11_opy_(config)
  if proxy:
    if proxy.endswith(bstack1ll1l11_opy_ (u"ࠬ࠴ࡰࡢࡥࠪৈ")) and os.path.isfile(proxy):
      bstack1l11ll11l_opy_[bstack1ll1l11_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩ৉")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1ll1l11_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৊")):
        proxies = bstack1ll1l1111_opy_(config, bstack11l1ll1111_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll11ll111_opy_ = proxies.popitem()
          if bstack1ll1l11_opy_ (u"ࠣ࠼࠲࠳ࠧো") in bstack1ll11ll111_opy_:
            parsed_url = urlparse(bstack1ll11ll111_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1ll1l11_opy_ (u"ࠤ࠽࠳࠴ࠨৌ") + bstack1ll11ll111_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1l11ll11l_opy_[bstack1ll1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ্࠭")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1l11ll11l_opy_[bstack1ll1l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৎ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1l11ll11l_opy_[bstack1ll1l11_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ৏")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1l11ll11l_opy_[bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩ৐")] = str(parsed_url.password)
  return bstack1l11ll11l_opy_
def bstack1lllll1l1_opy_(config):
  if bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬ৑") in config:
    return config[bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭৒")]
  return {}
def bstack111l11lll_opy_(caps):
  global bstack11l1111ll_opy_
  if bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ৓") in caps:
    caps[bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৔")][bstack1ll1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪ৕")] = True
    if bstack11l1111ll_opy_:
      caps[bstack1ll1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭৖")][bstack1ll1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨৗ")] = bstack11l1111ll_opy_
  else:
    caps[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬ৘")] = True
    if bstack11l1111ll_opy_:
      caps[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ৙")] = bstack11l1111ll_opy_
@measure(event_name=EVENTS.bstack11l11l11_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1111llll1_opy_():
  global CONFIG
  if not bstack1l1l1lll1_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭৚") in CONFIG and bstack11l1llllll_opy_(CONFIG[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ৛")]):
    if (
      bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨড়") in CONFIG
      and bstack11l1llllll_opy_(CONFIG[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩঢ়")].get(bstack1ll1l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡆ࡮ࡴࡡࡳࡻࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡦࡺࡩࡰࡰࠪ৞")))
    ):
      logger.debug(bstack1ll1l11_opy_ (u"ࠢࡍࡱࡦࡥࡱࠦࡢࡪࡰࡤࡶࡾࠦ࡮ࡰࡶࠣࡷࡹࡧࡲࡵࡧࡧࠤࡦࡹࠠࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡦࡰࡤࡦࡱ࡫ࡤࠣয়"))
      return
    bstack1l11ll11l_opy_ = bstack111lll11l_opy_(CONFIG)
    bstack11lll1lll1_opy_(CONFIG[bstack1ll1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫৠ")], bstack1l11ll11l_opy_)
def bstack11lll1lll1_opy_(key, bstack1l11ll11l_opy_):
  global bstack1ll1ll1l_opy_
  logger.info(bstack11111lll1_opy_)
  try:
    bstack1ll1ll1l_opy_ = Local()
    bstack1l1ll1111_opy_ = {bstack1ll1l11_opy_ (u"ࠩ࡮ࡩࡾ࠭ৡ"): key}
    bstack1l1ll1111_opy_.update(bstack1l11ll11l_opy_)
    logger.debug(bstack1l1ll1l11_opy_.format(str(bstack1l1ll1111_opy_)).replace(key, bstack1ll1l11_opy_ (u"ࠪ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧৢ")))
    bstack1ll1ll1l_opy_.start(**bstack1l1ll1111_opy_)
    if bstack1ll1ll1l_opy_.isRunning():
      logger.info(bstack1l11111l_opy_)
  except Exception as e:
    bstack1ll1ll1lll_opy_(bstack1l1l111ll_opy_.format(str(e)))
def bstack1ll1lll11l_opy_():
  global bstack1ll1ll1l_opy_
  if bstack1ll1ll1l_opy_.isRunning():
    logger.info(bstack1ll111ll1_opy_)
    bstack1ll1ll1l_opy_.stop()
  bstack1ll1ll1l_opy_ = None
def bstack1l11ll1ll_opy_(bstack1lll1ll1ll_opy_=[]):
  global CONFIG
  bstack1l11111ll1_opy_ = []
  bstack1ll1111l11_opy_ = [bstack1ll1l11_opy_ (u"ࠫࡴࡹࠧৣ"), bstack1ll1l11_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ৤"), bstack1ll1l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ৥"), bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ০"), bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭১"), bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ২")]
  try:
    for err in bstack1lll1ll1ll_opy_:
      bstack11111l111_opy_ = {}
      for k in bstack1ll1111l11_opy_:
        val = CONFIG[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭৩")][int(err[bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ৪")])].get(k)
        if val:
          bstack11111l111_opy_[k] = val
      if(err[bstack1ll1l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ৫")] != bstack1ll1l11_opy_ (u"࠭ࠧ৬")):
        bstack11111l111_opy_[bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡸ࠭৭")] = {
          err[bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭৮")]: err[bstack1ll1l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ৯")]
        }
        bstack1l11111ll1_opy_.append(bstack11111l111_opy_)
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶ࠽ࠤࠬৰ") + str(e))
  finally:
    return bstack1l11111ll1_opy_
def bstack11111111l_opy_(file_name):
  bstack111l11ll_opy_ = []
  try:
    bstack11l1l111l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack11l1l111l_opy_):
      with open(bstack11l1l111l_opy_) as f:
        bstack11ll11ll1l_opy_ = json.load(f)
        bstack111l11ll_opy_ = bstack11ll11ll1l_opy_
      os.remove(bstack11l1l111l_opy_)
    return bstack111l11ll_opy_
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡰࡧ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦ࡬ࡪࡵࡷ࠾ࠥ࠭ৱ") + str(e))
    return bstack111l11ll_opy_
def bstack1lll1ll1_opy_():
  try:
      from bstack_utils.constants import bstack11l1l1l1l_opy_, EVENTS
      from bstack_utils.helper import bstack11lllll1ll_opy_, get_host_info, bstack11lll1111_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack1l111l111_opy_ = os.path.join(os.getcwd(), bstack1ll1l11_opy_ (u"ࠬࡲ࡯ࡨࠩ৲"), bstack1ll1l11_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩ৳"))
      lock = FileLock(bstack1l111l111_opy_+bstack1ll1l11_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨ৴"))
      def bstack11l1lll111_opy_():
          try:
              with lock:
                  with open(bstack1l111l111_opy_, bstack1ll1l11_opy_ (u"ࠣࡴࠥ৵"), encoding=bstack1ll1l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ৶")) as file:
                      data = json.load(file)
                      config = {
                          bstack1ll1l11_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶࠦ৷"): {
                              bstack1ll1l11_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥ৸"): bstack1ll1l11_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣ৹"),
                          }
                      }
                      bstack1lll1l111l_opy_ = datetime.utcnow()
                      bstack1lllllll11_opy_ = bstack1lll1l111l_opy_.strftime(bstack1ll1l11_opy_ (u"ࠨ࡚ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࠱ࠩ࡫ࠦࡕࡕࡅࠥ৺"))
                      bstack1l1llll111_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ৻")) if os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ৼ")) else bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠤࡶࡨࡰࡘࡵ࡯ࡋࡧࠦ৽"))
                      payload = {
                          bstack1ll1l11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠢ৾"): bstack1ll1l11_opy_ (u"ࠦࡸࡪ࡫ࡠࡧࡹࡩࡳࡺࡳࠣ৿"),
                          bstack1ll1l11_opy_ (u"ࠧࡪࡡࡵࡣࠥ਀"): {
                              bstack1ll1l11_opy_ (u"ࠨࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡶࡷ࡬ࡨࠧਁ"): bstack1l1llll111_opy_,
                              bstack1ll1l11_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࡠࡦࡤࡽࠧਂ"): bstack1lllllll11_opy_,
                              bstack1ll1l11_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࠧਃ"): bstack1ll1l11_opy_ (u"ࠤࡖࡈࡐࡌࡥࡢࡶࡸࡶࡪࡖࡥࡳࡨࡲࡶࡲࡧ࡮ࡤࡧࠥ਄"),
                              bstack1ll1l11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡ࡭ࡷࡴࡴࠢਅ"): {
                                  bstack1ll1l11_opy_ (u"ࠦࡲ࡫ࡡࡴࡷࡵࡩࡸࠨਆ"): data,
                                  bstack1ll1l11_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢਇ"): bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣਈ"))
                              },
                              bstack1ll1l11_opy_ (u"ࠢࡶࡵࡨࡶࡤࡪࡡࡵࡣࠥਉ"): bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠣࡷࡶࡩࡷࡔࡡ࡮ࡧࠥਊ")),
                              bstack1ll1l11_opy_ (u"ࠤ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠧ਋"): get_host_info()
                          }
                      }
                      response = bstack11lllll1ll_opy_(bstack1ll1l11_opy_ (u"ࠥࡔࡔ࡙ࡔࠣ਌"), bstack11l1l1l1l_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack1ll1l11_opy_ (u"ࠦࡉࡧࡴࡢࠢࡶࡩࡳࡺࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡴࡰࠢࡾࢁࠥࡽࡩࡵࡪࠣࡨࡦࡺࡡࠡࡽࢀࠦ਍").format(bstack11l1l1l1l_opy_, payload))
                      else:
                          logger.debug(bstack1ll1l11_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡦࡰࡴࠣࡿࢂࠦࡷࡪࡶ࡫ࠤࡩࡧࡴࡢࠢࡾࢁࠧ਎").format(bstack11l1l1l1l_opy_, payload))
          except Exception as e:
              logger.debug(bstack1ll1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠࡼࡿࠥਏ").format(e))
      bstack11l1lll111_opy_()
      bstack1lll111l_opy_(bstack1l111l111_opy_, logger)
  except:
    pass
def bstack1l111lll11_opy_():
  global bstack1llll111l_opy_
  global bstack1lll11111_opy_
  global bstack1ll111ll11_opy_
  global bstack1lll1111_opy_
  global bstack1l11111lll_opy_
  global bstack11l1l11lll_opy_
  global CONFIG
  bstack11l1l111ll_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਐ"))
  if bstack11l1l111ll_opy_ in [bstack1ll1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ਑"), bstack1ll1l11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ਒")]:
    bstack111l1l11_opy_()
  percy.shutdown()
  if bstack1llll111l_opy_:
    logger.warning(bstack1l1ll1l1_opy_.format(str(bstack1llll111l_opy_)))
  else:
    try:
      bstack11l1ll11_opy_ = bstack111l1ll1_opy_(bstack1ll1l11_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩਓ"), logger)
      if bstack11l1ll11_opy_.get(bstack1ll1l11_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩਔ")) and bstack11l1ll11_opy_.get(bstack1ll1l11_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪਕ")).get(bstack1ll1l11_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨਖ")):
        logger.warning(bstack1l1ll1l1_opy_.format(str(bstack11l1ll11_opy_[bstack1ll1l11_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਗ")][bstack1ll1l11_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪਘ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack11ll11111l_opy_.invoke(bstack11lll1l1l1_opy_.bstack1lll11l1_opy_)
  logger.info(bstack111ll1l11_opy_)
  global bstack1ll1ll1l_opy_
  if bstack1ll1ll1l_opy_:
    bstack1ll1lll11l_opy_()
  try:
    for driver in bstack1lll11111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1ll11l111_opy_)
  if bstack11l1l11lll_opy_ == bstack1ll1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨਙ"):
    bstack1l11111lll_opy_ = bstack11111111l_opy_(bstack1ll1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫਚ"))
  if bstack11l1l11lll_opy_ == bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫਛ") and len(bstack1lll1111_opy_) == 0:
    bstack1lll1111_opy_ = bstack11111111l_opy_(bstack1ll1l11_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪਜ"))
    if len(bstack1lll1111_opy_) == 0:
      bstack1lll1111_opy_ = bstack11111111l_opy_(bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬਝ"))
  bstack1ll11l11_opy_ = bstack1ll1l11_opy_ (u"ࠧࠨਞ")
  if len(bstack1ll111ll11_opy_) > 0:
    bstack1ll11l11_opy_ = bstack1l11ll1ll_opy_(bstack1ll111ll11_opy_)
  elif len(bstack1lll1111_opy_) > 0:
    bstack1ll11l11_opy_ = bstack1l11ll1ll_opy_(bstack1lll1111_opy_)
  elif len(bstack1l11111lll_opy_) > 0:
    bstack1ll11l11_opy_ = bstack1l11ll1ll_opy_(bstack1l11111lll_opy_)
  elif len(bstack1l1lllllll_opy_) > 0:
    bstack1ll11l11_opy_ = bstack1l11ll1ll_opy_(bstack1l1lllllll_opy_)
  if bool(bstack1ll11l11_opy_):
    bstack11l1lll1_opy_(bstack1ll11l11_opy_)
  else:
    bstack11l1lll1_opy_()
  bstack1lll111l_opy_(bstack1l111111_opy_, logger)
  if bstack11l1l111ll_opy_ not in [bstack1ll1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩਟ")]:
    bstack1lll1ll1_opy_()
  bstack1ll1lllll_opy_.bstack1l1l11l1l_opy_(CONFIG)
  if len(bstack1l11111lll_opy_) > 0:
    sys.exit(len(bstack1l11111lll_opy_))
def bstack1ll1lllll1_opy_(bstack1ll11l11ll_opy_, frame):
  global bstack11lll1111_opy_
  logger.error(bstack11l1ll111l_opy_)
  bstack11lll1111_opy_.bstack1lll11lll1_opy_(bstack1ll1l11_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬਠ"), bstack1ll11l11ll_opy_)
  if hasattr(signal, bstack1ll1l11_opy_ (u"ࠪࡗ࡮࡭࡮ࡢ࡮ࡶࠫਡ")):
    bstack11lll1111_opy_.bstack1lll11lll1_opy_(bstack1ll1l11_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫਢ"), signal.Signals(bstack1ll11l11ll_opy_).name)
  else:
    bstack11lll1111_opy_.bstack1lll11lll1_opy_(bstack1ll1l11_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬਣ"), bstack1ll1l11_opy_ (u"࠭ࡓࡊࡉࡘࡒࡐࡔࡏࡘࡐࠪਤ"))
  if cli.is_running():
    bstack11ll11111l_opy_.invoke(bstack11lll1l1l1_opy_.bstack1lll11l1_opy_)
  bstack11l1l111ll_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਥ"))
  if bstack11l1l111ll_opy_ == bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਦ") and not cli.is_enabled(CONFIG):
    bstack1ll1l11l1l_opy_.stop(bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩਧ")))
  bstack1l111lll11_opy_()
  sys.exit(1)
def bstack1ll1ll1lll_opy_(err):
  logger.critical(bstack1l11111l1_opy_.format(str(err)))
  bstack11l1lll1_opy_(bstack1l11111l1_opy_.format(str(err)), True)
  atexit.unregister(bstack1l111lll11_opy_)
  bstack111l1l11_opy_()
  sys.exit(1)
def bstack11l1llll1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11l1lll1_opy_(message, True)
  atexit.unregister(bstack1l111lll11_opy_)
  bstack111l1l11_opy_()
  sys.exit(1)
def bstack1ll11l1ll1_opy_():
  global CONFIG
  global bstack11l1l1lll_opy_
  global bstack1l11l1l11l_opy_
  global bstack1lll111ll1_opy_
  CONFIG = bstack1lll111l1_opy_()
  load_dotenv(CONFIG.get(bstack1ll1l11_opy_ (u"ࠪࡩࡳࡼࡆࡪ࡮ࡨࠫਨ")))
  bstack1lll1llll_opy_()
  bstack11l11l111_opy_()
  CONFIG = bstack1111l1l11_opy_(CONFIG)
  update(CONFIG, bstack1l11l1l11l_opy_)
  update(CONFIG, bstack11l1l1lll_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack111111ll_opy_(CONFIG)
  bstack1lll111ll1_opy_ = bstack1l1l1lll1_opy_(CONFIG)
  os.environ[bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ਩")] = bstack1lll111ll1_opy_.__str__().lower()
  bstack11lll1111_opy_.bstack1lll11lll1_opy_(bstack1ll1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ਪ"), bstack1lll111ll1_opy_)
  if (bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਫ") in CONFIG and bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪਬ") in bstack11l1l1lll_opy_) or (
          bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫਭ") in CONFIG and bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬਮ") not in bstack1l11l1l11l_opy_):
    if os.getenv(bstack1ll1l11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧਯ")):
      CONFIG[bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ਰ")] = os.getenv(bstack1ll1l11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ਱"))
    else:
      if not CONFIG.get(bstack1ll1l11_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤਲ"), bstack1ll1l11_opy_ (u"ࠢࠣਲ਼")) in bstack1lll1lll1l_opy_:
        bstack11lll11l_opy_()
  elif (bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ਴") not in CONFIG and bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫਵ") in CONFIG) or (
          bstack1ll1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਸ਼") in bstack1l11l1l11l_opy_ and bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ਷") not in bstack11l1l1lll_opy_):
    del (CONFIG[bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧਸ")])
  if bstack11lll1l111_opy_(CONFIG):
    bstack1ll1ll1lll_opy_(bstack1ll11llll_opy_)
  Config.bstack11111l1l1_opy_().bstack1lll11lll1_opy_(bstack1ll1l11_opy_ (u"ࠨࡵࡴࡧࡵࡒࡦࡳࡥࠣਹ"), CONFIG[bstack1ll1l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ਺")])
  bstack1l111l1ll1_opy_()
  bstack1lllllllll_opy_()
  if bstack11l1llll1l_opy_ and not CONFIG.get(bstack1ll1l11_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦ਻"), bstack1ll1l11_opy_ (u"ࠤ਼ࠥ")) in bstack1lll1lll1l_opy_:
    CONFIG[bstack1ll1l11_opy_ (u"ࠪࡥࡵࡶࠧ਽")] = bstack1l1l11l11_opy_(CONFIG)
    logger.info(bstack1lllll11l1_opy_.format(CONFIG[bstack1ll1l11_opy_ (u"ࠫࡦࡶࡰࠨਾ")]))
  if not bstack1lll111ll1_opy_:
    CONFIG[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਿ")] = [{}]
def bstack1l11l111l_opy_(config, bstack1l11lllll_opy_):
  global CONFIG
  global bstack11l1llll1l_opy_
  CONFIG = config
  bstack11l1llll1l_opy_ = bstack1l11lllll_opy_
def bstack1lllllllll_opy_():
  global CONFIG
  global bstack11l1llll1l_opy_
  if bstack1ll1l11_opy_ (u"࠭ࡡࡱࡲࠪੀ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11l1llll1_opy_(e, bstack1lll1llll1_opy_)
    bstack11l1llll1l_opy_ = True
    bstack11lll1111_opy_.bstack1lll11lll1_opy_(bstack1ll1l11_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ੁ"), True)
def bstack1l1l11l11_opy_(config):
  bstack1l1lll111_opy_ = bstack1ll1l11_opy_ (u"ࠨࠩੂ")
  app = config[bstack1ll1l11_opy_ (u"ࠩࡤࡴࡵ࠭੃")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l11l1llll_opy_:
      if os.path.exists(app):
        bstack1l1lll111_opy_ = bstack1l1llllll1_opy_(config, app)
      elif bstack11l111l11_opy_(app):
        bstack1l1lll111_opy_ = app
      else:
        bstack1ll1ll1lll_opy_(bstack1lll1l111_opy_.format(app))
    else:
      if bstack11l111l11_opy_(app):
        bstack1l1lll111_opy_ = app
      elif os.path.exists(app):
        bstack1l1lll111_opy_ = bstack1l1llllll1_opy_(app)
      else:
        bstack1ll1ll1lll_opy_(bstack11ll11l1l_opy_)
  else:
    if len(app) > 2:
      bstack1ll1ll1lll_opy_(bstack11l1lll1l_opy_)
    elif len(app) == 2:
      if bstack1ll1l11_opy_ (u"ࠪࡴࡦࡺࡨࠨ੄") in app and bstack1ll1l11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ੅") in app:
        if os.path.exists(app[bstack1ll1l11_opy_ (u"ࠬࡶࡡࡵࡪࠪ੆")]):
          bstack1l1lll111_opy_ = bstack1l1llllll1_opy_(config, app[bstack1ll1l11_opy_ (u"࠭ࡰࡢࡶ࡫ࠫੇ")], app[bstack1ll1l11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪੈ")])
        else:
          bstack1ll1ll1lll_opy_(bstack1lll1l111_opy_.format(app))
      else:
        bstack1ll1ll1lll_opy_(bstack11l1lll1l_opy_)
    else:
      for key in app:
        if key in bstack1ll1l11ll_opy_:
          if key == bstack1ll1l11_opy_ (u"ࠨࡲࡤࡸ࡭࠭੉"):
            if os.path.exists(app[key]):
              bstack1l1lll111_opy_ = bstack1l1llllll1_opy_(config, app[key])
            else:
              bstack1ll1ll1lll_opy_(bstack1lll1l111_opy_.format(app))
          else:
            bstack1l1lll111_opy_ = app[key]
        else:
          bstack1ll1ll1lll_opy_(bstack1l111l111l_opy_)
  return bstack1l1lll111_opy_
def bstack11l111l11_opy_(bstack1l1lll111_opy_):
  import re
  bstack1llllll1ll_opy_ = re.compile(bstack1ll1l11_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ੊"))
  bstack111lll1l_opy_ = re.compile(bstack1ll1l11_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫ࠱࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢੋ"))
  if bstack1ll1l11_opy_ (u"ࠫࡧࡹ࠺࠰࠱ࠪੌ") in bstack1l1lll111_opy_ or re.fullmatch(bstack1llllll1ll_opy_, bstack1l1lll111_opy_) or re.fullmatch(bstack111lll1l_opy_, bstack1l1lll111_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1l11ll1l11_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1l1llllll1_opy_(config, path, bstack11ll1llll1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1ll1l11_opy_ (u"ࠬࡸࡢࠨ੍")).read()).hexdigest()
  bstack1llll1ll1l_opy_ = bstack1l1l11111_opy_(md5_hash)
  bstack1l1lll111_opy_ = None
  if bstack1llll1ll1l_opy_:
    logger.info(bstack1lll111l11_opy_.format(bstack1llll1ll1l_opy_, md5_hash))
    return bstack1llll1ll1l_opy_
  bstack1l1l1lllll_opy_ = datetime.datetime.now()
  bstack111l1111_opy_ = MultipartEncoder(
    fields={
      bstack1ll1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࠫ੎"): (os.path.basename(path), open(os.path.abspath(path), bstack1ll1l11_opy_ (u"ࠧࡳࡤࠪ੏")), bstack1ll1l11_opy_ (u"ࠨࡶࡨࡼࡹ࠵ࡰ࡭ࡣ࡬ࡲࠬ੐")),
      bstack1ll1l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬੑ"): bstack11ll1llll1_opy_
    }
  )
  response = requests.post(bstack11lll1ll1l_opy_, data=bstack111l1111_opy_,
                           headers={bstack1ll1l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ੒"): bstack111l1111_opy_.content_type},
                           auth=(config[bstack1ll1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭੓")], config[bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ੔")]))
  try:
    res = json.loads(response.text)
    bstack1l1lll111_opy_ = res[bstack1ll1l11_opy_ (u"࠭ࡡࡱࡲࡢࡹࡷࡲࠧ੕")]
    logger.info(bstack1l1l11lll_opy_.format(bstack1l1lll111_opy_))
    bstack1llll1111l_opy_(md5_hash, bstack1l1lll111_opy_)
    cli.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡻࡰ࡭ࡱࡤࡨࡤࡧࡰࡱࠤ੖"), datetime.datetime.now() - bstack1l1l1lllll_opy_)
  except ValueError as err:
    bstack1ll1ll1lll_opy_(bstack11ll11111_opy_.format(str(err)))
  return bstack1l1lll111_opy_
def bstack1l111l1ll1_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1ll111l11_opy_
  bstack11llll11_opy_ = 1
  bstack1111lll11_opy_ = 1
  if bstack1ll1l11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ੗") in CONFIG:
    bstack1111lll11_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ੘")]
  else:
    bstack1111lll11_opy_ = bstack1l111l11l_opy_(framework_name, args) or 1
  if bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਖ਼") in CONFIG:
    bstack11llll11_opy_ = len(CONFIG[bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਗ਼")])
  bstack1ll111l11_opy_ = int(bstack1111lll11_opy_) * int(bstack11llll11_opy_)
def bstack1l111l11l_opy_(framework_name, args):
  if framework_name == bstack1l11ll1l1l_opy_ and args and bstack1ll1l11_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪਜ਼") in args:
      bstack11ll1l1ll_opy_ = args.index(bstack1ll1l11_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫੜ"))
      return int(args[bstack11ll1l1ll_opy_ + 1]) or 1
  return 1
def bstack1l1l11111_opy_(md5_hash):
  bstack1ll111l1ll_opy_ = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠧࡿࠩ੝")), bstack1ll1l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨਫ਼"), bstack1ll1l11_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ੟"))
  if os.path.exists(bstack1ll111l1ll_opy_):
    bstack1lll1l11ll_opy_ = json.load(open(bstack1ll111l1ll_opy_, bstack1ll1l11_opy_ (u"ࠪࡶࡧ࠭੠")))
    if md5_hash in bstack1lll1l11ll_opy_:
      bstack1ll11lllll_opy_ = bstack1lll1l11ll_opy_[md5_hash]
      bstack11111l1ll_opy_ = datetime.datetime.now()
      bstack11l11lll_opy_ = datetime.datetime.strptime(bstack1ll11lllll_opy_[bstack1ll1l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ੡")], bstack1ll1l11_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ੢"))
      if (bstack11111l1ll_opy_ - bstack11l11lll_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1ll11lllll_opy_[bstack1ll1l11_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ੣")]):
        return None
      return bstack1ll11lllll_opy_[bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪ੤")]
  else:
    return None
def bstack1llll1111l_opy_(md5_hash, bstack1l1lll111_opy_):
  bstack11l11lll11_opy_ = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠨࢀࠪ੥")), bstack1ll1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ੦"))
  if not os.path.exists(bstack11l11lll11_opy_):
    os.makedirs(bstack11l11lll11_opy_)
  bstack1ll111l1ll_opy_ = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠪࢂࠬ੧")), bstack1ll1l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ੨"), bstack1ll1l11_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭੩"))
  bstack1l1lll11l1_opy_ = {
    bstack1ll1l11_opy_ (u"࠭ࡩࡥࠩ੪"): bstack1l1lll111_opy_,
    bstack1ll1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ੫"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll1l11_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ੬")),
    bstack1ll1l11_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ੭"): str(__version__)
  }
  if os.path.exists(bstack1ll111l1ll_opy_):
    bstack1lll1l11ll_opy_ = json.load(open(bstack1ll111l1ll_opy_, bstack1ll1l11_opy_ (u"ࠪࡶࡧ࠭੮")))
  else:
    bstack1lll1l11ll_opy_ = {}
  bstack1lll1l11ll_opy_[md5_hash] = bstack1l1lll11l1_opy_
  with open(bstack1ll111l1ll_opy_, bstack1ll1l11_opy_ (u"ࠦࡼ࠱ࠢ੯")) as outfile:
    json.dump(bstack1lll1l11ll_opy_, outfile)
def bstack11lllll11_opy_(self):
  return
def bstack1l1lll1l_opy_(self):
  return
def bstack1l111111l_opy_(self):
  global bstack11l111lll_opy_
  bstack11l111lll_opy_(self)
def bstack111l111ll_opy_():
  global bstack1l1l1l11l1_opy_
  bstack1l1l1l11l1_opy_ = True
@measure(event_name=EVENTS.bstack1l1l11l111_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1ll11111_opy_(self):
  global bstack1l111111ll_opy_
  global bstack1lllllll1l_opy_
  global bstack1l1lll11ll_opy_
  try:
    if bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬੰ") in bstack1l111111ll_opy_ and self.session_id != None and bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪੱ"), bstack1ll1l11_opy_ (u"ࠧࠨੲ")) != bstack1ll1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩੳ"):
      bstack11lll111ll_opy_ = bstack1ll1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩੴ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪੵ")
      if bstack11lll111ll_opy_ == bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ੶"):
        bstack1l111lll_opy_(logger)
      if self != None:
        bstack11lll1l11_opy_(self, bstack11lll111ll_opy_, bstack1ll1l11_opy_ (u"ࠬ࠲ࠠࠨ੷").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1ll1l11_opy_ (u"࠭ࠧ੸")
    if bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ੹") in bstack1l111111ll_opy_ and getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ੺"), None):
      bstack1ll1l1l1l1_opy_.bstack11ll1111l1_opy_(self, bstack11ll11ll11_opy_, logger, wait=True)
    if bstack1ll1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ੻") in bstack1l111111ll_opy_:
      if not threading.currentThread().behave_test_status:
        bstack11lll1l11_opy_(self, bstack1ll1l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ੼"))
      bstack111llllll_opy_.bstack1ll1lll1ll_opy_(self)
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ੽") + str(e))
  bstack1l1lll11ll_opy_(self)
  self.session_id = None
def bstack11ll111111_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack11ll1l11_opy_
    global bstack1l111111ll_opy_
    command_executor = kwargs.get(bstack1ll1l11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨ੾"), bstack1ll1l11_opy_ (u"࠭ࠧ੿"))
    bstack11ll1ll1ll_opy_ = False
    if type(command_executor) == str and bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ઀") in command_executor:
      bstack11ll1ll1ll_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫઁ") in str(getattr(command_executor, bstack1ll1l11_opy_ (u"ࠩࡢࡹࡷࡲࠧં"), bstack1ll1l11_opy_ (u"ࠪࠫઃ"))):
      bstack11ll1ll1ll_opy_ = True
    else:
      return bstack111llll1l_opy_(self, *args, **kwargs)
    if bstack11ll1ll1ll_opy_:
      bstack1l111111l1_opy_ = bstack11l11l1ll1_opy_.bstack1l1ll11l_opy_(CONFIG, bstack1l111111ll_opy_)
      if kwargs.get(bstack1ll1l11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ઄")):
        kwargs[bstack1ll1l11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭અ")] = bstack11ll1l11_opy_(kwargs[bstack1ll1l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧઆ")], bstack1l111111ll_opy_, bstack1l111111l1_opy_)
      elif kwargs.get(bstack1ll1l11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧઇ")):
        kwargs[bstack1ll1l11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨઈ")] = bstack11ll1l11_opy_(kwargs[bstack1ll1l11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩઉ")], bstack1l111111ll_opy_, bstack1l111111l1_opy_)
  except Exception as e:
    logger.error(bstack1ll1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥઊ").format(str(e)))
  return bstack111llll1l_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack11ll1ll11l_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack11ll111l_opy_(self, command_executor=bstack1ll1l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧઋ"), *args, **kwargs):
  bstack11l1l1ll1l_opy_ = bstack11ll111111_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1lll111111_opy_.on():
    return bstack11l1l1ll1l_opy_
  try:
    logger.debug(bstack1ll1l11_opy_ (u"ࠬࡉ࡯࡮࡯ࡤࡲࡩࠦࡅࡹࡧࡦࡹࡹࡵࡲࠡࡹ࡫ࡩࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡡ࡭ࡵࡨࠤ࠲ࠦࡻࡾࠩઌ").format(str(command_executor)))
    logger.debug(bstack1ll1l11_opy_ (u"࠭ࡈࡶࡤ࡙ࠣࡗࡒࠠࡪࡵࠣ࠱ࠥࢁࡽࠨઍ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ઎") in command_executor._url:
      bstack11lll1111_opy_.bstack1lll11lll1_opy_(bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩએ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬઐ") in command_executor):
    bstack11lll1111_opy_.bstack1lll11lll1_opy_(bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫઑ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack111l1l1l1_opy_ = getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ઒"), None)
  if bstack1ll1l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬઓ") in bstack1l111111ll_opy_ or bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬઔ") in bstack1l111111ll_opy_:
    bstack1ll1l11l1l_opy_.bstack1ll11ll11_opy_(self)
  if bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧક") in bstack1l111111ll_opy_ and bstack111l1l1l1_opy_ and bstack111l1l1l1_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨખ"), bstack1ll1l11_opy_ (u"ࠩࠪગ")) == bstack1ll1l11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫઘ"):
    bstack1ll1l11l1l_opy_.bstack1ll11ll11_opy_(self)
  return bstack11l1l1ll1l_opy_
def bstack1l1l1llll1_opy_(args):
  return bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬઙ") in str(args)
def bstack11l111ll_opy_(self, driver_command, *args, **kwargs):
  global bstack1ll1ll111_opy_
  global bstack1l1ll111l_opy_
  bstack1lll1lllll_opy_ = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩચ"), None) and bstack11ll111l1_opy_(
          threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬછ"), None)
  bstack11lllll1_opy_ = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧજ"), None) and bstack11ll111l1_opy_(
          threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪઝ"), None)
  bstack1l1l1l1l1l_opy_ = getattr(self, bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩઞ"), None) != None and getattr(self, bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪટ"), None) == True
  if not bstack1l1ll111l_opy_ and bstack1lll111ll1_opy_ and bstack1ll1lll1l_opy_.bstack1l11l1lll_opy_(CONFIG) and bstack1l11l111_opy_.bstack1l1l11ll1l_opy_(driver_command) and (bstack1l1l1l1l1l_opy_ or bstack1lll1lllll_opy_ or bstack11lllll1_opy_) and not bstack1l1l1llll1_opy_(args):
    try:
      bstack1l1ll111l_opy_ = True
      logger.debug(bstack1ll1l11_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭ઠ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack1ll1l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪડ").format(str(err)))
    bstack1l1ll111l_opy_ = False
  response = bstack1ll1ll111_opy_(self, driver_command, *args, **kwargs)
  if (bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬઢ") in str(bstack1l111111ll_opy_).lower() or bstack1ll1l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧણ") in str(bstack1l111111ll_opy_).lower()) and bstack1lll111111_opy_.on():
    try:
      if driver_command == bstack1ll1l11_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬત"):
        bstack1ll1l11l1l_opy_.bstack1ll1llll11_opy_({
            bstack1ll1l11_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨથ"): response[bstack1ll1l11_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩદ")],
            bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫધ"): bstack1ll1l11l1l_opy_.current_test_uuid() if bstack1ll1l11l1l_opy_.current_test_uuid() else bstack1lll111111_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack1ll1111ll_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1111l11l1_opy_(self, command_executor,
             desired_capabilities=None, bstack11llll1ll1_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1lllllll1l_opy_
  global bstack1ll1ll11l_opy_
  global bstack11l111111_opy_
  global bstack1l1l11l1l1_opy_
  global bstack11ll11l1ll_opy_
  global bstack1l111111ll_opy_
  global bstack111llll1l_opy_
  global bstack1lll11111_opy_
  global bstack11lll11l1_opy_
  global bstack11ll11ll11_opy_
  CONFIG[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧન")] = str(bstack1l111111ll_opy_) + str(__version__)
  bstack1111l111_opy_ = os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ઩")]
  bstack1l111111l1_opy_ = bstack11l11l1ll1_opy_.bstack1l1ll11l_opy_(CONFIG, bstack1l111111ll_opy_)
  CONFIG[bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪપ")] = bstack1111l111_opy_
  CONFIG[bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪફ")] = bstack1l111111l1_opy_
  if CONFIG.get(bstack1ll1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩબ"),bstack1ll1l11_opy_ (u"ࠪࠫભ")) and bstack1ll1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪમ") in bstack1l111111ll_opy_:
    CONFIG[bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬય")].pop(bstack1ll1l11_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫર"), None)
    CONFIG[bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ઱")].pop(bstack1ll1l11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭લ"), None)
  command_executor = bstack11l1ll1111_opy_()
  logger.debug(bstack1ll1l1l11l_opy_.format(command_executor))
  proxy = bstack1ll1l11l_opy_(CONFIG, proxy)
  bstack1lll1l1l_opy_ = 0 if bstack1ll1ll11l_opy_ < 0 else bstack1ll1ll11l_opy_
  try:
    if bstack1l1l11l1l1_opy_ is True:
      bstack1lll1l1l_opy_ = int(multiprocessing.current_process().name)
    elif bstack11ll11l1ll_opy_ is True:
      bstack1lll1l1l_opy_ = int(threading.current_thread().name)
  except:
    bstack1lll1l1l_opy_ = 0
  bstack11ll1111ll_opy_ = bstack1ll1l1ll_opy_(CONFIG, bstack1lll1l1l_opy_)
  logger.debug(bstack1ll1ll11l1_opy_.format(str(bstack11ll1111ll_opy_)))
  if bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ળ") in CONFIG and bstack11l1llllll_opy_(CONFIG[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ઴")]):
    bstack111l11lll_opy_(bstack11ll1111ll_opy_)
  if bstack1ll1lll1l_opy_.bstack1l1lllll1_opy_(CONFIG, bstack1lll1l1l_opy_) and bstack1ll1lll1l_opy_.bstack1l111ll111_opy_(bstack11ll1111ll_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    if cli.accessibility is None or not cli.accessibility.is_enabled():
      bstack1ll1lll1l_opy_.set_capabilities(bstack11ll1111ll_opy_, CONFIG)
  if desired_capabilities:
    bstack1ll1l1l1_opy_ = bstack1111l1l11_opy_(desired_capabilities)
    bstack1ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫવ")] = bstack1ll1ll1ll_opy_(CONFIG)
    bstack111ll111l_opy_ = bstack1ll1l1ll_opy_(bstack1ll1l1l1_opy_)
    if bstack111ll111l_opy_:
      bstack11ll1111ll_opy_ = update(bstack111ll111l_opy_, bstack11ll1111ll_opy_)
    desired_capabilities = None
  if options:
    bstack11ll1l111l_opy_(options, bstack11ll1111ll_opy_)
  if not options:
    options = bstack11l11111l_opy_(bstack11ll1111ll_opy_)
  bstack11ll11ll11_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨશ"))[bstack1lll1l1l_opy_]
  if proxy and bstack1llll11ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ષ")):
    options.proxy(proxy)
  if options and bstack1llll11ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭સ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1llll11ll_opy_() < version.parse(bstack1ll1l11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧહ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11ll1111ll_opy_)
  logger.info(bstack1lll1ll11l_opy_)
  bstack1ll11l1lll_opy_.end(EVENTS.bstack11ll1l1l_opy_.value, EVENTS.bstack11ll1l1l_opy_.value + bstack1ll1l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ઺"), EVENTS.bstack11ll1l1l_opy_.value + bstack1ll1l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ઻"), status=True, failure=None, test_name=bstack11l111111_opy_)
  if bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡶࡲࡰࡨ࡬ࡰࡪ઼࠭") in kwargs:
    del kwargs[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡰࡳࡱࡩ࡭ࡱ࡫ࠧઽ")]
  if bstack1llll11ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ા")):
    bstack111llll1l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
  elif bstack1llll11ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭િ")):
    bstack111llll1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              bstack11llll1ll1_opy_=bstack11llll1ll1_opy_, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1llll11ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨી")):
    bstack111llll1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              bstack11llll1ll1_opy_=bstack11llll1ll1_opy_, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack111llll1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              bstack11llll1ll1_opy_=bstack11llll1ll1_opy_, proxy=proxy,
              keep_alive=keep_alive)
  if bstack1ll1lll1l_opy_.bstack1l1lllll1_opy_(CONFIG, bstack1lll1l1l_opy_) and bstack1ll1lll1l_opy_.bstack1l111ll111_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫુ")][bstack1ll1l11_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩૂ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack1ll1lll1l_opy_.set_capabilities(bstack11ll1111ll_opy_, CONFIG)
  try:
    bstack1l11l11ll1_opy_ = bstack1ll1l11_opy_ (u"ࠫࠬૃ")
    if bstack1llll11ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭ૄ")):
      bstack1l11l11ll1_opy_ = self.caps.get(bstack1ll1l11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨૅ"))
    else:
      bstack1l11l11ll1_opy_ = self.capabilities.get(bstack1ll1l11_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ૆"))
    if bstack1l11l11ll1_opy_:
      bstack1111l11l_opy_(bstack1l11l11ll1_opy_)
      if bstack1llll11ll_opy_() <= version.parse(bstack1ll1l11_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨે")):
        self.command_executor._url = bstack1ll1l11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥૈ") + bstack1l11ll1lll_opy_ + bstack1ll1l11_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢૉ")
      else:
        self.command_executor._url = bstack1ll1l11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ૊") + bstack1l11l11ll1_opy_ + bstack1ll1l11_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨો")
      logger.debug(bstack1l11ll11l1_opy_.format(bstack1l11l11ll1_opy_))
    else:
      logger.debug(bstack1ll1l1111l_opy_.format(bstack1ll1l11_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢૌ")))
  except Exception as e:
    logger.debug(bstack1ll1l1111l_opy_.format(e))
  if bstack1ll1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ્࠭") in bstack1l111111ll_opy_:
    bstack1ll11l1l1l_opy_(bstack1ll1ll11l_opy_, bstack11lll11l1_opy_)
  bstack1lllllll1l_opy_ = self.session_id
  if bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ૎") in bstack1l111111ll_opy_ or bstack1ll1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ૏") in bstack1l111111ll_opy_ or bstack1ll1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩૐ") in bstack1l111111ll_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack111l1l1l1_opy_ = getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ૑"), None)
  if bstack1ll1l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ૒") in bstack1l111111ll_opy_ or bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ૓") in bstack1l111111ll_opy_:
    bstack1ll1l11l1l_opy_.bstack1ll11ll11_opy_(self)
  if bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ૔") in bstack1l111111ll_opy_ and bstack111l1l1l1_opy_ and bstack111l1l1l1_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ૕"), bstack1ll1l11_opy_ (u"ࠩࠪ૖")) == bstack1ll1l11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ૗"):
    bstack1ll1l11l1l_opy_.bstack1ll11ll11_opy_(self)
  bstack1lll11111_opy_.append(self)
  if bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૘") in CONFIG and bstack1ll1l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ૙") in CONFIG[bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૚")][bstack1lll1l1l_opy_]:
    bstack11l111111_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ૛")][bstack1lll1l1l_opy_][bstack1ll1l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭૜")]
  logger.debug(bstack11l11lll1_opy_.format(bstack1lllllll1l_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1l1111lll1_opy_
    def bstack1ll1l1ll1_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l1ll1lll_opy_
      if(bstack1ll1l11_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸ࠯࡬ࡶࠦ૝") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠪࢂࠬ૞")), bstack1ll1l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ૟"), bstack1ll1l11_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧૠ")), bstack1ll1l11_opy_ (u"࠭ࡷࠨૡ")) as fp:
          fp.write(bstack1ll1l11_opy_ (u"ࠢࠣૢ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1ll1l11_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥૣ")))):
          with open(args[1], bstack1ll1l11_opy_ (u"ࠩࡵࠫ૤")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1ll1l11_opy_ (u"ࠪࡥࡸࡿ࡮ࡤࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡤࡴࡥࡸࡒࡤ࡫ࡪ࠮ࡣࡰࡰࡷࡩࡽࡺࠬࠡࡲࡤ࡫ࡪࠦ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠩ૥") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1lll1111l1_opy_)
            if bstack1ll1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ૦") in CONFIG and str(CONFIG[bstack1ll1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ૧")]).lower() != bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ૨"):
                bstack111111ll1_opy_ = bstack1l1111lll1_opy_()
                bstack1lll11ll11_opy_ = bstack1ll1l11_opy_ (u"ࠧࠨࠩࠍ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࠐࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࠼ࠌࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࠾ࠎࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࠾ࠎࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࠏ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࠏࠦࠠࡵࡴࡼࠤࢀࢁࠊࠡࠢࠣࠤࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࠻ࠋࠢࠣࢁࢂࠦࡣࡢࡶࡦ࡬ࠥ࠮ࡥࡹࠫࠣࡿࢀࠐࠠࠡࠢࠣࡧࡴࡴࡳࡰ࡮ࡨ࠲ࡪࡸࡲࡰࡴࠫࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠿ࠨࠬࠡࡧࡻ࠭ࡀࠐࠠࠡࡿࢀࠎࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻࡼࠌࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࠬࢁࡣࡥࡲࡘࡶࡱࢃࠧࠡ࠭ࠣࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪ࠮ࠍࠤࠥࠦࠠ࠯࠰࠱ࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠍࠤࠥࢃࡽࠪ࠽ࠍࢁࢂࡁࠊ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠍࠫࠬ࠭૩").format(bstack111111ll1_opy_=bstack111111ll1_opy_)
            lines.insert(1, bstack1lll11ll11_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1ll1l11_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥ૪")), bstack1ll1l11_opy_ (u"ࠩࡺࠫ૫")) as bstack11l11l1l11_opy_:
              bstack11l11l1l11_opy_.writelines(lines)
        CONFIG[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ૬")] = str(bstack1l111111ll_opy_) + str(__version__)
        bstack1111l111_opy_ = os.environ[bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ૭")]
        bstack1l111111l1_opy_ = bstack11l11l1ll1_opy_.bstack1l1ll11l_opy_(CONFIG, bstack1l111111ll_opy_)
        CONFIG[bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ૮")] = bstack1111l111_opy_
        CONFIG[bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ૯")] = bstack1l111111l1_opy_
        bstack1lll1l1l_opy_ = 0 if bstack1ll1ll11l_opy_ < 0 else bstack1ll1ll11l_opy_
        try:
          if bstack1l1l11l1l1_opy_ is True:
            bstack1lll1l1l_opy_ = int(multiprocessing.current_process().name)
          elif bstack11ll11l1ll_opy_ is True:
            bstack1lll1l1l_opy_ = int(threading.current_thread().name)
        except:
          bstack1lll1l1l_opy_ = 0
        CONFIG[bstack1ll1l11_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢ૰")] = False
        CONFIG[bstack1ll1l11_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ૱")] = True
        bstack11ll1111ll_opy_ = bstack1ll1l1ll_opy_(CONFIG, bstack1lll1l1l_opy_)
        logger.debug(bstack1ll1ll11l1_opy_.format(str(bstack11ll1111ll_opy_)))
        if CONFIG.get(bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭૲")):
          bstack111l11lll_opy_(bstack11ll1111ll_opy_)
        if bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૳") in CONFIG and bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ૴") in CONFIG[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ૵")][bstack1lll1l1l_opy_]:
          bstack11l111111_opy_ = CONFIG[bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૶")][bstack1lll1l1l_opy_][bstack1ll1l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ૷")]
        args.append(os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠨࢀࠪ૸")), bstack1ll1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩૹ"), bstack1ll1l11_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬૺ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11ll1111ll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1ll1l11_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨૻ"))
      bstack1l1ll1lll_opy_ = True
      return bstack11l11ll1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l1l1ll111_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1ll1ll11l_opy_
    global bstack11l111111_opy_
    global bstack1l1l11l1l1_opy_
    global bstack11ll11l1ll_opy_
    global bstack1l111111ll_opy_
    CONFIG[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧૼ")] = str(bstack1l111111ll_opy_) + str(__version__)
    bstack1111l111_opy_ = os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ૽")]
    bstack1l111111l1_opy_ = bstack11l11l1ll1_opy_.bstack1l1ll11l_opy_(CONFIG, bstack1l111111ll_opy_)
    CONFIG[bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ૾")] = bstack1111l111_opy_
    CONFIG[bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ૿")] = bstack1l111111l1_opy_
    bstack1lll1l1l_opy_ = 0 if bstack1ll1ll11l_opy_ < 0 else bstack1ll1ll11l_opy_
    try:
      if bstack1l1l11l1l1_opy_ is True:
        bstack1lll1l1l_opy_ = int(multiprocessing.current_process().name)
      elif bstack11ll11l1ll_opy_ is True:
        bstack1lll1l1l_opy_ = int(threading.current_thread().name)
    except:
      bstack1lll1l1l_opy_ = 0
    CONFIG[bstack1ll1l11_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ଀")] = True
    bstack11ll1111ll_opy_ = bstack1ll1l1ll_opy_(CONFIG, bstack1lll1l1l_opy_)
    logger.debug(bstack1ll1ll11l1_opy_.format(str(bstack11ll1111ll_opy_)))
    if CONFIG.get(bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧଁ")):
      bstack111l11lll_opy_(bstack11ll1111ll_opy_)
    if bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଂ") in CONFIG and bstack1ll1l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪଃ") in CONFIG[bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ଄")][bstack1lll1l1l_opy_]:
      bstack11l111111_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଅ")][bstack1lll1l1l_opy_][bstack1ll1l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ଆ")]
    import urllib
    import json
    if bstack1ll1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ଇ") in CONFIG and str(CONFIG[bstack1ll1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧଈ")]).lower() != bstack1ll1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪଉ"):
        bstack1l1111l111_opy_ = bstack1l1111lll1_opy_()
        bstack111111ll1_opy_ = bstack1l1111l111_opy_ + urllib.parse.quote(json.dumps(bstack11ll1111ll_opy_))
    else:
        bstack111111ll1_opy_ = bstack1ll1l11_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧଊ") + urllib.parse.quote(json.dumps(bstack11ll1111ll_opy_))
    browser = self.connect(bstack111111ll1_opy_)
    return browser
except Exception as e:
    pass
def bstack111llll1_opy_():
    global bstack1l1ll1lll_opy_
    global bstack1l111111ll_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1l1l11_opy_
        global bstack11lll1111_opy_
        if not bstack1lll111ll1_opy_:
          global bstack1l111llll_opy_
          if not bstack1l111llll_opy_:
            from bstack_utils.helper import bstack11l11llll_opy_, bstack1lll11l11l_opy_, bstack1l11l11l11_opy_
            bstack1l111llll_opy_ = bstack11l11llll_opy_()
            bstack1lll11l11l_opy_(bstack1l111111ll_opy_)
            bstack1l111111l1_opy_ = bstack11l11l1ll1_opy_.bstack1l1ll11l_opy_(CONFIG, bstack1l111111ll_opy_)
            bstack11lll1111_opy_.bstack1lll11lll1_opy_(bstack1ll1l11_opy_ (u"ࠨࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡔࡗࡕࡄࡖࡅࡗࡣࡒࡇࡐࠣଋ"), bstack1l111111l1_opy_)
          BrowserType.connect = bstack1l1l1l11_opy_
          return
        BrowserType.launch = bstack1l1l1ll111_opy_
        bstack1l1ll1lll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll1l1ll1_opy_
      bstack1l1ll1lll_opy_ = True
    except Exception as e:
      pass
def bstack1lllll1l11_opy_(context, bstack1llll11ll1_opy_):
  try:
    context.page.evaluate(bstack1ll1l11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣଌ"), bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬ଍")+ json.dumps(bstack1llll11ll1_opy_) + bstack1ll1l11_opy_ (u"ࠤࢀࢁࠧ଎"))
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽ࠻ࠢࡾࢁࠧଏ").format(str(e), traceback.format_exc()))
def bstack11l11111_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1ll1l11_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧଐ"), bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ଑") + json.dumps(message) + bstack1ll1l11_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩ଒") + json.dumps(level) + bstack1ll1l11_opy_ (u"ࠧࡾࡿࠪଓ"))
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀ࠾ࠥࢁࡽࠣଔ").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack11ll1l11l1_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1l1l1llll_opy_(self, url):
  global bstack1ll1l11l1_opy_
  try:
    bstack1l1l111l11_opy_(url)
  except Exception as err:
    logger.debug(bstack1l111l1ll_opy_.format(str(err)))
  try:
    bstack1ll1l11l1_opy_(self, url)
  except Exception as e:
    try:
      bstack1l1lll1ll1_opy_ = str(e)
      if any(err_msg in bstack1l1lll1ll1_opy_ for err_msg in bstack11llllll11_opy_):
        bstack1l1l111l11_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l111l1ll_opy_.format(str(err)))
    raise e
def bstack11ll1l111_opy_(self):
  global bstack11l1l11111_opy_
  bstack11l1l11111_opy_ = self
  return
def bstack1ll1l1l111_opy_(self):
  global bstack1llll1lll_opy_
  bstack1llll1lll_opy_ = self
  return
def bstack1ll111ll1l_opy_(test_name, bstack11l1ll1l1l_opy_):
  global CONFIG
  if percy.bstack11l1ll1lll_opy_() == bstack1ll1l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢକ"):
    bstack11l1l11l11_opy_ = os.path.relpath(bstack11l1ll1l1l_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11l1l11l11_opy_)
    bstack1l1ll111l1_opy_ = suite_name + bstack1ll1l11_opy_ (u"ࠥ࠱ࠧଖ") + test_name
    threading.current_thread().percySessionName = bstack1l1ll111l1_opy_
def bstack1ll1l11111_opy_(self, test, *args, **kwargs):
  global bstack1l1111ll1_opy_
  test_name = None
  bstack11l1ll1l1l_opy_ = None
  if test:
    test_name = str(test.name)
    bstack11l1ll1l1l_opy_ = str(test.source)
  bstack1ll111ll1l_opy_(test_name, bstack11l1ll1l1l_opy_)
  bstack1l1111ll1_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1ll111lll1_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack11ll1l1lll_opy_(driver, bstack1l1ll111l1_opy_):
  if not bstack11l11ll111_opy_ and bstack1l1ll111l1_opy_:
      bstack1l1ll111ll_opy_ = {
          bstack1ll1l11_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫଗ"): bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ଘ"),
          bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩଙ"): {
              bstack1ll1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬଚ"): bstack1l1ll111l1_opy_
          }
      }
      bstack11ll111l11_opy_ = bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ଛ").format(json.dumps(bstack1l1ll111ll_opy_))
      driver.execute_script(bstack11ll111l11_opy_)
  if bstack11l1ll1ll1_opy_:
      bstack1l1l11111l_opy_ = {
          bstack1ll1l11_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩଜ"): bstack1ll1l11_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬଝ"),
          bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଞ"): {
              bstack1ll1l11_opy_ (u"ࠬࡪࡡࡵࡣࠪଟ"): bstack1l1ll111l1_opy_ + bstack1ll1l11_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨଠ"),
              bstack1ll1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ଡ"): bstack1ll1l11_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ଢ")
          }
      }
      if bstack11l1ll1ll1_opy_.status == bstack1ll1l11_opy_ (u"ࠩࡓࡅࡘ࡙ࠧଣ"):
          bstack1l1l1ll1_opy_ = bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨତ").format(json.dumps(bstack1l1l11111l_opy_))
          driver.execute_script(bstack1l1l1ll1_opy_)
          bstack11lll1l11_opy_(driver, bstack1ll1l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫଥ"))
      elif bstack11l1ll1ll1_opy_.status == bstack1ll1l11_opy_ (u"ࠬࡌࡁࡊࡎࠪଦ"):
          reason = bstack1ll1l11_opy_ (u"ࠨࠢଧ")
          bstack1l1111l1_opy_ = bstack1l1ll111l1_opy_ + bstack1ll1l11_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠨନ")
          if bstack11l1ll1ll1_opy_.message:
              reason = str(bstack11l1ll1ll1_opy_.message)
              bstack1l1111l1_opy_ = bstack1l1111l1_opy_ + bstack1ll1l11_opy_ (u"ࠨࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࠨ଩") + reason
          bstack1l1l11111l_opy_[bstack1ll1l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬପ")] = {
              bstack1ll1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩଫ"): bstack1ll1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪବ"),
              bstack1ll1l11_opy_ (u"ࠬࡪࡡࡵࡣࠪଭ"): bstack1l1111l1_opy_
          }
          bstack1l1l1ll1_opy_ = bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫମ").format(json.dumps(bstack1l1l11111l_opy_))
          driver.execute_script(bstack1l1l1ll1_opy_)
          bstack11lll1l11_opy_(driver, bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧଯ"), reason)
          bstack1111111l1_opy_(reason, str(bstack11l1ll1ll1_opy_), str(bstack1ll1ll11l_opy_), logger)
@measure(event_name=EVENTS.bstack1l111lll1_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1l1ll11l11_opy_(driver, test):
  if percy.bstack11l1ll1lll_opy_() == bstack1ll1l11_opy_ (u"ࠣࡶࡵࡹࡪࠨର") and percy.bstack111llll11_opy_() == bstack1ll1l11_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ଱"):
      bstack1ll1l111_opy_ = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ଲ"), None)
      bstack11llll1l_opy_(driver, bstack1ll1l111_opy_, test)
  if (bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨଳ"), None) and
      bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ଴"), None)) or (
      bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ଵ"), None) and
      bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩଶ"), None)):
      logger.info(bstack1ll1l11_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠠࠣଷ"))
      bstack1ll1lll1l_opy_.bstack11111lll_opy_(driver, name=test.name, path=test.source)
def bstack1ll11l11l1_opy_(test, bstack1l1ll111l1_opy_):
    try:
      bstack1l1l1lllll_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1ll1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧସ")] = bstack1l1ll111l1_opy_
      if bstack11l1ll1ll1_opy_:
        if bstack11l1ll1ll1_opy_.status == bstack1ll1l11_opy_ (u"ࠪࡔࡆ࡙ࡓࠨହ"):
          data[bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ଺")] = bstack1ll1l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ଻")
        elif bstack11l1ll1ll1_opy_.status == bstack1ll1l11_opy_ (u"࠭ࡆࡂࡋࡏ଼ࠫ"):
          data[bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧଽ")] = bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨା")
          if bstack11l1ll1ll1_opy_.message:
            data[bstack1ll1l11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩି")] = str(bstack11l1ll1ll1_opy_.message)
      user = CONFIG[bstack1ll1l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬୀ")]
      key = CONFIG[bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧୁ")]
      url = bstack1ll1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠱ࡾࢁ࠳ࡰࡳࡰࡰࠪୂ").format(user, key, bstack1lllllll1l_opy_)
      headers = {
        bstack1ll1l11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬୃ"): bstack1ll1l11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪୄ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
        cli.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠣࡪࡷࡸࡵࡀࡵࡱࡦࡤࡸࡪࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡴࡢࡶࡸࡷࠧ୅"), datetime.datetime.now() - bstack1l1l1lllll_opy_)
    except Exception as e:
      logger.error(bstack11l11l1l_opy_.format(str(e)))
def bstack1l11lll111_opy_(test, bstack1l1ll111l1_opy_):
  global CONFIG
  global bstack1llll1lll_opy_
  global bstack11l1l11111_opy_
  global bstack1lllllll1l_opy_
  global bstack11l1ll1ll1_opy_
  global bstack11l111111_opy_
  global bstack11ll111lll_opy_
  global bstack1ll1l1ll1l_opy_
  global bstack11ll1ll11_opy_
  global bstack1l1l1lll11_opy_
  global bstack1lll11111_opy_
  global bstack11ll11ll11_opy_
  try:
    if not bstack1lllllll1l_opy_:
      with open(os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠩࢁࠫ୆")), bstack1ll1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪେ"), bstack1ll1l11_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ୈ"))) as f:
        bstack1ll1ll1111_opy_ = json.loads(bstack1ll1l11_opy_ (u"ࠧࢁࠢ୉") + f.read().strip() + bstack1ll1l11_opy_ (u"࠭ࠢࡹࠤ࠽ࠤࠧࡿࠢࠨ୊") + bstack1ll1l11_opy_ (u"ࠢࡾࠤୋ"))
        bstack1lllllll1l_opy_ = bstack1ll1ll1111_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1lll11111_opy_:
    for driver in bstack1lll11111_opy_:
      if bstack1lllllll1l_opy_ == driver.session_id:
        if test:
          bstack1l1ll11l11_opy_(driver, test)
        bstack11ll1l1lll_opy_(driver, bstack1l1ll111l1_opy_)
  elif bstack1lllllll1l_opy_:
    bstack1ll11l11l1_opy_(test, bstack1l1ll111l1_opy_)
  if bstack1llll1lll_opy_:
    bstack1ll1l1ll1l_opy_(bstack1llll1lll_opy_)
  if bstack11l1l11111_opy_:
    bstack11ll1ll11_opy_(bstack11l1l11111_opy_)
  if bstack1l1l1l11l1_opy_:
    bstack1l1l1lll11_opy_()
def bstack111ll11l1_opy_(self, test, *args, **kwargs):
  bstack1l1ll111l1_opy_ = None
  if test:
    bstack1l1ll111l1_opy_ = str(test.name)
  bstack1l11lll111_opy_(test, bstack1l1ll111l1_opy_)
  bstack11ll111lll_opy_(self, test, *args, **kwargs)
def bstack111ll1l1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1111ll1ll_opy_
  global CONFIG
  global bstack1lll11111_opy_
  global bstack1lllllll1l_opy_
  bstack11ll1l1111_opy_ = None
  try:
    if bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧୌ"), None) or bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰ୍ࠫ"), None):
      try:
        if not bstack1lllllll1l_opy_:
          with open(os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠪࢂࠬ୎")), bstack1ll1l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ୏"), bstack1ll1l11_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ୐"))) as f:
            bstack1ll1ll1111_opy_ = json.loads(bstack1ll1l11_opy_ (u"ࠨࡻࠣ୑") + f.read().strip() + bstack1ll1l11_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩ୒") + bstack1ll1l11_opy_ (u"ࠣࡿࠥ୓"))
            bstack1lllllll1l_opy_ = bstack1ll1ll1111_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1lll11111_opy_:
        for driver in bstack1lll11111_opy_:
          if bstack1lllllll1l_opy_ == driver.session_id:
            bstack11ll1l1111_opy_ = driver
    bstack1l1111ll_opy_ = bstack1ll1lll1l_opy_.bstack11ll1ll1l1_opy_(test.tags)
    if bstack11ll1l1111_opy_:
      threading.current_thread().isA11yTest = bstack1ll1lll1l_opy_.bstack1lllll111l_opy_(bstack11ll1l1111_opy_, bstack1l1111ll_opy_)
      threading.current_thread().isAppA11yTest = bstack1ll1lll1l_opy_.bstack1lllll111l_opy_(bstack11ll1l1111_opy_, bstack1l1111ll_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1l1111ll_opy_
      threading.current_thread().isAppA11yTest = bstack1l1111ll_opy_
  except:
    pass
  bstack1111ll1ll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11l1ll1ll1_opy_
  try:
    bstack11l1ll1ll1_opy_ = self._test
  except:
    bstack11l1ll1ll1_opy_ = self.test
def bstack1111l1l1l_opy_():
  global bstack1ll1111l1l_opy_
  try:
    if os.path.exists(bstack1ll1111l1l_opy_):
      os.remove(bstack1ll1111l1l_opy_)
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ୔") + str(e))
def bstack1l11ll1ll1_opy_():
  global bstack1ll1111l1l_opy_
  bstack11l1ll11_opy_ = {}
  try:
    if not os.path.isfile(bstack1ll1111l1l_opy_):
      with open(bstack1ll1111l1l_opy_, bstack1ll1l11_opy_ (u"ࠪࡻࠬ୕")):
        pass
      with open(bstack1ll1111l1l_opy_, bstack1ll1l11_opy_ (u"ࠦࡼ࠱ࠢୖ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1ll1111l1l_opy_):
      bstack11l1ll11_opy_ = json.load(open(bstack1ll1111l1l_opy_, bstack1ll1l11_opy_ (u"ࠬࡸࡢࠨୗ")))
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ୘") + str(e))
  finally:
    return bstack11l1ll11_opy_
def bstack1ll11l1l1l_opy_(platform_index, item_index):
  global bstack1ll1111l1l_opy_
  try:
    bstack11l1ll11_opy_ = bstack1l11ll1ll1_opy_()
    bstack11l1ll11_opy_[item_index] = platform_index
    with open(bstack1ll1111l1l_opy_, bstack1ll1l11_opy_ (u"ࠢࡸ࠭ࠥ୙")) as outfile:
      json.dump(bstack11l1ll11_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡻࡷ࡯ࡴࡪࡰࡪࠤࡹࡵࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭୚") + str(e))
def bstack1lll1l1l1l_opy_(bstack1111ll1l1_opy_):
  global CONFIG
  bstack1llll11l_opy_ = bstack1ll1l11_opy_ (u"ࠩࠪ୛")
  if not bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଡ଼") in CONFIG:
    logger.info(bstack1ll1l11_opy_ (u"ࠫࡓࡵࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠣࡴࡦࡹࡳࡦࡦࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡴࡨࡴࡴࡸࡴࠡࡨࡲࡶࠥࡘ࡯ࡣࡱࡷࠤࡷࡻ࡮ࠨଢ଼"))
  try:
    platform = CONFIG[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୞")][bstack1111ll1l1_opy_]
    if bstack1ll1l11_opy_ (u"࠭࡯ࡴࠩୟ") in platform:
      bstack1llll11l_opy_ += str(platform[bstack1ll1l11_opy_ (u"ࠧࡰࡵࠪୠ")]) + bstack1ll1l11_opy_ (u"ࠨ࠮ࠣࠫୡ")
    if bstack1ll1l11_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬୢ") in platform:
      bstack1llll11l_opy_ += str(platform[bstack1ll1l11_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ୣ")]) + bstack1ll1l11_opy_ (u"ࠫ࠱ࠦࠧ୤")
    if bstack1ll1l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ୥") in platform:
      bstack1llll11l_opy_ += str(platform[bstack1ll1l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ୦")]) + bstack1ll1l11_opy_ (u"ࠧ࠭ࠢࠪ୧")
    if bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ୨") in platform:
      bstack1llll11l_opy_ += str(platform[bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ୩")]) + bstack1ll1l11_opy_ (u"ࠪ࠰ࠥ࠭୪")
    if bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ୫") in platform:
      bstack1llll11l_opy_ += str(platform[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ୬")]) + bstack1ll1l11_opy_ (u"࠭ࠬࠡࠩ୭")
    if bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ୮") in platform:
      bstack1llll11l_opy_ += str(platform[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ୯")]) + bstack1ll1l11_opy_ (u"ࠩ࠯ࠤࠬ୰")
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠪࡗࡴࡳࡥࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡸࡷ࡯࡮ࡨࠢࡩࡳࡷࠦࡲࡦࡲࡲࡶࡹࠦࡧࡦࡰࡨࡶࡦࡺࡩࡰࡰࠪୱ") + str(e))
  finally:
    if bstack1llll11l_opy_[len(bstack1llll11l_opy_) - 2:] == bstack1ll1l11_opy_ (u"ࠫ࠱ࠦࠧ୲"):
      bstack1llll11l_opy_ = bstack1llll11l_opy_[:-2]
    return bstack1llll11l_opy_
def bstack111ll1111_opy_(path, bstack1llll11l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11lll111_opy_ = ET.parse(path)
    bstack11ll11llll_opy_ = bstack11lll111_opy_.getroot()
    bstack11ll11l11l_opy_ = None
    for suite in bstack11ll11llll_opy_.iter(bstack1ll1l11_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ୳")):
      if bstack1ll1l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭୴") in suite.attrib:
        suite.attrib[bstack1ll1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ୵")] += bstack1ll1l11_opy_ (u"ࠨࠢࠪ୶") + bstack1llll11l_opy_
        bstack11ll11l11l_opy_ = suite
    bstack1ll1ll11ll_opy_ = None
    for robot in bstack11ll11llll_opy_.iter(bstack1ll1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ୷")):
      bstack1ll1ll11ll_opy_ = robot
    bstack1l111l11l1_opy_ = len(bstack1ll1ll11ll_opy_.findall(bstack1ll1l11_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ୸")))
    if bstack1l111l11l1_opy_ == 1:
      bstack1ll1ll11ll_opy_.remove(bstack1ll1ll11ll_opy_.findall(bstack1ll1l11_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ୹"))[0])
      bstack1ll11lll1l_opy_ = ET.Element(bstack1ll1l11_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ୺"), attrib={bstack1ll1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ୻"): bstack1ll1l11_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࡹࠧ୼"), bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫ୽"): bstack1ll1l11_opy_ (u"ࠩࡶ࠴ࠬ୾")})
      bstack1ll1ll11ll_opy_.insert(1, bstack1ll11lll1l_opy_)
      bstack11lll1ll_opy_ = None
      for suite in bstack1ll1ll11ll_opy_.iter(bstack1ll1l11_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ୿")):
        bstack11lll1ll_opy_ = suite
      bstack11lll1ll_opy_.append(bstack11ll11l11l_opy_)
      bstack1l111ll11l_opy_ = None
      for status in bstack11ll11l11l_opy_.iter(bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ஀")):
        bstack1l111ll11l_opy_ = status
      bstack11lll1ll_opy_.append(bstack1l111ll11l_opy_)
    bstack11lll111_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠪ஁") + str(e))
def bstack11lll111l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11ll111ll1_opy_
  global CONFIG
  if bstack1ll1l11_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥஂ") in options:
    del options[bstack1ll1l11_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦஃ")]
  bstack1llllll1l_opy_ = bstack1l11ll1ll1_opy_()
  for bstack11ll1l11l_opy_ in bstack1llllll1l_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1ll1l11_opy_ (u"ࠨࡲࡤࡦࡴࡺ࡟ࡳࡧࡶࡹࡱࡺࡳࠨ஄"), str(bstack11ll1l11l_opy_), bstack1ll1l11_opy_ (u"ࠩࡲࡹࡹࡶࡵࡵ࠰ࡻࡱࡱ࠭அ"))
    bstack111ll1111_opy_(path, bstack1lll1l1l1l_opy_(bstack1llllll1l_opy_[bstack11ll1l11l_opy_]))
  bstack1111l1l1l_opy_()
  return bstack11ll111ll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l11l11111_opy_(self, ff_profile_dir):
  global bstack1lllllll1_opy_
  if not ff_profile_dir:
    return None
  return bstack1lllllll1_opy_(self, ff_profile_dir)
def bstack1ll111l1l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11l1111ll_opy_
  bstack11l11ll1l1_opy_ = []
  if bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ஆ") in CONFIG:
    bstack11l11ll1l1_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧஇ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1ll1l11_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨஈ")],
      pabot_args[bstack1ll1l11_opy_ (u"ࠨࡶࡦࡴࡥࡳࡸ࡫ࠢஉ")],
      argfile,
      pabot_args.get(bstack1ll1l11_opy_ (u"ࠢࡩ࡫ࡹࡩࠧஊ")),
      pabot_args[bstack1ll1l11_opy_ (u"ࠣࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠦ஋")],
      platform[0],
      bstack11l1111ll_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1ll1l11_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡪ࡮ࡲࡥࡴࠤ஌")] or [(bstack1ll1l11_opy_ (u"ࠥࠦ஍"), None)]
    for platform in enumerate(bstack11l11ll1l1_opy_)
  ]
def bstack1l11lll1ll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l1l1ll11l_opy_=bstack1ll1l11_opy_ (u"ࠫࠬஎ")):
  global bstack1ll1l1l1ll_opy_
  self.platform_index = platform_index
  self.bstack1l1l1l1l11_opy_ = bstack1l1l1ll11l_opy_
  bstack1ll1l1l1ll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1llll1ll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l111lll1l_opy_
  global bstack1lllll11l_opy_
  bstack1lll11111l_opy_ = copy.deepcopy(item)
  if not bstack1ll1l11_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧஏ") in item.options:
    bstack1lll11111l_opy_.options[bstack1ll1l11_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨஐ")] = []
  bstack11l1l1l1ll_opy_ = bstack1lll11111l_opy_.options[bstack1ll1l11_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ஑")].copy()
  for v in bstack1lll11111l_opy_.options[bstack1ll1l11_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪஒ")]:
    if bstack1ll1l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨஓ") in v:
      bstack11l1l1l1ll_opy_.remove(v)
    if bstack1ll1l11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪஔ") in v:
      bstack11l1l1l1ll_opy_.remove(v)
    if bstack1ll1l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨக") in v:
      bstack11l1l1l1ll_opy_.remove(v)
  bstack11l1l1l1ll_opy_.insert(0, bstack1ll1l11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛࠾ࢀࢃࠧ஖").format(bstack1lll11111l_opy_.platform_index))
  bstack11l1l1l1ll_opy_.insert(0, bstack1ll1l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭஗").format(bstack1lll11111l_opy_.bstack1l1l1l1l11_opy_))
  bstack1lll11111l_opy_.options[bstack1ll1l11_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ஘")] = bstack11l1l1l1ll_opy_
  if bstack1lllll11l_opy_:
    bstack1lll11111l_opy_.options[bstack1ll1l11_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪங")].insert(0, bstack1ll1l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔ࠼ࡾࢁࠬச").format(bstack1lllll11l_opy_))
  return bstack1l111lll1l_opy_(caller_id, datasources, is_last, bstack1lll11111l_opy_, outs_dir)
def bstack11l1111l1_opy_(command, item_index):
  if bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ஛")):
    os.environ[bstack1ll1l11_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬஜ")] = json.dumps(CONFIG[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ஝")][item_index % bstack1l11lllll1_opy_])
  global bstack1lllll11l_opy_
  if bstack1lllll11l_opy_:
    command[0] = command[0].replace(bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬஞ"), bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠫட") + str(
      item_index) + bstack1ll1l11_opy_ (u"ࠨࠢࠪ஠") + bstack1lllll11l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1ll1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ஡"),
                                    bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧ஢") + str(item_index), 1)
def bstack1l1ll1l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1llll1llll_opy_
  bstack11l1111l1_opy_(command, item_index)
  return bstack1llll1llll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1lll1lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1llll1llll_opy_
  bstack11l1111l1_opy_(command, item_index)
  return bstack1llll1llll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1lll1ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1llll1llll_opy_
  bstack11l1111l1_opy_(command, item_index)
  return bstack1llll1llll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1l11l111ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1llll1llll_opy_
  bstack11l1111l1_opy_(command, item_index)
  return bstack1llll1llll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1lllll1lll_opy_(self, runner, quiet=False, capture=True):
  global bstack1ll1llllll_opy_
  bstack1l1ll1lll1_opy_ = bstack1ll1llllll_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1ll1l11_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࡟ࡢࡴࡵࠫண")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1ll1l11_opy_ (u"ࠬ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡧࡲࡳࠩத")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l1ll1lll1_opy_
def bstack11lll1ll11_opy_(runner, hook_name, context, element, bstack1llllllll_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack11l1ll1l11_opy_.bstack1lll11ll1l_opy_(hook_name, element)
    bstack1llllllll_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack11l1ll1l11_opy_.bstack11l1ll11l1_opy_(element)
      if hook_name not in [bstack1ll1l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪ஥"), bstack1ll1l11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪ஦")] and args and hasattr(args[0], bstack1ll1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨ஧")):
        args[0].error_message = bstack1ll1l11_opy_ (u"ࠩࠪந")
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡨࡢࡰࡧࡰࡪࠦࡨࡰࡱ࡮ࡷࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬன").format(str(e)))
@measure(event_name=EVENTS.bstack1l111l1l1_opy_, stage=STAGE.bstack1l11lll1l_opy_, hook_type=bstack1ll1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡅࡱࡲࠢப"), bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack11l11ll11l_opy_(runner, name, context, bstack1llllllll_opy_, *args):
    if runner.hooks.get(bstack1ll1l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ஫")).__name__ != bstack1ll1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢࡨࡪ࡬ࡡࡶ࡮ࡷࡣ࡭ࡵ࡯࡬ࠤ஬"):
      bstack11lll1ll11_opy_(runner, name, context, runner, bstack1llllllll_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1l11l111l1_opy_(bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭஭")) else context.browser
      runner.driver_initialised = bstack1ll1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧம")
    except Exception as e:
      logger.debug(bstack1ll1l11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦ࠼ࠣࡿࢂ࠭ய").format(str(e)))
def bstack1ll11111l1_opy_(runner, name, context, bstack1llllllll_opy_, *args):
    bstack11lll1ll11_opy_(runner, name, context, context.feature, bstack1llllllll_opy_, *args)
    try:
      if not bstack11l11ll111_opy_:
        bstack11ll1l1111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11l111l1_opy_(bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩர")) else context.browser
        if is_driver_active(bstack11ll1l1111_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1ll1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧற")
          bstack1llll11ll1_opy_ = str(runner.feature.name)
          bstack1lllll1l11_opy_(context, bstack1llll11ll1_opy_)
          bstack11ll1l1111_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪல") + json.dumps(bstack1llll11ll1_opy_) + bstack1ll1l11_opy_ (u"࠭ࡽࡾࠩள"))
    except Exception as e:
      logger.debug(bstack1ll1l11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧழ").format(str(e)))
def bstack1ll1ll111l_opy_(runner, name, context, bstack1llllllll_opy_, *args):
    if hasattr(context, bstack1ll1l11_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪவ")):
        bstack11l1ll1l11_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack1ll1l11_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫஶ")) else context.feature
    bstack11lll1ll11_opy_(runner, name, context, target, bstack1llllllll_opy_, *args)
@measure(event_name=EVENTS.bstack1l11l11ll_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1l11l1l11_opy_(runner, name, context, bstack1llllllll_opy_, *args):
    if len(context.scenario.tags) == 0: bstack11l1ll1l11_opy_.start_test(context)
    bstack11lll1ll11_opy_(runner, name, context, context.scenario, bstack1llllllll_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack111llllll_opy_.bstack1llll1111_opy_(context, *args)
    try:
      bstack11ll1l1111_opy_ = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩஷ"), context.browser)
      if is_driver_active(bstack11ll1l1111_opy_):
        bstack1ll1l11l1l_opy_.bstack1ll11ll11_opy_(bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪஸ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll1l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢஹ")
        if (not bstack11l11ll111_opy_):
          scenario_name = args[0].name
          feature_name = bstack1llll11ll1_opy_ = str(runner.feature.name)
          bstack1llll11ll1_opy_ = feature_name + bstack1ll1l11_opy_ (u"࠭ࠠ࠮ࠢࠪ஺") + scenario_name
          if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ஻"):
            bstack1lllll1l11_opy_(context, bstack1llll11ll1_opy_)
            bstack11ll1l1111_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭஼") + json.dumps(bstack1llll11ll1_opy_) + bstack1ll1l11_opy_ (u"ࠩࢀࢁࠬ஽"))
    except Exception as e:
      logger.debug(bstack1ll1l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫா").format(str(e)))
@measure(event_name=EVENTS.bstack1l111l1l1_opy_, stage=STAGE.bstack1l11lll1l_opy_, hook_type=bstack1ll1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡗࡹ࡫ࡰࠣி"), bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1llllll111_opy_(runner, name, context, bstack1llllllll_opy_, *args):
    bstack11lll1ll11_opy_(runner, name, context, args[0], bstack1llllllll_opy_, *args)
    try:
      bstack11ll1l1111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11l111l1_opy_(bstack1ll1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫீ")) else context.browser
      if is_driver_active(bstack11ll1l1111_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦு")
        bstack11l1ll1l11_opy_.bstack1l111ll1l_opy_(args[0])
        if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧூ"):
          feature_name = bstack1llll11ll1_opy_ = str(runner.feature.name)
          bstack1llll11ll1_opy_ = feature_name + bstack1ll1l11_opy_ (u"ࠨࠢ࠰ࠤࠬ௃") + context.scenario.name
          bstack11ll1l1111_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ௄") + json.dumps(bstack1llll11ll1_opy_) + bstack1ll1l11_opy_ (u"ࠪࢁࢂ࠭௅"))
    except Exception as e:
      logger.debug(bstack1ll1l11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡵࡧࡳ࠾ࠥࢁࡽࠨெ").format(str(e)))
@measure(event_name=EVENTS.bstack1l111l1l1_opy_, stage=STAGE.bstack1l11lll1l_opy_, hook_type=bstack1ll1l11_opy_ (u"ࠧࡧࡦࡵࡧࡵࡗࡹ࡫ࡰࠣே"), bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1111ll11_opy_(runner, name, context, bstack1llllllll_opy_, *args):
  bstack11l1ll1l11_opy_.bstack1llll11111_opy_(args[0])
  try:
    bstack1l11l1l1l1_opy_ = args[0].status.name
    bstack11ll1l1111_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬை") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack11ll1l1111_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1ll1l11_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧ௉")
        feature_name = bstack1llll11ll1_opy_ = str(runner.feature.name)
        bstack1llll11ll1_opy_ = feature_name + bstack1ll1l11_opy_ (u"ࠨࠢ࠰ࠤࠬொ") + context.scenario.name
        bstack11ll1l1111_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧோ") + json.dumps(bstack1llll11ll1_opy_) + bstack1ll1l11_opy_ (u"ࠪࢁࢂ࠭ௌ"))
    if str(bstack1l11l1l1l1_opy_).lower() == bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧ்ࠫ"):
      bstack11l1l1l111_opy_ = bstack1ll1l11_opy_ (u"ࠬ࠭௎")
      bstack1l1111l1ll_opy_ = bstack1ll1l11_opy_ (u"࠭ࠧ௏")
      bstack1l1ll1l1l_opy_ = bstack1ll1l11_opy_ (u"ࠧࠨௐ")
      try:
        import traceback
        bstack11l1l1l111_opy_ = runner.exception.__class__.__name__
        bstack1ll11ll1ll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l1111l1ll_opy_ = bstack1ll1l11_opy_ (u"ࠨࠢࠪ௑").join(bstack1ll11ll1ll_opy_)
        bstack1l1ll1l1l_opy_ = bstack1ll11ll1ll_opy_[-1]
      except Exception as e:
        logger.debug(bstack11lllll1l_opy_.format(str(e)))
      bstack11l1l1l111_opy_ += bstack1l1ll1l1l_opy_
      bstack11l11111_opy_(context, json.dumps(str(args[0].name) + bstack1ll1l11_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ௒") + str(bstack1l1111l1ll_opy_)),
                          bstack1ll1l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ௓"))
      if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ௔"):
        bstack11llllll1_opy_(getattr(context, bstack1ll1l11_opy_ (u"ࠬࡶࡡࡨࡧࠪ௕"), None), bstack1ll1l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ௖"), bstack11l1l1l111_opy_)
        bstack11ll1l1111_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬௗ") + json.dumps(str(args[0].name) + bstack1ll1l11_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢ௘") + str(bstack1l1111l1ll_opy_)) + bstack1ll1l11_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩ௙"))
      if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ௚"):
        bstack11lll1l11_opy_(bstack11ll1l1111_opy_, bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ௛"), bstack1ll1l11_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ௜") + str(bstack11l1l1l111_opy_))
    else:
      bstack11l11111_opy_(context, bstack1ll1l11_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢ௝"), bstack1ll1l11_opy_ (u"ࠢࡪࡰࡩࡳࠧ௞"))
      if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ௟"):
        bstack11llllll1_opy_(getattr(context, bstack1ll1l11_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ௠"), None), bstack1ll1l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ௡"))
      bstack11ll1l1111_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ௢") + json.dumps(str(args[0].name) + bstack1ll1l11_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤ௣")) + bstack1ll1l11_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ௤"))
      if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ௥"):
        bstack11lll1l11_opy_(bstack11ll1l1111_opy_, bstack1ll1l11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ௦"))
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡳࡵࡧࡳ࠾ࠥࢁࡽࠨ௧").format(str(e)))
  bstack11lll1ll11_opy_(runner, name, context, args[0], bstack1llllllll_opy_, *args)
@measure(event_name=EVENTS.bstack1l111l11ll_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1llll11l1_opy_(runner, name, context, bstack1llllllll_opy_, *args):
  bstack11l1ll1l11_opy_.end_test(args[0])
  try:
    bstack1l11111ll_opy_ = args[0].status.name
    bstack11ll1l1111_opy_ = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ௨"), context.browser)
    bstack111llllll_opy_.bstack1ll1lll1ll_opy_(bstack11ll1l1111_opy_)
    if str(bstack1l11111ll_opy_).lower() == bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ௩"):
      bstack11l1l1l111_opy_ = bstack1ll1l11_opy_ (u"ࠬ࠭௪")
      bstack1l1111l1ll_opy_ = bstack1ll1l11_opy_ (u"࠭ࠧ௫")
      bstack1l1ll1l1l_opy_ = bstack1ll1l11_opy_ (u"ࠧࠨ௬")
      try:
        import traceback
        bstack11l1l1l111_opy_ = runner.exception.__class__.__name__
        bstack1ll11ll1ll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l1111l1ll_opy_ = bstack1ll1l11_opy_ (u"ࠨࠢࠪ௭").join(bstack1ll11ll1ll_opy_)
        bstack1l1ll1l1l_opy_ = bstack1ll11ll1ll_opy_[-1]
      except Exception as e:
        logger.debug(bstack11lllll1l_opy_.format(str(e)))
      bstack11l1l1l111_opy_ += bstack1l1ll1l1l_opy_
      bstack11l11111_opy_(context, json.dumps(str(args[0].name) + bstack1ll1l11_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ௮") + str(bstack1l1111l1ll_opy_)),
                          bstack1ll1l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ௯"))
      if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ௰") or runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ௱"):
        bstack11llllll1_opy_(getattr(context, bstack1ll1l11_opy_ (u"࠭ࡰࡢࡩࡨࠫ௲"), None), bstack1ll1l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ௳"), bstack11l1l1l111_opy_)
        bstack11ll1l1111_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭௴") + json.dumps(str(args[0].name) + bstack1ll1l11_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ௵") + str(bstack1l1111l1ll_opy_)) + bstack1ll1l11_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪ௶"))
      if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ௷") or runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ௸"):
        bstack11lll1l11_opy_(bstack11ll1l1111_opy_, bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭௹"), bstack1ll1l11_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦ௺") + str(bstack11l1l1l111_opy_))
    else:
      bstack11l11111_opy_(context, bstack1ll1l11_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤ௻"), bstack1ll1l11_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢ௼"))
      if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ௽") or runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫ௾"):
        bstack11llllll1_opy_(getattr(context, bstack1ll1l11_opy_ (u"ࠬࡶࡡࡨࡧࠪ௿"), None), bstack1ll1l11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨఀ"))
      bstack11ll1l1111_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬఁ") + json.dumps(str(args[0].name) + bstack1ll1l11_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧం")) + bstack1ll1l11_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨః"))
      if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧఄ") or runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫఅ"):
        bstack11lll1l11_opy_(bstack11ll1l1111_opy_, bstack1ll1l11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧఆ"))
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨఇ").format(str(e)))
  bstack11lll1ll11_opy_(runner, name, context, context.scenario, bstack1llllllll_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l1llll1l1_opy_(runner, name, context, bstack1llllllll_opy_, *args):
    target = context.scenario if hasattr(context, bstack1ll1l11_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩఈ")) else context.feature
    bstack11lll1ll11_opy_(runner, name, context, target, bstack1llllllll_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1lll1111l_opy_(runner, name, context, bstack1llllllll_opy_, *args):
    try:
      bstack11ll1l1111_opy_ = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧఉ"), context.browser)
      bstack111l11l1l_opy_ = bstack1ll1l11_opy_ (u"ࠩࠪఊ")
      if context.failed is True:
        bstack1llll1lll1_opy_ = []
        bstack11ll1111l_opy_ = []
        bstack1l1ll1l111_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1llll1lll1_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1ll11ll1ll_opy_ = traceback.format_tb(exc_tb)
            bstack1ll1llll1_opy_ = bstack1ll1l11_opy_ (u"ࠪࠤࠬఋ").join(bstack1ll11ll1ll_opy_)
            bstack11ll1111l_opy_.append(bstack1ll1llll1_opy_)
            bstack1l1ll1l111_opy_.append(bstack1ll11ll1ll_opy_[-1])
        except Exception as e:
          logger.debug(bstack11lllll1l_opy_.format(str(e)))
        bstack11l1l1l111_opy_ = bstack1ll1l11_opy_ (u"ࠫࠬఌ")
        for i in range(len(bstack1llll1lll1_opy_)):
          bstack11l1l1l111_opy_ += bstack1llll1lll1_opy_[i] + bstack1l1ll1l111_opy_[i] + bstack1ll1l11_opy_ (u"ࠬࡢ࡮ࠨ఍")
        bstack111l11l1l_opy_ = bstack1ll1l11_opy_ (u"࠭ࠠࠨఎ").join(bstack11ll1111l_opy_)
        if runner.driver_initialised in [bstack1ll1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣఏ"), bstack1ll1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧఐ")]:
          bstack11l11111_opy_(context, bstack111l11l1l_opy_, bstack1ll1l11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ఑"))
          bstack11llllll1_opy_(getattr(context, bstack1ll1l11_opy_ (u"ࠪࡴࡦ࡭ࡥࠨఒ"), None), bstack1ll1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦఓ"), bstack11l1l1l111_opy_)
          bstack11ll1l1111_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪఔ") + json.dumps(bstack111l11l1l_opy_) + bstack1ll1l11_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭క"))
          bstack11lll1l11_opy_(bstack11ll1l1111_opy_, bstack1ll1l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢఖ"), bstack1ll1l11_opy_ (u"ࠣࡕࡲࡱࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯ࡴࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡠࡳࠨగ") + str(bstack11l1l1l111_opy_))
          bstack11ll1llll_opy_ = bstack11lll111l_opy_(bstack111l11l1l_opy_, runner.feature.name, logger)
          if (bstack11ll1llll_opy_ != None):
            bstack1l1lllllll_opy_.append(bstack11ll1llll_opy_)
      else:
        if runner.driver_initialised in [bstack1ll1l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥఘ"), bstack1ll1l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢఙ")]:
          bstack11l11111_opy_(context, bstack1ll1l11_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢచ") + str(runner.feature.name) + bstack1ll1l11_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢఛ"), bstack1ll1l11_opy_ (u"ࠨࡩ࡯ࡨࡲࠦజ"))
          bstack11llllll1_opy_(getattr(context, bstack1ll1l11_opy_ (u"ࠧࡱࡣࡪࡩࠬఝ"), None), bstack1ll1l11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣఞ"))
          bstack11ll1l1111_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧట") + json.dumps(bstack1ll1l11_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨఠ") + str(runner.feature.name) + bstack1ll1l11_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨడ")) + bstack1ll1l11_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫఢ"))
          bstack11lll1l11_opy_(bstack11ll1l1111_opy_, bstack1ll1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ణ"))
          bstack11ll1llll_opy_ = bstack11lll111l_opy_(bstack111l11l1l_opy_, runner.feature.name, logger)
          if (bstack11ll1llll_opy_ != None):
            bstack1l1lllllll_opy_.append(bstack11ll1llll_opy_)
    except Exception as e:
      logger.debug(bstack1ll1l11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩత").format(str(e)))
    bstack11lll1ll11_opy_(runner, name, context, context.feature, bstack1llllllll_opy_, *args)
@measure(event_name=EVENTS.bstack1l111l1l1_opy_, stage=STAGE.bstack1l11lll1l_opy_, hook_type=bstack1ll1l11_opy_ (u"ࠣࡣࡩࡸࡪࡸࡁ࡭࡮ࠥథ"), bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1l11ll1l_opy_(runner, name, context, bstack1llllllll_opy_, *args):
    bstack11lll1ll11_opy_(runner, name, context, runner, bstack1llllllll_opy_, *args)
def bstack1lll1lll11_opy_(self, name, context, *args):
  if bstack1lll111ll1_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1l11lllll1_opy_
    bstack11lll1l1_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬద")][platform_index]
    os.environ[bstack1ll1l11_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫధ")] = json.dumps(bstack11lll1l1_opy_)
  global bstack1llllllll_opy_
  if not hasattr(self, bstack1ll1l11_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡥࡥࠩన")):
    self.driver_initialised = None
  bstack11ll111l1l_opy_ = {
      bstack1ll1l11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩ఩"): bstack11l11ll11l_opy_,
      bstack1ll1l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧప"): bstack1ll11111l1_opy_,
      bstack1ll1l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡵࡣࡪࠫఫ"): bstack1ll1ll111l_opy_,
      bstack1ll1l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪబ"): bstack1l11l1l11_opy_,
      bstack1ll1l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠧభ"): bstack1llllll111_opy_,
      bstack1ll1l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶࠧమ"): bstack1111ll11_opy_,
      bstack1ll1l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬయ"): bstack1llll11l1_opy_,
      bstack1ll1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡹࡧࡧࠨర"): bstack1l1llll1l1_opy_,
      bstack1ll1l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ఱ"): bstack1lll1111l_opy_,
      bstack1ll1l11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪల"): bstack1l11ll1l_opy_
  }
  handler = bstack11ll111l1l_opy_.get(name, bstack1llllllll_opy_)
  handler(self, name, context, bstack1llllllll_opy_, *args)
  if name in [bstack1ll1l11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨళ"), bstack1ll1l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪఴ"), bstack1ll1l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭వ")]:
    try:
      bstack11ll1l1111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11l111l1_opy_(bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪశ")) else context.browser
      bstack1111ll11l_opy_ = (
        (name == bstack1ll1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨష") and self.driver_initialised == bstack1ll1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥస")) or
        (name == bstack1ll1l11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧహ") and self.driver_initialised == bstack1ll1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤ఺")) or
        (name == bstack1ll1l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ఻") and self.driver_initialised in [bstack1ll1l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳ఼ࠧ"), bstack1ll1l11_opy_ (u"ࠦ࡮ࡴࡳࡵࡧࡳࠦఽ")]) or
        (name == bstack1ll1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩా") and self.driver_initialised == bstack1ll1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦి"))
      )
      if bstack1111ll11l_opy_:
        self.driver_initialised = None
        bstack11ll1l1111_opy_.quit()
    except Exception:
      pass
def bstack111l11ll1_opy_(config, startdir):
  return bstack1ll1l11_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧీ").format(bstack1ll1l11_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢు"))
notset = Notset()
def bstack1l1l1l1l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11ll11l1_opy_
  if str(name).lower() == bstack1ll1l11_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩూ"):
    return bstack1ll1l11_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤృ")
  else:
    return bstack11ll11l1_opy_(self, name, default, skip)
def bstack1lll1l11l1_opy_(item, when):
  global bstack1l11ll111_opy_
  try:
    bstack1l11ll111_opy_(item, when)
  except Exception as e:
    pass
def bstack11llll1111_opy_():
  return
def bstack111lll111_opy_(type, name, status, reason, bstack1l111lllll_opy_, bstack11lll11111_opy_):
  bstack1l1ll111ll_opy_ = {
    bstack1ll1l11_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫౄ"): type,
    bstack1ll1l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ౅"): {}
  }
  if type == bstack1ll1l11_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨె"):
    bstack1l1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪే")][bstack1ll1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧై")] = bstack1l111lllll_opy_
    bstack1l1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ౉")][bstack1ll1l11_opy_ (u"ࠪࡨࡦࡺࡡࠨొ")] = json.dumps(str(bstack11lll11111_opy_))
  if type == bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬో"):
    bstack1l1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨౌ")][bstack1ll1l11_opy_ (u"࠭࡮ࡢ࡯ࡨ్ࠫ")] = name
  if type == bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ౎"):
    bstack1l1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ౏")][bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ౐")] = status
    if status == bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ౑"):
      bstack1l1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ౒")][bstack1ll1l11_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ౓")] = json.dumps(str(reason))
  bstack11ll111l11_opy_ = bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ౔").format(json.dumps(bstack1l1ll111ll_opy_))
  return bstack11ll111l11_opy_
def bstack1ll1l11lll_opy_(driver_command, response):
    if driver_command == bstack1ll1l11_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷౕࠫ"):
        bstack1ll1l11l1l_opy_.bstack1ll1llll11_opy_({
            bstack1ll1l11_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ౖࠧ"): response[bstack1ll1l11_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ౗")],
            bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪౘ"): bstack1ll1l11l1l_opy_.current_test_uuid()
        })
def bstack1l1ll11ll_opy_(item, call, rep):
  global bstack1l11l1l1l_opy_
  global bstack1lll11111_opy_
  global bstack11l11ll111_opy_
  name = bstack1ll1l11_opy_ (u"ࠫࠬౙ")
  try:
    if rep.when == bstack1ll1l11_opy_ (u"ࠬࡩࡡ࡭࡮ࠪౚ"):
      bstack1lllllll1l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack11l11ll111_opy_:
          name = str(rep.nodeid)
          bstack111ll1lll_opy_ = bstack111lll111_opy_(bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ౛"), name, bstack1ll1l11_opy_ (u"ࠧࠨ౜"), bstack1ll1l11_opy_ (u"ࠨࠩౝ"), bstack1ll1l11_opy_ (u"ࠩࠪ౞"), bstack1ll1l11_opy_ (u"ࠪࠫ౟"))
          threading.current_thread().bstack1111111ll_opy_ = name
          for driver in bstack1lll11111_opy_:
            if bstack1lllllll1l_opy_ == driver.session_id:
              driver.execute_script(bstack111ll1lll_opy_)
      except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫౠ").format(str(e)))
      try:
        bstack1l1lll1l1l_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1ll1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ౡ"):
          status = bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ౢ") if rep.outcome.lower() == bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧౣ") else bstack1ll1l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ౤")
          reason = bstack1ll1l11_opy_ (u"ࠩࠪ౥")
          if status == bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ౦"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ౧") if status == bstack1ll1l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ౨") else bstack1ll1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ౩")
          data = name + bstack1ll1l11_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ౪") if status == bstack1ll1l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ౫") else name + bstack1ll1l11_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬ౬") + reason
          bstack1ll1l1l11_opy_ = bstack111lll111_opy_(bstack1ll1l11_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ౭"), bstack1ll1l11_opy_ (u"ࠫࠬ౮"), bstack1ll1l11_opy_ (u"ࠬ࠭౯"), bstack1ll1l11_opy_ (u"࠭ࠧ౰"), level, data)
          for driver in bstack1lll11111_opy_:
            if bstack1lllllll1l_opy_ == driver.session_id:
              driver.execute_script(bstack1ll1l1l11_opy_)
      except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ౱").format(str(e)))
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬ౲").format(str(e)))
  bstack1l11l1l1l_opy_(item, call, rep)
def bstack11llll1l_opy_(driver, bstack1ll11l1l1_opy_, test=None):
  global bstack1ll1ll11l_opy_
  if test != None:
    bstack1l1111ll1l_opy_ = getattr(test, bstack1ll1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ౳"), None)
    bstack1lllll1111_opy_ = getattr(test, bstack1ll1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ౴"), None)
    PercySDK.screenshot(driver, bstack1ll11l1l1_opy_, bstack1l1111ll1l_opy_=bstack1l1111ll1l_opy_, bstack1lllll1111_opy_=bstack1lllll1111_opy_, bstack1ll11lll_opy_=bstack1ll1ll11l_opy_)
  else:
    PercySDK.screenshot(driver, bstack1ll11l1l1_opy_)
@measure(event_name=EVENTS.bstack1ll1111l_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1l111l1l_opy_(driver):
  if bstack111ll1l1l_opy_.bstack11l1l1lll1_opy_() is True or bstack111ll1l1l_opy_.capturing() is True:
    return
  bstack111ll1l1l_opy_.bstack1lll1l1l1_opy_()
  while not bstack111ll1l1l_opy_.bstack11l1l1lll1_opy_():
    bstack1l1lll11_opy_ = bstack111ll1l1l_opy_.bstack11l1lll11_opy_()
    bstack11llll1l_opy_(driver, bstack1l1lll11_opy_)
  bstack111ll1l1l_opy_.bstack1llllll11l_opy_()
def bstack1llll1l1ll_opy_(sequence, driver_command, response = None, bstack1l1llll1l_opy_ = None, args = None):
    try:
      if sequence != bstack1ll1l11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ౵"):
        return
      if percy.bstack11l1ll1lll_opy_() == bstack1ll1l11_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦ౶"):
        return
      bstack1l1lll11_opy_ = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ౷"), None)
      for command in bstack1ll11ll1_opy_:
        if command == driver_command:
          for driver in bstack1lll11111_opy_:
            bstack1l111l1l_opy_(driver)
      bstack1l1lllll11_opy_ = percy.bstack111llll11_opy_()
      if driver_command in bstack1lll11ll_opy_[bstack1l1lllll11_opy_]:
        bstack111ll1l1l_opy_.bstack111111111_opy_(bstack1l1lll11_opy_, driver_command)
    except Exception as e:
      pass
def bstack1ll1lll1l1_opy_(framework_name):
  if bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ౸")):
      return
  bstack11lll1111_opy_.bstack1lll11lll1_opy_(bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬ౹"), True)
  global bstack1l111111ll_opy_
  global bstack1l1ll1lll_opy_
  global bstack11llllllll_opy_
  bstack1l111111ll_opy_ = framework_name
  logger.info(bstack1111lll1l_opy_.format(bstack1l111111ll_opy_.split(bstack1ll1l11_opy_ (u"ࠩ࠰ࠫ౺"))[0]))
  bstack1ll1l11ll1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1lll111ll1_opy_:
      Service.start = bstack11lllll11_opy_
      Service.stop = bstack1l1lll1l_opy_
      webdriver.Remote.get = bstack1l1l1llll_opy_
      WebDriver.close = bstack1l111111l_opy_
      WebDriver.quit = bstack1ll11111_opy_
      webdriver.Remote.__init__ = bstack1111l11l1_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1lll111ll1_opy_:
        webdriver.Remote.__init__ = bstack11ll111l_opy_
    WebDriver.execute = bstack11l111ll_opy_
    bstack1l1ll1lll_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1lll111ll1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack111l111ll_opy_
  except Exception as e:
    pass
  bstack111llll1_opy_()
  if not bstack1l1ll1lll_opy_:
    bstack11l1llll1_opy_(bstack1ll1l11_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧ౻"), bstack1l111l1111_opy_)
  if bstack11l1lll11l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._11l11lllll_opy_ = bstack1l1l1l1ll1_opy_
    except Exception as e:
      logger.error(bstack1ll111llll_opy_.format(str(e)))
  if bstack1ll1l1lll1_opy_():
    bstack1l1l11l1_opy_(CONFIG, logger)
  if (bstack1ll1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ౼") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack11l1ll1lll_opy_() == bstack1ll1l11_opy_ (u"ࠧࡺࡲࡶࡧࠥ౽"):
          bstack1l1l1ll11_opy_(bstack1llll1l1ll_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l11l11111_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1ll1l1l111_opy_
      except Exception as e:
        logger.warn(bstack1lll11l1ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack11ll1l111_opy_
      except Exception as e:
        logger.debug(bstack1l1llll1ll_opy_ + str(e))
    except Exception as e:
      bstack11l1llll1_opy_(e, bstack1lll11l1ll_opy_)
    Output.start_test = bstack1ll1l11111_opy_
    Output.end_test = bstack111ll11l1_opy_
    TestStatus.__init__ = bstack111ll1l1_opy_
    QueueItem.__init__ = bstack1l11lll1ll_opy_
    pabot._create_items = bstack1ll111l1l_opy_
    try:
      from pabot import __version__ as bstack1l11ll1111_opy_
      if version.parse(bstack1l11ll1111_opy_) >= version.parse(bstack1ll1l11_opy_ (u"࠭࠴࠯࠴࠱࠴ࠬ౾")):
        pabot._run = bstack1l11l111ll_opy_
      elif version.parse(bstack1l11ll1111_opy_) >= version.parse(bstack1ll1l11_opy_ (u"ࠧ࠳࠰࠴࠹࠳࠶ࠧ౿")):
        pabot._run = bstack1lll1ll1l_opy_
      elif version.parse(bstack1l11ll1111_opy_) >= version.parse(bstack1ll1l11_opy_ (u"ࠨ࠴࠱࠵࠸࠴࠰ࠨಀ")):
        pabot._run = bstack1lll1lll1_opy_
      else:
        pabot._run = bstack1l1ll1l11l_opy_
    except Exception as e:
      pabot._run = bstack1l1ll1l11l_opy_
    pabot._create_command_for_execution = bstack1llll1ll_opy_
    pabot._report_results = bstack11lll111l1_opy_
  if bstack1ll1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩಁ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l1llll1_opy_(e, bstack11l1l1ll_opy_)
    Runner.run_hook = bstack1lll1lll11_opy_
    Step.run = bstack1lllll1lll_opy_
  if bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪಂ") in str(framework_name).lower():
    if not bstack1lll111ll1_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack111l11ll1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack11llll1111_opy_
      Config.getoption = bstack1l1l1l1l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l1ll11ll_opy_
    except Exception as e:
      pass
def bstack11l1ll1ll_opy_():
  global CONFIG
  if bstack1ll1l11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫಃ") in CONFIG and int(CONFIG[bstack1ll1l11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ಄")]) > 1:
    logger.warn(bstack1l11llll1_opy_)
def bstack1l1l11lll1_opy_(arg, bstack111l1l1l_opy_, bstack111l11ll_opy_=None):
  global CONFIG
  global bstack1l11ll1lll_opy_
  global bstack11l1llll1l_opy_
  global bstack1lll111ll1_opy_
  global bstack11lll1111_opy_
  bstack11l1l111ll_opy_ = bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ಅ")
  if bstack111l1l1l_opy_ and isinstance(bstack111l1l1l_opy_, str):
    bstack111l1l1l_opy_ = eval(bstack111l1l1l_opy_)
  CONFIG = bstack111l1l1l_opy_[bstack1ll1l11_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧಆ")]
  bstack1l11ll1lll_opy_ = bstack111l1l1l_opy_[bstack1ll1l11_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩಇ")]
  bstack11l1llll1l_opy_ = bstack111l1l1l_opy_[bstack1ll1l11_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫಈ")]
  bstack1lll111ll1_opy_ = bstack111l1l1l_opy_[bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ಉ")]
  bstack11lll1111_opy_.bstack1lll11lll1_opy_(bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬಊ"), bstack1lll111ll1_opy_)
  os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧಋ")] = bstack11l1l111ll_opy_
  os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬಌ")] = json.dumps(CONFIG)
  os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧ಍")] = bstack1l11ll1lll_opy_
  os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩಎ")] = str(bstack11l1llll1l_opy_)
  os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨಏ")] = str(True)
  if bstack1l1l1l11l_opy_(arg, [bstack1ll1l11_opy_ (u"ࠪ࠱ࡳ࠭ಐ"), bstack1ll1l11_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ಑")]) != -1:
    os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭ಒ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11ll11l11_opy_)
    return
  bstack1ll1l111l1_opy_()
  global bstack1ll111l11_opy_
  global bstack1ll1ll11l_opy_
  global bstack11l1111ll_opy_
  global bstack1lllll11l_opy_
  global bstack1lll1111_opy_
  global bstack11llllllll_opy_
  global bstack1l1l11l1l1_opy_
  arg.append(bstack1ll1l11_opy_ (u"ࠨ࠭ࡘࠤಓ"))
  arg.append(bstack1ll1l11_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡎࡱࡧࡹࡱ࡫ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡰࡴࡴࡸࡴࡦࡦ࠽ࡴࡾࡺࡥࡴࡶ࠱ࡔࡾࡺࡥࡴࡶ࡚ࡥࡷࡴࡩ࡯ࡩࠥಔ"))
  arg.append(bstack1ll1l11_opy_ (u"ࠣ࠯࡚ࠦಕ"))
  arg.append(bstack1ll1l11_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡗ࡬ࡪࠦࡨࡰࡱ࡮࡭ࡲࡶ࡬ࠣಖ"))
  global bstack111llll1l_opy_
  global bstack1l1lll11ll_opy_
  global bstack1ll1ll111_opy_
  global bstack1111ll1ll_opy_
  global bstack1lllllll1_opy_
  global bstack1ll1l1l1ll_opy_
  global bstack1l111lll1l_opy_
  global bstack11l111lll_opy_
  global bstack1ll1l11l1_opy_
  global bstack1l111l1l1l_opy_
  global bstack11ll11l1_opy_
  global bstack1l11ll111_opy_
  global bstack1l11l1l1l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack111llll1l_opy_ = webdriver.Remote.__init__
    bstack1l1lll11ll_opy_ = WebDriver.quit
    bstack11l111lll_opy_ = WebDriver.close
    bstack1ll1l11l1_opy_ = WebDriver.get
    bstack1ll1ll111_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1ll11l1ll_opy_(CONFIG) and bstack1l1ll11lll_opy_():
    if bstack1llll11ll_opy_() < version.parse(bstack1l1llll11l_opy_):
      logger.error(bstack1l1l1l1lll_opy_.format(bstack1llll11ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l111l1l1l_opy_ = RemoteConnection._11l11lllll_opy_
      except Exception as e:
        logger.error(bstack1ll111llll_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack11ll11l1_opy_ = Config.getoption
    from _pytest import runner
    bstack1l11ll111_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1lllll11ll_opy_)
  try:
    from pytest_bdd import reporting
    bstack1l11l1l1l_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫಗ"))
  bstack11l1111ll_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨಘ"), {}).get(bstack1ll1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧಙ"))
  bstack1l1l11l1l1_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack11ll111ll_opy_():
      bstack11ll11111l_opy_.invoke(bstack11lll1l1l1_opy_.CONNECT, bstack1l1ll1l1ll_opy_())
    platform_index = int(os.environ.get(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ಚ"), bstack1ll1l11_opy_ (u"ࠧ࠱ࠩಛ")))
  else:
    bstack1ll1lll1l1_opy_(bstack1l1l1l111_opy_)
  os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩಜ")] = CONFIG[bstack1ll1l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫಝ")]
  os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ಞ")] = CONFIG[bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧಟ")]
  os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨಠ")] = bstack1lll111ll1_opy_.__str__()
  from _pytest.config import main as bstack111l1111l_opy_
  bstack1111l1111_opy_ = []
  try:
    bstack1ll1lll1_opy_ = bstack111l1111l_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1111l1l1_opy_()
    if bstack1ll1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪಡ") in multiprocessing.current_process().__dict__.keys():
      for bstack1lll1l1lll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1111l1111_opy_.append(bstack1lll1l1lll_opy_)
    try:
      bstack11ll11ll_opy_ = (bstack1111l1111_opy_, int(bstack1ll1lll1_opy_))
      bstack111l11ll_opy_.append(bstack11ll11ll_opy_)
    except:
      bstack111l11ll_opy_.append((bstack1111l1111_opy_, bstack1ll1lll1_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1111l1111_opy_.append({bstack1ll1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಢ"): bstack1ll1l11_opy_ (u"ࠨࡒࡵࡳࡨ࡫ࡳࡴࠢࠪಣ") + os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩತ")), bstack1ll1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩಥ"): traceback.format_exc(), bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪದ"): int(os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬಧ")))})
    bstack111l11ll_opy_.append((bstack1111l1111_opy_, 1))
def bstack11l11l11l_opy_(arg):
  global bstack11l111l1l_opy_
  bstack1ll1lll1l1_opy_(bstack1ll11llll1_opy_)
  os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧನ")] = str(bstack11l1llll1l_opy_)
  from behave.__main__ import main as bstack111ll11ll_opy_
  status_code = bstack111ll11ll_opy_(arg)
  if status_code != 0:
    bstack11l111l1l_opy_ = status_code
def bstack11lllllll_opy_():
  logger.info(bstack11l1llll11_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭಩"), help=bstack1ll1l11_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࠩಪ"))
  parser.add_argument(bstack1ll1l11_opy_ (u"ࠩ࠰ࡹࠬಫ"), bstack1ll1l11_opy_ (u"ࠪ࠱࠲ࡻࡳࡦࡴࡱࡥࡲ࡫ࠧಬ"), help=bstack1ll1l11_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡷࡶࡩࡷࡴࡡ࡮ࡧࠪಭ"))
  parser.add_argument(bstack1ll1l11_opy_ (u"ࠬ࠳࡫ࠨಮ"), bstack1ll1l11_opy_ (u"࠭࠭࠮࡭ࡨࡽࠬಯ"), help=bstack1ll1l11_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡦࡩࡣࡦࡵࡶࠤࡰ࡫ࡹࠨರ"))
  parser.add_argument(bstack1ll1l11_opy_ (u"ࠨ࠯ࡩࠫಱ"), bstack1ll1l11_opy_ (u"ࠩ࠰࠱࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧಲ"), help=bstack1ll1l11_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩಳ"))
  bstack1llll11l11_opy_ = parser.parse_args()
  try:
    bstack1ll1l1ll11_opy_ = bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡫ࡪࡴࡥࡳ࡫ࡦ࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨ಴")
    if bstack1llll11l11_opy_.framework and bstack1llll11l11_opy_.framework not in (bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬವ"), bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧಶ")):
      bstack1ll1l1ll11_opy_ = bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ಷ")
    bstack11lll1lll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1l1ll11_opy_)
    bstack1l1lllll1l_opy_ = open(bstack11lll1lll_opy_, bstack1ll1l11_opy_ (u"ࠨࡴࠪಸ"))
    bstack1l1l111l_opy_ = bstack1l1lllll1l_opy_.read()
    bstack1l1lllll1l_opy_.close()
    if bstack1llll11l11_opy_.username:
      bstack1l1l111l_opy_ = bstack1l1l111l_opy_.replace(bstack1ll1l11_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩಹ"), bstack1llll11l11_opy_.username)
    if bstack1llll11l11_opy_.key:
      bstack1l1l111l_opy_ = bstack1l1l111l_opy_.replace(bstack1ll1l11_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬ಺"), bstack1llll11l11_opy_.key)
    if bstack1llll11l11_opy_.framework:
      bstack1l1l111l_opy_ = bstack1l1l111l_opy_.replace(bstack1ll1l11_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ಻"), bstack1llll11l11_opy_.framework)
    file_name = bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨ಼")
    file_path = os.path.abspath(file_name)
    bstack1lll1ll1l1_opy_ = open(file_path, bstack1ll1l11_opy_ (u"࠭ࡷࠨಽ"))
    bstack1lll1ll1l1_opy_.write(bstack1l1l111l_opy_)
    bstack1lll1ll1l1_opy_.close()
    logger.info(bstack11lll11lll_opy_)
    try:
      os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩಾ")] = bstack1llll11l11_opy_.framework if bstack1llll11l11_opy_.framework != None else bstack1ll1l11_opy_ (u"ࠣࠤಿ")
      config = yaml.safe_load(bstack1l1l111l_opy_)
      config[bstack1ll1l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩೀ")] = bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰ࡷࡪࡺࡵࡱࠩು")
      bstack1llllll11_opy_(bstack1ll1ll1ll1_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1l1l1ll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1l11ll1l1_opy_.format(str(e)))
def bstack1llllll11_opy_(bstack1l11l1ll1l_opy_, config, bstack11ll1lll1l_opy_={}):
  global bstack1lll111ll1_opy_
  global bstack11l1l11lll_opy_
  global bstack11lll1111_opy_
  if not config:
    return
  bstack1l11lll1_opy_ = bstack1lll11l1l_opy_ if not bstack1lll111ll1_opy_ else (
    bstack1l11l1111l_opy_ if bstack1ll1l11_opy_ (u"ࠫࡦࡶࡰࠨೂ") in config else (
        bstack111l1l11l_opy_ if config.get(bstack1ll1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩೃ")) else bstack11l1l1l1l1_opy_
    )
)
  bstack1l11l1lll1_opy_ = False
  bstack1l1l11ll11_opy_ = False
  if bstack1lll111ll1_opy_ is True:
      if bstack1ll1l11_opy_ (u"࠭ࡡࡱࡲࠪೄ") in config:
          bstack1l11l1lll1_opy_ = True
      else:
          bstack1l1l11ll11_opy_ = True
  bstack1l111111l1_opy_ = bstack11l11l1ll1_opy_.bstack1l1ll11l_opy_(config, bstack11l1l11lll_opy_)
  bstack1ll11ll1l_opy_ = bstack1l1l1l1l1_opy_()
  data = {
    bstack1ll1l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ೅"): config[bstack1ll1l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪೆ")],
    bstack1ll1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬೇ"): config[bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ೈ")],
    bstack1ll1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ೉"): bstack1l11l1ll1l_opy_,
    bstack1ll1l11_opy_ (u"ࠬࡪࡥࡵࡧࡦࡸࡪࡪࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩೊ"): os.environ.get(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨೋ"), bstack11l1l11lll_opy_),
    bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩೌ"): bstack111ll1ll1_opy_,
    bstack1ll1l11_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮್ࠪ"): bstack1llll1l1_opy_(),
    bstack1ll1l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ೎"): {
      bstack1ll1l11_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ೏"): str(config[bstack1ll1l11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ೐")]) if bstack1ll1l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ೑") in config else bstack1ll1l11_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢ೒"),
      bstack1ll1l11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡘࡨࡶࡸ࡯࡯࡯ࠩ೓"): sys.version,
      bstack1ll1l11_opy_ (u"ࠨࡴࡨࡪࡪࡸࡲࡦࡴࠪ೔"): bstack1l1l111l1l_opy_(os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫೕ"), bstack11l1l11lll_opy_)),
      bstack1ll1l11_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬೖ"): bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ೗"),
      bstack1ll1l11_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭೘"): bstack1l11lll1_opy_,
      bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫ೙"): bstack1l111111l1_opy_,
      bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡠࡷࡸ࡭ࡩ࠭೚"): os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭೛")],
      bstack1ll1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ೜"): os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬೝ"), bstack11l1l11lll_opy_),
      bstack1ll1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧೞ"): bstack1l1lll111l_opy_(os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ೟"), bstack11l1l11lll_opy_)),
      bstack1ll1l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬೠ"): bstack1ll11ll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬೡ")),
      bstack1ll1l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧೢ"): bstack1ll11ll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪೣ")),
      bstack1ll1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭೤"): config[bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ೥")] if config[bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ೦")] else bstack1ll1l11_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢ೧"),
      bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ೨"): str(config[bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ೩")]) if bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ೪") in config else bstack1ll1l11_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦ೫"),
      bstack1ll1l11_opy_ (u"ࠫࡴࡹࠧ೬"): sys.platform,
      bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧ೭"): socket.gethostname(),
      bstack1ll1l11_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ೮"): bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩ೯"))
    }
  }
  if not bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨ೰")) is None:
    data[bstack1ll1l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬೱ")][bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡒ࡫ࡴࡢࡦࡤࡸࡦ࠭ೲ")] = {
      bstack1ll1l11_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫೳ"): bstack1ll1l11_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦࠪ೴"),
      bstack1ll1l11_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭೵"): bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧ೶")),
      bstack1ll1l11_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࡏࡷࡰࡦࡪࡸࠧ೷"): bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬ೸"))
    }
  if bstack1l11l1ll1l_opy_ == bstack11lll11l11_opy_:
    data[bstack1ll1l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭೹")][bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡆࡳࡳ࡬ࡩࡨࠩ೺")] = bstack1ll1111ll1_opy_(config)
    data[bstack1ll1l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ೻")][bstack1ll1l11_opy_ (u"࠭ࡩࡴࡒࡨࡶࡨࡿࡁࡶࡶࡲࡉࡳࡧࡢ࡭ࡧࡧࠫ೼")] = percy.bstack11l1l11ll1_opy_
    data[bstack1ll1l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ೽")][bstack1ll1l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡂࡶ࡫࡯ࡨࡎࡪࠧ೾")] = percy.percy_build_id
  update(data[bstack1ll1l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ೿")], bstack11ll1lll1l_opy_)
  try:
    response = bstack11lllll1ll_opy_(bstack1ll1l11_opy_ (u"ࠪࡔࡔ࡙ࡔࠨഀ"), bstack1ll1l11l11_opy_(bstack11l1l1111l_opy_), data, {
      bstack1ll1l11_opy_ (u"ࠫࡦࡻࡴࡩࠩഁ"): (config[bstack1ll1l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧം")], config[bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩഃ")])
    })
    if response:
      logger.debug(bstack111l11l1_opy_.format(bstack1l11l1ll1l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11l1l11l_opy_.format(str(e)))
def bstack1l1l111l1l_opy_(framework):
  return bstack1ll1l11_opy_ (u"ࠢࡼࡿ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦഄ").format(str(framework), __version__) if framework else bstack1ll1l11_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤഅ").format(
    __version__)
def bstack1ll1l111l1_opy_():
  global CONFIG
  global bstack111l1lll_opy_
  if bool(CONFIG):
    return
  try:
    bstack1ll11l1ll1_opy_()
    logger.debug(bstack1llll111_opy_.format(str(CONFIG)))
    bstack111l1lll_opy_ = bstack1ll1lllll_opy_.bstack1ll11111ll_opy_(CONFIG, bstack111l1lll_opy_)
    bstack1ll1l11ll1_opy_()
  except Exception as e:
    logger.error(bstack1ll1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨആ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll1111111_opy_
  atexit.register(bstack1l111lll11_opy_)
  signal.signal(signal.SIGINT, bstack1ll1lllll1_opy_)
  signal.signal(signal.SIGTERM, bstack1ll1lllll1_opy_)
def bstack1ll1111111_opy_(exctype, value, traceback):
  global bstack1lll11111_opy_
  try:
    for driver in bstack1lll11111_opy_:
      bstack11lll1l11_opy_(driver, bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪഇ"), bstack1ll1l11_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢഈ") + str(value))
  except Exception:
    pass
  logger.info(bstack1l11l1111_opy_)
  bstack11l1lll1_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11l1lll1_opy_(message=bstack1ll1l11_opy_ (u"ࠬ࠭ഉ"), bstack1l1lll1lll_opy_ = False):
  global CONFIG
  bstack1ll11l111l_opy_ = bstack1ll1l11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠨഊ") if bstack1l1lll1lll_opy_ else bstack1ll1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ഋ")
  try:
    if message:
      bstack11ll1lll1l_opy_ = {
        bstack1ll11l111l_opy_ : str(message)
      }
      bstack1llllll11_opy_(bstack11lll11l11_opy_, CONFIG, bstack11ll1lll1l_opy_)
    else:
      bstack1llllll11_opy_(bstack11lll11l11_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11l11l1l1l_opy_.format(str(e)))
def bstack11l1lll1l1_opy_(bstack1111l11ll_opy_, size):
  bstack1l1111111l_opy_ = []
  while len(bstack1111l11ll_opy_) > size:
    bstack1lll11l1l1_opy_ = bstack1111l11ll_opy_[:size]
    bstack1l1111111l_opy_.append(bstack1lll11l1l1_opy_)
    bstack1111l11ll_opy_ = bstack1111l11ll_opy_[size:]
  bstack1l1111111l_opy_.append(bstack1111l11ll_opy_)
  return bstack1l1111111l_opy_
def bstack11l1lllll1_opy_(args):
  if bstack1ll1l11_opy_ (u"ࠨ࠯ࡰࠫഌ") in args and bstack1ll1l11_opy_ (u"ࠩࡳࡨࡧ࠭഍") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack11ll1l1l_opy_, stage=STAGE.bstack1l11l1l1ll_opy_)
def run_on_browserstack(bstack1llll111ll_opy_=None, bstack111l11ll_opy_=None, bstack11ll1lll1_opy_=False):
  global CONFIG
  global bstack1l11ll1lll_opy_
  global bstack11l1llll1l_opy_
  global bstack11l1l11lll_opy_
  global bstack11lll1111_opy_
  bstack11l1l111ll_opy_ = bstack1ll1l11_opy_ (u"ࠪࠫഎ")
  bstack1lll111l_opy_(bstack1l111111_opy_, logger)
  if bstack1llll111ll_opy_ and isinstance(bstack1llll111ll_opy_, str):
    bstack1llll111ll_opy_ = eval(bstack1llll111ll_opy_)
  if bstack1llll111ll_opy_:
    CONFIG = bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫഏ")]
    bstack1l11ll1lll_opy_ = bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ഐ")]
    bstack11l1llll1l_opy_ = bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ഑")]
    bstack11lll1111_opy_.bstack1lll11lll1_opy_(bstack1ll1l11_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩഒ"), bstack11l1llll1l_opy_)
    bstack11l1l111ll_opy_ = bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨഓ")
  bstack11lll1111_opy_.bstack1lll11lll1_opy_(bstack1ll1l11_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫഔ"), uuid4().__str__())
  logger.info(bstack1ll1l11_opy_ (u"ࠪࡗࡉࡑࠠࡳࡷࡱࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨക") + bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ഖ")));
  logger.debug(bstack1ll1l11_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪ࠽ࠨഗ") + bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨഘ")))
  if not bstack11ll1lll1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11ll11l11_opy_)
      return
    if sys.argv[1] == bstack1ll1l11_opy_ (u"ࠧ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪങ") or sys.argv[1] == bstack1ll1l11_opy_ (u"ࠨ࠯ࡹࠫച"):
      logger.info(bstack1ll1l11_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡕࡇࡏࠥࡼࡻࡾࠩഛ").format(__version__))
      return
    if sys.argv[1] == bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩജ"):
      bstack11lllllll_opy_()
      return
  args = sys.argv
  bstack1ll1l111l1_opy_()
  global bstack1ll111l11_opy_
  global bstack1l11lllll1_opy_
  global bstack1l1l11l1l1_opy_
  global bstack11ll11l1ll_opy_
  global bstack1ll1ll11l_opy_
  global bstack11l1111ll_opy_
  global bstack1lllll11l_opy_
  global bstack1ll111ll11_opy_
  global bstack1lll1111_opy_
  global bstack11llllllll_opy_
  global bstack11lllll11l_opy_
  bstack1l11lllll1_opy_ = len(CONFIG.get(bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧഝ"), []))
  if not bstack11l1l111ll_opy_:
    if args[1] == bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬഞ") or args[1] == bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧട"):
      bstack11l1l111ll_opy_ = bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧഠ")
      args = args[2:]
    elif args[1] == bstack1ll1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧഡ"):
      bstack11l1l111ll_opy_ = bstack1ll1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨഢ")
      args = args[2:]
    elif args[1] == bstack1ll1l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩണ"):
      bstack11l1l111ll_opy_ = bstack1ll1l11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪത")
      args = args[2:]
    elif args[1] == bstack1ll1l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ഥ"):
      bstack11l1l111ll_opy_ = bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧദ")
      args = args[2:]
    elif args[1] == bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧധ"):
      bstack11l1l111ll_opy_ = bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨന")
      args = args[2:]
    elif args[1] == bstack1ll1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩഩ"):
      bstack11l1l111ll_opy_ = bstack1ll1l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪപ")
      args = args[2:]
    else:
      if not bstack1ll1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഫ") in CONFIG or str(CONFIG[bstack1ll1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨബ")]).lower() in [bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ഭ"), bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨമ")]:
        bstack11l1l111ll_opy_ = bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨയ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬര")]).lower() == bstack1ll1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩറ"):
        bstack11l1l111ll_opy_ = bstack1ll1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪല")
        args = args[1:]
      elif str(CONFIG[bstack1ll1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨള")]).lower() == bstack1ll1l11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬഴ"):
        bstack11l1l111ll_opy_ = bstack1ll1l11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭വ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫശ")]).lower() == bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩഷ"):
        bstack11l1l111ll_opy_ = bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪസ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഹ")]).lower() == bstack1ll1l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬഺ"):
        bstack11l1l111ll_opy_ = bstack1ll1l11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ഻࠭")
        args = args[1:]
      else:
        os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌ഼ࠩ")] = bstack11l1l111ll_opy_
        bstack1ll1ll1lll_opy_(bstack111lllll1_opy_)
  os.environ[bstack1ll1l11_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩഽ")] = bstack11l1l111ll_opy_
  bstack11l1l11lll_opy_ = bstack11l1l111ll_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack1l1l1111l_opy_ = bstack11l1111l_opy_[bstack1ll1l11_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭ാ")] if bstack11l1l111ll_opy_ == bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪി") and bstack1l1l1ll1l_opy_() else bstack11l1l111ll_opy_
      bstack11ll11111l_opy_.invoke(bstack11lll1l1l1_opy_.bstack11111l11l_opy_, bstack111lll1l1_opy_(
        sdk_version=__version__,
        path_config=bstack1ll1ll1l1l_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1l1l1111l_opy_,
        frameworks=[bstack1l1l1111l_opy_],
        framework_versions={
          bstack1l1l1111l_opy_: bstack1l1lll111l_opy_(bstack1ll1l11_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪീ") if bstack11l1l111ll_opy_ in [bstack1ll1l11_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫു"), bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬൂ"), bstack1ll1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨൃ")] else bstack11l1l111ll_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥൄ"), None):
        CONFIG[bstack1ll1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦ൅")] = cli.config.get(bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧെ"), None)
    except Exception as e:
      bstack11ll11111l_opy_.invoke(bstack11lll1l1l1_opy_.bstack1111l111l_opy_, e.__traceback__, 1)
    if bstack11l1llll1l_opy_:
      CONFIG[bstack1ll1l11_opy_ (u"ࠦࡦࡶࡰࠣേ")] = cli.config[bstack1ll1l11_opy_ (u"ࠧࡧࡰࡱࠤൈ")]
      logger.info(bstack1lllll11l1_opy_.format(CONFIG[bstack1ll1l11_opy_ (u"࠭ࡡࡱࡲࠪ൉")]))
  else:
    bstack11ll11111l_opy_.clear()
  global bstack11l11ll1_opy_
  global bstack1l111llll_opy_
  if bstack1llll111ll_opy_:
    try:
      bstack1l1l1lllll_opy_ = datetime.datetime.now()
      os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩൊ")] = bstack11l1l111ll_opy_
      bstack1llllll11_opy_(bstack1l11l11lll_opy_, CONFIG)
      cli.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠣࡪࡷࡸࡵࡀࡳࡥ࡭ࡢࡸࡪࡹࡴࡠࡣࡷࡸࡪࡳࡰࡵࡧࡧࠦോ"), datetime.datetime.now() - bstack1l1l1lllll_opy_)
    except Exception as e:
      logger.debug(bstack11l11llll1_opy_.format(str(e)))
  global bstack111llll1l_opy_
  global bstack1l1lll11ll_opy_
  global bstack1l1111ll1_opy_
  global bstack11ll111lll_opy_
  global bstack11ll1ll11_opy_
  global bstack1ll1l1ll1l_opy_
  global bstack1111ll1ll_opy_
  global bstack1lllllll1_opy_
  global bstack1llll1llll_opy_
  global bstack1ll1l1l1ll_opy_
  global bstack1l111lll1l_opy_
  global bstack11l111lll_opy_
  global bstack1llllllll_opy_
  global bstack1ll1llllll_opy_
  global bstack1ll1l11l1_opy_
  global bstack1l111l1l1l_opy_
  global bstack11ll11l1_opy_
  global bstack1l11ll111_opy_
  global bstack11ll111ll1_opy_
  global bstack1l11l1l1l_opy_
  global bstack1ll1ll111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack111llll1l_opy_ = webdriver.Remote.__init__
    bstack1l1lll11ll_opy_ = WebDriver.quit
    bstack11l111lll_opy_ = WebDriver.close
    bstack1ll1l11l1_opy_ = WebDriver.get
    bstack1ll1ll111_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11l11ll1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack11l11llll_opy_
    bstack1l111llll_opy_ = bstack11l11llll_opy_()
  except Exception as e:
    pass
  try:
    global bstack1l1l1lll11_opy_
    from QWeb.keywords import browser
    bstack1l1l1lll11_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1ll11l1ll_opy_(CONFIG) and bstack1l1ll11lll_opy_():
    if bstack1llll11ll_opy_() < version.parse(bstack1l1llll11l_opy_):
      logger.error(bstack1l1l1l1lll_opy_.format(bstack1llll11ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l111l1l1l_opy_ = RemoteConnection._11l11lllll_opy_
      except Exception as e:
        logger.error(bstack1ll111llll_opy_.format(str(e)))
  if not CONFIG.get(bstack1ll1l11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫൌ"), False) and not bstack1llll111ll_opy_:
    logger.info(bstack11ll1l1l1_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack1ll1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫്ࠧ") in CONFIG and str(CONFIG[bstack1ll1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨൎ")]).lower() != bstack1ll1l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ൏"):
      bstack11l1ll111_opy_()
    elif bstack11l1l111ll_opy_ != bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൐") or (bstack11l1l111ll_opy_ == bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ൑") and not bstack1llll111ll_opy_):
      bstack11l1l11ll_opy_()
  if (bstack11l1l111ll_opy_ in [bstack1ll1l11_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ൒"), bstack1ll1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ൓"), bstack1ll1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫൔ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l11l11111_opy_
        bstack1ll1l1ll1l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1lll11l1ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack11ll1ll11_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l1llll1ll_opy_ + str(e))
    except Exception as e:
      bstack11l1llll1_opy_(e, bstack1lll11l1ll_opy_)
    if bstack11l1l111ll_opy_ != bstack1ll1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬൕ"):
      bstack1111l1l1l_opy_()
    bstack1l1111ll1_opy_ = Output.start_test
    bstack11ll111lll_opy_ = Output.end_test
    bstack1111ll1ll_opy_ = TestStatus.__init__
    bstack1llll1llll_opy_ = pabot._run
    bstack1ll1l1l1ll_opy_ = QueueItem.__init__
    bstack1l111lll1l_opy_ = pabot._create_command_for_execution
    bstack11ll111ll1_opy_ = pabot._report_results
  if bstack11l1l111ll_opy_ == bstack1ll1l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬൖ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l1llll1_opy_(e, bstack11l1l1ll_opy_)
    bstack1llllllll_opy_ = Runner.run_hook
    bstack1ll1llllll_opy_ = Step.run
  if bstack11l1l111ll_opy_ == bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ൗ"):
    try:
      from _pytest.config import Config
      bstack11ll11l1_opy_ = Config.getoption
      from _pytest import runner
      bstack1l11ll111_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1lllll11ll_opy_)
    try:
      from pytest_bdd import reporting
      bstack1l11l1l1l_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1ll1l11_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ൘"))
  try:
    framework_name = bstack1ll1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ൙") if bstack11l1l111ll_opy_ in [bstack1ll1l11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ൚"), bstack1ll1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ൛"), bstack1ll1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ൜")] else bstack11111111_opy_(bstack11l1l111ll_opy_)
    bstack111l11l11_opy_ = {
      bstack1ll1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭൝"): bstack1ll1l11_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ൞") if bstack11l1l111ll_opy_ == bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧൟ") and bstack1l1l1ll1l_opy_() else framework_name,
      bstack1ll1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬൠ"): bstack1l1lll111l_opy_(framework_name),
      bstack1ll1l11_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧൡ"): __version__,
      bstack1ll1l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫൢ"): bstack11l1l111ll_opy_
    }
    if bstack11l1l111ll_opy_ in bstack1llll11l1l_opy_ + bstack1l1111111_opy_:
      if bstack1lll111ll1_opy_ and bstack1ll1lll1l_opy_.bstack1l11l1lll_opy_(CONFIG):
        if bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫൣ") in CONFIG:
          os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭൤")] = os.getenv(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ൥"), json.dumps(CONFIG[bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ൦")]))
          CONFIG[bstack1ll1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ൧")].pop(bstack1ll1l11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ൨"), None)
          CONFIG[bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ൩")].pop(bstack1ll1l11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ൪"), None)
        bstack111l11l11_opy_[bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ൫")] = {
          bstack1ll1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ൬"): bstack1ll1l11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ൭"),
          bstack1ll1l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩ൮"): str(bstack1llll11ll_opy_())
        }
    if bstack11l1l111ll_opy_ not in [bstack1ll1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ൯")] and not cli.is_running():
      bstack11l1l1l11_opy_ = bstack1ll1l11l1l_opy_.launch(CONFIG, bstack111l11l11_opy_)
  except Exception as e:
    logger.debug(bstack1l1l1ll1ll_opy_.format(bstack1ll1l11_opy_ (u"ࠪࡘࡪࡹࡴࡉࡷࡥࠫ൰"), str(e)))
  if bstack11l1l111ll_opy_ == bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ൱"):
    bstack1l1l11l1l1_opy_ = True
    if bstack1llll111ll_opy_ and bstack11ll1lll1_opy_:
      bstack11l1111ll_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ൲"), {}).get(bstack1ll1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ൳"))
      bstack1ll1lll1l1_opy_(bstack1111111l_opy_)
    elif bstack1llll111ll_opy_:
      bstack11l1111ll_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ൴"), {}).get(bstack1ll1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ൵"))
      global bstack1lll11111_opy_
      try:
        if bstack11l1lllll1_opy_(bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ൶")]) and multiprocessing.current_process().name == bstack1ll1l11_opy_ (u"ࠪ࠴ࠬ൷"):
          bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ൸")].remove(bstack1ll1l11_opy_ (u"ࠬ࠳࡭ࠨ൹"))
          bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩൺ")].remove(bstack1ll1l11_opy_ (u"ࠧࡱࡦࡥࠫൻ"))
          bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫർ")] = bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬൽ")][0]
          with open(bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ൾ")], bstack1ll1l11_opy_ (u"ࠫࡷ࠭ൿ")) as f:
            bstack1ll1111lll_opy_ = f.read()
          bstack11ll1lll11_opy_ = bstack1ll1l11_opy_ (u"ࠧࠨࠢࡧࡴࡲࡱࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡪ࡫ࠡ࡫ࡰࡴࡴࡸࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨ࠿ࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࠩࡽࢀ࠭ࡀࠦࡦࡳࡱࡰࠤࡵࡪࡢࠡ࡫ࡰࡴࡴࡸࡴࠡࡒࡧࡦࡀࠦ࡯ࡨࡡࡧࡦࠥࡃࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࡴࡨࡥࡰࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡨࡪ࡬ࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠫࡷࡪࡲࡦ࠭ࠢࡤࡶ࡬࠲ࠠࡵࡧࡰࡴࡴࡸࡡࡳࡻࠣࡁࠥ࠶ࠩ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡴࡼ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡧࡲࡨࠢࡀࠤࡸࡺࡲࠩ࡫ࡱࡸ࠭ࡧࡲࡨࠫ࠮࠵࠵࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡫ࡸࡤࡧࡳࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡣࡶࠤࡪࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡱࡣࡶࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡳ࡬ࡥࡤࡣࠪࡶࡩࡱ࡬ࠬࡢࡴࡪ࠰ࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࠦ࠽ࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࡴࡨࡥࡰࠦ࠽ࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡑࡦࡥࠬ࠮࠴ࡳࡦࡶࡢࡸࡷࡧࡣࡦࠪࠬࡠࡳࠨࠢࠣ඀").format(str(bstack1llll111ll_opy_))
          bstack11l1ll1l_opy_ = bstack11ll1lll11_opy_ + bstack1ll1111lll_opy_
          bstack11l11ll1l_opy_ = bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඁ")] + bstack1ll1l11_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡶࡨࡱࡵ࠴ࡰࡺࠩං")
          with open(bstack11l11ll1l_opy_, bstack1ll1l11_opy_ (u"ࠨࡹࠪඃ")):
            pass
          with open(bstack11l11ll1l_opy_, bstack1ll1l11_opy_ (u"ࠤࡺ࠯ࠧ඄")) as f:
            f.write(bstack11l1ll1l_opy_)
          import subprocess
          bstack1l111ll11_opy_ = subprocess.run([bstack1ll1l11_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࠥඅ"), bstack11l11ll1l_opy_])
          if os.path.exists(bstack11l11ll1l_opy_):
            os.unlink(bstack11l11ll1l_opy_)
          os._exit(bstack1l111ll11_opy_.returncode)
        else:
          if bstack11l1lllll1_opy_(bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧආ")]):
            bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨඇ")].remove(bstack1ll1l11_opy_ (u"࠭࠭࡮ࠩඈ"))
            bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඉ")].remove(bstack1ll1l11_opy_ (u"ࠨࡲࡧࡦࠬඊ"))
            bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬඋ")] = bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ඌ")][0]
          bstack1ll1lll1l1_opy_(bstack1111111l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧඍ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1ll1l11_opy_ (u"ࠬࡥ࡟࡯ࡣࡰࡩࡤࡥࠧඎ")] = bstack1ll1l11_opy_ (u"࠭࡟ࡠ࡯ࡤ࡭ࡳࡥ࡟ࠨඏ")
          mod_globals[bstack1ll1l11_opy_ (u"ࠧࡠࡡࡩ࡭ࡱ࡫࡟ࡠࠩඐ")] = os.path.abspath(bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫඑ")])
          exec(open(bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬඒ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1ll1l11_opy_ (u"ࠪࡇࡦࡻࡧࡩࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠪඓ").format(str(e)))
          for driver in bstack1lll11111_opy_:
            bstack111l11ll_opy_.append({
              bstack1ll1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩඔ"): bstack1llll111ll_opy_[bstack1ll1l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨඕ")],
              bstack1ll1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬඖ"): str(e),
              bstack1ll1l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭඗"): multiprocessing.current_process().name
            })
            bstack11lll1l11_opy_(driver, bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ඘"), bstack1ll1l11_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ඙") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1lll11111_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11l1llll1l_opy_, CONFIG, logger)
      bstack1111llll1_opy_()
      bstack11l1ll1ll_opy_()
      percy.bstack1l1lll1111_opy_()
      bstack111l1l1l_opy_ = {
        bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ක"): args[0],
        bstack1ll1l11_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫඛ"): CONFIG,
        bstack1ll1l11_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ග"): bstack1l11ll1lll_opy_,
        bstack1ll1l11_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨඝ"): bstack11l1llll1l_opy_
      }
      if bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪඞ") in CONFIG:
        bstack1lll1l1111_opy_ = bstack11lll1l1ll_opy_(args, logger, CONFIG, bstack1lll111ll1_opy_, bstack1l11lllll1_opy_)
        bstack1ll111ll11_opy_ = bstack1lll1l1111_opy_.bstack1l1llllll_opy_(run_on_browserstack, bstack111l1l1l_opy_, bstack11l1lllll1_opy_(args))
      else:
        if bstack11l1lllll1_opy_(args):
          bstack111l1l1l_opy_[bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫඟ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack111l1l1l_opy_,))
          test.start()
          test.join()
        else:
          bstack1ll1lll1l1_opy_(bstack1111111l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1ll1l11_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫච")] = bstack1ll1l11_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬඡ")
          mod_globals[bstack1ll1l11_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭ජ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11l1l111ll_opy_ == bstack1ll1l11_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫඣ") or bstack11l1l111ll_opy_ == bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬඤ"):
    percy.init(bstack11l1llll1l_opy_, CONFIG, logger)
    percy.bstack1l1lll1111_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11l1llll1_opy_(e, bstack1lll11l1ll_opy_)
    bstack1111llll1_opy_()
    bstack1ll1lll1l1_opy_(bstack1l11ll1l1l_opy_)
    if bstack1lll111ll1_opy_:
      bstack1l111l1ll1_opy_(bstack1l11ll1l1l_opy_, args)
      if bstack1ll1l11_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬඥ") in args:
        i = args.index(bstack1ll1l11_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ඦ"))
        args.pop(i)
        args.pop(i)
      if bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬට") not in CONFIG:
        CONFIG[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ඨ")] = [{}]
        bstack1l11lllll1_opy_ = 1
      if bstack1ll111l11_opy_ == 0:
        bstack1ll111l11_opy_ = 1
      args.insert(0, str(bstack1ll111l11_opy_))
      args.insert(0, str(bstack1ll1l11_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩඩ")))
    if bstack1ll1l11l1l_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l11111l1l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack111ll1ll_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1ll1l11_opy_ (u"ࠧࡘࡏࡃࡑࡗࡣࡔࡖࡔࡊࡑࡑࡗࠧඪ"),
        ).parse_args(bstack1l11111l1l_opy_)
        bstack11l111l1_opy_ = args.index(bstack1l11111l1l_opy_[0]) if len(bstack1l11111l1l_opy_) > 0 else len(args)
        args.insert(bstack11l111l1_opy_, str(bstack1ll1l11_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪණ")))
        args.insert(bstack11l111l1_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡳࡱࡥࡳࡹࡥ࡬ࡪࡵࡷࡩࡳ࡫ࡲ࠯ࡲࡼࠫඬ"))))
        if bstack11l1llllll_opy_(os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭ත"))) and str(os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ථ"), bstack1ll1l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨද"))) != bstack1ll1l11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩධ"):
          for bstack1ll1l1l1l_opy_ in bstack111ll1ll_opy_:
            args.remove(bstack1ll1l1l1l_opy_)
          bstack11l1l1ll1_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩන")).split(bstack1ll1l11_opy_ (u"࠭ࠬࠨ඲"))
          for bstack1l1ll1111l_opy_ in bstack11l1l1ll1_opy_:
            args.append(bstack1l1ll1111l_opy_)
      except Exception as e:
        logger.error(bstack1ll1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡴࡵࡣࡦ࡬࡮ࡴࡧࠡ࡮࡬ࡷࡹ࡫࡮ࡦࡴࠣࡪࡴࡸࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࠡࡇࡵࡶࡴࡸࠠ࠮ࠢࠥඳ").format(e))
    pabot.main(args)
  elif bstack11l1l111ll_opy_ == bstack1ll1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩප"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11l1llll1_opy_(e, bstack1lll11l1ll_opy_)
    for a in args:
      if bstack1ll1l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨඵ") in a:
        bstack1ll1ll11l_opy_ = int(a.split(bstack1ll1l11_opy_ (u"ࠪ࠾ࠬබ"))[1])
      if bstack1ll1l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨභ") in a:
        bstack11l1111ll_opy_ = str(a.split(bstack1ll1l11_opy_ (u"ࠬࡀࠧම"))[1])
      if bstack1ll1l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ඹ") in a:
        bstack1lllll11l_opy_ = str(a.split(bstack1ll1l11_opy_ (u"ࠧ࠻ࠩය"))[1])
    bstack11llll1ll_opy_ = None
    if bstack1ll1l11_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧර") in args:
      i = args.index(bstack1ll1l11_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨ඼"))
      args.pop(i)
      bstack11llll1ll_opy_ = args.pop(i)
    if bstack11llll1ll_opy_ is not None:
      global bstack11lll11l1_opy_
      bstack11lll11l1_opy_ = bstack11llll1ll_opy_
    bstack1ll1lll1l1_opy_(bstack1l11ll1l1l_opy_)
    run_cli(args)
    if bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧල") in multiprocessing.current_process().__dict__.keys():
      for bstack1lll1l1lll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack111l11ll_opy_.append(bstack1lll1l1lll_opy_)
  elif bstack11l1l111ll_opy_ == bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ඾"):
    bstack1llll1l111_opy_ = bstack1ll1l1l1l1_opy_(args, logger, CONFIG, bstack1lll111ll1_opy_)
    bstack1llll1l111_opy_.bstack1l1ll1ll11_opy_()
    bstack1111llll1_opy_()
    bstack11ll11l1ll_opy_ = True
    bstack11llllllll_opy_ = bstack1llll1l111_opy_.bstack111l1lll1_opy_()
    bstack1llll1l111_opy_.bstack111l1l1l_opy_(bstack11l11ll111_opy_)
    bstack111111l1_opy_ = bstack1llll1l111_opy_.bstack1l1llllll_opy_(bstack1l1l11lll1_opy_, {
      bstack1ll1l11_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭඿"): bstack1l11ll1lll_opy_,
      bstack1ll1l11_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨව"): bstack11l1llll1l_opy_,
      bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪශ"): bstack1lll111ll1_opy_
    })
    try:
      bstack1111l1111_opy_, bstack11llll111_opy_ = map(list, zip(*bstack111111l1_opy_))
      bstack1lll1111_opy_ = bstack1111l1111_opy_[0]
      for status_code in bstack11llll111_opy_:
        if status_code != 0:
          bstack11lllll11l_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1ll1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡨࡶࡷࡵࡲࡴࠢࡤࡲࡩࠦࡳࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠲ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠼ࠣࡿࢂࠨෂ").format(str(e)))
  elif bstack11l1l111ll_opy_ == bstack1ll1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩස"):
    try:
      from behave.__main__ import main as bstack111ll11ll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11l1llll1_opy_(e, bstack11l1l1ll_opy_)
    bstack1111llll1_opy_()
    bstack11ll11l1ll_opy_ = True
    bstack11l11l1ll_opy_ = 1
    if bstack1ll1l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪහ") in CONFIG:
      bstack11l11l1ll_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫළ")]
    if bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨෆ") in CONFIG:
      bstack11llll1l1_opy_ = int(bstack11l11l1ll_opy_) * int(len(CONFIG[bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෇")]))
    else:
      bstack11llll1l1_opy_ = int(bstack11l11l1ll_opy_)
    config = Configuration(args)
    bstack1l1l111ll1_opy_ = config.paths
    if len(bstack1l1l111ll1_opy_) == 0:
      import glob
      pattern = bstack1ll1l11_opy_ (u"ࠧࠫࠬ࠲࠮࠳࡬ࡥࡢࡶࡸࡶࡪ࠭෈")
      bstack1lll111l1l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1lll111l1l_opy_)
      config = Configuration(args)
      bstack1l1l111ll1_opy_ = config.paths
    bstack11lll1l11l_opy_ = [os.path.normpath(item) for item in bstack1l1l111ll1_opy_]
    bstack11lll1111l_opy_ = [os.path.normpath(item) for item in args]
    bstack11ll11lll1_opy_ = [item for item in bstack11lll1111l_opy_ if item not in bstack11lll1l11l_opy_]
    import platform as pf
    if pf.system().lower() == bstack1ll1l11_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩ෉"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11lll1l11l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11llll11ll_opy_)))
                    for bstack11llll11ll_opy_ in bstack11lll1l11l_opy_]
    bstack1l11llll_opy_ = []
    for spec in bstack11lll1l11l_opy_:
      bstack11ll1l1ll1_opy_ = []
      bstack11ll1l1ll1_opy_ += bstack11ll11lll1_opy_
      bstack11ll1l1ll1_opy_.append(spec)
      bstack1l11llll_opy_.append(bstack11ll1l1ll1_opy_)
    execution_items = []
    for bstack11ll1l1ll1_opy_ in bstack1l11llll_opy_:
      if bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷ්ࠬ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭෋")]):
          item = {}
          item[bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࠨ෌")] = bstack1ll1l11_opy_ (u"ࠬࠦࠧ෍").join(bstack11ll1l1ll1_opy_)
          item[bstack1ll1l11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ෎")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࠫා")] = bstack1ll1l11_opy_ (u"ࠨࠢࠪැ").join(bstack11ll1l1ll1_opy_)
        item[bstack1ll1l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨෑ")] = 0
        execution_items.append(item)
    bstack1ll1ll11_opy_ = bstack11l1lll1l1_opy_(execution_items, bstack11llll1l1_opy_)
    for execution_item in bstack1ll1ll11_opy_:
      bstack1ll11ll1l1_opy_ = []
      for item in execution_item:
        bstack1ll11ll1l1_opy_.append(bstack1ll11111l_opy_(name=str(item[bstack1ll1l11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩි")]),
                                             target=bstack11l11l11l_opy_,
                                             args=(item[bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࠨී")],)))
      for t in bstack1ll11ll1l1_opy_:
        t.start()
      for t in bstack1ll11ll1l1_opy_:
        t.join()
  else:
    bstack1ll1ll1lll_opy_(bstack111lllll1_opy_)
  if not bstack1llll111ll_opy_:
    bstack111l1l11_opy_()
    if(bstack11l1l111ll_opy_ in [bstack1ll1l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬු"), bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෕")]):
      bstack1lll1ll1_opy_()
  bstack1ll1lllll_opy_.bstack1l11l1ll1_opy_()
def browserstack_initialize(bstack11l1l11l1_opy_=None):
  logger.info(bstack1ll1l11_opy_ (u"ࠧࡓࡷࡱࡲ࡮ࡴࡧࠡࡕࡇࡏࠥࡽࡩࡵࡪࠣࡥࡷ࡭ࡳ࠻ࠢࠪූ") + str(bstack11l1l11l1_opy_))
  run_on_browserstack(bstack11l1l11l1_opy_, None, True)
@measure(event_name=EVENTS.bstack11l1l1111_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack111l1l11_opy_():
  global CONFIG
  global bstack11l1l11lll_opy_
  global bstack11lllll11l_opy_
  global bstack11l111l1l_opy_
  global bstack11lll1111_opy_
  bstack11l1ll11l_opy_.bstack1l11lll11l_opy_()
  if cli.is_running():
    bstack11ll11111l_opy_.invoke(bstack11lll1l1l1_opy_.bstack1lll11l1_opy_)
  if bstack11l1l11lll_opy_ == bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ෗"):
    if not cli.is_enabled(CONFIG):
      bstack1ll1l11l1l_opy_.stop()
  else:
    bstack1ll1l11l1l_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack1lll111111_opy_.bstack1l11l1l1_opy_()
  if bstack1ll1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ෘ") in CONFIG and str(CONFIG[bstack1ll1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧෙ")]).lower() != bstack1ll1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪේ"):
    bstack111l1ll11_opy_, bstack1lll111ll_opy_ = bstack1ll111l1_opy_()
  else:
    bstack111l1ll11_opy_, bstack1lll111ll_opy_ = get_build_link()
  bstack111l1l1ll_opy_(bstack111l1ll11_opy_)
  logger.info(bstack1ll1l11_opy_ (u"࡙ࠬࡄࡌࠢࡵࡹࡳࠦࡥ࡯ࡦࡨࡨࠥ࡬࡯ࡳࠢ࡬ࡨ࠿࠭ෛ") + bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨො"), bstack1ll1l11_opy_ (u"ࠧࠨෝ")) + bstack1ll1l11_opy_ (u"ࠨ࠮ࠣࡸࡪࡹࡴࡩࡷࡥࠤ࡮ࡪ࠺ࠡࠩෞ") + os.getenv(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧෟ"), bstack1ll1l11_opy_ (u"ࠪࠫ෠")))
  if bstack111l1ll11_opy_ is not None and bstack11lll11ll_opy_() != -1:
    sessions = bstack1l1ll1ll1l_opy_(bstack111l1ll11_opy_)
    bstack111ll111_opy_(sessions, bstack1lll111ll_opy_)
  if bstack11l1l11lll_opy_ == bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ෡") and bstack11lllll11l_opy_ != 0:
    sys.exit(bstack11lllll11l_opy_)
  if bstack11l1l11lll_opy_ == bstack1ll1l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ෢") and bstack11l111l1l_opy_ != 0:
    sys.exit(bstack11l111l1l_opy_)
def bstack111l1l1ll_opy_(new_id):
    global bstack111ll1ll1_opy_
    bstack111ll1ll1_opy_ = new_id
def bstack11111111_opy_(bstack11ll1ll1l_opy_):
  if bstack11ll1ll1l_opy_:
    return bstack11ll1ll1l_opy_.capitalize()
  else:
    return bstack1ll1l11_opy_ (u"࠭ࠧ෣")
@measure(event_name=EVENTS.bstack1l1l1111_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1l111ll1_opy_(bstack1l1l111111_opy_):
  if bstack1ll1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ෤") in bstack1l1l111111_opy_ and bstack1l1l111111_opy_[bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭෥")] != bstack1ll1l11_opy_ (u"ࠩࠪ෦"):
    return bstack1l1l111111_opy_[bstack1ll1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ෧")]
  else:
    bstack1l1ll111l1_opy_ = bstack1ll1l11_opy_ (u"ࠦࠧ෨")
    if bstack1ll1l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ෩") in bstack1l1l111111_opy_ and bstack1l1l111111_opy_[bstack1ll1l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭෪")] != None:
      bstack1l1ll111l1_opy_ += bstack1l1l111111_opy_[bstack1ll1l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ෫")] + bstack1ll1l11_opy_ (u"ࠣ࠮ࠣࠦ෬")
      if bstack1l1l111111_opy_[bstack1ll1l11_opy_ (u"ࠩࡲࡷࠬ෭")] == bstack1ll1l11_opy_ (u"ࠥ࡭ࡴࡹࠢ෮"):
        bstack1l1ll111l1_opy_ += bstack1ll1l11_opy_ (u"ࠦ࡮ࡕࡓࠡࠤ෯")
      bstack1l1ll111l1_opy_ += (bstack1l1l111111_opy_[bstack1ll1l11_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ෰")] or bstack1ll1l11_opy_ (u"࠭ࠧ෱"))
      return bstack1l1ll111l1_opy_
    else:
      bstack1l1ll111l1_opy_ += bstack11111111_opy_(bstack1l1l111111_opy_[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨෲ")]) + bstack1ll1l11_opy_ (u"ࠣࠢࠥෳ") + (
              bstack1l1l111111_opy_[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ෴")] or bstack1ll1l11_opy_ (u"ࠪࠫ෵")) + bstack1ll1l11_opy_ (u"ࠦ࠱ࠦࠢ෶")
      if bstack1l1l111111_opy_[bstack1ll1l11_opy_ (u"ࠬࡵࡳࠨ෷")] == bstack1ll1l11_opy_ (u"ࠨࡗࡪࡰࡧࡳࡼࡹࠢ෸"):
        bstack1l1ll111l1_opy_ += bstack1ll1l11_opy_ (u"ࠢࡘ࡫ࡱࠤࠧ෹")
      bstack1l1ll111l1_opy_ += bstack1l1l111111_opy_[bstack1ll1l11_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ෺")] or bstack1ll1l11_opy_ (u"ࠩࠪ෻")
      return bstack1l1ll111l1_opy_
@measure(event_name=EVENTS.bstack11llll1l11_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1l1l1l11ll_opy_(bstack1ll11l1l11_opy_):
  if bstack1ll11l1l11_opy_ == bstack1ll1l11_opy_ (u"ࠥࡨࡴࡴࡥࠣ෼"):
    return bstack1ll1l11_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡃࡰ࡯ࡳࡰࡪࡺࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ෽")
  elif bstack1ll11l1l11_opy_ == bstack1ll1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ෾"):
    return bstack1ll1l11_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡋࡧࡩ࡭ࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ෿")
  elif bstack1ll11l1l11_opy_ == bstack1ll1l11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ฀"):
    return bstack1ll1l11_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡔࡦࡹࡳࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨก")
  elif bstack1ll11l1l11_opy_ == bstack1ll1l11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣข"):
    return bstack1ll1l11_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡇࡵࡶࡴࡸ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬฃ")
  elif bstack1ll11l1l11_opy_ == bstack1ll1l11_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧค"):
    return bstack1ll1l11_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࠤࡧࡨࡥ࠸࠸࠶࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࠦࡩࡪࡧ࠳࠳࠸ࠥࡂ࡙࡯࡭ࡦࡱࡸࡸࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪฅ")
  elif bstack1ll11l1l11_opy_ == bstack1ll1l11_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠢฆ"):
    return bstack1ll1l11_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࡕࡹࡳࡴࡩ࡯ࡩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨง")
  else:
    return bstack1ll1l11_opy_ (u"ࠨ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࠬจ") + bstack11111111_opy_(
      bstack1ll11l1l11_opy_) + bstack1ll1l11_opy_ (u"ࠩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨฉ")
def bstack11lll1ll1_opy_(session):
  return bstack1ll1l11_opy_ (u"ࠪࡀࡹࡸࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡳࡱࡺࠦࡃࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࡾࢁࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࡽࢀࡀ࠴ࡧ࠾࠽࠱ࡷࡨࡃࢁࡽࡼࡿ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁ࠵ࡴࡳࡀࠪช").format(
    session[bstack1ll1l11_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨซ")], bstack1l111ll1_opy_(session), bstack1l1l1l11ll_opy_(session[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠫฌ")]),
    bstack1l1l1l11ll_opy_(session[bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ญ")]),
    bstack11111111_opy_(session[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨฎ")] or session[bstack1ll1l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨฏ")] or bstack1ll1l11_opy_ (u"ࠩࠪฐ")) + bstack1ll1l11_opy_ (u"ࠥࠤࠧฑ") + (session[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ฒ")] or bstack1ll1l11_opy_ (u"ࠬ࠭ณ")),
    session[bstack1ll1l11_opy_ (u"࠭࡯ࡴࠩด")] + bstack1ll1l11_opy_ (u"ࠢࠡࠤต") + session[bstack1ll1l11_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬถ")], session[bstack1ll1l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫท")] or bstack1ll1l11_opy_ (u"ࠪࠫธ"),
    session[bstack1ll1l11_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨน")] if session[bstack1ll1l11_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩบ")] else bstack1ll1l11_opy_ (u"࠭ࠧป"))
@measure(event_name=EVENTS.bstack1ll11lll1_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack111ll111_opy_(sessions, bstack1lll111ll_opy_):
  try:
    bstack1ll1l111l_opy_ = bstack1ll1l11_opy_ (u"ࠢࠣผ")
    if not os.path.exists(bstack1l1111l11l_opy_):
      os.mkdir(bstack1l1111l11l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1l11_opy_ (u"ࠨࡣࡶࡷࡪࡺࡳ࠰ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭ฝ")), bstack1ll1l11_opy_ (u"ࠩࡵࠫพ")) as f:
      bstack1ll1l111l_opy_ = f.read()
    bstack1ll1l111l_opy_ = bstack1ll1l111l_opy_.replace(bstack1ll1l11_opy_ (u"ࠪࡿࠪࡘࡅࡔࡗࡏࡘࡘࡥࡃࡐࡗࡑࡘࠪࢃࠧฟ"), str(len(sessions)))
    bstack1ll1l111l_opy_ = bstack1ll1l111l_opy_.replace(bstack1ll1l11_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠧࢀࠫภ"), bstack1lll111ll_opy_)
    bstack1ll1l111l_opy_ = bstack1ll1l111l_opy_.replace(bstack1ll1l11_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠩࢂ࠭ม"),
                                              sessions[0].get(bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡡ࡮ࡧࠪย")) if sessions[0] else bstack1ll1l11_opy_ (u"ࠧࠨร"))
    with open(os.path.join(bstack1l1111l11l_opy_, bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬฤ")), bstack1ll1l11_opy_ (u"ࠩࡺࠫล")) as stream:
      stream.write(bstack1ll1l111l_opy_.split(bstack1ll1l11_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧฦ"))[0])
      for session in sessions:
        stream.write(bstack11lll1ll1_opy_(session))
      stream.write(bstack1ll1l111l_opy_.split(bstack1ll1l11_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨว"))[1])
    logger.info(bstack1ll1l11_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠢࡤࡸࠥࢁࡽࠨศ").format(bstack1l1111l11l_opy_));
  except Exception as e:
    logger.debug(bstack11lllllll1_opy_.format(str(e)))
def bstack1l1ll1ll1l_opy_(bstack111l1ll11_opy_):
  global CONFIG
  try:
    bstack1l1l1lllll_opy_ = datetime.datetime.now()
    host = bstack1ll1l11_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩษ") if bstack1ll1l11_opy_ (u"ࠧࡢࡲࡳࠫส") in CONFIG else bstack1ll1l11_opy_ (u"ࠨࡣࡳ࡭ࠬห")
    user = CONFIG[bstack1ll1l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫฬ")]
    key = CONFIG[bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭อ")]
    bstack1lll1l11l_opy_ = bstack1ll1l11_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪฮ") if bstack1ll1l11_opy_ (u"ࠬࡧࡰࡱࠩฯ") in CONFIG else (bstack1ll1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪะ") if CONFIG.get(bstack1ll1l11_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫั")) else bstack1ll1l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪา"))
    url = bstack1ll1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠰࡭ࡷࡴࡴࠧำ").format(user, key, host, bstack1lll1l11l_opy_,
                                                                                bstack111l1ll11_opy_)
    headers = {
      bstack1ll1l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩิ"): bstack1ll1l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧี"),
    }
    proxies = bstack1ll1l1111_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      cli.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࡫ࡪࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࡡ࡯࡭ࡸࡺࠢึ"), datetime.datetime.now() - bstack1l1l1lllll_opy_)
      return list(map(lambda session: session[bstack1ll1l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࠫื")], response.json()))
  except Exception as e:
    logger.debug(bstack11llllll_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1l111l1l11_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def get_build_link():
  global CONFIG
  global bstack111ll1ll1_opy_
  try:
    if bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧุࠪ") in CONFIG:
      bstack1l1l1lllll_opy_ = datetime.datetime.now()
      host = bstack1ll1l11_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧูࠫ") if bstack1ll1l11_opy_ (u"ࠩࡤࡴࡵฺ࠭") in CONFIG else bstack1ll1l11_opy_ (u"ࠪࡥࡵ࡯ࠧ฻")
      user = CONFIG[bstack1ll1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭฼")]
      key = CONFIG[bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ฽")]
      bstack1lll1l11l_opy_ = bstack1ll1l11_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ฾") if bstack1ll1l11_opy_ (u"ࠧࡢࡲࡳࠫ฿") in CONFIG else bstack1ll1l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪเ")
      url = bstack1ll1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠩแ").format(user, key, host, bstack1lll1l11l_opy_)
      headers = {
        bstack1ll1l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩโ"): bstack1ll1l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧใ"),
      }
      if bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧไ") in CONFIG:
        params = {bstack1ll1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫๅ"): CONFIG[bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪๆ")], bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ็"): CONFIG[bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ่ࠫ")]}
      else:
        params = {bstack1ll1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ้"): CONFIG[bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫๊ࠧ")]}
      proxies = bstack1ll1l1111_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1llll1ll1_opy_ = response.json()[0][bstack1ll1l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨ๋")]
        if bstack1llll1ll1_opy_:
          bstack1lll111ll_opy_ = bstack1llll1ll1_opy_[bstack1ll1l11_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪ์")].split(bstack1ll1l11_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭ํ"))[0] + bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩ๎") + bstack1llll1ll1_opy_[
            bstack1ll1l11_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ๏")]
          logger.info(bstack11ll11l1l1_opy_.format(bstack1lll111ll_opy_))
          bstack111ll1ll1_opy_ = bstack1llll1ll1_opy_[bstack1ll1l11_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭๐")]
          bstack1l1l1l1111_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ๑")]
          if bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ๒") in CONFIG:
            bstack1l1l1l1111_opy_ += bstack1ll1l11_opy_ (u"࠭ࠠࠨ๓") + CONFIG[bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ๔")]
          if bstack1l1l1l1111_opy_ != bstack1llll1ll1_opy_[bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭๕")]:
            logger.debug(bstack11llll11l1_opy_.format(bstack1llll1ll1_opy_[bstack1ll1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ๖")], bstack1l1l1l1111_opy_))
          cli.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻ࡩࡨࡸࡤࡨࡵࡪ࡮ࡧࡣࡱ࡯࡮࡬ࠤ๗"), datetime.datetime.now() - bstack1l1l1lllll_opy_)
          return [bstack1llll1ll1_opy_[bstack1ll1l11_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ๘")], bstack1lll111ll_opy_]
    else:
      logger.warn(bstack11l1l1llll_opy_)
  except Exception as e:
    logger.debug(bstack1l1111l1l_opy_.format(str(e)))
  return [None, None]
def bstack1l1l111l11_opy_(url, bstack1lll1ll111_opy_=False):
  global CONFIG
  global bstack1llll111l_opy_
  if not bstack1llll111l_opy_:
    hostname = bstack11lllll1l1_opy_(url)
    is_private = bstack1l111ll1l1_opy_(hostname)
    if (bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ๙") in CONFIG and not bstack11l1llllll_opy_(CONFIG[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ๚")])) and (is_private or bstack1lll1ll111_opy_):
      bstack1llll111l_opy_ = hostname
def bstack11lllll1l1_opy_(url):
  return urlparse(url).hostname
def bstack1l111ll1l1_opy_(hostname):
  for bstack1111ll111_opy_ in bstack1lll11ll1_opy_:
    regex = re.compile(bstack1111ll111_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l11l111l1_opy_(bstack1l1l1l111l_opy_):
  return True if bstack1l1l1l111l_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack111l111l1_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1ll1ll11l_opy_
  bstack1l1ll1ll_opy_ = not (bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ๛"), None) and bstack11ll111l1_opy_(
          threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ๜"), None))
  bstack1111l1lll_opy_ = getattr(driver, bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ๝"), None) != True
  bstack11lllll1_opy_ = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ๞"), None) and bstack11ll111l1_opy_(
          threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭๟"), None)
  if bstack11lllll1_opy_:
    if not bstack1llllll1l1_opy_():
      logger.warning(bstack1ll1l11_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤ๠"))
      return {}
    logger.debug(bstack1ll1l11_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪ๡"))
    logger.debug(perform_scan(driver, driver_command=bstack1ll1l11_opy_ (u"ࠧࡦࡺࡨࡧࡺࡺࡥࡔࡥࡵ࡭ࡵࡺࠧ๢")))
    results = bstack1llll1ll11_opy_(bstack1ll1l11_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡴࠤ๣"))
    if results is not None and results.get(bstack1ll1l11_opy_ (u"ࠤ࡬ࡷࡸࡻࡥࡴࠤ๤")) is not None:
        return results[bstack1ll1l11_opy_ (u"ࠥ࡭ࡸࡹࡵࡦࡵࠥ๥")]
    logger.error(bstack1ll1l11_opy_ (u"ࠦࡓࡵࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡓࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨ๦"))
    return []
  if not bstack1ll1lll1l_opy_.bstack1l1lllll1_opy_(CONFIG, bstack1ll1ll11l_opy_) or (bstack1111l1lll_opy_ and bstack1l1ll1ll_opy_):
    logger.warning(bstack1ll1l11_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣ๧"))
    return {}
  try:
    logger.debug(bstack1ll1l11_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪ๨"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l11l111_opy_.bstack1l1ll1llll_opy_)
    return results
  except Exception:
    logger.error(bstack1ll1l11_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡼ࡫ࡲࡦࠢࡩࡳࡺࡴࡤ࠯ࠤ๩"))
    return {}
@measure(event_name=EVENTS.bstack1ll11lll11_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1ll1ll11l_opy_
  bstack1l1ll1ll_opy_ = not (bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ๪"), None) and bstack11ll111l1_opy_(
          threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ๫"), None))
  bstack1111l1lll_opy_ = getattr(driver, bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ๬"), None) != True
  bstack11lllll1_opy_ = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ๭"), None) and bstack11ll111l1_opy_(
          threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ๮"), None)
  if bstack11lllll1_opy_:
    if not bstack1llllll1l1_opy_():
      logger.warning(bstack1ll1l11_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻ࠱ࠦ๯"))
      return {}
    logger.debug(bstack1ll1l11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠬ๰"))
    logger.debug(perform_scan(driver, driver_command=bstack1ll1l11_opy_ (u"ࠨࡧࡻࡩࡨࡻࡴࡦࡕࡦࡶ࡮ࡶࡴࠨ๱")))
    results = bstack1llll1ll11_opy_(bstack1ll1l11_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡕࡸࡱࡲࡧࡲࡺࠤ๲"))
    if results is not None and results.get(bstack1ll1l11_opy_ (u"ࠥࡷࡺࡳ࡭ࡢࡴࡼࠦ๳")) is not None:
        return results[bstack1ll1l11_opy_ (u"ࠦࡸࡻ࡭࡮ࡣࡵࡽࠧ๴")]
    logger.error(bstack1ll1l11_opy_ (u"ࠧࡔ࡯ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡔࡨࡷࡺࡲࡴࡴࠢࡖࡹࡲࡳࡡࡳࡻࠣࡻࡦࡹࠠࡧࡱࡸࡲࡩ࠴ࠢ๵"))
    return {}
  if not bstack1ll1lll1l_opy_.bstack1l1lllll1_opy_(CONFIG, bstack1ll1ll11l_opy_) or (bstack1111l1lll_opy_ and bstack1l1ll1ll_opy_):
    logger.warning(bstack1ll1l11_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺ࠰ࠥ๶"))
    return {}
  try:
    logger.debug(bstack1ll1l11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠬ๷"))
    logger.debug(perform_scan(driver))
    bstack1llll1l11_opy_ = driver.execute_async_script(bstack1l11l111_opy_.bstack1l11l1ll_opy_)
    return bstack1llll1l11_opy_
  except Exception:
    logger.error(bstack1ll1l11_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤ๸"))
    return {}
def bstack1llllll1l1_opy_():
  global CONFIG
  global bstack1ll1ll11l_opy_
  bstack1lll1l1ll1_opy_ = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ๹"), None) and bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ๺"), None)
  if not bstack1ll1lll1l_opy_.bstack1l1lllll1_opy_(CONFIG, bstack1ll1ll11l_opy_) or not bstack1lll1l1ll1_opy_:
        logger.warning(bstack1ll1l11_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦ๻"))
        return False
  return True
def bstack1llll1ll11_opy_(bstack11ll11l111_opy_):
    bstack111l1l111_opy_ = bstack1ll1l11l1l_opy_.current_test_uuid() if bstack1ll1l11l1l_opy_.current_test_uuid() else bstack1lll111111_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack1llllllll1_opy_(bstack111l1l111_opy_, bstack11ll11l111_opy_))
        try:
            return future.result(timeout=bstack11111llll_opy_)
        except TimeoutError:
            logger.error(bstack1ll1l11_opy_ (u"࡚ࠧࡩ࡮ࡧࡲࡹࡹࠦࡡࡧࡶࡨࡶࠥࢁࡽࡴࠢࡺ࡬࡮ࡲࡥࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠦ๼").format(bstack11111llll_opy_))
        except Exception as ex:
            logger.debug(bstack1ll1l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡸࡥࡵࡴ࡬ࡩࡻ࡯࡮ࡨࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡿࢂ࠴ࠠࡆࡴࡵࡳࡷࠦ࠭ࠡࡽࢀࠦ๽").format(bstack11ll11l111_opy_, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack11l1l1l11l_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1ll1ll11l_opy_
  bstack1l1ll1ll_opy_ = not (bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ๾"), None) and bstack11ll111l1_opy_(
          threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ๿"), None))
  bstack111l1llll_opy_ = not (bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ຀"), None) and bstack11ll111l1_opy_(
          threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬກ"), None))
  bstack1111l1lll_opy_ = getattr(driver, bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫຂ"), None) != True
  if not bstack1ll1lll1l_opy_.bstack1l1lllll1_opy_(CONFIG, bstack1ll1ll11l_opy_) or (bstack1111l1lll_opy_ and bstack1l1ll1ll_opy_ and bstack111l1llll_opy_):
    logger.warning(bstack1ll1l11_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷࡻ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠢ຃"))
    return {}
  try:
    bstack111ll11l_opy_ = bstack1ll1l11_opy_ (u"࠭ࡡࡱࡲࠪຄ") in CONFIG and CONFIG.get(bstack1ll1l11_opy_ (u"ࠧࡢࡲࡳࠫ຅"), bstack1ll1l11_opy_ (u"ࠨࠩຆ"))
    session_id = getattr(driver, bstack1ll1l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ງ"), None)
    if not session_id:
      logger.warning(bstack1ll1l11_opy_ (u"ࠥࡒࡴࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡤࡳ࡫ࡹࡩࡷࠨຈ"))
      return {bstack1ll1l11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥຉ"): bstack1ll1l11_opy_ (u"ࠧࡔ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࠥ࡬࡯ࡶࡰࡧࠦຊ")}
    if bstack111ll11l_opy_:
      try:
        bstack11l1llll_opy_ = {
              bstack1ll1l11_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪ຋"): os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬຌ"), os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬຍ"), bstack1ll1l11_opy_ (u"ࠩࠪຎ"))),
              bstack1ll1l11_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪຏ"): bstack1ll1l11l1l_opy_.current_test_uuid() if bstack1ll1l11l1l_opy_.current_test_uuid() else bstack1lll111111_opy_.current_hook_uuid(),
              bstack1ll1l11_opy_ (u"ࠫࡦࡻࡴࡩࡊࡨࡥࡩ࡫ࡲࠨຐ"): os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪຑ")),
              bstack1ll1l11_opy_ (u"࠭ࡳࡤࡣࡱࡘ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ຒ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1ll1l11_opy_ (u"ࠧࡵࡪࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬຓ"): os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ດ"), bstack1ll1l11_opy_ (u"ࠩࠪຕ")),
              bstack1ll1l11_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪຖ"): kwargs.get(bstack1ll1l11_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣࡨࡵ࡭࡮ࡣࡱࡨࠬທ"), None) or bstack1ll1l11_opy_ (u"ࠬ࠭ຘ")
          }
        if not hasattr(thread_local, bstack1ll1l11_opy_ (u"࠭ࡢࡢࡵࡨࡣࡦࡶࡰࡠࡣ࠴࠵ࡾࡥࡳࡤࡴ࡬ࡴࡹ࠭ນ")):
            scripts = {bstack1ll1l11_opy_ (u"ࠧࡴࡥࡤࡲࠬບ"): bstack1l11l111_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack11l1lll1ll_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack11l1lll1ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡵࡦࡥࡳ࠭ປ")] = bstack11l1lll1ll_opy_[bstack1ll1l11_opy_ (u"ࠩࡶࡧࡦࡴࠧຜ")] % json.dumps(bstack11l1llll_opy_)
        bstack1l11l111_opy_.bstack1l1l11ll_opy_(bstack11l1lll1ll_opy_)
        bstack1l11l111_opy_.store()
        bstack1l111l11_opy_ = driver.execute_script(bstack1l11l111_opy_.perform_scan)
      except Exception as bstack1l1lll1l1_opy_:
        logger.info(bstack1ll1l11_opy_ (u"ࠥࡅࡵࡶࡩࡶ࡯ࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࠥຝ") + str(bstack1l1lll1l1_opy_))
        bstack1l111l11_opy_ = {bstack1ll1l11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥພ"): str(bstack1l1lll1l1_opy_)}
    else:
      bstack1l111l11_opy_ = driver.execute_async_script(bstack1l11l111_opy_.perform_scan, {bstack1ll1l11_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬຟ"): kwargs.get(bstack1ll1l11_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧຠ"), None) or bstack1ll1l11_opy_ (u"ࠧࠨມ")})
    return bstack1l111l11_opy_
  except Exception as err:
    logger.error(bstack1ll1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠠࡼࡿࠥຢ").format(str(err)))
    return {}