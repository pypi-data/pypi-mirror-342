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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l111l11ll_opy_
bstack11l1l1ll_opy_ = Config.bstack11l1ll1ll1_opy_()
def bstack111l1ll1l1l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111l1ll1lll_opy_(bstack111l1ll1ll1_opy_, bstack111l1ll111l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111l1ll1ll1_opy_):
        with open(bstack111l1ll1ll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111l1ll1l1l_opy_(bstack111l1ll1ll1_opy_):
        pac = get_pac(url=bstack111l1ll1ll1_opy_)
    else:
        raise Exception(bstack11111ll_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩᴅ").format(bstack111l1ll1ll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11111ll_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦᴆ"), 80))
        bstack111l1ll1l11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111l1ll1l11_opy_ = bstack11111ll_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬᴇ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111l1ll111l_opy_, bstack111l1ll1l11_opy_)
    return proxy_url
def bstack1ll111ll1l_opy_(config):
    return bstack11111ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᴈ") in config or bstack11111ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᴉ") in config
def bstack11lll1l1ll_opy_(config):
    if not bstack1ll111ll1l_opy_(config):
        return
    if config.get(bstack11111ll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᴊ")):
        return config.get(bstack11111ll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᴋ"))
    if config.get(bstack11111ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᴌ")):
        return config.get(bstack11111ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᴍ"))
def bstack1l1l11ll_opy_(config, bstack111l1ll111l_opy_):
    proxy = bstack11lll1l1ll_opy_(config)
    proxies = {}
    if config.get(bstack11111ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᴎ")) or config.get(bstack11111ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᴏ")):
        if proxy.endswith(bstack11111ll_opy_ (u"࠭࠮ࡱࡣࡦࠫᴐ")):
            proxies = bstack1l111111_opy_(proxy, bstack111l1ll111l_opy_)
        else:
            proxies = {
                bstack11111ll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᴑ"): proxy
            }
    bstack11l1l1ll_opy_.bstack1ll11111l_opy_(bstack11111ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨᴒ"), proxies)
    return proxies
def bstack1l111111_opy_(bstack111l1ll1ll1_opy_, bstack111l1ll111l_opy_):
    proxies = {}
    global bstack111l1ll11l1_opy_
    if bstack11111ll_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬᴓ") in globals():
        return bstack111l1ll11l1_opy_
    try:
        proxy = bstack111l1ll1lll_opy_(bstack111l1ll1ll1_opy_, bstack111l1ll111l_opy_)
        if bstack11111ll_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥᴔ") in proxy:
            proxies = {}
        elif bstack11111ll_opy_ (u"ࠦࡍ࡚ࡔࡑࠤᴕ") in proxy or bstack11111ll_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦᴖ") in proxy or bstack11111ll_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧᴗ") in proxy:
            bstack111l1ll11ll_opy_ = proxy.split(bstack11111ll_opy_ (u"ࠢࠡࠤᴘ"))
            if bstack11111ll_opy_ (u"ࠣ࠼࠲࠳ࠧᴙ") in bstack11111ll_opy_ (u"ࠤࠥᴚ").join(bstack111l1ll11ll_opy_[1:]):
                proxies = {
                    bstack11111ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᴛ"): bstack11111ll_opy_ (u"ࠦࠧᴜ").join(bstack111l1ll11ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack11111ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᴝ"): str(bstack111l1ll11ll_opy_[0]).lower() + bstack11111ll_opy_ (u"ࠨ࠺࠰࠱ࠥᴞ") + bstack11111ll_opy_ (u"ࠢࠣᴟ").join(bstack111l1ll11ll_opy_[1:])
                }
        elif bstack11111ll_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢᴠ") in proxy:
            bstack111l1ll11ll_opy_ = proxy.split(bstack11111ll_opy_ (u"ࠤࠣࠦᴡ"))
            if bstack11111ll_opy_ (u"ࠥ࠾࠴࠵ࠢᴢ") in bstack11111ll_opy_ (u"ࠦࠧᴣ").join(bstack111l1ll11ll_opy_[1:]):
                proxies = {
                    bstack11111ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᴤ"): bstack11111ll_opy_ (u"ࠨࠢᴥ").join(bstack111l1ll11ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack11111ll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᴦ"): bstack11111ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᴧ") + bstack11111ll_opy_ (u"ࠤࠥᴨ").join(bstack111l1ll11ll_opy_[1:])
                }
        else:
            proxies = {
                bstack11111ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᴩ"): proxy
            }
    except Exception as e:
        print(bstack11111ll_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᴪ"), bstack11l111l11ll_opy_.format(bstack111l1ll1ll1_opy_, str(e)))
    bstack111l1ll11l1_opy_ = proxies
    return proxies