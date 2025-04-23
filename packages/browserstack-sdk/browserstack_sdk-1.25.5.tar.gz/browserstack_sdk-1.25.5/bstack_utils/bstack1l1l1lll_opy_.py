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
import re
from bstack_utils.bstack11111l11_opy_ import bstack111l1ll1111_opy_
def bstack111l1l11l1l_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll1l11_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᴩ")):
        return bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᴪ")
    elif fixture_name.startswith(bstack1ll1l11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᴫ")):
        return bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᴬ")
    elif fixture_name.startswith(bstack1ll1l11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᴭ")):
        return bstack1ll1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᴮ")
    elif fixture_name.startswith(bstack1ll1l11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᴯ")):
        return bstack1ll1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᴰ")
def bstack111l1l11l11_opy_(fixture_name):
    return bool(re.match(bstack1ll1l11_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࠪࡩࡹࡳࡩࡴࡪࡱࡱࢀࡲࡵࡤࡶ࡮ࡨ࠭ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᴱ"), fixture_name))
def bstack111l1l1ll11_opy_(fixture_name):
    return bool(re.match(bstack1ll1l11_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᴲ"), fixture_name))
def bstack111l1l1l1l1_opy_(fixture_name):
    return bool(re.match(bstack1ll1l11_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᴳ"), fixture_name))
def bstack111l1l1l1ll_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll1l11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᴴ")):
        return bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᴵ"), bstack1ll1l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᴶ")
    elif fixture_name.startswith(bstack1ll1l11_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᴷ")):
        return bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᴸ"), bstack1ll1l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᴹ")
    elif fixture_name.startswith(bstack1ll1l11_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᴺ")):
        return bstack1ll1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᴻ"), bstack1ll1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᴼ")
    elif fixture_name.startswith(bstack1ll1l11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᴽ")):
        return bstack1ll1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᴾ"), bstack1ll1l11_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᴿ")
    return None, None
def bstack111l1l11ll1_opy_(hook_name):
    if hook_name in [bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᵀ"), bstack1ll1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᵁ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111l1l1llll_opy_(hook_name):
    if hook_name in [bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᵂ"), bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᵃ")]:
        return bstack1ll1l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᵄ")
    elif hook_name in [bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩᵅ"), bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᵆ")]:
        return bstack1ll1l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᵇ")
    elif hook_name in [bstack1ll1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᵈ"), bstack1ll1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᵉ")]:
        return bstack1ll1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᵊ")
    elif hook_name in [bstack1ll1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᵋ"), bstack1ll1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᵌ")]:
        return bstack1ll1l11_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᵍ")
    return hook_name
def bstack111l1l111ll_opy_(node, scenario):
    if hasattr(node, bstack1ll1l11_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᵎ")):
        parts = node.nodeid.rsplit(bstack1ll1l11_opy_ (u"ࠨ࡛ࠣᵏ"))
        params = parts[-1]
        return bstack1ll1l11_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢᵐ").format(scenario.name, params)
    return scenario.name
def bstack111l1l1ll1l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1ll1l11_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᵑ")):
            examples = list(node.callspec.params[bstack1ll1l11_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨᵒ")].values())
        return examples
    except:
        return []
def bstack111l1l11lll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111l1l1l111_opy_(report):
    try:
        status = bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᵓ")
        if report.passed or (report.failed and hasattr(report, bstack1ll1l11_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᵔ"))):
            status = bstack1ll1l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᵕ")
        elif report.skipped:
            status = bstack1ll1l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᵖ")
        bstack111l1ll1111_opy_(status)
    except:
        pass
def bstack1l1lll1l1l_opy_(status):
    try:
        bstack111l1l1lll1_opy_ = bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᵗ")
        if status == bstack1ll1l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᵘ"):
            bstack111l1l1lll1_opy_ = bstack1ll1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᵙ")
        elif status == bstack1ll1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᵚ"):
            bstack111l1l1lll1_opy_ = bstack1ll1l11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᵛ")
        bstack111l1ll1111_opy_(bstack111l1l1lll1_opy_)
    except:
        pass
def bstack111l1l1l11l_opy_(item=None, report=None, summary=None, extra=None):
    return