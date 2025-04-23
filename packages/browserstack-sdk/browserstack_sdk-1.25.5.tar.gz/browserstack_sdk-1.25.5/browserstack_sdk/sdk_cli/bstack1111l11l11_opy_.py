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
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack1ll1l1l1111_opy_,
    bstack1111l1lll1_opy_,
    bstack11111l1lll_opy_,
    bstack111111ll1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1ll11l1lll_opy_ import bstack111111lll1_opy_
from bstack_utils.constants import EVENTS
class bstack1111111ll1_opy_(bstack1ll1l1l1111_opy_):
    bstack1ll11ll1ll1_opy_ = bstack1ll1l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨጕ")
    NAME = bstack1ll1l11_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤ጖")
    bstack1lll1l1111l_opy_ = bstack1ll1l11_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤ጗")
    bstack1lll1l11ll1_opy_ = bstack1ll1l11_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤጘ")
    bstack1l1ll1l1111_opy_ = bstack1ll1l11_opy_ (u"ࠥ࡭ࡳࡶࡵࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣጙ")
    bstack1lll1l1l1ll_opy_ = bstack1ll1l11_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥጚ")
    bstack1ll1l1l1l11_opy_ = bstack1ll1l11_opy_ (u"ࠧ࡯ࡳࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡩࡷࡥࠦጛ")
    bstack1l1ll11llll_opy_ = bstack1ll1l11_opy_ (u"ࠨࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥጜ")
    bstack1l1ll11ll1l_opy_ = bstack1ll1l11_opy_ (u"ࠢࡦࡰࡧࡩࡩࡥࡡࡵࠤጝ")
    bstack1111l11ll1_opy_ = bstack1ll1l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤጞ")
    bstack1ll1ll1llll_opy_ = bstack1ll1l11_opy_ (u"ࠤࡱࡩࡼࡹࡥࡴࡵ࡬ࡳࡳࠨጟ")
    bstack1l1ll1l11l1_opy_ = bstack1ll1l11_opy_ (u"ࠥ࡫ࡪࡺࠢጠ")
    bstack1lllllll11l_opy_ = bstack1ll1l11_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣጡ")
    bstack1ll11ll1l1l_opy_ = bstack1ll1l11_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࠣጢ")
    bstack1ll11lll111_opy_ = bstack1ll1l11_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࡣࡶࡽࡳࡩࠢጣ")
    bstack1l1ll1l11ll_opy_ = bstack1ll1l11_opy_ (u"ࠢࡲࡷ࡬ࡸࠧጤ")
    bstack1l1ll11ll11_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1lll11ll_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1l1ll111_opy_: Any
    bstack1ll1l111111_opy_: Dict
    def __init__(
        self,
        bstack1ll1lll11ll_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1ll1l1ll111_opy_: Dict[str, Any],
        methods=[bstack1ll1l11_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥጥ"), bstack1ll1l11_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤጦ"), bstack1ll1l11_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦጧ"), bstack1ll1l11_opy_ (u"ࠦࡶࡻࡩࡵࠤጨ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1ll1lll11ll_opy_ = bstack1ll1lll11ll_opy_
        self.platform_index = platform_index
        self.bstack1ll1l11l11l_opy_(methods)
        self.bstack1ll1l1ll111_opy_ = bstack1ll1l1ll111_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1ll1l1l1111_opy_.get_data(bstack1111111ll1_opy_.bstack1lll1l11ll1_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1ll1l1l1111_opy_.get_data(bstack1111111ll1_opy_.bstack1lll1l1111l_opy_, target, strict)
    @staticmethod
    def bstack1l1ll1l111l_opy_(target: object, strict=True):
        return bstack1ll1l1l1111_opy_.get_data(bstack1111111ll1_opy_.bstack1l1ll1l1111_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1ll1l1l1111_opy_.get_data(bstack1111111ll1_opy_.bstack1lll1l1l1ll_opy_, target, strict)
    @staticmethod
    def bstack1ll1l11ll1l_opy_(instance: bstack1111l1lll1_opy_) -> bool:
        return bstack1ll1l1l1111_opy_.bstack11111l11l1_opy_(instance, bstack1111111ll1_opy_.bstack1ll1l1l1l11_opy_, False)
    @staticmethod
    def bstack1ll1l111ll1_opy_(instance: bstack1111l1lll1_opy_, default_value=None):
        return bstack1ll1l1l1111_opy_.bstack11111l11l1_opy_(instance, bstack1111111ll1_opy_.bstack1lll1l1111l_opy_, default_value)
    @staticmethod
    def bstack1ll1l1111ll_opy_(instance: bstack1111l1lll1_opy_, default_value=None):
        return bstack1ll1l1l1111_opy_.bstack11111l11l1_opy_(instance, bstack1111111ll1_opy_.bstack1lll1l1l1ll_opy_, default_value)
    @staticmethod
    def bstack1l1ll11l1ll_opy_(hub_url: str, bstack1l1ll11l111_opy_=bstack1ll1l11_opy_ (u"ࠧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤጩ")):
        try:
            bstack1l1ll11l1l1_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l1ll11l1l1_opy_.endswith(bstack1l1ll11l111_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1111l11111_opy_(method_name: str):
        return method_name == bstack1ll1l11_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢጪ")
    @staticmethod
    def bstack1ll1l1ll1ll_opy_(method_name: str, *args):
        return (
            bstack1111111ll1_opy_.bstack1111l11111_opy_(method_name)
            and bstack1111111ll1_opy_.bstack1ll1ll1l1l1_opy_(*args) == bstack1111111ll1_opy_.bstack1ll1ll1llll_opy_
        )
    @staticmethod
    def bstack1ll1l111lll_opy_(method_name: str, *args):
        if not bstack1111111ll1_opy_.bstack1111l11111_opy_(method_name):
            return False
        if not bstack1111111ll1_opy_.bstack1ll11ll1l1l_opy_ in bstack1111111ll1_opy_.bstack1ll1ll1l1l1_opy_(*args):
            return False
        bstack1ll1l1111l1_opy_ = bstack1111111ll1_opy_.bstack1ll1l11111l_opy_(*args)
        return bstack1ll1l1111l1_opy_ and bstack1ll1l11_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢጫ") in bstack1ll1l1111l1_opy_ and bstack1ll1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤጬ") in bstack1ll1l1111l1_opy_[bstack1ll1l11_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤጭ")]
    @staticmethod
    def bstack1ll1l111l1l_opy_(method_name: str, *args):
        if not bstack1111111ll1_opy_.bstack1111l11111_opy_(method_name):
            return False
        if not bstack1111111ll1_opy_.bstack1ll11ll1l1l_opy_ in bstack1111111ll1_opy_.bstack1ll1ll1l1l1_opy_(*args):
            return False
        bstack1ll1l1111l1_opy_ = bstack1111111ll1_opy_.bstack1ll1l11111l_opy_(*args)
        return (
            bstack1ll1l1111l1_opy_
            and bstack1ll1l11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥጮ") in bstack1ll1l1111l1_opy_
            and bstack1ll1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡥࡵ࡭ࡵࡺࠢጯ") in bstack1ll1l1111l1_opy_[bstack1ll1l11_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧጰ")]
        )
    @staticmethod
    def bstack1ll1ll1l1l1_opy_(*args):
        return str(bstack1111111ll1_opy_.bstack111111l11l_opy_(*args)).lower()
    @staticmethod
    def bstack111111l11l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l11111l_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack11l1ll1111_opy_(driver):
        command_executor = getattr(driver, bstack1ll1l11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤጱ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1ll1l11_opy_ (u"ࠢࡠࡷࡵࡰࠧጲ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1ll1l11_opy_ (u"ࠣࡡࡦࡰ࡮࡫࡮ࡵࡡࡦࡳࡳ࡬ࡩࡨࠤጳ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1ll1l11_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡡࡶࡩࡷࡼࡥࡳࡡࡤࡨࡩࡸࠢጴ"), None)
        return hub_url
    def bstack1ll1ll1l1ll_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1ll1l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨጵ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1ll1l11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢጶ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1ll1l11_opy_ (u"ࠧࡥࡵࡳ࡮ࠥጷ")):
                setattr(command_executor, bstack1ll1l11_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦጸ"), hub_url)
                result = True
        if result:
            self.bstack1ll1lll11ll_opy_ = hub_url
            bstack1111111ll1_opy_.bstack1lllllll1l1_opy_(instance, bstack1111111ll1_opy_.bstack1lll1l1111l_opy_, hub_url)
            bstack1111111ll1_opy_.bstack1lllllll1l1_opy_(
                instance, bstack1111111ll1_opy_.bstack1ll1l1l1l11_opy_, bstack1111111ll1_opy_.bstack1l1ll11l1ll_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1ll11llll11_opy_(bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_]):
        return bstack1ll1l11_opy_ (u"ࠢ࠻ࠤጹ").join((bstack11111l1lll_opy_(bstack111111111l_opy_[0]).name, bstack111111ll1l_opy_(bstack111111111l_opy_[1]).name))
    @staticmethod
    def bstack111111l1l1_opy_(bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_], callback: Callable):
        bstack1ll11llllll_opy_ = bstack1111111ll1_opy_.bstack1ll11llll11_opy_(bstack111111111l_opy_)
        if not bstack1ll11llllll_opy_ in bstack1111111ll1_opy_.bstack1l1ll11ll11_opy_:
            bstack1111111ll1_opy_.bstack1l1ll11ll11_opy_[bstack1ll11llllll_opy_] = []
        bstack1111111ll1_opy_.bstack1l1ll11ll11_opy_[bstack1ll11llllll_opy_].append(callback)
    def bstack1ll11lll11l_opy_(self, instance: bstack1111l1lll1_opy_, method_name: str, bstack1ll11lllll1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1ll1l11_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣጺ")):
            return
        cmd = args[0] if method_name == bstack1ll1l11_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥጻ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l1ll11lll1_opy_ = bstack1ll1l11_opy_ (u"ࠥ࠾ࠧጼ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠧጽ") + bstack1l1ll11lll1_opy_, bstack1ll11lllll1_opy_)
    def bstack1ll11llll1l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll1l111l11_opy_, bstack1ll11ll1lll_opy_ = bstack111111111l_opy_
        bstack1ll11llllll_opy_ = bstack1111111ll1_opy_.bstack1ll11llll11_opy_(bstack111111111l_opy_)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡵ࡮ࡠࡪࡲࡳࡰࡀࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጾ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠨࠢጿ"))
        if bstack1ll1l111l11_opy_ == bstack11111l1lll_opy_.QUIT:
            if bstack1ll11ll1lll_opy_ == bstack111111ll1l_opy_.PRE:
                bstack11111l11ll_opy_ = bstack111111lll1_opy_.bstack11111l1111_opy_(EVENTS.bstack1l1l11l111_opy_.value)
                bstack1ll1l1l1111_opy_.bstack1lllllll1l1_opy_(instance, EVENTS.bstack1l1l11l111_opy_.value, bstack11111l11ll_opy_)
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠦፀ").format(instance, method_name, bstack1ll1l111l11_opy_, bstack1ll11ll1lll_opy_))
        if bstack1ll1l111l11_opy_ == bstack11111l1lll_opy_.bstack1lll11llll1_opy_:
            if bstack1ll11ll1lll_opy_ == bstack111111ll1l_opy_.POST and not bstack1111111ll1_opy_.bstack1lll1l11ll1_opy_ in instance.data:
                session_id = getattr(target, bstack1ll1l11_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧፁ"), None)
                if session_id:
                    instance.data[bstack1111111ll1_opy_.bstack1lll1l11ll1_opy_] = session_id
        elif (
            bstack1ll1l111l11_opy_ == bstack11111l1lll_opy_.bstack1111l1l1l1_opy_
            and bstack1111111ll1_opy_.bstack1ll1ll1l1l1_opy_(*args) == bstack1111111ll1_opy_.bstack1ll1ll1llll_opy_
        ):
            if bstack1ll11ll1lll_opy_ == bstack111111ll1l_opy_.PRE:
                hub_url = bstack1111111ll1_opy_.bstack11l1ll1111_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1111111ll1_opy_.bstack1lll1l1111l_opy_: hub_url,
                            bstack1111111ll1_opy_.bstack1ll1l1l1l11_opy_: bstack1111111ll1_opy_.bstack1l1ll11l1ll_opy_(hub_url),
                            bstack1111111ll1_opy_.bstack1111l11ll1_opy_: int(
                                os.environ.get(bstack1ll1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤፂ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll1l1111l1_opy_ = bstack1111111ll1_opy_.bstack1ll1l11111l_opy_(*args)
                bstack1l1ll1l111l_opy_ = bstack1ll1l1111l1_opy_.get(bstack1ll1l11_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤፃ"), None) if bstack1ll1l1111l1_opy_ else None
                if isinstance(bstack1l1ll1l111l_opy_, dict):
                    instance.data[bstack1111111ll1_opy_.bstack1l1ll1l1111_opy_] = copy.deepcopy(bstack1l1ll1l111l_opy_)
                    instance.data[bstack1111111ll1_opy_.bstack1lll1l1l1ll_opy_] = bstack1l1ll1l111l_opy_
            elif bstack1ll11ll1lll_opy_ == bstack111111ll1l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1ll1l11_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥፄ"), dict()).get(bstack1ll1l11_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡏࡤࠣፅ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1111111ll1_opy_.bstack1lll1l11ll1_opy_: framework_session_id,
                                bstack1111111ll1_opy_.bstack1l1ll11llll_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1ll1l111l11_opy_ == bstack11111l1lll_opy_.bstack1111l1l1l1_opy_
            and bstack1111111ll1_opy_.bstack1ll1ll1l1l1_opy_(*args) == bstack1111111ll1_opy_.bstack1l1ll1l11ll_opy_
            and bstack1ll11ll1lll_opy_ == bstack111111ll1l_opy_.POST
        ):
            instance.data[bstack1111111ll1_opy_.bstack1l1ll11ll1l_opy_] = datetime.now(tz=timezone.utc)
        if bstack1ll11llllll_opy_ in bstack1111111ll1_opy_.bstack1l1ll11ll11_opy_:
            bstack1ll11lll1l1_opy_ = None
            for callback in bstack1111111ll1_opy_.bstack1l1ll11ll11_opy_[bstack1ll11llllll_opy_]:
                try:
                    bstack1ll1l11l111_opy_ = callback(self, target, exec, bstack111111111l_opy_, result, *args, **kwargs)
                    if bstack1ll11lll1l1_opy_ == None:
                        bstack1ll11lll1l1_opy_ = bstack1ll1l11l111_opy_
                except Exception as e:
                    self.logger.error(bstack1ll1l11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࠦፆ") + str(e) + bstack1ll1l11_opy_ (u"ࠢࠣፇ"))
                    traceback.print_exc()
            if bstack1ll1l111l11_opy_ == bstack11111l1lll_opy_.QUIT:
                if bstack1ll11ll1lll_opy_ == bstack111111ll1l_opy_.POST:
                    bstack11111l11ll_opy_ = bstack1ll1l1l1111_opy_.bstack11111l11l1_opy_(instance, EVENTS.bstack1l1l11l111_opy_.value)
                    if bstack11111l11ll_opy_!=None:
                        bstack111111lll1_opy_.end(EVENTS.bstack1l1l11l111_opy_.value, bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣፈ"), bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢፉ"), True, None)
            if bstack1ll11ll1lll_opy_ == bstack111111ll1l_opy_.PRE and callable(bstack1ll11lll1l1_opy_):
                return bstack1ll11lll1l1_opy_
            elif bstack1ll11ll1lll_opy_ == bstack111111ll1l_opy_.POST and bstack1ll11lll1l1_opy_:
                return bstack1ll11lll1l1_opy_
    def bstack1ll1l11l1l1_opy_(
        self, method_name, previous_state: bstack11111l1lll_opy_, *args, **kwargs
    ) -> bstack11111l1lll_opy_:
        if method_name == bstack1ll1l11_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧፊ") or method_name == bstack1ll1l11_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦፋ"):
            return bstack11111l1lll_opy_.bstack1lll11llll1_opy_
        if method_name == bstack1ll1l11_opy_ (u"ࠧࡷࡵࡪࡶࠥፌ"):
            return bstack11111l1lll_opy_.QUIT
        if method_name == bstack1ll1l11_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢፍ"):
            if previous_state != bstack11111l1lll_opy_.NONE:
                bstack1l1ll11l11l_opy_ = bstack1111111ll1_opy_.bstack1ll1ll1l1l1_opy_(*args)
                if bstack1l1ll11l11l_opy_ == bstack1111111ll1_opy_.bstack1ll1ll1llll_opy_:
                    return bstack11111l1lll_opy_.bstack1lll11llll1_opy_
            return bstack11111l1lll_opy_.bstack1111l1l1l1_opy_
        return bstack11111l1lll_opy_.NONE