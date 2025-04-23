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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1111llll_opy_
bstack11lll1111_opy_ = Config.bstack11111l1l1_opy_()
def bstack111l1ll11l1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111l1ll1ll1_opy_(bstack111l1ll1l1l_opy_, bstack111l1ll1lll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111l1ll1l1l_opy_):
        with open(bstack111l1ll1l1l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111l1ll11l1_opy_(bstack111l1ll1l1l_opy_):
        pac = get_pac(url=bstack111l1ll1l1l_opy_)
    else:
        raise Exception(bstack1ll1l11_opy_ (u"ࠧࡑࡣࡦࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠧᴃ").format(bstack111l1ll1l1l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1ll1l11_opy_ (u"ࠣ࠺࠱࠼࠳࠾࠮࠹ࠤᴄ"), 80))
        bstack111l1ll1l11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111l1ll1l11_opy_ = bstack1ll1l11_opy_ (u"ࠩ࠳࠲࠵࠴࠰࠯࠲ࠪᴅ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111l1ll1lll_opy_, bstack111l1ll1l11_opy_)
    return proxy_url
def bstack1ll11l1ll_opy_(config):
    return bstack1ll1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᴆ") in config or bstack1ll1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᴇ") in config
def bstack11l11ll11_opy_(config):
    if not bstack1ll11l1ll_opy_(config):
        return
    if config.get(bstack1ll1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᴈ")):
        return config.get(bstack1ll1l11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᴉ"))
    if config.get(bstack1ll1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᴊ")):
        return config.get(bstack1ll1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᴋ"))
def bstack1ll1l1111_opy_(config, bstack111l1ll1lll_opy_):
    proxy = bstack11l11ll11_opy_(config)
    proxies = {}
    if config.get(bstack1ll1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᴌ")) or config.get(bstack1ll1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᴍ")):
        if proxy.endswith(bstack1ll1l11_opy_ (u"ࠫ࠳ࡶࡡࡤࠩᴎ")):
            proxies = bstack1llll1l11l_opy_(proxy, bstack111l1ll1lll_opy_)
        else:
            proxies = {
                bstack1ll1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᴏ"): proxy
            }
    bstack11lll1111_opy_.bstack1lll11lll1_opy_(bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ᴐ"), proxies)
    return proxies
def bstack1llll1l11l_opy_(bstack111l1ll1l1l_opy_, bstack111l1ll1lll_opy_):
    proxies = {}
    global bstack111l1ll11ll_opy_
    if bstack1ll1l11_opy_ (u"ࠧࡑࡃࡆࡣࡕࡘࡏ࡙࡛ࠪᴑ") in globals():
        return bstack111l1ll11ll_opy_
    try:
        proxy = bstack111l1ll1ll1_opy_(bstack111l1ll1l1l_opy_, bstack111l1ll1lll_opy_)
        if bstack1ll1l11_opy_ (u"ࠣࡆࡌࡖࡊࡉࡔࠣᴒ") in proxy:
            proxies = {}
        elif bstack1ll1l11_opy_ (u"ࠤࡋࡘ࡙ࡖࠢᴓ") in proxy or bstack1ll1l11_opy_ (u"ࠥࡌ࡙࡚ࡐࡔࠤᴔ") in proxy or bstack1ll1l11_opy_ (u"ࠦࡘࡕࡃࡌࡕࠥᴕ") in proxy:
            bstack111l1ll111l_opy_ = proxy.split(bstack1ll1l11_opy_ (u"ࠧࠦࠢᴖ"))
            if bstack1ll1l11_opy_ (u"ࠨ࠺࠰࠱ࠥᴗ") in bstack1ll1l11_opy_ (u"ࠢࠣᴘ").join(bstack111l1ll111l_opy_[1:]):
                proxies = {
                    bstack1ll1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᴙ"): bstack1ll1l11_opy_ (u"ࠤࠥᴚ").join(bstack111l1ll111l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᴛ"): str(bstack111l1ll111l_opy_[0]).lower() + bstack1ll1l11_opy_ (u"ࠦ࠿࠵࠯ࠣᴜ") + bstack1ll1l11_opy_ (u"ࠧࠨᴝ").join(bstack111l1ll111l_opy_[1:])
                }
        elif bstack1ll1l11_opy_ (u"ࠨࡐࡓࡑ࡛࡝ࠧᴞ") in proxy:
            bstack111l1ll111l_opy_ = proxy.split(bstack1ll1l11_opy_ (u"ࠢࠡࠤᴟ"))
            if bstack1ll1l11_opy_ (u"ࠣ࠼࠲࠳ࠧᴠ") in bstack1ll1l11_opy_ (u"ࠤࠥᴡ").join(bstack111l1ll111l_opy_[1:]):
                proxies = {
                    bstack1ll1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᴢ"): bstack1ll1l11_opy_ (u"ࠦࠧᴣ").join(bstack111l1ll111l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᴤ"): bstack1ll1l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᴥ") + bstack1ll1l11_opy_ (u"ࠢࠣᴦ").join(bstack111l1ll111l_opy_[1:])
                }
        else:
            proxies = {
                bstack1ll1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᴧ"): proxy
            }
    except Exception as e:
        print(bstack1ll1l11_opy_ (u"ࠤࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨᴨ"), bstack11l1111llll_opy_.format(bstack111l1ll1l1l_opy_, str(e)))
    bstack111l1ll11ll_opy_ = proxies
    return proxies