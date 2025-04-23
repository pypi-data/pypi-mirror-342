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
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack11111lllll_opy_
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack11111l1lll_opy_,
    bstack111111ll1l_opy_,
    bstack1ll1l1l1111_opy_,
    bstack1111l1lll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import bstack1111111ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11lll_opy_ import bstack1lll1l111l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll111lll1l_opy_ import bstack1lll11l1ll1_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack11111lllll_opy_
import weakref
class bstack1lll111lll1_opy_(bstack11111lllll_opy_):
    bstack1lll11l11ll_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1111l1lll1_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1111l1lll1_opy_]]
    def __init__(self, bstack1lll11l11ll_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1111ll1l1_opy_ = dict()
        self.bstack1lll11l11ll_opy_ = bstack1lll11l11ll_opy_
        self.frameworks = frameworks
        bstack1lll1l111l1_opy_.bstack111111l1l1_opy_((bstack11111l1lll_opy_.bstack1lll11llll1_opy_, bstack111111ll1l_opy_.POST), self.__1l1111ll11l_opy_)
        if any(bstack1111111ll1_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1111111ll1_opy_.bstack111111l1l1_opy_(
                (bstack11111l1lll_opy_.bstack1111l1l1l1_opy_, bstack111111ll1l_opy_.PRE), self.__1l1111lll11_opy_
            )
            bstack1111111ll1_opy_.bstack111111l1l1_opy_(
                (bstack11111l1lll_opy_.QUIT, bstack111111ll1l_opy_.POST), self.__1l1111ll111_opy_
            )
    def __1l1111ll11l_opy_(
        self,
        f: bstack1lll1l111l1_opy_,
        bstack1lll1l1llll_opy_: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1ll1l11_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣᔍ"):
                return
            contexts = bstack1lll1l1llll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1ll1l11_opy_ (u"ࠢࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠧᔎ") in page.url:
                                self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡕࡷࡳࡷ࡯࡮ࡨࠢࡷ࡬ࡪࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠥᔏ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1ll1l1l1111_opy_.bstack1lllllll1l1_opy_(instance, self.bstack1lll11l11ll_opy_, True)
                                self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡱࡣࡪࡩࡤ࡯࡮ࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᔐ") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠥࠦᔑ"))
        except Exception as e:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡲࡪࡰࡪࠤࡳ࡫ࡷࠡࡲࡤ࡫ࡪࠦ࠺ࠣᔒ"),e)
    def __1l1111lll11_opy_(
        self,
        f: bstack1111111ll1_opy_,
        driver: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1ll1l1l1111_opy_.bstack11111l11l1_opy_(instance, self.bstack1lll11l11ll_opy_, False):
            return
        if not f.bstack1l1ll11l1ll_opy_(f.hub_url(driver)):
            self.bstack1l1111ll1l1_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1ll1l1l1111_opy_.bstack1lllllll1l1_opy_(instance, self.bstack1lll11l11ll_opy_, True)
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡥࡴ࡬ࡺࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᔓ") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠨࠢᔔ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1ll1l1l1111_opy_.bstack1lllllll1l1_opy_(instance, self.bstack1lll11l11ll_opy_, True)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᔕ") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠣࠤᔖ"))
    def __1l1111ll111_opy_(
        self,
        f: bstack1111111ll1_opy_,
        driver: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l1111ll1ll_opy_(instance)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡴࡹ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᔗ") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠥࠦᔘ"))
    def bstack1lll111l1l1_opy_(self, context: bstack1lll11l1ll1_opy_, reverse=True) -> List[Tuple[Callable, bstack1111l1lll1_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l1l1llllll_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1111111ll1_opy_.bstack1ll1l11ll1l_opy_(data[1])
                    and data[1].bstack1l1l1llllll_opy_(context)
                    and getattr(data[0](), bstack1ll1l11_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᔙ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1l1ll111lll_opy_, reverse=reverse)
    def bstack1lll111l11l_opy_(self, context: bstack1lll11l1ll1_opy_, reverse=True) -> List[Tuple[Callable, bstack1111l1lll1_opy_]]:
        matches = []
        for data in self.bstack1l1111ll1l1_opy_.values():
            if (
                data[1].bstack1l1l1llllll_opy_(context)
                and getattr(data[0](), bstack1ll1l11_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᔚ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1l1ll111lll_opy_, reverse=reverse)
    def bstack1l1111l1lll_opy_(self, instance: bstack1111l1lll1_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l1111ll1ll_opy_(self, instance: bstack1111l1lll1_opy_) -> bool:
        if self.bstack1l1111l1lll_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1ll1l1l1111_opy_.bstack1lllllll1l1_opy_(instance, self.bstack1lll11l11ll_opy_, False)
            return True
        return False