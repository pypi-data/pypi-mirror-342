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
import threading
import logging
import bstack_utils.accessibility as bstack1l1111l1_opy_
from bstack_utils.helper import bstack1l1llll11l_opy_
logger = logging.getLogger(__name__)
def bstack1lllll1111_opy_(bstack11ll1l1ll1_opy_):
  return True if bstack11ll1l1ll1_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1ll11111_opy_(context, *args):
    tags = getattr(args[0], bstack11111ll_opy_ (u"ࠧࡵࡣࡪࡷࠬᙐ"), [])
    bstack1ll1l1111l_opy_ = bstack1l1111l1_opy_.bstack11l11ll1l1_opy_(tags)
    threading.current_thread().isA11yTest = bstack1ll1l1111l_opy_
    try:
      bstack1ll1111l_opy_ = threading.current_thread().bstackSessionDriver if bstack1lllll1111_opy_(bstack11111ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧᙑ")) else context.browser
      if bstack1ll1111l_opy_ and bstack1ll1111l_opy_.session_id and bstack1ll1l1111l_opy_ and bstack1l1llll11l_opy_(
              threading.current_thread(), bstack11111ll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᙒ"), None):
          threading.current_thread().isA11yTest = bstack1l1111l1_opy_.bstack1l11l1l11_opy_(bstack1ll1111l_opy_, bstack1ll1l1111l_opy_)
    except Exception as e:
       logger.debug(bstack11111ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡧ࠱࠲ࡻࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࡀࠠࡼࡿࠪᙓ").format(str(e)))
def bstack11ll1111l_opy_(bstack1ll1111l_opy_):
    if bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᙔ"), None) and bstack1l1llll11l_opy_(
      threading.current_thread(), bstack11111ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᙕ"), None) and not bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"࠭ࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࠩᙖ"), False):
      threading.current_thread().a11y_stop = True
      bstack1l1111l1_opy_.bstack11ll11l1l_opy_(bstack1ll1111l_opy_, name=bstack11111ll_opy_ (u"ࠢࠣᙗ"), path=bstack11111ll_opy_ (u"ࠣࠤᙘ"))