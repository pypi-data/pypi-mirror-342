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
import collections
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11ll1lll1ll_opy_, bstack1lll11ll1_opy_, bstack1111lllll_opy_, bstack1lll11lll_opy_,
                                    bstack11ll1l1l111_opy_, bstack11ll1l11ll1_opy_, bstack11ll1l1ll1l_opy_, bstack11ll1l1lll1_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1ll1llll_opy_, bstack1ll111llll_opy_
from bstack_utils.proxy import bstack1ll1l1111_opy_, bstack11l11ll11_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1ll1lllll_opy_
from browserstack_sdk._version import __version__
bstack11lll1111_opy_ = Config.bstack11111l1l1_opy_()
logger = bstack1ll1lllll_opy_.get_logger(__name__, bstack1ll1lllll_opy_.bstack1l1l1111l1l_opy_())
def bstack11lllll1ll1_opy_(config):
    return config[bstack1ll1l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᦝ")]
def bstack11llll1lll1_opy_(config):
    return config[bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᦞ")]
def bstack11l11lll1l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1l1l1l1l_opy_(obj):
    values = []
    bstack11l1l1111ll_opy_ = re.compile(bstack1ll1l11_opy_ (u"ࡲࠣࡠࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࡜ࡥ࠭ࠧࠦᦟ"), re.I)
    for key in obj.keys():
        if bstack11l1l1111ll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l1lll11ll_opy_(config):
    tags = []
    tags.extend(bstack11l1l1l1l1l_opy_(os.environ))
    tags.extend(bstack11l1l1l1l1l_opy_(config))
    return tags
def bstack11l1lll11l1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1l1ll1ll_opy_(bstack11ll11111l1_opy_):
    if not bstack11ll11111l1_opy_:
        return bstack1ll1l11_opy_ (u"ࠨࠩᦠ")
    return bstack1ll1l11_opy_ (u"ࠤࡾࢁࠥ࠮ࡻࡾࠫࠥᦡ").format(bstack11ll11111l1_opy_.name, bstack11ll11111l1_opy_.email)
def bstack11llll11ll1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1lll111l_opy_ = repo.common_dir
        info = {
            bstack1ll1l11_opy_ (u"ࠥࡷ࡭ࡧࠢᦢ"): repo.head.commit.hexsha,
            bstack1ll1l11_opy_ (u"ࠦࡸ࡮࡯ࡳࡶࡢࡷ࡭ࡧࠢᦣ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1ll1l11_opy_ (u"ࠧࡨࡲࡢࡰࡦ࡬ࠧᦤ"): repo.active_branch.name,
            bstack1ll1l11_opy_ (u"ࠨࡴࡢࡩࠥᦥ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1ll1l11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࠥᦦ"): bstack11l1l1ll1ll_opy_(repo.head.commit.committer),
            bstack1ll1l11_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࡣࡩࡧࡴࡦࠤᦧ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1ll1l11_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࠤᦨ"): bstack11l1l1ll1ll_opy_(repo.head.commit.author),
            bstack1ll1l11_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡢࡨࡦࡺࡥࠣᦩ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1ll1l11_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧᦪ"): repo.head.commit.message,
            bstack1ll1l11_opy_ (u"ࠧࡸ࡯ࡰࡶࠥᦫ"): repo.git.rev_parse(bstack1ll1l11_opy_ (u"ࠨ࠭࠮ࡵ࡫ࡳࡼ࠳ࡴࡰࡲ࡯ࡩࡻ࡫࡬ࠣ᦬")),
            bstack1ll1l11_opy_ (u"ࠢࡤࡱࡰࡱࡴࡴ࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣ᦭"): bstack11l1lll111l_opy_,
            bstack1ll1l11_opy_ (u"ࠣࡹࡲࡶࡰࡺࡲࡦࡧࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦ᦮"): subprocess.check_output([bstack1ll1l11_opy_ (u"ࠤࡪ࡭ࡹࠨ᦯"), bstack1ll1l11_opy_ (u"ࠥࡶࡪࡼ࠭ࡱࡣࡵࡷࡪࠨᦰ"), bstack1ll1l11_opy_ (u"ࠦ࠲࠳ࡧࡪࡶ࠰ࡧࡴࡳ࡭ࡰࡰ࠰ࡨ࡮ࡸࠢᦱ")]).strip().decode(
                bstack1ll1l11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᦲ")),
            bstack1ll1l11_opy_ (u"ࠨ࡬ࡢࡵࡷࡣࡹࡧࡧࠣᦳ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1ll1l11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡳࡠࡵ࡬ࡲࡨ࡫࡟࡭ࡣࡶࡸࡤࡺࡡࡨࠤᦴ"): repo.git.rev_list(
                bstack1ll1l11_opy_ (u"ࠣࡽࢀ࠲࠳ࢁࡽࠣᦵ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11ll111l1l1_opy_ = []
        for remote in remotes:
            bstack11l1llll1l1_opy_ = {
                bstack1ll1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᦶ"): remote.name,
                bstack1ll1l11_opy_ (u"ࠥࡹࡷࡲࠢᦷ"): remote.url,
            }
            bstack11ll111l1l1_opy_.append(bstack11l1llll1l1_opy_)
        bstack11l1lllll11_opy_ = {
            bstack1ll1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᦸ"): bstack1ll1l11_opy_ (u"ࠧ࡭ࡩࡵࠤᦹ"),
            **info,
            bstack1ll1l11_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡹࠢᦺ"): bstack11ll111l1l1_opy_
        }
        bstack11l1lllll11_opy_ = bstack11l1ll1l11l_opy_(bstack11l1lllll11_opy_)
        return bstack11l1lllll11_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᦻ").format(err))
        return {}
def bstack11l1ll1l11l_opy_(bstack11l1lllll11_opy_):
    bstack11l1l1ll11l_opy_ = bstack11l1l1l1ll1_opy_(bstack11l1lllll11_opy_)
    if bstack11l1l1ll11l_opy_ and bstack11l1l1ll11l_opy_ > bstack11ll1l1l111_opy_:
        bstack11ll11l11l1_opy_ = bstack11l1l1ll11l_opy_ - bstack11ll1l1l111_opy_
        bstack11ll11ll1ll_opy_ = bstack11l1ll1lll1_opy_(bstack11l1lllll11_opy_[bstack1ll1l11_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᦼ")], bstack11ll11l11l1_opy_)
        bstack11l1lllll11_opy_[bstack1ll1l11_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᦽ")] = bstack11ll11ll1ll_opy_
        logger.info(bstack1ll1l11_opy_ (u"ࠥࡘ࡭࡫ࠠࡤࡱࡰࡱ࡮ࡺࠠࡩࡣࡶࠤࡧ࡫ࡥ࡯ࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨ࠳ࠦࡓࡪࡼࡨࠤࡴ࡬ࠠࡤࡱࡰࡱ࡮ࡺࠠࡢࡨࡷࡩࡷࠦࡴࡳࡷࡱࡧࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡻࡾࠢࡎࡆࠧᦾ")
                    .format(bstack11l1l1l1ll1_opy_(bstack11l1lllll11_opy_) / 1024))
    return bstack11l1lllll11_opy_
def bstack11l1l1l1ll1_opy_(bstack1llllll1l_opy_):
    try:
        if bstack1llllll1l_opy_:
            bstack11ll11111ll_opy_ = json.dumps(bstack1llllll1l_opy_)
            bstack11l1lll1lll_opy_ = sys.getsizeof(bstack11ll11111ll_opy_)
            return bstack11l1lll1lll_opy_
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠦࡘࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡦࡲࡣࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡵ࡬ࡾࡪࠦ࡯ࡧࠢࡍࡗࡔࡔࠠࡰࡤ࡭ࡩࡨࡺ࠺ࠡࡽࢀࠦᦿ").format(e))
    return -1
def bstack11l1ll1lll1_opy_(field, bstack11ll111l1ll_opy_):
    try:
        bstack11l1llll11l_opy_ = len(bytes(bstack11ll1l11ll1_opy_, bstack1ll1l11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᧀ")))
        bstack11ll11l11ll_opy_ = bytes(field, bstack1ll1l11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᧁ"))
        bstack11l1lll1l1l_opy_ = len(bstack11ll11l11ll_opy_)
        bstack11l1ll11ll1_opy_ = ceil(bstack11l1lll1l1l_opy_ - bstack11ll111l1ll_opy_ - bstack11l1llll11l_opy_)
        if bstack11l1ll11ll1_opy_ > 0:
            bstack11l1ll11lll_opy_ = bstack11ll11l11ll_opy_[:bstack11l1ll11ll1_opy_].decode(bstack1ll1l11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᧂ"), errors=bstack1ll1l11_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࠨᧃ")) + bstack11ll1l11ll1_opy_
            return bstack11l1ll11lll_opy_
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡵࡴࡸࡲࡨࡧࡴࡪࡰࡪࠤ࡫࡯ࡥ࡭ࡦ࠯ࠤࡳࡵࡴࡩ࡫ࡱ࡫ࠥࡽࡡࡴࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨࠥ࡮ࡥࡳࡧ࠽ࠤࢀࢃࠢᧄ").format(e))
    return field
def bstack1l1l11l1ll_opy_():
    env = os.environ
    if (bstack1ll1l11_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣᧅ") in env and len(env[bstack1ll1l11_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤᧆ")]) > 0) or (
            bstack1ll1l11_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦᧇ") in env and len(env[bstack1ll1l11_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧᧈ")]) > 0):
        return {
            bstack1ll1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᧉ"): bstack1ll1l11_opy_ (u"ࠣࡌࡨࡲࡰ࡯࡮ࡴࠤ᧊"),
            bstack1ll1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᧋"): env.get(bstack1ll1l11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᧌")),
            bstack1ll1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᧍"): env.get(bstack1ll1l11_opy_ (u"ࠧࡐࡏࡃࡡࡑࡅࡒࡋࠢ᧎")),
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᧏"): env.get(bstack1ll1l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᧐"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠣࡅࡌࠦ᧑")) == bstack1ll1l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᧒") and bstack11l1llllll_opy_(env.get(bstack1ll1l11_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡆࡍࠧ᧓"))):
        return {
            bstack1ll1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᧔"): bstack1ll1l11_opy_ (u"ࠧࡉࡩࡳࡥ࡯ࡩࡈࡏࠢ᧕"),
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᧖"): env.get(bstack1ll1l11_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᧗")),
            bstack1ll1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᧘"): env.get(bstack1ll1l11_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡍࡓࡇࠨ᧙")),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᧚"): env.get(bstack1ll1l11_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࠢ᧛"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠧࡉࡉࠣ᧜")) == bstack1ll1l11_opy_ (u"ࠨࡴࡳࡷࡨࠦ᧝") and bstack11l1llllll_opy_(env.get(bstack1ll1l11_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙ࠢ᧞"))):
        return {
            bstack1ll1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨ᧟"): bstack1ll1l11_opy_ (u"ࠤࡗࡶࡦࡼࡩࡴࠢࡆࡍࠧ᧠"),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᧡"): env.get(bstack1ll1l11_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢ࡛ࡊࡈ࡟ࡖࡔࡏࠦ᧢")),
            bstack1ll1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᧣"): env.get(bstack1ll1l11_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ᧤")),
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᧥"): env.get(bstack1ll1l11_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᧦"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠤࡆࡍࠧ᧧")) == bstack1ll1l11_opy_ (u"ࠥࡸࡷࡻࡥࠣ᧨") and env.get(bstack1ll1l11_opy_ (u"ࠦࡈࡏ࡟ࡏࡃࡐࡉࠧ᧩")) == bstack1ll1l11_opy_ (u"ࠧࡩ࡯ࡥࡧࡶ࡬࡮ࡶࠢ᧪"):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᧫"): bstack1ll1l11_opy_ (u"ࠢࡄࡱࡧࡩࡸ࡮ࡩࡱࠤ᧬"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᧭"): None,
            bstack1ll1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᧮"): None,
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᧯"): None
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠢ᧰")) and env.get(bstack1ll1l11_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠣ᧱")):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᧲"): bstack1ll1l11_opy_ (u"ࠢࡃ࡫ࡷࡦࡺࡩ࡫ࡦࡶࠥ᧳"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᧴"): env.get(bstack1ll1l11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡍࡉࡕࡡࡋࡘ࡙ࡖ࡟ࡐࡔࡌࡋࡎࡔࠢ᧵")),
            bstack1ll1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᧶"): None,
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᧷"): env.get(bstack1ll1l11_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᧸"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡊࠤ᧹")) == bstack1ll1l11_opy_ (u"ࠢࡵࡴࡸࡩࠧ᧺") and bstack11l1llllll_opy_(env.get(bstack1ll1l11_opy_ (u"ࠣࡆࡕࡓࡓࡋࠢ᧻"))):
        return {
            bstack1ll1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᧼"): bstack1ll1l11_opy_ (u"ࠥࡈࡷࡵ࡮ࡦࠤ᧽"),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᧾"): env.get(bstack1ll1l11_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡐࡎࡔࡋࠣ᧿")),
            bstack1ll1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᨀ"): None,
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᨁ"): env.get(bstack1ll1l11_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᨂ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠤࡆࡍࠧᨃ")) == bstack1ll1l11_opy_ (u"ࠥࡸࡷࡻࡥࠣᨄ") and bstack11l1llllll_opy_(env.get(bstack1ll1l11_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋࠢᨅ"))):
        return {
            bstack1ll1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᨆ"): bstack1ll1l11_opy_ (u"ࠨࡓࡦ࡯ࡤࡴ࡭ࡵࡲࡦࠤᨇ"),
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᨈ"): env.get(bstack1ll1l11_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡔࡘࡇࡂࡐࡌ࡞ࡆ࡚ࡉࡐࡐࡢ࡙ࡗࡒࠢᨉ")),
            bstack1ll1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᨊ"): env.get(bstack1ll1l11_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᨋ")),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᨌ"): env.get(bstack1ll1l11_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠣᨍ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡊࠤᨎ")) == bstack1ll1l11_opy_ (u"ࠢࡵࡴࡸࡩࠧᨏ") and bstack11l1llllll_opy_(env.get(bstack1ll1l11_opy_ (u"ࠣࡉࡌࡘࡑࡇࡂࡠࡅࡌࠦᨐ"))):
        return {
            bstack1ll1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᨑ"): bstack1ll1l11_opy_ (u"ࠥࡋ࡮ࡺࡌࡢࡤࠥᨒ"),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᨓ"): env.get(bstack1ll1l11_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤ࡛ࡒࡍࠤᨔ")),
            bstack1ll1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᨕ"): env.get(bstack1ll1l11_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᨖ")),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᨗ"): env.get(bstack1ll1l11_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡌࡈᨘࠧ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠥࡇࡎࠨᨙ")) == bstack1ll1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤᨚ") and bstack11l1llllll_opy_(env.get(bstack1ll1l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠣᨛ"))):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᨜"): bstack1ll1l11_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡱࡩࡵࡧࠥ᨝"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᨞"): env.get(bstack1ll1l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ᨟")),
            bstack1ll1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᨠ"): env.get(bstack1ll1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡍࡃࡅࡉࡑࠨᨡ")) or env.get(bstack1ll1l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᨢ")),
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᨣ"): env.get(bstack1ll1l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᨤ"))
        }
    if bstack11l1llllll_opy_(env.get(bstack1ll1l11_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᨥ"))):
        return {
            bstack1ll1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᨦ"): bstack1ll1l11_opy_ (u"࡚ࠥ࡮ࡹࡵࡢ࡮ࠣࡗࡹࡻࡤࡪࡱࠣࡘࡪࡧ࡭ࠡࡕࡨࡶࡻ࡯ࡣࡦࡵࠥᨧ"),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᨨ"): bstack1ll1l11_opy_ (u"ࠧࢁࡽࡼࡿࠥᨩ").format(env.get(bstack1ll1l11_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᨪ")), env.get(bstack1ll1l11_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࡎࡊࠧᨫ"))),
            bstack1ll1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᨬ"): env.get(bstack1ll1l11_opy_ (u"ࠤࡖ࡝ࡘ࡚ࡅࡎࡡࡇࡉࡋࡏࡎࡊࡖࡌࡓࡓࡏࡄࠣᨭ")),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᨮ"): env.get(bstack1ll1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᨯ"))
        }
    if bstack11l1llllll_opy_(env.get(bstack1ll1l11_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘࠢᨰ"))):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᨱ"): bstack1ll1l11_opy_ (u"ࠢࡂࡲࡳࡺࡪࡿ࡯ࡳࠤᨲ"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᨳ"): bstack1ll1l11_opy_ (u"ࠤࡾࢁ࠴ࡶࡲࡰ࡬ࡨࡧࡹ࠵ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠣᨴ").format(env.get(bstack1ll1l11_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤ࡛ࡒࡍࠩᨵ")), env.get(bstack1ll1l11_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡁࡄࡅࡒ࡙ࡓ࡚࡟ࡏࡃࡐࡉࠬᨶ")), env.get(bstack1ll1l11_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡕࡏ࡙ࡌ࠭ᨷ")), env.get(bstack1ll1l11_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪᨸ"))),
            bstack1ll1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᨹ"): env.get(bstack1ll1l11_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᨺ")),
            bstack1ll1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᨻ"): env.get(bstack1ll1l11_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᨼ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠦࡆࡠࡕࡓࡇࡢࡌ࡙࡚ࡐࡠࡗࡖࡉࡗࡥࡁࡈࡇࡑࡘࠧᨽ")) and env.get(bstack1ll1l11_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᨾ")):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᨿ"): bstack1ll1l11_opy_ (u"ࠢࡂࡼࡸࡶࡪࠦࡃࡊࠤᩀ"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᩁ"): bstack1ll1l11_opy_ (u"ࠤࡾࢁࢀࢃ࠯ࡠࡤࡸ࡭ࡱࡪ࠯ࡳࡧࡶࡹࡱࡺࡳࡀࡤࡸ࡭ࡱࡪࡉࡥ࠿ࡾࢁࠧᩂ").format(env.get(bstack1ll1l11_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ᩃ")), env.get(bstack1ll1l11_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࠩᩄ")), env.get(bstack1ll1l11_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠬᩅ"))),
            bstack1ll1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᩆ"): env.get(bstack1ll1l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᩇ")),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᩈ"): env.get(bstack1ll1l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᩉ"))
        }
    if any([env.get(bstack1ll1l11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᩊ")), env.get(bstack1ll1l11_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᩋ")), env.get(bstack1ll1l11_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤᩌ"))]):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᩍ"): bstack1ll1l11_opy_ (u"ࠢࡂ࡙ࡖࠤࡈࡵࡤࡦࡄࡸ࡭ࡱࡪࠢᩎ"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᩏ"): env.get(bstack1ll1l11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡖࡕࡃࡎࡌࡇࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᩐ")),
            bstack1ll1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᩑ"): env.get(bstack1ll1l11_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᩒ")),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᩓ"): env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᩔ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧᩕ")):
        return {
            bstack1ll1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨᩖ"): bstack1ll1l11_opy_ (u"ࠤࡅࡥࡲࡨ࡯ࡰࠤᩗ"),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᩘ"): env.get(bstack1ll1l11_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡕࡩࡸࡻ࡬ࡵࡵࡘࡶࡱࠨᩙ")),
            bstack1ll1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᩚ"): env.get(bstack1ll1l11_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡳࡩࡱࡵࡸࡏࡵࡢࡏࡣࡰࡩࠧᩛ")),
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᩜ"): env.get(bstack1ll1l11_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨᩝ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࠥᩞ")) or env.get(bstack1ll1l11_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧ᩟")):
        return {
            bstack1ll1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᩠"): bstack1ll1l11_opy_ (u"ࠧ࡝ࡥࡳࡥ࡮ࡩࡷࠨᩡ"),
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᩢ"): env.get(bstack1ll1l11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᩣ")),
            bstack1ll1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᩤ"): bstack1ll1l11_opy_ (u"ࠤࡐࡥ࡮ࡴࠠࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠤᩥ") if env.get(bstack1ll1l11_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧᩦ")) else None,
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᩧ"): env.get(bstack1ll1l11_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡇࡊࡖࡢࡇࡔࡓࡍࡊࡖࠥᩨ"))
        }
    if any([env.get(bstack1ll1l11_opy_ (u"ࠨࡇࡄࡒࡢࡔࡗࡕࡊࡆࡅࡗࠦᩩ")), env.get(bstack1ll1l11_opy_ (u"ࠢࡈࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᩪ")), env.get(bstack1ll1l11_opy_ (u"ࠣࡉࡒࡓࡌࡒࡅࡠࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᩫ"))]):
        return {
            bstack1ll1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᩬ"): bstack1ll1l11_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡇࡱࡵࡵࡥࠤᩭ"),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᩮ"): None,
            bstack1ll1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᩯ"): env.get(bstack1ll1l11_opy_ (u"ࠨࡐࡓࡑࡍࡉࡈ࡚࡟ࡊࡆࠥᩰ")),
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᩱ"): env.get(bstack1ll1l11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᩲ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࠧᩳ")):
        return {
            bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᩴ"): bstack1ll1l11_opy_ (u"ࠦࡘ࡮ࡩࡱࡲࡤࡦࡱ࡫ࠢ᩵"),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᩶"): env.get(bstack1ll1l11_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ᩷")),
            bstack1ll1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᩸"): bstack1ll1l11_opy_ (u"ࠣࡌࡲࡦࠥࠩࡻࡾࠤ᩹").format(env.get(bstack1ll1l11_opy_ (u"ࠩࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠬ᩺"))) if env.get(bstack1ll1l11_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉࠨ᩻")) else None,
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᩼"): env.get(bstack1ll1l11_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᩽"))
        }
    if bstack11l1llllll_opy_(env.get(bstack1ll1l11_opy_ (u"ࠨࡎࡆࡖࡏࡍࡋ࡟ࠢ᩾"))):
        return {
            bstack1ll1l11_opy_ (u"ࠢ࡯ࡣࡰࡩ᩿ࠧ"): bstack1ll1l11_opy_ (u"ࠣࡐࡨࡸࡱ࡯ࡦࡺࠤ᪀"),
            bstack1ll1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᪁"): env.get(bstack1ll1l11_opy_ (u"ࠥࡈࡊࡖࡌࡐ࡛ࡢ࡙ࡗࡒࠢ᪂")),
            bstack1ll1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᪃"): env.get(bstack1ll1l11_opy_ (u"࡙ࠧࡉࡕࡇࡢࡒࡆࡓࡅࠣ᪄")),
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᪅"): env.get(bstack1ll1l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤ᪆"))
        }
    if bstack11l1llllll_opy_(env.get(bstack1ll1l11_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡃࡆࡘࡎࡕࡎࡔࠤ᪇"))):
        return {
            bstack1ll1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᪈"): bstack1ll1l11_opy_ (u"ࠥࡋ࡮ࡺࡈࡶࡤࠣࡅࡨࡺࡩࡰࡰࡶࠦ᪉"),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᪊"): bstack1ll1l11_opy_ (u"ࠧࢁࡽ࠰ࡽࢀ࠳ࡦࡩࡴࡪࡱࡱࡷ࠴ࡸࡵ࡯ࡵ࠲ࡿࢂࠨ᪋").format(env.get(bstack1ll1l11_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡓࡆࡔ࡙ࡉࡗࡥࡕࡓࡎࠪ᪌")), env.get(bstack1ll1l11_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡇࡓࡓࡘࡏࡔࡐࡔ࡜ࠫ᪍")), env.get(bstack1ll1l11_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠨ᪎"))),
            bstack1ll1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᪏"): env.get(bstack1ll1l11_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢ࡛ࡔࡘࡋࡇࡎࡒ࡛ࠧ᪐")),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᪑"): env.get(bstack1ll1l11_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠧ᪒"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡊࠤ᪓")) == bstack1ll1l11_opy_ (u"ࠢࡵࡴࡸࡩࠧ᪔") and env.get(bstack1ll1l11_opy_ (u"ࠣࡘࡈࡖࡈࡋࡌࠣ᪕")) == bstack1ll1l11_opy_ (u"ࠤ࠴ࠦ᪖"):
        return {
            bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣ᪗"): bstack1ll1l11_opy_ (u"࡛ࠦ࡫ࡲࡤࡧ࡯ࠦ᪘"),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᪙"): bstack1ll1l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࡻࡾࠤ᪚").format(env.get(bstack1ll1l11_opy_ (u"ࠧࡗࡇࡕࡇࡊࡒ࡟ࡖࡔࡏࠫ᪛"))),
            bstack1ll1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᪜"): None,
            bstack1ll1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᪝"): None,
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ᪞")):
        return {
            bstack1ll1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪟"): bstack1ll1l11_opy_ (u"࡚ࠧࡥࡢ࡯ࡦ࡭ࡹࡿࠢ᪠"),
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᪡"): None,
            bstack1ll1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪢"): env.get(bstack1ll1l11_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠤ᪣")),
            bstack1ll1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᪤"): env.get(bstack1ll1l11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᪥"))
        }
    if any([env.get(bstack1ll1l11_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋࠢ᪦")), env.get(bstack1ll1l11_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡕࡐࠧᪧ")), env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦ᪨")), env.get(bstack1ll1l11_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢࡘࡊࡇࡍࠣ᪩"))]):
        return {
            bstack1ll1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪪"): bstack1ll1l11_opy_ (u"ࠤࡆࡳࡳࡩ࡯ࡶࡴࡶࡩࠧ᪫"),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᪬"): None,
            bstack1ll1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᪭"): env.get(bstack1ll1l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ᪮")) or None,
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᪯"): env.get(bstack1ll1l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤ᪰"), 0)
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ᪱")):
        return {
            bstack1ll1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᪲"): bstack1ll1l11_opy_ (u"ࠥࡋࡴࡉࡄࠣ᪳"),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᪴"): None,
            bstack1ll1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫᪵ࠢ"): env.get(bstack1ll1l11_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈ᪶ࠦ")),
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪷"): env.get(bstack1ll1l11_opy_ (u"ࠣࡉࡒࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡃࡐࡗࡑࡘࡊࡘ᪸ࠢ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊ᪹ࠢ")):
        return {
            bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥ᪺ࠣ"): bstack1ll1l11_opy_ (u"ࠦࡈࡵࡤࡦࡈࡵࡩࡸ࡮ࠢ᪻"),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᪼"): env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐ᪽ࠧ")),
            bstack1ll1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪾"): env.get(bstack1ll1l11_opy_ (u"ࠣࡅࡉࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈᪿࠦ")),
            bstack1ll1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲᫀࠣ"): env.get(bstack1ll1l11_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ᫁"))
        }
    return {bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᫂"): None}
def get_host_info():
    return {
        bstack1ll1l11_opy_ (u"ࠧ࡮࡯ࡴࡶࡱࡥࡲ࡫᫃ࠢ"): platform.node(),
        bstack1ll1l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭᫄ࠣ"): platform.system(),
        bstack1ll1l11_opy_ (u"ࠢࡵࡻࡳࡩࠧ᫅"): platform.machine(),
        bstack1ll1l11_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤ᫆"): platform.version(),
        bstack1ll1l11_opy_ (u"ࠤࡤࡶࡨ࡮ࠢ᫇"): platform.architecture()[0]
    }
def bstack1l1ll11lll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l11lllll1_opy_():
    if bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ᫈")):
        return bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ᫉")
    return bstack1ll1l11_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧ᫊ࠫ")
def bstack11l1l11lll1_opy_(driver):
    info = {
        bstack1ll1l11_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᫋"): driver.capabilities,
        bstack1ll1l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫᫌ"): driver.session_id,
        bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᫍ"): driver.capabilities.get(bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᫎ"), None),
        bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᫏"): driver.capabilities.get(bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᫐"), None),
        bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧ᫑"): driver.capabilities.get(bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬ᫒"), None),
        bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪ᫓"):driver.capabilities.get(bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ᫔"), None),
    }
    if bstack11l11lllll1_opy_() == bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᫕"):
        if bstack1l11lllll_opy_():
            info[bstack1ll1l11_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ᫖")] = bstack1ll1l11_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪ᫗")
        elif driver.capabilities.get(bstack1ll1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᫘"), {}).get(bstack1ll1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ᫙"), False):
            info[bstack1ll1l11_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ᫚")] = bstack1ll1l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ᫛")
        else:
            info[bstack1ll1l11_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪ᫜")] = bstack1ll1l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ᫝")
    return info
