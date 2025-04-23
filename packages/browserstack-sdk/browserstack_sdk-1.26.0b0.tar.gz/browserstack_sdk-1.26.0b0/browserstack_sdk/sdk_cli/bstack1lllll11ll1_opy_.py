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
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import (
    bstack1111l1l11l_opy_,
    bstack1111l1111l_opy_,
    bstack1111l11l1l_opy_,
    bstack11111l1ll1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll111l1l_opy_
from bstack_utils.constants import EVENTS
class bstack1ll1lllll11_opy_(bstack1111l1l11l_opy_):
    bstack1l11llllll1_opy_ = bstack11111ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᒱ")
    NAME = bstack11111ll_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᒲ")
    bstack1l1ll11l1ll_opy_ = bstack11111ll_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬ࠣᒳ")
    bstack1l1ll11l111_opy_ = bstack11111ll_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᒴ")
    bstack1l1111lllll_opy_ = bstack11111ll_opy_ (u"ࠤ࡬ࡲࡵࡻࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᒵ")
    bstack1l1ll111l1l_opy_ = bstack11111ll_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᒶ")
    bstack1l1l111ll1l_opy_ = bstack11111ll_opy_ (u"ࠦ࡮ࡹ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡨࡶࡤࠥᒷ")
    bstack1l1111ll1l1_opy_ = bstack11111ll_opy_ (u"ࠧࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᒸ")
    bstack1l111l11111_opy_ = bstack11111ll_opy_ (u"ࠨࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᒹ")
    bstack1ll1ll111ll_opy_ = bstack11111ll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᒺ")
    bstack1l1l1l11lll_opy_ = bstack11111ll_opy_ (u"ࠣࡰࡨࡻࡸ࡫ࡳࡴ࡫ࡲࡲࠧᒻ")
    bstack1l111l1111l_opy_ = bstack11111ll_opy_ (u"ࠤࡪࡩࡹࠨᒼ")
    bstack1l1llll1l1l_opy_ = bstack11111ll_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢᒽ")
    bstack1l11lllll11_opy_ = bstack11111ll_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࠢᒾ")
    bstack1l1l1111l1l_opy_ = bstack11111ll_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࡢࡵࡼࡲࡨࠨᒿ")
    bstack1l111l111l1_opy_ = bstack11111ll_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᓀ")
    bstack1l1111ll1ll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l11l1l11_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll111ll11_opy_: Any
    bstack1l11lllllll_opy_: Dict
    def __init__(
        self,
        bstack1l1l11l1l11_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lll111ll11_opy_: Dict[str, Any],
        methods=[bstack11111ll_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᓁ"), bstack11111ll_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᓂ"), bstack11111ll_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᓃ"), bstack11111ll_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᓄ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1l11l1l11_opy_ = bstack1l1l11l1l11_opy_
        self.platform_index = platform_index
        self.bstack1111111111_opy_(methods)
        self.bstack1lll111ll11_opy_ = bstack1lll111ll11_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1111l1l11l_opy_.get_data(bstack1ll1lllll11_opy_.bstack1l1ll11l111_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1111l1l11l_opy_.get_data(bstack1ll1lllll11_opy_.bstack1l1ll11l1ll_opy_, target, strict)
    @staticmethod
    def bstack1l1111lll1l_opy_(target: object, strict=True):
        return bstack1111l1l11l_opy_.get_data(bstack1ll1lllll11_opy_.bstack1l1111lllll_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1111l1l11l_opy_.get_data(bstack1ll1lllll11_opy_.bstack1l1ll111l1l_opy_, target, strict)
    @staticmethod
    def bstack1ll1l1l1ll1_opy_(instance: bstack1111l1111l_opy_) -> bool:
        return bstack1111l1l11l_opy_.bstack11111lll1l_opy_(instance, bstack1ll1lllll11_opy_.bstack1l1l111ll1l_opy_, False)
    @staticmethod
    def bstack1ll1l111l11_opy_(instance: bstack1111l1111l_opy_, default_value=None):
        return bstack1111l1l11l_opy_.bstack11111lll1l_opy_(instance, bstack1ll1lllll11_opy_.bstack1l1ll11l1ll_opy_, default_value)
    @staticmethod
    def bstack1ll1ll1l11l_opy_(instance: bstack1111l1111l_opy_, default_value=None):
        return bstack1111l1l11l_opy_.bstack11111lll1l_opy_(instance, bstack1ll1lllll11_opy_.bstack1l1ll111l1l_opy_, default_value)
    @staticmethod
    def bstack1ll11ll1ll1_opy_(hub_url: str, bstack1l1111llll1_opy_=bstack11111ll_opy_ (u"ࠦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠣᓅ")):
        try:
            bstack1l1111lll11_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l1111lll11_opy_.endswith(bstack1l1111llll1_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1l1l11l1_opy_(method_name: str):
        return method_name == bstack11111ll_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᓆ")
    @staticmethod
    def bstack1ll1l1l1111_opy_(method_name: str, *args):
        return (
            bstack1ll1lllll11_opy_.bstack1ll1l1l11l1_opy_(method_name)
            and bstack1ll1lllll11_opy_.bstack1l1l11ll1l1_opy_(*args) == bstack1ll1lllll11_opy_.bstack1l1l1l11lll_opy_
        )
    @staticmethod
    def bstack1ll11llll11_opy_(method_name: str, *args):
        if not bstack1ll1lllll11_opy_.bstack1ll1l1l11l1_opy_(method_name):
            return False
        if not bstack1ll1lllll11_opy_.bstack1l11lllll11_opy_ in bstack1ll1lllll11_opy_.bstack1l1l11ll1l1_opy_(*args):
            return False
        bstack1ll11ll11ll_opy_ = bstack1ll1lllll11_opy_.bstack1ll11lll11l_opy_(*args)
        return bstack1ll11ll11ll_opy_ and bstack11111ll_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᓇ") in bstack1ll11ll11ll_opy_ and bstack11111ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᓈ") in bstack1ll11ll11ll_opy_[bstack11111ll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᓉ")]
    @staticmethod
    def bstack1ll11lll1ll_opy_(method_name: str, *args):
        if not bstack1ll1lllll11_opy_.bstack1ll1l1l11l1_opy_(method_name):
            return False
        if not bstack1ll1lllll11_opy_.bstack1l11lllll11_opy_ in bstack1ll1lllll11_opy_.bstack1l1l11ll1l1_opy_(*args):
            return False
        bstack1ll11ll11ll_opy_ = bstack1ll1lllll11_opy_.bstack1ll11lll11l_opy_(*args)
        return (
            bstack1ll11ll11ll_opy_
            and bstack11111ll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᓊ") in bstack1ll11ll11ll_opy_
            and bstack11111ll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡤࡴ࡬ࡴࡹࠨᓋ") in bstack1ll11ll11ll_opy_[bstack11111ll_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᓌ")]
        )
    @staticmethod
    def bstack1l1l11ll1l1_opy_(*args):
        return str(bstack1ll1lllll11_opy_.bstack1ll11llll1l_opy_(*args)).lower()
    @staticmethod
    def bstack1ll11llll1l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11lll11l_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1l111l11l_opy_(driver):
        command_executor = getattr(driver, bstack11111ll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᓍ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11111ll_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᓎ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11111ll_opy_ (u"ࠢࡠࡥ࡯࡭ࡪࡴࡴࡠࡥࡲࡲ࡫࡯ࡧࠣᓏ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11111ll_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡠࡵࡨࡶࡻ࡫ࡲࡠࡣࡧࡨࡷࠨᓐ"), None)
        return hub_url
    def bstack1l1l11l1ll1_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11111ll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᓑ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11111ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᓒ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11111ll_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᓓ")):
                setattr(command_executor, bstack11111ll_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᓔ"), hub_url)
                result = True
        if result:
            self.bstack1l1l11l1l11_opy_ = hub_url
            bstack1ll1lllll11_opy_.bstack11111l11ll_opy_(instance, bstack1ll1lllll11_opy_.bstack1l1ll11l1ll_opy_, hub_url)
            bstack1ll1lllll11_opy_.bstack11111l11ll_opy_(
                instance, bstack1ll1lllll11_opy_.bstack1l1l111ll1l_opy_, bstack1ll1lllll11_opy_.bstack1ll11ll1ll1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l1l1111l11_opy_(bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_]):
        return bstack11111ll_opy_ (u"ࠨ࠺ࠣᓕ").join((bstack1111l11l1l_opy_(bstack11111l111l_opy_[0]).name, bstack11111l1ll1_opy_(bstack11111l111l_opy_[1]).name))
    @staticmethod
    def bstack1ll1ll11l11_opy_(bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_], callback: Callable):
        bstack1l1l11111l1_opy_ = bstack1ll1lllll11_opy_.bstack1l1l1111l11_opy_(bstack11111l111l_opy_)
        if not bstack1l1l11111l1_opy_ in bstack1ll1lllll11_opy_.bstack1l1111ll1ll_opy_:
            bstack1ll1lllll11_opy_.bstack1l1111ll1ll_opy_[bstack1l1l11111l1_opy_] = []
        bstack1ll1lllll11_opy_.bstack1l1111ll1ll_opy_[bstack1l1l11111l1_opy_].append(callback)
    def bstack11111l11l1_opy_(self, instance: bstack1111l1111l_opy_, method_name: str, bstack1111l11lll_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11111ll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᓖ")):
            return
        cmd = args[0] if method_name == bstack11111ll_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᓗ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l111l111ll_opy_ = bstack11111ll_opy_ (u"ࠤ࠽ࠦᓘ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠦᓙ") + bstack1l111l111ll_opy_, bstack1111l11lll_opy_)
    def bstack111111ll11_opy_(
        self,
        target: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack11111l1lll_opy_, bstack1l11lllll1l_opy_ = bstack11111l111l_opy_
        bstack1l1l11111l1_opy_ = bstack1ll1lllll11_opy_.bstack1l1l1111l11_opy_(bstack11111l111l_opy_)
        self.logger.debug(bstack11111ll_opy_ (u"ࠦࡴࡴ࡟ࡩࡱࡲ࡯࠿ࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᓚ") + str(kwargs) + bstack11111ll_opy_ (u"ࠧࠨᓛ"))
        if bstack11111l1lll_opy_ == bstack1111l11l1l_opy_.QUIT:
            if bstack1l11lllll1l_opy_ == bstack11111l1ll1_opy_.PRE:
                bstack1ll1ll1l1ll_opy_ = bstack1llll111l1l_opy_.bstack1ll1l111lll_opy_(EVENTS.bstack1l11l1lll1_opy_.value)
                bstack1111l1l11l_opy_.bstack11111l11ll_opy_(instance, EVENTS.bstack1l11l1lll1_opy_.value, bstack1ll1ll1l1ll_opy_)
                self.logger.debug(bstack11111ll_opy_ (u"ࠨࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠥᓜ").format(instance, method_name, bstack11111l1lll_opy_, bstack1l11lllll1l_opy_))
        if bstack11111l1lll_opy_ == bstack1111l11l1l_opy_.bstack1111111l11_opy_:
            if bstack1l11lllll1l_opy_ == bstack11111l1ll1_opy_.POST and not bstack1ll1lllll11_opy_.bstack1l1ll11l111_opy_ in instance.data:
                session_id = getattr(target, bstack11111ll_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᓝ"), None)
                if session_id:
                    instance.data[bstack1ll1lllll11_opy_.bstack1l1ll11l111_opy_] = session_id
        elif (
            bstack11111l1lll_opy_ == bstack1111l11l1l_opy_.bstack1llllllll1l_opy_
            and bstack1ll1lllll11_opy_.bstack1l1l11ll1l1_opy_(*args) == bstack1ll1lllll11_opy_.bstack1l1l1l11lll_opy_
        ):
            if bstack1l11lllll1l_opy_ == bstack11111l1ll1_opy_.PRE:
                hub_url = bstack1ll1lllll11_opy_.bstack1l111l11l_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1ll1lllll11_opy_.bstack1l1ll11l1ll_opy_: hub_url,
                            bstack1ll1lllll11_opy_.bstack1l1l111ll1l_opy_: bstack1ll1lllll11_opy_.bstack1ll11ll1ll1_opy_(hub_url),
                            bstack1ll1lllll11_opy_.bstack1ll1ll111ll_opy_: int(
                                os.environ.get(bstack11111ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᓞ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll11ll11ll_opy_ = bstack1ll1lllll11_opy_.bstack1ll11lll11l_opy_(*args)
                bstack1l1111lll1l_opy_ = bstack1ll11ll11ll_opy_.get(bstack11111ll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᓟ"), None) if bstack1ll11ll11ll_opy_ else None
                if isinstance(bstack1l1111lll1l_opy_, dict):
                    instance.data[bstack1ll1lllll11_opy_.bstack1l1111lllll_opy_] = copy.deepcopy(bstack1l1111lll1l_opy_)
                    instance.data[bstack1ll1lllll11_opy_.bstack1l1ll111l1l_opy_] = bstack1l1111lll1l_opy_
            elif bstack1l11lllll1l_opy_ == bstack11111l1ll1_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11111ll_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᓠ"), dict()).get(bstack11111ll_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡎࡪࠢᓡ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1ll1lllll11_opy_.bstack1l1ll11l111_opy_: framework_session_id,
                                bstack1ll1lllll11_opy_.bstack1l1111ll1l1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack11111l1lll_opy_ == bstack1111l11l1l_opy_.bstack1llllllll1l_opy_
            and bstack1ll1lllll11_opy_.bstack1l1l11ll1l1_opy_(*args) == bstack1ll1lllll11_opy_.bstack1l111l111l1_opy_
            and bstack1l11lllll1l_opy_ == bstack11111l1ll1_opy_.POST
        ):
            instance.data[bstack1ll1lllll11_opy_.bstack1l111l11111_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l1l11111l1_opy_ in bstack1ll1lllll11_opy_.bstack1l1111ll1ll_opy_:
            bstack1l1l111111l_opy_ = None
            for callback in bstack1ll1lllll11_opy_.bstack1l1111ll1ll_opy_[bstack1l1l11111l1_opy_]:
                try:
                    bstack1l1l11111ll_opy_ = callback(self, target, exec, bstack11111l111l_opy_, result, *args, **kwargs)
                    if bstack1l1l111111l_opy_ == None:
                        bstack1l1l111111l_opy_ = bstack1l1l11111ll_opy_
                except Exception as e:
                    self.logger.error(bstack11111ll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࠥᓢ") + str(e) + bstack11111ll_opy_ (u"ࠨࠢᓣ"))
                    traceback.print_exc()
            if bstack11111l1lll_opy_ == bstack1111l11l1l_opy_.QUIT:
                if bstack1l11lllll1l_opy_ == bstack11111l1ll1_opy_.POST:
                    bstack1ll1ll1l1ll_opy_ = bstack1111l1l11l_opy_.bstack11111lll1l_opy_(instance, EVENTS.bstack1l11l1lll1_opy_.value)
                    if bstack1ll1ll1l1ll_opy_!=None:
                        bstack1llll111l1l_opy_.end(EVENTS.bstack1l11l1lll1_opy_.value, bstack1ll1ll1l1ll_opy_+bstack11111ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᓤ"), bstack1ll1ll1l1ll_opy_+bstack11111ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᓥ"), True, None)
            if bstack1l11lllll1l_opy_ == bstack11111l1ll1_opy_.PRE and callable(bstack1l1l111111l_opy_):
                return bstack1l1l111111l_opy_
            elif bstack1l11lllll1l_opy_ == bstack11111l1ll1_opy_.POST and bstack1l1l111111l_opy_:
                return bstack1l1l111111l_opy_
    def bstack1llllllll11_opy_(
        self, method_name, previous_state: bstack1111l11l1l_opy_, *args, **kwargs
    ) -> bstack1111l11l1l_opy_:
        if method_name == bstack11111ll_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦᓦ") or method_name == bstack11111ll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᓧ"):
            return bstack1111l11l1l_opy_.bstack1111111l11_opy_
        if method_name == bstack11111ll_opy_ (u"ࠦࡶࡻࡩࡵࠤᓨ"):
            return bstack1111l11l1l_opy_.QUIT
        if method_name == bstack11111ll_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᓩ"):
            if previous_state != bstack1111l11l1l_opy_.NONE:
                bstack1ll1ll1ll11_opy_ = bstack1ll1lllll11_opy_.bstack1l1l11ll1l1_opy_(*args)
                if bstack1ll1ll1ll11_opy_ == bstack1ll1lllll11_opy_.bstack1l1l1l11lll_opy_:
                    return bstack1111l11l1l_opy_.bstack1111111l11_opy_
            return bstack1111l11l1l_opy_.bstack1llllllll1l_opy_
        return bstack1111l11l1l_opy_.NONE