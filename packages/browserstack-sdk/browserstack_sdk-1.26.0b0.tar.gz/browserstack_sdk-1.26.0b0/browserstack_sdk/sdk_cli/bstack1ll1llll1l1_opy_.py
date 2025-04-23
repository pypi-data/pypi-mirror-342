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
class bstack1llll1ll1ll_opy_(bstack1111l1l11l_opy_):
    bstack1l11llllll1_opy_ = bstack11111ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣፈ")
    bstack1l1ll11l111_opy_ = bstack11111ll_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤፉ")
    bstack1l1ll11l1ll_opy_ = bstack11111ll_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࠦፊ")
    bstack1l1ll111l1l_opy_ = bstack11111ll_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥፋ")
    bstack1l11lllll11_opy_ = bstack11111ll_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࠣፌ")
    bstack1l1l1111l1l_opy_ = bstack11111ll_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࡣࡶࡽࡳࡩࠢፍ")
    NAME = bstack11111ll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦፎ")
    bstack1l1l1111111_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll111ll11_opy_: Any
    bstack1l11lllllll_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11111ll_opy_ (u"ࠣ࡮ࡤࡹࡳࡩࡨࠣፏ"), bstack11111ll_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࠥፐ"), bstack11111ll_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧፑ"), bstack11111ll_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࠥፒ"), bstack11111ll_opy_ (u"ࠧࡪࡩࡴࡲࡤࡸࡨ࡮ࠢፓ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1111111111_opy_(methods)
    def bstack11111l11l1_opy_(self, instance: bstack1111l1111l_opy_, method_name: str, bstack1111l11lll_opy_: timedelta, *args, **kwargs):
        pass
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
        bstack1l1l11111l1_opy_ = bstack1llll1ll1ll_opy_.bstack1l1l1111l11_opy_(bstack11111l111l_opy_)
        if bstack1l1l11111l1_opy_ in bstack1llll1ll1ll_opy_.bstack1l1l1111111_opy_:
            bstack1l1l111111l_opy_ = None
            for callback in bstack1llll1ll1ll_opy_.bstack1l1l1111111_opy_[bstack1l1l11111l1_opy_]:
                try:
                    bstack1l1l11111ll_opy_ = callback(self, target, exec, bstack11111l111l_opy_, result, *args, **kwargs)
                    if bstack1l1l111111l_opy_ == None:
                        bstack1l1l111111l_opy_ = bstack1l1l11111ll_opy_
                except Exception as e:
                    self.logger.error(bstack11111ll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࠦፔ") + str(e) + bstack11111ll_opy_ (u"ࠢࠣፕ"))
                    traceback.print_exc()
            if bstack1l11lllll1l_opy_ == bstack11111l1ll1_opy_.PRE and callable(bstack1l1l111111l_opy_):
                return bstack1l1l111111l_opy_
            elif bstack1l11lllll1l_opy_ == bstack11111l1ll1_opy_.POST and bstack1l1l111111l_opy_:
                return bstack1l1l111111l_opy_
    def bstack1llllllll11_opy_(
        self, method_name, previous_state: bstack1111l11l1l_opy_, *args, **kwargs
    ) -> bstack1111l11l1l_opy_:
        if method_name == bstack11111ll_opy_ (u"ࠨ࡮ࡤࡹࡳࡩࡨࠨፖ") or method_name == bstack11111ll_opy_ (u"ࠩࡦࡳࡳࡴࡥࡤࡶࠪፗ") or method_name == bstack11111ll_opy_ (u"ࠪࡲࡪࡽ࡟ࡱࡣࡪࡩࠬፘ"):
            return bstack1111l11l1l_opy_.bstack1111111l11_opy_
        if method_name == bstack11111ll_opy_ (u"ࠫࡩ࡯ࡳࡱࡣࡷࡧ࡭࠭ፙ"):
            return bstack1111l11l1l_opy_.bstack1lllllllll1_opy_
        if method_name == bstack11111ll_opy_ (u"ࠬࡩ࡬ࡰࡵࡨࠫፚ"):
            return bstack1111l11l1l_opy_.QUIT
        return bstack1111l11l1l_opy_.NONE
    @staticmethod
    def bstack1l1l1111l11_opy_(bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_]):
        return bstack11111ll_opy_ (u"ࠨ࠺ࠣ፛").join((bstack1111l11l1l_opy_(bstack11111l111l_opy_[0]).name, bstack11111l1ll1_opy_(bstack11111l111l_opy_[1]).name))
    @staticmethod
    def bstack1ll1ll11l11_opy_(bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_], callback: Callable):
        bstack1l1l11111l1_opy_ = bstack1llll1ll1ll_opy_.bstack1l1l1111l11_opy_(bstack11111l111l_opy_)
        if not bstack1l1l11111l1_opy_ in bstack1llll1ll1ll_opy_.bstack1l1l1111111_opy_:
            bstack1llll1ll1ll_opy_.bstack1l1l1111111_opy_[bstack1l1l11111l1_opy_] = []
        bstack1llll1ll1ll_opy_.bstack1l1l1111111_opy_[bstack1l1l11111l1_opy_].append(callback)
    @staticmethod
    def bstack1ll1l1l11l1_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll1l1l1111_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1ll1l11l_opy_(instance: bstack1111l1111l_opy_, default_value=None):
        return bstack1111l1l11l_opy_.bstack11111lll1l_opy_(instance, bstack1llll1ll1ll_opy_.bstack1l1ll111l1l_opy_, default_value)
    @staticmethod
    def bstack1ll1l1l1ll1_opy_(instance: bstack1111l1111l_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll1l111l11_opy_(instance: bstack1111l1111l_opy_, default_value=None):
        return bstack1111l1l11l_opy_.bstack11111lll1l_opy_(instance, bstack1llll1ll1ll_opy_.bstack1l1ll11l1ll_opy_, default_value)
    @staticmethod
    def bstack1ll11llll1l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11llll11_opy_(method_name: str, *args):
        if not bstack1llll1ll1ll_opy_.bstack1ll1l1l11l1_opy_(method_name):
            return False
        if not bstack1llll1ll1ll_opy_.bstack1l11lllll11_opy_ in bstack1llll1ll1ll_opy_.bstack1l1l11ll1l1_opy_(*args):
            return False
        bstack1ll11ll11ll_opy_ = bstack1llll1ll1ll_opy_.bstack1ll11lll11l_opy_(*args)
        return bstack1ll11ll11ll_opy_ and bstack11111ll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢ፜") in bstack1ll11ll11ll_opy_ and bstack11111ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤ፝") in bstack1ll11ll11ll_opy_[bstack11111ll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤ፞")]
    @staticmethod
    def bstack1ll11lll1ll_opy_(method_name: str, *args):
        if not bstack1llll1ll1ll_opy_.bstack1ll1l1l11l1_opy_(method_name):
            return False
        if not bstack1llll1ll1ll_opy_.bstack1l11lllll11_opy_ in bstack1llll1ll1ll_opy_.bstack1l1l11ll1l1_opy_(*args):
            return False
        bstack1ll11ll11ll_opy_ = bstack1llll1ll1ll_opy_.bstack1ll11lll11l_opy_(*args)
        return (
            bstack1ll11ll11ll_opy_
            and bstack11111ll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥ፟") in bstack1ll11ll11ll_opy_
            and bstack11111ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡥࡵ࡭ࡵࡺࠢ፠") in bstack1ll11ll11ll_opy_[bstack11111ll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ፡")]
        )
    @staticmethod
    def bstack1l1l11ll1l1_opy_(*args):
        return str(bstack1llll1ll1ll_opy_.bstack1ll11llll1l_opy_(*args)).lower()