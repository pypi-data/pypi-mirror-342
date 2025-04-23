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
class bstack1lll1l111l1_opy_(bstack1ll1l1l1111_opy_):
    bstack1ll11ll1ll1_opy_ = bstack1ll1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᆬ")
    bstack1lll1l11ll1_opy_ = bstack1ll1l11_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᆭ")
    bstack1lll1l1111l_opy_ = bstack1ll1l11_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧᆮ")
    bstack1lll1l1l1ll_opy_ = bstack1ll1l11_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᆯ")
    bstack1ll11ll1l1l_opy_ = bstack1ll1l11_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤᆰ")
    bstack1ll11lll111_opy_ = bstack1ll1l11_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣᆱ")
    NAME = bstack1ll1l11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᆲ")
    bstack1ll11lll1ll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1l1ll111_opy_: Any
    bstack1ll1l111111_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1ll1l11_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤᆳ"), bstack1ll1l11_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦᆴ"), bstack1ll1l11_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᆵ"), bstack1ll1l11_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦᆶ"), bstack1ll1l11_opy_ (u"ࠨࡤࡪࡵࡳࡥࡹࡩࡨࠣᆷ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1ll1l11l11l_opy_(methods)
    def bstack1ll11lll11l_opy_(self, instance: bstack1111l1lll1_opy_, method_name: str, bstack1ll11lllll1_opy_: timedelta, *args, **kwargs):
        pass
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
        bstack1ll11llllll_opy_ = bstack1lll1l111l1_opy_.bstack1ll11llll11_opy_(bstack111111111l_opy_)
        if bstack1ll11llllll_opy_ in bstack1lll1l111l1_opy_.bstack1ll11lll1ll_opy_:
            bstack1ll11lll1l1_opy_ = None
            for callback in bstack1lll1l111l1_opy_.bstack1ll11lll1ll_opy_[bstack1ll11llllll_opy_]:
                try:
                    bstack1ll1l11l111_opy_ = callback(self, target, exec, bstack111111111l_opy_, result, *args, **kwargs)
                    if bstack1ll11lll1l1_opy_ == None:
                        bstack1ll11lll1l1_opy_ = bstack1ll1l11l111_opy_
                except Exception as e:
                    self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧᆸ") + str(e) + bstack1ll1l11_opy_ (u"ࠣࠤᆹ"))
                    traceback.print_exc()
            if bstack1ll11ll1lll_opy_ == bstack111111ll1l_opy_.PRE and callable(bstack1ll11lll1l1_opy_):
                return bstack1ll11lll1l1_opy_
            elif bstack1ll11ll1lll_opy_ == bstack111111ll1l_opy_.POST and bstack1ll11lll1l1_opy_:
                return bstack1ll11lll1l1_opy_
    def bstack1ll1l11l1l1_opy_(
        self, method_name, previous_state: bstack11111l1lll_opy_, *args, **kwargs
    ) -> bstack11111l1lll_opy_:
        if method_name == bstack1ll1l11_opy_ (u"ࠩ࡯ࡥࡺࡴࡣࡩࠩᆺ") or method_name == bstack1ll1l11_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫᆻ") or method_name == bstack1ll1l11_opy_ (u"ࠫࡳ࡫ࡷࡠࡲࡤ࡫ࡪ࠭ᆼ"):
            return bstack11111l1lll_opy_.bstack1lll11llll1_opy_
        if method_name == bstack1ll1l11_opy_ (u"ࠬࡪࡩࡴࡲࡤࡸࡨ࡮ࠧᆽ"):
            return bstack11111l1lll_opy_.bstack1lll11ll1l1_opy_
        if method_name == bstack1ll1l11_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠬᆾ"):
            return bstack11111l1lll_opy_.QUIT
        return bstack11111l1lll_opy_.NONE
    @staticmethod
    def bstack1ll11llll11_opy_(bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_]):
        return bstack1ll1l11_opy_ (u"ࠢ࠻ࠤᆿ").join((bstack11111l1lll_opy_(bstack111111111l_opy_[0]).name, bstack111111ll1l_opy_(bstack111111111l_opy_[1]).name))
    @staticmethod
    def bstack111111l1l1_opy_(bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_], callback: Callable):
        bstack1ll11llllll_opy_ = bstack1lll1l111l1_opy_.bstack1ll11llll11_opy_(bstack111111111l_opy_)
        if not bstack1ll11llllll_opy_ in bstack1lll1l111l1_opy_.bstack1ll11lll1ll_opy_:
            bstack1lll1l111l1_opy_.bstack1ll11lll1ll_opy_[bstack1ll11llllll_opy_] = []
        bstack1lll1l111l1_opy_.bstack1ll11lll1ll_opy_[bstack1ll11llllll_opy_].append(callback)
    @staticmethod
    def bstack1111l11111_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll1l1ll1ll_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1l1111ll_opy_(instance: bstack1111l1lll1_opy_, default_value=None):
        return bstack1ll1l1l1111_opy_.bstack11111l11l1_opy_(instance, bstack1lll1l111l1_opy_.bstack1lll1l1l1ll_opy_, default_value)
    @staticmethod
    def bstack1ll1l11ll1l_opy_(instance: bstack1111l1lll1_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll1l111ll1_opy_(instance: bstack1111l1lll1_opy_, default_value=None):
        return bstack1ll1l1l1111_opy_.bstack11111l11l1_opy_(instance, bstack1lll1l111l1_opy_.bstack1lll1l1111l_opy_, default_value)
    @staticmethod
    def bstack111111l11l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l111lll_opy_(method_name: str, *args):
        if not bstack1lll1l111l1_opy_.bstack1111l11111_opy_(method_name):
            return False
        if not bstack1lll1l111l1_opy_.bstack1ll11ll1l1l_opy_ in bstack1lll1l111l1_opy_.bstack1ll1ll1l1l1_opy_(*args):
            return False
        bstack1ll1l1111l1_opy_ = bstack1lll1l111l1_opy_.bstack1ll1l11111l_opy_(*args)
        return bstack1ll1l1111l1_opy_ and bstack1ll1l11_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᇀ") in bstack1ll1l1111l1_opy_ and bstack1ll1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᇁ") in bstack1ll1l1111l1_opy_[bstack1ll1l11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᇂ")]
    @staticmethod
    def bstack1ll1l111l1l_opy_(method_name: str, *args):
        if not bstack1lll1l111l1_opy_.bstack1111l11111_opy_(method_name):
            return False
        if not bstack1lll1l111l1_opy_.bstack1ll11ll1l1l_opy_ in bstack1lll1l111l1_opy_.bstack1ll1ll1l1l1_opy_(*args):
            return False
        bstack1ll1l1111l1_opy_ = bstack1lll1l111l1_opy_.bstack1ll1l11111l_opy_(*args)
        return (
            bstack1ll1l1111l1_opy_
            and bstack1ll1l11_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᇃ") in bstack1ll1l1111l1_opy_
            and bstack1ll1l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡦࡶ࡮ࡶࡴࠣᇄ") in bstack1ll1l1111l1_opy_[bstack1ll1l11_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᇅ")]
        )
    @staticmethod
    def bstack1ll1ll1l1l1_opy_(*args):
        return str(bstack1lll1l111l1_opy_.bstack111111l11l_opy_(*args)).lower()