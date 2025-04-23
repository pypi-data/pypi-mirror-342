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
from browserstack_sdk.bstack1l111llll1_opy_ import bstack1ll1l1l1l1_opy_
from browserstack_sdk.bstack111ll1ll1l_opy_ import RobotHandler
def bstack1l1lll111l_opy_(framework):
    if framework.lower() == bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᦑ"):
        return bstack1ll1l1l1l1_opy_.version()
    elif framework.lower() == bstack1ll1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᦒ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1ll1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩᦓ"):
        import behave
        return behave.__version__
    else:
        return bstack1ll1l11_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫᦔ")
def bstack1l1l1l1l1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1ll1l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ᦕ"))
        framework_version.append(importlib.metadata.version(bstack1ll1l11_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᦖ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᦗ"))
        framework_version.append(importlib.metadata.version(bstack1ll1l11_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᦘ")))
    except:
        pass
    return {
        bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᦙ"): bstack1ll1l11_opy_ (u"ࠩࡢࠫᦚ").join(framework_name),
        bstack1ll1l11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫᦛ"): bstack1ll1l11_opy_ (u"ࠫࡤ࠭ᦜ").join(framework_version)
    }