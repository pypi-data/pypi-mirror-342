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
from browserstack_sdk.bstack11l1lll1ll_opy_ import bstack11llll1l_opy_
from browserstack_sdk.bstack111l1l1111_opy_ import RobotHandler
def bstack1l1111l1l_opy_(framework):
    if framework.lower() == bstack11111ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᦒ"):
        return bstack11llll1l_opy_.version()
    elif framework.lower() == bstack11111ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᦓ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11111ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᦔ"):
        import behave
        return behave.__version__
    else:
        return bstack11111ll_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࠬᦕ")
def bstack1ll1llll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11111ll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧᦖ"))
        framework_version.append(importlib.metadata.version(bstack11111ll_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᦗ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11111ll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᦘ"))
        framework_version.append(importlib.metadata.version(bstack11111ll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᦙ")))
    except:
        pass
    return {
        bstack11111ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᦚ"): bstack11111ll_opy_ (u"ࠪࡣࠬᦛ").join(framework_name),
        bstack11111ll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᦜ"): bstack11111ll_opy_ (u"ࠬࡥࠧᦝ").join(framework_version)
    }