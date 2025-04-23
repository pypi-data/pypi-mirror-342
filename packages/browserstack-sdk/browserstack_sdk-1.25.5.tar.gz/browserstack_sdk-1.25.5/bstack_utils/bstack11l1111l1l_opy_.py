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
import threading
from bstack_utils.helper import bstack11l1llllll_opy_
from bstack_utils.constants import bstack11ll1l1l1l1_opy_, EVENTS, STAGE
from bstack_utils.bstack1ll1lllll_opy_ import get_logger
logger = get_logger(__name__)
class bstack1lll111111_opy_:
    bstack111l11llll1_opy_ = None
    @classmethod
    def bstack1l11l1l1_opy_(cls):
        if cls.on() and os.getenv(bstack1ll1l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣἡ")):
            logger.info(
                bstack1ll1l11_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧἢ").format(os.getenv(bstack1ll1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥἣ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪἤ"), None) is None or os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫἥ")] == bstack1ll1l11_opy_ (u"ࠣࡰࡸࡰࡱࠨἦ"):
            return False
        return True
    @classmethod
    def bstack1111l1l1ll1_opy_(cls, bs_config, framework=bstack1ll1l11_opy_ (u"ࠤࠥἧ")):
        bstack11lll111l1l_opy_ = False
        for fw in bstack11ll1l1l1l1_opy_:
            if fw in framework:
                bstack11lll111l1l_opy_ = True
        return bstack11l1llllll_opy_(bs_config.get(bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧἨ"), bstack11lll111l1l_opy_))
    @classmethod
    def bstack1111l11lll1_opy_(cls, framework):
        return framework in bstack11ll1l1l1l1_opy_
    @classmethod
    def bstack1111ll1111l_opy_(cls, bs_config, framework):
        return cls.bstack1111l1l1ll1_opy_(bs_config, framework) is True and cls.bstack1111l11lll1_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨἩ"), None)
    @staticmethod
    def bstack11l11l111l_opy_():
        if getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩἪ"), None):
            return {
                bstack1ll1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫἫ"): bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࠬἬ"),
                bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨἭ"): getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭Ἦ"), None)
            }
        if getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧἯ"), None):
            return {
                bstack1ll1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩἰ"): bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪἱ"),
                bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ἲ"): getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫἳ"), None)
            }
        return None
    @staticmethod
    def bstack1111l1l11l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lll111111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111ll11ll1_opy_(test, hook_name=None):
        bstack1111l1l1111_opy_ = test.parent
        if hook_name in [bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ἴ"), bstack1ll1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪἵ"), bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩἶ"), bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ἷ")]:
            bstack1111l1l1111_opy_ = test
        scope = []
        while bstack1111l1l1111_opy_ is not None:
            scope.append(bstack1111l1l1111_opy_.name)
            bstack1111l1l1111_opy_ = bstack1111l1l1111_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1111l11llll_opy_(hook_type):
        if hook_type == bstack1ll1l11_opy_ (u"ࠧࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠥἸ"):
            return bstack1ll1l11_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡮࡯ࡰ࡭ࠥἹ")
        elif hook_type == bstack1ll1l11_opy_ (u"ࠢࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠦἺ"):
            return bstack1ll1l11_opy_ (u"ࠣࡖࡨࡥࡷࡪ࡯ࡸࡰࠣ࡬ࡴࡵ࡫ࠣἻ")
    @staticmethod
    def bstack1111l1l111l_opy_(bstack11lll1l11l_opy_):
        try:
            if not bstack1lll111111_opy_.on():
                return bstack11lll1l11l_opy_
            if os.environ.get(bstack1ll1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠢἼ"), None) == bstack1ll1l11_opy_ (u"ࠥࡸࡷࡻࡥࠣἽ"):
                tests = os.environ.get(bstack1ll1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠣἾ"), None)
                if tests is None or tests == bstack1ll1l11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥἿ"):
                    return bstack11lll1l11l_opy_
                bstack11lll1l11l_opy_ = tests.split(bstack1ll1l11_opy_ (u"࠭ࠬࠨὀ"))
                return bstack11lll1l11l_opy_
        except Exception as exc:
            logger.debug(bstack1ll1l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡦࡴࡸࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡀࠠࠣὁ") + str(str(exc)) + bstack1ll1l11_opy_ (u"ࠣࠤὂ"))
        return bstack11lll1l11l_opy_