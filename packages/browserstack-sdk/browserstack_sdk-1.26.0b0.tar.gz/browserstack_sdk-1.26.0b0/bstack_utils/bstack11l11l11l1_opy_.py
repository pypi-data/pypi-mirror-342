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
import threading
from bstack_utils.helper import bstack1l1111llll_opy_
from bstack_utils.constants import bstack11ll1ll11l1_opy_, EVENTS, STAGE
from bstack_utils.bstack11ll11llll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11lll1l1_opy_:
    bstack111l11lll11_opy_ = None
    @classmethod
    def bstack1l1lll1l1l_opy_(cls):
        if cls.on() and os.getenv(bstack11111ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥἣ")):
            logger.info(
                bstack11111ll_opy_ (u"࠭ࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠩἤ").format(os.getenv(bstack11111ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧἥ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬἦ"), None) is None or os.environ[bstack11111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ἧ")] == bstack11111ll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣἨ"):
            return False
        return True
    @classmethod
    def bstack1111l1l11ll_opy_(cls, bs_config, framework=bstack11111ll_opy_ (u"ࠦࠧἩ")):
        bstack11lll111l1l_opy_ = False
        for fw in bstack11ll1ll11l1_opy_:
            if fw in framework:
                bstack11lll111l1l_opy_ = True
        return bstack1l1111llll_opy_(bs_config.get(bstack11111ll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩἪ"), bstack11lll111l1l_opy_))
    @classmethod
    def bstack1111l1l111l_opy_(cls, framework):
        return framework in bstack11ll1ll11l1_opy_
    @classmethod
    def bstack1111ll11ll1_opy_(cls, bs_config, framework):
        return cls.bstack1111l1l11ll_opy_(bs_config, framework) is True and cls.bstack1111l1l111l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11111ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪἫ"), None)
    @staticmethod
    def bstack11l11111l1_opy_():
        if getattr(threading.current_thread(), bstack11111ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫἬ"), None):
            return {
                bstack11111ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭Ἥ"): bstack11111ll_opy_ (u"ࠩࡷࡩࡸࡺࠧἮ"),
                bstack11111ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪἯ"): getattr(threading.current_thread(), bstack11111ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨἰ"), None)
            }
        if getattr(threading.current_thread(), bstack11111ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩἱ"), None):
            return {
                bstack11111ll_opy_ (u"࠭ࡴࡺࡲࡨࠫἲ"): bstack11111ll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬἳ"),
                bstack11111ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨἴ"): getattr(threading.current_thread(), bstack11111ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ἵ"), None)
            }
        return None
    @staticmethod
    def bstack1111l11lll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11lll1l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111l1l111l_opy_(test, hook_name=None):
        bstack1111l11llll_opy_ = test.parent
        if hook_name in [bstack11111ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨἶ"), bstack11111ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬἷ"), bstack11111ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫἸ"), bstack11111ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨἹ")]:
            bstack1111l11llll_opy_ = test
        scope = []
        while bstack1111l11llll_opy_ is not None:
            scope.append(bstack1111l11llll_opy_.name)
            bstack1111l11llll_opy_ = bstack1111l11llll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1111l1l1111_opy_(hook_type):
        if hook_type == bstack11111ll_opy_ (u"ࠢࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠧἺ"):
            return bstack11111ll_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡩࡱࡲ࡯ࠧἻ")
        elif hook_type == bstack11111ll_opy_ (u"ࠤࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍࠨἼ"):
            return bstack11111ll_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥ࡮࡯ࡰ࡭ࠥἽ")
    @staticmethod
    def bstack1111l1l11l1_opy_(bstack1l1llll1l_opy_):
        try:
            if not bstack11lll1l1_opy_.on():
                return bstack1l1llll1l_opy_
            if os.environ.get(bstack11111ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠤἾ"), None) == bstack11111ll_opy_ (u"ࠧࡺࡲࡶࡧࠥἿ"):
                tests = os.environ.get(bstack11111ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠥὀ"), None)
                if tests is None or tests == bstack11111ll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧὁ"):
                    return bstack1l1llll1l_opy_
                bstack1l1llll1l_opy_ = tests.split(bstack11111ll_opy_ (u"ࠨ࠮ࠪὂ"))
                return bstack1l1llll1l_opy_
        except Exception as exc:
            logger.debug(bstack11111ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡨࡶࡺࡴࠠࡩࡣࡱࡨࡱ࡫ࡲ࠻ࠢࠥὃ") + str(str(exc)) + bstack11111ll_opy_ (u"ࠥࠦὄ"))
        return bstack1l1llll1l_opy_