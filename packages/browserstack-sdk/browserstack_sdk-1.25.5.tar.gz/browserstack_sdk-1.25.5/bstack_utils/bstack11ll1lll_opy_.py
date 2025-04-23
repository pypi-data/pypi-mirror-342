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
import threading
import logging
import bstack_utils.accessibility as bstack1ll1lll1l_opy_
from bstack_utils.helper import bstack11ll111l1_opy_
logger = logging.getLogger(__name__)
def bstack1l11l111l1_opy_(bstack1l1l1l111l_opy_):
  return True if bstack1l1l1l111l_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1llll1111_opy_(context, *args):
    tags = getattr(args[0], bstack1ll1l11_opy_ (u"ࠧࡵࡣࡪࡷࠬᙐ"), [])
    bstack1l1111ll_opy_ = bstack1ll1lll1l_opy_.bstack11ll1ll1l1_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l1111ll_opy_
    try:
      bstack11ll1l1111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11l111l1_opy_(bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧᙑ")) else context.browser
      if bstack11ll1l1111_opy_ and bstack11ll1l1111_opy_.session_id and bstack1l1111ll_opy_ and bstack11ll111l1_opy_(
              threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᙒ"), None):
          threading.current_thread().isA11yTest = bstack1ll1lll1l_opy_.bstack1lllll111l_opy_(bstack11ll1l1111_opy_, bstack1l1111ll_opy_)
    except Exception as e:
       logger.debug(bstack1ll1l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡧ࠱࠲ࡻࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࡀࠠࡼࡿࠪᙓ").format(str(e)))
def bstack1ll1lll1ll_opy_(bstack11ll1l1111_opy_):
    if bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᙔ"), None) and bstack11ll111l1_opy_(
      threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᙕ"), None) and not bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࠩᙖ"), False):
      threading.current_thread().a11y_stop = True
      bstack1ll1lll1l_opy_.bstack11111lll_opy_(bstack11ll1l1111_opy_, name=bstack1ll1l11_opy_ (u"ࠢࠣᙗ"), path=bstack1ll1l11_opy_ (u"ࠣࠤᙘ"))