def bstack1l11lllll_opy_():
    if bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ᫞")):
        return True
    if bstack11l1llllll_opy_(os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭᫟"), None)):
        return True
    return False
def bstack11lllll1ll_opy_(bstack11ll11ll11l_opy_, url, data, config):
    headers = config.get(bstack1ll1l11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ᫠"), None)
    proxies = bstack1ll1l1111_opy_(config, url)
    auth = config.get(bstack1ll1l11_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ᫡"), None)
    response = requests.request(
            bstack11ll11ll11l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11l1lll1l1_opy_(bstack1111l11ll_opy_, size):
    bstack1l1111111l_opy_ = []
    while len(bstack1111l11ll_opy_) > size:
        bstack1lll11l1l1_opy_ = bstack1111l11ll_opy_[:size]
        bstack1l1111111l_opy_.append(bstack1lll11l1l1_opy_)
        bstack1111l11ll_opy_ = bstack1111l11ll_opy_[size:]
    bstack1l1111111l_opy_.append(bstack1111l11ll_opy_)
    return bstack1l1111111l_opy_
def bstack11l1llllll1_opy_(message, bstack11ll11l1ll1_opy_=False):
    os.write(1, bytes(message, bstack1ll1l11_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᫢")))
    os.write(1, bytes(bstack1ll1l11_opy_ (u"ࠩ࡟ࡲࠬ᫣"), bstack1ll1l11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᫤")))
    if bstack11ll11l1ll1_opy_:
        with open(bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡴ࠷࠱ࡺ࠯ࠪ᫥") + os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ᫦")] + bstack1ll1l11_opy_ (u"࠭࠮࡭ࡱࡪࠫ᫧"), bstack1ll1l11_opy_ (u"ࠧࡢࠩ᫨")) as f:
            f.write(message + bstack1ll1l11_opy_ (u"ࠨ࡞ࡱࠫ᫩"))
def bstack1llll1l1l11_opy_():
    return os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ᫪")].lower() == bstack1ll1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨ᫫")
def bstack1ll1l11l11_opy_(bstack11l1l1l1111_opy_):
    return bstack1ll1l11_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪ᫬").format(bstack11ll1lll1ll_opy_, bstack11l1l1l1111_opy_)
def bstack1lllllll11_opy_():
    return bstack111l1l1ll1_opy_().replace(tzinfo=None).isoformat() + bstack1ll1l11_opy_ (u"ࠬࡠࠧ᫭")
def bstack11l1lll1l11_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1ll1l11_opy_ (u"࡚࠭ࠨ᫮"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1ll1l11_opy_ (u"࡛ࠧࠩ᫯")))).total_seconds() * 1000
def bstack11l1ll1l111_opy_(timestamp):
    return bstack11l1l111l1l_opy_(timestamp).isoformat() + bstack1ll1l11_opy_ (u"ࠨ࡜ࠪ᫰")
def bstack11l11llllll_opy_(bstack11ll1111lll_opy_):
    date_format = bstack1ll1l11_opy_ (u"ࠩࠨ࡝ࠪࡳࠥࡥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠧ᫱")
    bstack11l1l1lllll_opy_ = datetime.datetime.strptime(bstack11ll1111lll_opy_, date_format)
    return bstack11l1l1lllll_opy_.isoformat() + bstack1ll1l11_opy_ (u"ࠪ࡞ࠬ᫲")
def bstack11l1l1ll1l1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᫳")
    else:
        return bstack1ll1l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ᫴")
def bstack11l1llllll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1ll1l11_opy_ (u"࠭ࡴࡳࡷࡨࠫ᫵")
def bstack11ll11l1l11_opy_(val):
    return val.__str__().lower() == bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭᫶")
def bstack111l11lll1_opy_(bstack11ll111llll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11ll111llll_opy_ as e:
                print(bstack1ll1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣ᫷").format(func.__name__, bstack11ll111llll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11ll11ll111_opy_(bstack11l1ll1l1ll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1ll1l1ll_opy_(cls, *args, **kwargs)
            except bstack11ll111llll_opy_ as e:
                print(bstack1ll1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤ᫸").format(bstack11l1ll1l1ll_opy_.__name__, bstack11ll111llll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11ll11ll111_opy_
    else:
        return decorator
def bstack1l1l1lll1_opy_(bstack1111lllll1_opy_):
    if os.getenv(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭᫹")) is not None:
        return bstack11l1llllll_opy_(os.getenv(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ᫺")))
    if bstack1ll1l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᫻") in bstack1111lllll1_opy_ and bstack11ll11l1l11_opy_(bstack1111lllll1_opy_[bstack1ll1l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᫼")]):
        return False
    if bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᫽") in bstack1111lllll1_opy_ and bstack11ll11l1l11_opy_(bstack1111lllll1_opy_[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᫾")]):
        return False
    return True
def bstack1l1l1ll1l_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l1l1l1l11_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠤ᫿"), None)
        return bstack11l1l1l1l11_opy_ is None or bstack11l1l1l1l11_opy_ == bstack1ll1l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᬀ")
    except Exception as e:
        return False
def bstack11l1ll1111_opy_(hub_url, CONFIG):
    if bstack1llll11ll_opy_() <= version.parse(bstack1ll1l11_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫᬁ")):
        if hub_url:
            return bstack1ll1l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᬂ") + hub_url + bstack1ll1l11_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥᬃ")
        return bstack1111lllll_opy_
    if hub_url:
        return bstack1ll1l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᬄ") + hub_url + bstack1ll1l11_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤᬅ")
    return bstack1lll11lll_opy_
def bstack11ll11l1111_opy_():
    return isinstance(os.getenv(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨᬆ")), str)
def bstack11lllll1l1_opy_(url):
    return urlparse(url).hostname
def bstack1l111ll1l1_opy_(hostname):
    for bstack1111ll111_opy_ in bstack1lll11ll1_opy_:
        regex = re.compile(bstack1111ll111_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1l11l11l_opy_(bstack11l1l11ll11_opy_, file_name, logger):
    bstack11l11lll11_opy_ = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠪࢂࠬᬇ")), bstack11l1l11ll11_opy_)
    try:
        if not os.path.exists(bstack11l11lll11_opy_):
            os.makedirs(bstack11l11lll11_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠫࢃ࠭ᬈ")), bstack11l1l11ll11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1ll1l11_opy_ (u"ࠬࡽࠧᬉ")):
                pass
            with open(file_path, bstack1ll1l11_opy_ (u"ࠨࡷࠬࠤᬊ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1ll1llll_opy_.format(str(e)))
def bstack11l1llll1ll_opy_(file_name, key, value, logger):
    file_path = bstack11l1l11l11l_opy_(bstack1ll1l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᬋ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11l1ll11_opy_ = json.load(open(file_path, bstack1ll1l11_opy_ (u"ࠨࡴࡥࠫᬌ")))
        else:
            bstack11l1ll11_opy_ = {}
        bstack11l1ll11_opy_[key] = value
        with open(file_path, bstack1ll1l11_opy_ (u"ࠤࡺ࠯ࠧᬍ")) as outfile:
            json.dump(bstack11l1ll11_opy_, outfile)
def bstack111l1ll1_opy_(file_name, logger):
    file_path = bstack11l1l11l11l_opy_(bstack1ll1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᬎ"), file_name, logger)
    bstack11l1ll11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1ll1l11_opy_ (u"ࠫࡷ࠭ᬏ")) as bstack11ll1ll1_opy_:
            bstack11l1ll11_opy_ = json.load(bstack11ll1ll1_opy_)
    return bstack11l1ll11_opy_
def bstack1lll111l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫࠺ࠡࠩᬐ") + file_path + bstack1ll1l11_opy_ (u"࠭ࠠࠨᬑ") + str(e))
def bstack1llll11ll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1ll1l11_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤᬒ")
def bstack1ll1ll1ll_opy_(config):
    if bstack1ll1l11_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᬓ") in config:
        del (config[bstack1ll1l11_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᬔ")])
        return False
    if bstack1llll11ll_opy_() < version.parse(bstack1ll1l11_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩᬕ")):
        return False
    if bstack1llll11ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪᬖ")):
        return True
    if bstack1ll1l11_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᬗ") in config and config[bstack1ll1l11_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᬘ")] is False:
        return False
    else:
        return True
def bstack1l1l1l11l_opy_(args_list, bstack11ll111ll1l_opy_):
    index = -1
    for value in bstack11ll111ll1l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111llll1l1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111llll1l1_opy_ = bstack111llll1l1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1ll1l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᬙ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᬚ"), exception=exception)
    def bstack1111ll1111_opy_(self):
        if self.result != bstack1ll1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᬛ"):
            return None
        if isinstance(self.exception_type, str) and bstack1ll1l11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᬜ") in self.exception_type:
            return bstack1ll1l11_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᬝ")
        return bstack1ll1l11_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᬞ")
    def bstack11l11llll11_opy_(self):
        if self.result != bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᬟ"):
            return None
        if self.bstack111llll1l1_opy_:
            return self.bstack111llll1l1_opy_
        return bstack11l1l11ll1l_opy_(self.exception)
def bstack11l1l11ll1l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11ll1111l1l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11ll111l1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l1l11l1_opy_(config, logger):
    try:
        import playwright
        bstack11l1l1111l1_opy_ = playwright.__file__
        bstack11l1ll1ll1l_opy_ = os.path.split(bstack11l1l1111l1_opy_)
        bstack11l1ll1111l_opy_ = bstack11l1ll1ll1l_opy_[0] + bstack1ll1l11_opy_ (u"ࠧ࠰ࡦࡵ࡭ࡻ࡫ࡲ࠰ࡲࡤࡧࡰࡧࡧࡦ࠱࡯࡭ࡧ࠵ࡣ࡭࡫࠲ࡧࡱ࡯࠮࡫ࡵࠪᬠ")
        os.environ[bstack1ll1l11_opy_ (u"ࠨࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜ࠫᬡ")] = bstack11l11ll11_opy_(config)
        with open(bstack11l1ll1111l_opy_, bstack1ll1l11_opy_ (u"ࠩࡵࠫᬢ")) as f:
            bstack1ll1111lll_opy_ = f.read()
            bstack11l1l11111l_opy_ = bstack1ll1l11_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩᬣ")
            bstack11l1l1l1lll_opy_ = bstack1ll1111lll_opy_.find(bstack11l1l11111l_opy_)
            if bstack11l1l1l1lll_opy_ == -1:
              process = subprocess.Popen(bstack1ll1l11_opy_ (u"ࠦࡳࡶ࡭ࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠣᬤ"), shell=True, cwd=bstack11l1ll1ll1l_opy_[0])
              process.wait()
              bstack11l1l1llll1_opy_ = bstack1ll1l11_opy_ (u"ࠬࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶࠥ࠿ࠬᬥ")
              bstack11l1ll1llll_opy_ = bstack1ll1l11_opy_ (u"ࠨࠢࠣࠢ࡟ࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴ࡝ࠤ࠾ࠤࡨࡵ࡮ࡴࡶࠣࡿࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠡࡿࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ࠩ࠼ࠢ࡬ࡪࠥ࠮ࡰࡳࡱࡦࡩࡸࡹ࠮ࡦࡰࡹ࠲ࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠩࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠬ࠮ࡁࠠࠣࠤࠥᬦ")
              bstack11ll11l1l1l_opy_ = bstack1ll1111lll_opy_.replace(bstack11l1l1llll1_opy_, bstack11l1ll1llll_opy_)
              with open(bstack11l1ll1111l_opy_, bstack1ll1l11_opy_ (u"ࠧࡸࠩᬧ")) as f:
                f.write(bstack11ll11l1l1l_opy_)
    except Exception as e:
        logger.error(bstack1ll111llll_opy_.format(str(e)))
def bstack1llll1l1_opy_():
  try:
    bstack11l1l1l11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨᬨ"))
    bstack11l1l111lll_opy_ = []
    if os.path.exists(bstack11l1l1l11l1_opy_):
      with open(bstack11l1l1l11l1_opy_) as f:
        bstack11l1l111lll_opy_ = json.load(f)
      os.remove(bstack11l1l1l11l1_opy_)
    return bstack11l1l111lll_opy_
  except:
    pass
  return []
def bstack1111l11l_opy_(bstack1l11l11ll1_opy_):
  try:
    bstack11l1l111lll_opy_ = []
    bstack11l1l1l11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩᬩ"))
    if os.path.exists(bstack11l1l1l11l1_opy_):
      with open(bstack11l1l1l11l1_opy_) as f:
        bstack11l1l111lll_opy_ = json.load(f)
    bstack11l1l111lll_opy_.append(bstack1l11l11ll1_opy_)
    with open(bstack11l1l1l11l1_opy_, bstack1ll1l11_opy_ (u"ࠪࡻࠬᬪ")) as f:
        json.dump(bstack11l1l111lll_opy_, f)
  except:
    pass
def bstack1l111lll_opy_(logger, bstack11ll1111l11_opy_ = False):
  try:
    test_name = os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧᬫ"), bstack1ll1l11_opy_ (u"ࠬ࠭ᬬ"))
    if test_name == bstack1ll1l11_opy_ (u"࠭ࠧᬭ"):
        test_name = threading.current_thread().__dict__.get(bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࡂࡥࡦࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠭ᬮ"), bstack1ll1l11_opy_ (u"ࠨࠩᬯ"))
    bstack11ll111l11l_opy_ = bstack1ll1l11_opy_ (u"ࠩ࠯ࠤࠬᬰ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11ll1111l11_opy_:
        bstack1lll1l1l_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᬱ"), bstack1ll1l11_opy_ (u"ࠫ࠵࠭ᬲ"))
        bstack11ll1llll_opy_ = {bstack1ll1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᬳ"): test_name, bstack1ll1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶ᬴ࠬ"): bstack11ll111l11l_opy_, bstack1ll1l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᬵ"): bstack1lll1l1l_opy_}
        bstack11l1ll11l11_opy_ = []
        bstack11l1l11l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᬶ"))
        if os.path.exists(bstack11l1l11l1l1_opy_):
            with open(bstack11l1l11l1l1_opy_) as f:
                bstack11l1ll11l11_opy_ = json.load(f)
        bstack11l1ll11l11_opy_.append(bstack11ll1llll_opy_)
        with open(bstack11l1l11l1l1_opy_, bstack1ll1l11_opy_ (u"ࠩࡺࠫᬷ")) as f:
            json.dump(bstack11l1ll11l11_opy_, f)
    else:
        bstack11ll1llll_opy_ = {bstack1ll1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨᬸ"): test_name, bstack1ll1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᬹ"): bstack11ll111l11l_opy_, bstack1ll1l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᬺ"): str(multiprocessing.current_process().name)}
        if bstack1ll1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪᬻ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11ll1llll_opy_)
  except Exception as e:
      logger.warn(bstack1ll1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦᬼ").format(e))
def bstack1111111l1_opy_(error_message, test_name, index, logger):
  try:
    bstack11ll11ll1l1_opy_ = []
    bstack11ll1llll_opy_ = {bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᬽ"): test_name, bstack1ll1l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᬾ"): error_message, bstack1ll1l11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᬿ"): index}
    bstack11l1l1ll111_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᭀ"))
    if os.path.exists(bstack11l1l1ll111_opy_):
        with open(bstack11l1l1ll111_opy_) as f:
            bstack11ll11ll1l1_opy_ = json.load(f)
    bstack11ll11ll1l1_opy_.append(bstack11ll1llll_opy_)
    with open(bstack11l1l1ll111_opy_, bstack1ll1l11_opy_ (u"ࠬࡽࠧᭁ")) as f:
        json.dump(bstack11ll11ll1l1_opy_, f)
  except Exception as e:
    logger.warn(bstack1ll1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᭂ").format(e))
def bstack11lll111l_opy_(bstack111l11l1l_opy_, name, logger):
  try:
    bstack11ll1llll_opy_ = {bstack1ll1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᭃ"): name, bstack1ll1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸ᭄ࠧ"): bstack111l11l1l_opy_, bstack1ll1l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᭅ"): str(threading.current_thread()._name)}
    return bstack11ll1llll_opy_
  except Exception as e:
    logger.warn(bstack1ll1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᭆ").format(e))
  return
def bstack11l1lll1111_opy_():
    return platform.system() == bstack1ll1l11_opy_ (u"ࠫ࡜࡯࡮ࡥࡱࡺࡷࠬᭇ")
def bstack1lll11llll_opy_(bstack11l1l111l11_opy_, config, logger):
    bstack11ll111111l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l1l111l11_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡰࡹ࡫ࡲࠡࡥࡲࡲ࡫࡯ࡧࠡ࡭ࡨࡽࡸࠦࡢࡺࠢࡵࡩ࡬࡫ࡸࠡ࡯ࡤࡸࡨ࡮࠺ࠡࡽࢀࠦᭈ").format(e))
    return bstack11ll111111l_opy_
def bstack11ll11l111l_opy_(bstack11l1lllllll_opy_, bstack11l1l1lll11_opy_):
    bstack11l1l1l11ll_opy_ = version.parse(bstack11l1lllllll_opy_)
    bstack11l1ll11111_opy_ = version.parse(bstack11l1l1lll11_opy_)
    if bstack11l1l1l11ll_opy_ > bstack11l1ll11111_opy_:
        return 1
    elif bstack11l1l1l11ll_opy_ < bstack11l1ll11111_opy_:
        return -1
    else:
        return 0
def bstack111l1l1ll1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1l111l1l_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11ll11lll11_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11ll1l11_opy_(options, framework, bstack1l111111l1_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1ll1l11_opy_ (u"࠭ࡧࡦࡶࠪᭉ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l11llll11_opy_ = caps.get(bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᭊ"))
    bstack11l11lll1ll_opy_ = True
    bstack1111l111_opy_ = os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᭋ")]
    if bstack11ll11l1l11_opy_(caps.get(bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩ࡜࠹ࡃࠨᭌ"))) or bstack11ll11l1l11_opy_(caps.get(bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡥࡷ࠴ࡥࠪ᭍"))):
        bstack11l11lll1ll_opy_ = False
    if bstack1ll1ll1ll_opy_({bstack1ll1l11_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦ᭎"): bstack11l11lll1ll_opy_}):
        bstack1l11llll11_opy_ = bstack1l11llll11_opy_ or {}
        bstack1l11llll11_opy_[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᭏")] = bstack11ll11lll11_opy_(framework)
        bstack1l11llll11_opy_[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᭐")] = bstack1llll1l1l11_opy_()
        bstack1l11llll11_opy_[bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ᭑")] = bstack1111l111_opy_
        bstack1l11llll11_opy_[bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᭒")] = bstack1l111111l1_opy_
        if getattr(options, bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪ᭓"), None):
            options.set_capability(bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᭔"), bstack1l11llll11_opy_)
        else:
            options[bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᭕")] = bstack1l11llll11_opy_
    else:
        if getattr(options, bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭᭖"), None):
            options.set_capability(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᭗"), bstack11ll11lll11_opy_(framework))
            options.set_capability(bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᭘"), bstack1llll1l1l11_opy_())
            options.set_capability(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ᭙"), bstack1111l111_opy_)
            options.set_capability(bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᭚"), bstack1l111111l1_opy_)
        else:
            options[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ᭛")] = bstack11ll11lll11_opy_(framework)
            options[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ᭜")] = bstack1llll1l1l11_opy_()
            options[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ᭝")] = bstack1111l111_opy_
            options[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ᭞")] = bstack1l111111l1_opy_
    return options
def bstack11l1lllll1l_opy_(bstack11l1l1l111l_opy_, framework):
    bstack1l111111l1_opy_ = bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤ᭟"))
    if bstack11l1l1l111l_opy_ and len(bstack11l1l1l111l_opy_.split(bstack1ll1l11_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ᭠"))) > 1:
        ws_url = bstack11l1l1l111l_opy_.split(bstack1ll1l11_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ᭡"))[0]
        if bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭᭢") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l1l111ll1_opy_ = json.loads(urllib.parse.unquote(bstack11l1l1l111l_opy_.split(bstack1ll1l11_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ᭣"))[1]))
            bstack11l1l111ll1_opy_ = bstack11l1l111ll1_opy_ or {}
            bstack1111l111_opy_ = os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ᭤")]
            bstack11l1l111ll1_opy_[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᭥")] = str(framework) + str(__version__)
            bstack11l1l111ll1_opy_[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᭦")] = bstack1llll1l1l11_opy_()
            bstack11l1l111ll1_opy_[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ᭧")] = bstack1111l111_opy_
            bstack11l1l111ll1_opy_[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᭨")] = bstack1l111111l1_opy_
            bstack11l1l1l111l_opy_ = bstack11l1l1l111l_opy_.split(bstack1ll1l11_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ᭩"))[0] + bstack1ll1l11_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ᭪") + urllib.parse.quote(json.dumps(bstack11l1l111ll1_opy_))
    return bstack11l1l1l111l_opy_
def bstack11l11llll_opy_():
    global bstack1l111llll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l111llll_opy_ = BrowserType.connect
    return bstack1l111llll_opy_
def bstack1lll11l11l_opy_(framework_name):
    global bstack1l111111ll_opy_
    bstack1l111111ll_opy_ = framework_name
    return framework_name
def bstack1l1l1l11_opy_(self, *args, **kwargs):
    global bstack1l111llll_opy_
    try:
        global bstack1l111111ll_opy_
        if bstack1ll1l11_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩ᭫") in kwargs:
            kwargs[bstack1ll1l11_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ᭬ࠪ")] = bstack11l1lllll1l_opy_(
                kwargs.get(bstack1ll1l11_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫ᭭"), None),
                bstack1l111111ll_opy_
            )
    except Exception as e:
        logger.error(bstack1ll1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡖࡈࡐࠦࡣࡢࡲࡶ࠾ࠥࢁࡽࠣ᭮").format(str(e)))
    return bstack1l111llll_opy_(self, *args, **kwargs)
def bstack11ll111lll1_opy_(bstack11l1ll11l1l_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1ll1l1111_opy_(bstack11l1ll11l1l_opy_, bstack1ll1l11_opy_ (u"ࠤࠥ᭯"))
        if proxies and proxies.get(bstack1ll1l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤ᭰")):
            parsed_url = urlparse(proxies.get(bstack1ll1l11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥ᭱")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1ll1l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨ᭲")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩ᭳")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1ll1l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ᭴")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1ll1l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫ᭵")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1ll1111ll1_opy_(bstack11l1ll11l1l_opy_):
    bstack11l1ll1l1l1_opy_ = {
        bstack11ll1l1lll1_opy_[bstack11ll1111ll1_opy_]: bstack11l1ll11l1l_opy_[bstack11ll1111ll1_opy_]
        for bstack11ll1111ll1_opy_ in bstack11l1ll11l1l_opy_
        if bstack11ll1111ll1_opy_ in bstack11ll1l1lll1_opy_
    }
    bstack11l1ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤ᭶")] = bstack11ll111lll1_opy_(bstack11l1ll11l1l_opy_, bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥ᭷")))
    bstack11l1ll1ll11_opy_ = [element.lower() for element in bstack11ll1l1ll1l_opy_]
    bstack11ll11l1lll_opy_(bstack11l1ll1l1l1_opy_, bstack11l1ll1ll11_opy_)
    return bstack11l1ll1l1l1_opy_
def bstack11ll11l1lll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1ll1l11_opy_ (u"ࠦ࠯࠰ࠪࠫࠤ᭸")
    for value in d.values():
        if isinstance(value, dict):
            bstack11ll11l1lll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11ll11l1lll_opy_(item, keys)
def bstack1llllll111l_opy_():
    bstack11l1llll111_opy_ = [os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡏࡌࡆࡕࡢࡈࡎࡘࠢ᭹")), os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠨࡾࠣ᭺")), bstack1ll1l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ᭻")), os.path.join(bstack1ll1l11_opy_ (u"ࠨ࠱ࡷࡱࡵ࠭᭼"), bstack1ll1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ᭽"))]
    for path in bstack11l1llll111_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1ll1l11_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥ᭾") + str(path) + bstack1ll1l11_opy_ (u"ࠦࠬࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠢ᭿"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1ll1l11_opy_ (u"ࠧࡍࡩࡷ࡫ࡱ࡫ࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠣࡪࡴࡸࠠࠨࠤᮀ") + str(path) + bstack1ll1l11_opy_ (u"ࠨࠧࠣᮁ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1ll1l11_opy_ (u"ࠢࡇ࡫࡯ࡩࠥ࠭ࠢᮂ") + str(path) + bstack1ll1l11_opy_ (u"ࠣࠩࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡭ࡧࡳࠡࡶ࡫ࡩࠥࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷ࠳ࠨᮃ"))
            else:
                logger.debug(bstack1ll1l11_opy_ (u"ࠤࡆࡶࡪࡧࡴࡪࡰࡪࠤ࡫࡯࡬ࡦࠢࠪࠦᮄ") + str(path) + bstack1ll1l11_opy_ (u"ࠥࠫࠥࡽࡩࡵࡪࠣࡻࡷ࡯ࡴࡦࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳ࠴ࠢᮅ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1ll1l11_opy_ (u"ࠦࡔࡶࡥࡳࡣࡷ࡭ࡴࡴࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦࠣࡪࡴࡸࠠࠨࠤᮆ") + str(path) + bstack1ll1l11_opy_ (u"ࠧ࠭࠮ࠣᮇ"))
            return path
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡵࡱࠢࡩ࡭ࡱ࡫ࠠࠨࡽࡳࡥࡹ࡮ࡽࠨ࠼ࠣࠦᮈ") + str(e) + bstack1ll1l11_opy_ (u"ࠢࠣᮉ"))
    logger.debug(bstack1ll1l11_opy_ (u"ࠣࡃ࡯ࡰࠥࡶࡡࡵࡪࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠧᮊ"))
    return None
@measure(event_name=EVENTS.bstack11ll1ll11ll_opy_, stage=STAGE.bstack1l11lll1l_opy_)
def bstack1l11ll11ll1_opy_(binary_path, bstack1l1l1l11l1l_opy_, bs_config):
    logger.debug(bstack1ll1l11_opy_ (u"ࠤࡆࡹࡷࡸࡥ࡯ࡶࠣࡇࡑࡏࠠࡑࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧ࠾ࠥࢁࡽࠣᮋ").format(binary_path))
    bstack11ll111l111_opy_ = bstack1ll1l11_opy_ (u"ࠪࠫᮌ")
    bstack11ll111ll11_opy_ = {
        bstack1ll1l11_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᮍ"): __version__,
        bstack1ll1l11_opy_ (u"ࠧࡵࡳࠣᮎ"): platform.system(),
        bstack1ll1l11_opy_ (u"ࠨ࡯ࡴࡡࡤࡶࡨ࡮ࠢᮏ"): platform.machine(),
        bstack1ll1l11_opy_ (u"ࠢࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧᮐ"): bstack1ll1l11_opy_ (u"ࠨ࠲ࠪᮑ"),
        bstack1ll1l11_opy_ (u"ࠤࡶࡨࡰࡥ࡬ࡢࡰࡪࡹࡦ࡭ࡥࠣᮒ"): bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᮓ")
    }
    try:
        if binary_path:
            bstack11ll111ll11_opy_[bstack1ll1l11_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᮔ")] = subprocess.check_output([binary_path, bstack1ll1l11_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨᮕ")]).strip().decode(bstack1ll1l11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᮖ"))
        response = requests.request(
            bstack1ll1l11_opy_ (u"ࠧࡈࡇࡗࠫᮗ"),
            url=bstack1ll1l11l11_opy_(bstack11ll1ll11l1_opy_),
            headers=None,
            auth=(bs_config[bstack1ll1l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᮘ")], bs_config[bstack1ll1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᮙ")]),
            json=None,
            params=bstack11ll111ll11_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1ll1l11_opy_ (u"ࠪࡹࡷࡲࠧᮚ") in data.keys() and bstack1ll1l11_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡨࡤࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪᮛ") in data.keys():
            logger.debug(bstack1ll1l11_opy_ (u"ࠧࡔࡥࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡢࡪࡰࡤࡶࡾ࠲ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡤ࡬ࡲࡦࡸࡹࠡࡸࡨࡶࡸ࡯࡯࡯࠼ࠣࡿࢂࠨᮜ").format(bstack11ll111ll11_opy_[bstack1ll1l11_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫᮝ")]))
            bstack11l11llll1l_opy_ = bstack11l1ll111l1_opy_(data[bstack1ll1l11_opy_ (u"ࠧࡶࡴ࡯ࠫᮞ")], bstack1l1l1l11l1l_opy_)
            bstack11ll111l111_opy_ = os.path.join(bstack1l1l1l11l1l_opy_, bstack11l11llll1l_opy_)
            os.chmod(bstack11ll111l111_opy_, 0o777) # bstack11l1l11l1ll_opy_ permission
            return bstack11ll111l111_opy_
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡳ࡫ࡷࠡࡕࡇࡏࠥࢁࡽࠣᮟ").format(e))
    return binary_path
@measure(event_name=EVENTS.bstack11ll1l1l11l_opy_, stage=STAGE.bstack1l11lll1l_opy_)
def bstack11l1ll111l1_opy_(bstack11ll1111111_opy_, bstack11l1l11llll_opy_):
    logger.debug(bstack1ll1l11_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮࠼ࠣࠦᮠ") + str(bstack11ll1111111_opy_) + bstack1ll1l11_opy_ (u"ࠥࠦᮡ"))
    zip_path = os.path.join(bstack11l1l11llll_opy_, bstack1ll1l11_opy_ (u"ࠦࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࡠࡨ࡬ࡰࡪ࠴ࡺࡪࡲࠥᮢ"))
    bstack11l11llll1l_opy_ = bstack1ll1l11_opy_ (u"ࠬ࠭ᮣ")
    with requests.get(bstack11ll1111111_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1ll1l11_opy_ (u"ࠨࡷࡣࠤᮤ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1ll1l11_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹ࠯ࠤᮥ"))
    with zipfile.ZipFile(zip_path, bstack1ll1l11_opy_ (u"ࠨࡴࠪᮦ")) as zip_ref:
        bstack11ll11lll1l_opy_ = zip_ref.namelist()
        if len(bstack11ll11lll1l_opy_) > 0:
            bstack11l11llll1l_opy_ = bstack11ll11lll1l_opy_[0] # bstack11l1l11l111_opy_ bstack11lll11111l_opy_ will be bstack11l1ll111ll_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l1l11llll_opy_)
        logger.debug(bstack1ll1l11_opy_ (u"ࠤࡉ࡭ࡱ࡫ࡳࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡦࡺࡷࡶࡦࡩࡴࡦࡦࠣࡸࡴࠦࠧࠣᮧ") + str(bstack11l1l11llll_opy_) + bstack1ll1l11_opy_ (u"ࠥࠫࠧᮨ"))
    os.remove(zip_path)
    return bstack11l11llll1l_opy_
def get_cli_dir():
    bstack11l1l111111_opy_ = bstack1llllll111l_opy_()
    if bstack11l1l111111_opy_:
        bstack1l1l1l11l1l_opy_ = os.path.join(bstack11l1l111111_opy_, bstack1ll1l11_opy_ (u"ࠦࡨࡲࡩࠣᮩ"))
        if not os.path.exists(bstack1l1l1l11l1l_opy_):
            os.makedirs(bstack1l1l1l11l1l_opy_, mode=0o777, exist_ok=True)
        return bstack1l1l1l11l1l_opy_
    else:
        raise FileNotFoundError(bstack1ll1l11_opy_ (u"ࠧࡔ࡯ࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡩࡳࡷࠦࡴࡩࡧࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿ࠮᮪ࠣ"))
def bstack1l11l1ll1ll_opy_(bstack1l1l1l11l1l_opy_):
    bstack1ll1l11_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡺࡨࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮ࡴࠠࡢࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠮ࠣࠤ᮫ࠥ")
    bstack11l1lll1ll1_opy_ = [
        os.path.join(bstack1l1l1l11l1l_opy_, f)
        for f in os.listdir(bstack1l1l1l11l1l_opy_)
        if os.path.isfile(os.path.join(bstack1l1l1l11l1l_opy_, f)) and f.startswith(bstack1ll1l11_opy_ (u"ࠢࡣ࡫ࡱࡥࡷࡿ࠭ࠣᮬ"))
    ]
    if len(bstack11l1lll1ll1_opy_) > 0:
        return max(bstack11l1lll1ll1_opy_, key=os.path.getmtime) # get bstack11l1l1lll1l_opy_ binary
    return bstack1ll1l11_opy_ (u"ࠣࠤᮭ")
def bstack1l111lll1ll_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l111lll1ll_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d