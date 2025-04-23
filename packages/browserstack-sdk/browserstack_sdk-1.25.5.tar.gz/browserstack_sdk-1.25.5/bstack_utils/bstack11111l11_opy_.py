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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1l11l11l_opy_, bstack11lllll1l1_opy_, bstack11ll111l1_opy_, bstack1l111ll1l1_opy_, \
    bstack11l1llll1ll_opy_
from bstack_utils.measure import measure
def bstack1l111lll11_opy_(bstack111l111ll1l_opy_):
    for driver in bstack111l111ll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11llll1l11_opy_, stage=STAGE.bstack1l11lll1l_opy_)
def bstack11lll1l11_opy_(driver, status, reason=bstack1ll1l11_opy_ (u"ࠨࠩᵴ")):
    bstack11lll1111_opy_ = Config.bstack11111l1l1_opy_()
    if bstack11lll1111_opy_.bstack1111lll11l_opy_():
        return
    bstack111ll1lll_opy_ = bstack111lll111_opy_(bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᵵ"), bstack1ll1l11_opy_ (u"ࠪࠫᵶ"), status, reason, bstack1ll1l11_opy_ (u"ࠫࠬᵷ"), bstack1ll1l11_opy_ (u"ࠬ࠭ᵸ"))
    driver.execute_script(bstack111ll1lll_opy_)
@measure(event_name=EVENTS.bstack11llll1l11_opy_, stage=STAGE.bstack1l11lll1l_opy_)
def bstack11llllll1_opy_(page, status, reason=bstack1ll1l11_opy_ (u"࠭ࠧᵹ")):
    try:
        if page is None:
            return
        bstack11lll1111_opy_ = Config.bstack11111l1l1_opy_()
        if bstack11lll1111_opy_.bstack1111lll11l_opy_():
            return
        bstack111ll1lll_opy_ = bstack111lll111_opy_(bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᵺ"), bstack1ll1l11_opy_ (u"ࠨࠩᵻ"), status, reason, bstack1ll1l11_opy_ (u"ࠩࠪᵼ"), bstack1ll1l11_opy_ (u"ࠪࠫᵽ"))
        page.evaluate(bstack1ll1l11_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᵾ"), bstack111ll1lll_opy_)
    except Exception as e:
        print(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡼࡿࠥᵿ"), e)
def bstack111lll111_opy_(type, name, status, reason, bstack1l111lllll_opy_, bstack11lll11111_opy_):
    bstack1l1ll111ll_opy_ = {
        bstack1ll1l11_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ᶀ"): type,
        bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᶁ"): {}
    }
    if type == bstack1ll1l11_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪᶂ"):
        bstack1l1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᶃ")][bstack1ll1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᶄ")] = bstack1l111lllll_opy_
        bstack1l1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᶅ")][bstack1ll1l11_opy_ (u"ࠬࡪࡡࡵࡣࠪᶆ")] = json.dumps(str(bstack11lll11111_opy_))
    if type == bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᶇ"):
        bstack1l1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᶈ")][bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᶉ")] = name
    if type == bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᶊ"):
        bstack1l1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᶋ")][bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᶌ")] = status
        if status == bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᶍ") and str(reason) != bstack1ll1l11_opy_ (u"ࠨࠢᶎ"):
            bstack1l1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᶏ")][bstack1ll1l11_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨᶐ")] = json.dumps(str(reason))
    bstack11ll111l11_opy_ = bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧᶑ").format(json.dumps(bstack1l1ll111ll_opy_))
    return bstack11ll111l11_opy_
def bstack1l1l111l11_opy_(url, config, logger, bstack1lll1ll111_opy_=False):
    hostname = bstack11lllll1l1_opy_(url)
    is_private = bstack1l111ll1l1_opy_(hostname)
    try:
        if is_private or bstack1lll1ll111_opy_:
            file_path = bstack11l1l11l11l_opy_(bstack1ll1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᶒ"), bstack1ll1l11_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪᶓ"), logger)
            if os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᶔ")) and eval(
                    os.environ.get(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᶕ"))):
                return
            if (bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᶖ") in config and not config[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᶗ")]):
                os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᶘ")] = str(True)
                bstack111l111l1ll_opy_ = {bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬᶙ"): hostname}
                bstack11l1llll1ll_opy_(bstack1ll1l11_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪᶚ"), bstack1ll1l11_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪᶛ"), bstack111l111l1ll_opy_, logger)
    except Exception as e:
        pass
def bstack111l11lll_opy_(caps, bstack111l111lll1_opy_):
    if bstack1ll1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᶜ") in caps:
        caps[bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᶝ")][bstack1ll1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧᶞ")] = True
        if bstack111l111lll1_opy_:
            caps[bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᶟ")][bstack1ll1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᶠ")] = bstack111l111lll1_opy_
    else:
        caps[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩᶡ")] = True
        if bstack111l111lll1_opy_:
            caps[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᶢ")] = bstack111l111lll1_opy_
def bstack111l1ll1111_opy_(bstack111l1l111l_opy_):
    bstack111l111ll11_opy_ = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪᶣ"), bstack1ll1l11_opy_ (u"ࠧࠨᶤ"))
    if bstack111l111ll11_opy_ == bstack1ll1l11_opy_ (u"ࠨࠩᶥ") or bstack111l111ll11_opy_ == bstack1ll1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᶦ"):
        threading.current_thread().testStatus = bstack111l1l111l_opy_
    else:
        if bstack111l1l111l_opy_ == bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᶧ"):
            threading.current_thread().testStatus = bstack111l1l111l_opy_