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
from browserstack_sdk.sdk_cli.bstack1llll11l1ll_opy_ import bstack1lllllll11l_opy_
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import (
    bstack1111l11l1l_opy_,
    bstack11111l1ll1_opy_,
    bstack1111l1l11l_opy_,
    bstack1111l1111l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lllll11ll1_opy_ import bstack1ll1lllll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1llll1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1111l11ll1_opy_ import bstack111111l1ll_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1llll11l1ll_opy_ import bstack1lllllll11l_opy_
import weakref
class bstack1ll11l11lll_opy_(bstack1lllllll11l_opy_):
    bstack1ll11l1ll1l_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1111l1111l_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1111l1111l_opy_]]
    def __init__(self, bstack1ll11l1ll1l_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1ll11l1l11l_opy_ = dict()
        self.bstack1ll11l1ll1l_opy_ = bstack1ll11l1ll1l_opy_
        self.frameworks = frameworks
        bstack1llll1ll1ll_opy_.bstack1ll1ll11l11_opy_((bstack1111l11l1l_opy_.bstack1111111l11_opy_, bstack11111l1ll1_opy_.POST), self.__1ll11l111ll_opy_)
        if any(bstack1ll1lllll11_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll1lllll11_opy_.bstack1ll1ll11l11_opy_(
                (bstack1111l11l1l_opy_.bstack1llllllll1l_opy_, bstack11111l1ll1_opy_.PRE), self.__1ll11l11ll1_opy_
            )
            bstack1ll1lllll11_opy_.bstack1ll1ll11l11_opy_(
                (bstack1111l11l1l_opy_.QUIT, bstack11111l1ll1_opy_.POST), self.__1ll11l1l1ll_opy_
            )
    def __1ll11l111ll_opy_(
        self,
        f: bstack1llll1ll1ll_opy_,
        bstack1ll11l1llll_opy_: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack11111ll_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᆠ"):
                return
            contexts = bstack1ll11l1llll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11111ll_opy_ (u"ࠧࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠥᆡ") in page.url:
                                self.logger.debug(bstack11111ll_opy_ (u"ࠨࡓࡵࡱࡵ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡳ࡫ࡷࠡࡲࡤ࡫ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠣᆢ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1111l1l11l_opy_.bstack11111l11ll_opy_(instance, self.bstack1ll11l1ll1l_opy_, True)
                                self.logger.debug(bstack11111ll_opy_ (u"ࠢࡠࡡࡲࡲࡤࡶࡡࡨࡧࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᆣ") + str(instance.ref()) + bstack11111ll_opy_ (u"ࠣࠤᆤ"))
        except Exception as e:
            self.logger.debug(bstack11111ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࠿ࠨᆥ"),e)
    def __1ll11l11ll1_opy_(
        self,
        f: bstack1ll1lllll11_opy_,
        driver: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1111l1l11l_opy_.bstack11111lll1l_opy_(instance, self.bstack1ll11l1ll1l_opy_, False):
            return
        if not f.bstack1ll11ll1ll1_opy_(f.hub_url(driver)):
            self.bstack1ll11l1l11l_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1111l1l11l_opy_.bstack11111l11ll_opy_(instance, self.bstack1ll11l1ll1l_opy_, True)
            self.logger.debug(bstack11111ll_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᆦ") + str(instance.ref()) + bstack11111ll_opy_ (u"ࠦࠧᆧ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1111l1l11l_opy_.bstack11111l11ll_opy_(instance, self.bstack1ll11l1ll1l_opy_, True)
        self.logger.debug(bstack11111ll_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᆨ") + str(instance.ref()) + bstack11111ll_opy_ (u"ࠨࠢᆩ"))
    def __1ll11l1l1ll_opy_(
        self,
        f: bstack1ll1lllll11_opy_,
        driver: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll11l11l11_opy_(instance)
        self.logger.debug(bstack11111ll_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡲࡷ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᆪ") + str(instance.ref()) + bstack11111ll_opy_ (u"ࠣࠤᆫ"))
    def bstack1ll11l1lll1_opy_(self, context: bstack111111l1ll_opy_, reverse=True) -> List[Tuple[Callable, bstack1111l1111l_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll11l11l1l_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll1lllll11_opy_.bstack1ll1l1l1ll1_opy_(data[1])
                    and data[1].bstack1ll11l11l1l_opy_(context)
                    and getattr(data[0](), bstack11111ll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᆬ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1111l1l111_opy_, reverse=reverse)
    def bstack1ll11l1ll11_opy_(self, context: bstack111111l1ll_opy_, reverse=True) -> List[Tuple[Callable, bstack1111l1111l_opy_]]:
        matches = []
        for data in self.bstack1ll11l1l11l_opy_.values():
            if (
                data[1].bstack1ll11l11l1l_opy_(context)
                and getattr(data[0](), bstack11111ll_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᆭ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1111l1l111_opy_, reverse=reverse)
    def bstack1ll11l1l111_opy_(self, instance: bstack1111l1111l_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll11l11l11_opy_(self, instance: bstack1111l1111l_opy_) -> bool:
        if self.bstack1ll11l1l111_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1111l1l11l_opy_.bstack11111l11ll_opy_(instance, self.bstack1ll11l1ll1l_opy_, False)
            return True
        return False