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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1l1111ll_opy_, bstack1l11l111_opy_, bstack1l1llll11l_opy_, bstack11ll1lll1_opy_, \
    bstack11l1l11l11l_opy_
from bstack_utils.measure import measure
def bstack111111l11_opy_(bstack111l111ll11_opy_):
    for driver in bstack111l111ll11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1l11ll_opy_, stage=STAGE.bstack1l11111ll1_opy_)
def bstack1l1l11l111_opy_(driver, status, reason=bstack11111ll_opy_ (u"ࠪࠫᵶ")):
    bstack11l1l1ll_opy_ = Config.bstack11l1ll1ll1_opy_()
    if bstack11l1l1ll_opy_.bstack1111lllll1_opy_():
        return
    bstack1111ll1l1_opy_ = bstack1l1l1ll1l_opy_(bstack11111ll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᵷ"), bstack11111ll_opy_ (u"ࠬ࠭ᵸ"), status, reason, bstack11111ll_opy_ (u"࠭ࠧᵹ"), bstack11111ll_opy_ (u"ࠧࠨᵺ"))
    driver.execute_script(bstack1111ll1l1_opy_)
@measure(event_name=EVENTS.bstack1ll1l11ll_opy_, stage=STAGE.bstack1l11111ll1_opy_)
def bstack1lllll11l_opy_(page, status, reason=bstack11111ll_opy_ (u"ࠨࠩᵻ")):
    try:
        if page is None:
            return
        bstack11l1l1ll_opy_ = Config.bstack11l1ll1ll1_opy_()
        if bstack11l1l1ll_opy_.bstack1111lllll1_opy_():
            return
        bstack1111ll1l1_opy_ = bstack1l1l1ll1l_opy_(bstack11111ll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᵼ"), bstack11111ll_opy_ (u"ࠪࠫᵽ"), status, reason, bstack11111ll_opy_ (u"ࠫࠬᵾ"), bstack11111ll_opy_ (u"ࠬ࠭ᵿ"))
        page.evaluate(bstack11111ll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᶀ"), bstack1111ll1l1_opy_)
    except Exception as e:
        print(bstack11111ll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧᶁ"), e)
def bstack1l1l1ll1l_opy_(type, name, status, reason, bstack1lll1l1l1_opy_, bstack11ll1ll11_opy_):
    bstack1ll1ll11_opy_ = {
        bstack11111ll_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨᶂ"): type,
        bstack11111ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᶃ"): {}
    }
    if type == bstack11111ll_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬᶄ"):
        bstack1ll1ll11_opy_[bstack11111ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᶅ")][bstack11111ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᶆ")] = bstack1lll1l1l1_opy_
        bstack1ll1ll11_opy_[bstack11111ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᶇ")][bstack11111ll_opy_ (u"ࠧࡥࡣࡷࡥࠬᶈ")] = json.dumps(str(bstack11ll1ll11_opy_))
    if type == bstack11111ll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᶉ"):
        bstack1ll1ll11_opy_[bstack11111ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᶊ")][bstack11111ll_opy_ (u"ࠪࡲࡦࡳࡥࠨᶋ")] = name
    if type == bstack11111ll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᶌ"):
        bstack1ll1ll11_opy_[bstack11111ll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᶍ")][bstack11111ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᶎ")] = status
        if status == bstack11111ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᶏ") and str(reason) != bstack11111ll_opy_ (u"ࠣࠤᶐ"):
            bstack1ll1ll11_opy_[bstack11111ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᶑ")][bstack11111ll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪᶒ")] = json.dumps(str(reason))
    bstack1l1lllll1_opy_ = bstack11111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩᶓ").format(json.dumps(bstack1ll1ll11_opy_))
    return bstack1l1lllll1_opy_
def bstack1llll1ll_opy_(url, config, logger, bstack11l11lll1l_opy_=False):
    hostname = bstack1l11l111_opy_(url)
    is_private = bstack11ll1lll1_opy_(hostname)
    try:
        if is_private or bstack11l11lll1l_opy_:
            file_path = bstack11l1l1111ll_opy_(bstack11111ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᶔ"), bstack11111ll_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᶕ"), logger)
            if os.environ.get(bstack11111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᶖ")) and eval(
                    os.environ.get(bstack11111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᶗ"))):
                return
            if (bstack11111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᶘ") in config and not config[bstack11111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᶙ")]):
                os.environ[bstack11111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᶚ")] = str(True)
                bstack111l111lll1_opy_ = {bstack11111ll_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧᶛ"): hostname}
                bstack11l1l11l11l_opy_(bstack11111ll_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᶜ"), bstack11111ll_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬᶝ"), bstack111l111lll1_opy_, logger)
    except Exception as e:
        pass
def bstack111ll1ll_opy_(caps, bstack111l111ll1l_opy_):
    if bstack11111ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᶞ") in caps:
        caps[bstack11111ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᶟ")][bstack11111ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩᶠ")] = True
        if bstack111l111ll1l_opy_:
            caps[bstack11111ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᶡ")][bstack11111ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᶢ")] = bstack111l111ll1l_opy_
    else:
        caps[bstack11111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫᶣ")] = True
        if bstack111l111ll1l_opy_:
            caps[bstack11111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᶤ")] = bstack111l111ll1l_opy_
def bstack111l1l11l11_opy_(bstack111lll1111_opy_):
    bstack111l111l1ll_opy_ = bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬᶥ"), bstack11111ll_opy_ (u"ࠩࠪᶦ"))
    if bstack111l111l1ll_opy_ == bstack11111ll_opy_ (u"ࠪࠫᶧ") or bstack111l111l1ll_opy_ == bstack11111ll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᶨ"):
        threading.current_thread().testStatus = bstack111lll1111_opy_
    else:
        if bstack111lll1111_opy_ == bstack11111ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᶩ"):
            threading.current_thread().testStatus = bstack111lll1111_opy_