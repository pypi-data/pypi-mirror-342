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
import re
from bstack_utils.bstack11lll111ll_opy_ import bstack111l1l11l11_opy_
def bstack111l1l1l111_opy_(fixture_name):
    if fixture_name.startswith(bstack11111ll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᴫ")):
        return bstack11111ll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᴬ")
    elif fixture_name.startswith(bstack11111ll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᴭ")):
        return bstack11111ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᴮ")
    elif fixture_name.startswith(bstack11111ll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᴯ")):
        return bstack11111ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᴰ")
    elif fixture_name.startswith(bstack11111ll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᴱ")):
        return bstack11111ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᴲ")
def bstack111l1ll1111_opy_(fixture_name):
    return bool(re.match(bstack11111ll_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᴳ"), fixture_name))
def bstack111l1l11ll1_opy_(fixture_name):
    return bool(re.match(bstack11111ll_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᴴ"), fixture_name))
def bstack111l1l11lll_opy_(fixture_name):
    return bool(re.match(bstack11111ll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᴵ"), fixture_name))
def bstack111l1l1ll1l_opy_(fixture_name):
    if fixture_name.startswith(bstack11111ll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᴶ")):
        return bstack11111ll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᴷ"), bstack11111ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᴸ")
    elif fixture_name.startswith(bstack11111ll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᴹ")):
        return bstack11111ll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᴺ"), bstack11111ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᴻ")
    elif fixture_name.startswith(bstack11111ll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᴼ")):
        return bstack11111ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᴽ"), bstack11111ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᴾ")
    elif fixture_name.startswith(bstack11111ll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᴿ")):
        return bstack11111ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᵀ"), bstack11111ll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᵁ")
    return None, None
def bstack111l1l111ll_opy_(hook_name):
    if hook_name in [bstack11111ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᵂ"), bstack11111ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᵃ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111l1l11l1l_opy_(hook_name):
    if hook_name in [bstack11111ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᵄ"), bstack11111ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᵅ")]:
        return bstack11111ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᵆ")
    elif hook_name in [bstack11111ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᵇ"), bstack11111ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᵈ")]:
        return bstack11111ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᵉ")
    elif hook_name in [bstack11111ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᵊ"), bstack11111ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᵋ")]:
        return bstack11111ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᵌ")
    elif hook_name in [bstack11111ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᵍ"), bstack11111ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᵎ")]:
        return bstack11111ll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᵏ")
    return hook_name
def bstack111l1l1llll_opy_(node, scenario):
    if hasattr(node, bstack11111ll_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᵐ")):
        parts = node.nodeid.rsplit(bstack11111ll_opy_ (u"ࠣ࡝ࠥᵑ"))
        params = parts[-1]
        return bstack11111ll_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᵒ").format(scenario.name, params)
    return scenario.name
def bstack111l1l1l1ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11111ll_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᵓ")):
            examples = list(node.callspec.params[bstack11111ll_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᵔ")].values())
        return examples
    except:
        return []
def bstack111l1l1l11l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111l1l1lll1_opy_(report):
    try:
        status = bstack11111ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᵕ")
        if report.passed or (report.failed and hasattr(report, bstack11111ll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᵖ"))):
            status = bstack11111ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᵗ")
        elif report.skipped:
            status = bstack11111ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᵘ")
        bstack111l1l11l11_opy_(status)
    except:
        pass
def bstack11l1l11l_opy_(status):
    try:
        bstack111l1l1ll11_opy_ = bstack11111ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᵙ")
        if status == bstack11111ll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᵚ"):
            bstack111l1l1ll11_opy_ = bstack11111ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᵛ")
        elif status == bstack11111ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᵜ"):
            bstack111l1l1ll11_opy_ = bstack11111ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᵝ")
        bstack111l1l11l11_opy_(bstack111l1l1ll11_opy_)
    except:
        pass
def bstack111l1l1l1l1_opy_(item=None, report=None, summary=None, extra=None):
    return