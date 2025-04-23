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
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll11l1ll_opy_ import bstack1lllllll11l_opy_
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import (
    bstack1111l11l1l_opy_,
    bstack11111l1ll1_opy_,
    bstack1111l1111l_opy_,
)
from bstack_utils.helper import  bstack1l1llll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll11ll1_opy_ import bstack1ll1lllll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll1l11ll_opy_, bstack1lll1l1l1l1_opy_, bstack1llllll1l11_opy_, bstack1ll1lllllll_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11ll111ll_opy_ import bstack1111l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lll11_opy_ import bstack1llll11llll_opy_
from bstack_utils.percy import bstack1l111l1l11_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll1l1ll11_opy_(bstack1lllllll11l_opy_):
    def __init__(self, bstack1l1ll1lll1l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1ll1lll1l_opy_ = bstack1l1ll1lll1l_opy_
        self.percy = bstack1l111l1l11_opy_()
        self.bstack11llll11l1_opy_ = bstack1111l11l1_opy_()
        self.bstack1l1ll1ll1ll_opy_()
        bstack1ll1lllll11_opy_.bstack1ll1ll11l11_opy_((bstack1111l11l1l_opy_.bstack1llllllll1l_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1l1ll1lll11_opy_)
        TestFramework.bstack1ll1ll11l11_opy_((bstack1llll1l11ll_opy_.TEST, bstack1llllll1l11_opy_.POST), self.bstack1ll1l1ll1l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll1l1l1_opy_(self, instance: bstack1111l1111l_opy_, driver: object):
        bstack1ll1111lll1_opy_ = TestFramework.bstack111111l1l1_opy_(instance.context)
        for t in bstack1ll1111lll1_opy_:
            bstack1ll111l1111_opy_ = TestFramework.bstack11111lll1l_opy_(t, bstack1llll11llll_opy_.bstack1ll111l1l11_opy_, [])
            if any(instance is d[1] for d in bstack1ll111l1111_opy_) or instance == driver:
                return t
    def bstack1l1ll1lll11_opy_(
        self,
        f: bstack1ll1lllll11_opy_,
        driver: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll1lllll11_opy_.bstack1ll1l1l11l1_opy_(method_name):
                return
            platform_index = f.bstack11111lll1l_opy_(instance, bstack1ll1lllll11_opy_.bstack1ll1ll111ll_opy_, 0)
            bstack1l1llll11l1_opy_ = self.bstack1l1lll1l1l1_opy_(instance, driver)
            bstack1l1ll1l11ll_opy_ = TestFramework.bstack11111lll1l_opy_(bstack1l1llll11l1_opy_, TestFramework.bstack1l1ll1ll111_opy_, None)
            if not bstack1l1ll1l11ll_opy_:
                self.logger.debug(bstack11111ll_opy_ (u"ࠤࡲࡲࡤࡶࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡷ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡢࡵࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡾ࡫ࡴࠡࡵࡷࡥࡷࡺࡥࡥࠤሪ"))
                return
            driver_command = f.bstack1ll11llll1l_opy_(*args)
            for command in bstack1l1ll111ll_opy_:
                if command == driver_command:
                    self.bstack1l1ll11lll_opy_(driver, platform_index)
            bstack11l1lllll_opy_ = self.percy.bstack1ll111l1ll_opy_()
            if driver_command in bstack1l111l111_opy_[bstack11l1lllll_opy_]:
                self.bstack11llll11l1_opy_.bstack11l1llll1_opy_(bstack1l1ll1l11ll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥ࡫ࡲࡳࡱࡵࠦራ"), e)
    def bstack1ll1l1ll1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll111l1l_opy_
        bstack1ll111l1111_opy_ = f.bstack11111lll1l_opy_(instance, bstack1llll11llll_opy_.bstack1ll111l1l11_opy_, [])
        if not bstack1ll111l1111_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨሬ") + str(kwargs) + bstack11111ll_opy_ (u"ࠧࠨር"))
            return
        if len(bstack1ll111l1111_opy_) > 1:
            self.logger.debug(bstack11111ll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣሮ") + str(kwargs) + bstack11111ll_opy_ (u"ࠢࠣሯ"))
        bstack1l1ll1ll11l_opy_, bstack1l1ll1l1ll1_opy_ = bstack1ll111l1111_opy_[0]
        driver = bstack1l1ll1ll11l_opy_()
        if not driver:
            self.logger.debug(bstack11111ll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤሰ") + str(kwargs) + bstack11111ll_opy_ (u"ࠤࠥሱ"))
            return
        bstack1l1ll1llll1_opy_ = {
            TestFramework.bstack1ll1lll111l_opy_: bstack11111ll_opy_ (u"ࠥࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨሲ"),
            TestFramework.bstack1ll1ll1lll1_opy_: bstack11111ll_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡸࡹ࡮ࡪࠢሳ"),
            TestFramework.bstack1l1ll1ll111_opy_: bstack11111ll_opy_ (u"ࠧࡺࡥࡴࡶࠣࡶࡪࡸࡵ࡯ࠢࡱࡥࡲ࡫ࠢሴ")
        }
        bstack1l1ll1ll1l1_opy_ = { key: f.bstack11111lll1l_opy_(instance, key) for key in bstack1l1ll1llll1_opy_ }
        bstack1l1ll1l11l1_opy_ = [key for key, value in bstack1l1ll1ll1l1_opy_.items() if not value]
        if bstack1l1ll1l11l1_opy_:
            for key in bstack1l1ll1l11l1_opy_:
                self.logger.debug(bstack11111ll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠤስ") + str(key) + bstack11111ll_opy_ (u"ࠢࠣሶ"))
            return
        platform_index = f.bstack11111lll1l_opy_(instance, bstack1ll1lllll11_opy_.bstack1ll1ll111ll_opy_, 0)
        if self.bstack1l1ll1lll1l_opy_.percy_capture_mode == bstack11111ll_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥሷ"):
            bstack1111111l1_opy_ = bstack1l1ll1ll1l1_opy_.get(TestFramework.bstack1l1ll1ll111_opy_) + bstack11111ll_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧሸ")
            bstack1ll1ll1l1ll_opy_ = bstack1llll111l1l_opy_.bstack1ll1l111lll_opy_(EVENTS.bstack1l1ll1l1lll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1111111l1_opy_,
                bstack1l1ll1l1l1_opy_=bstack1l1ll1ll1l1_opy_[TestFramework.bstack1ll1lll111l_opy_],
                bstack11111111_opy_=bstack1l1ll1ll1l1_opy_[TestFramework.bstack1ll1ll1lll1_opy_],
                bstack1ll111ll11_opy_=platform_index
            )
            bstack1llll111l1l_opy_.end(EVENTS.bstack1l1ll1l1lll_opy_.value, bstack1ll1ll1l1ll_opy_+bstack11111ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥሹ"), bstack1ll1ll1l1ll_opy_+bstack11111ll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤሺ"), True, None, None, None, None, test_name=bstack1111111l1_opy_)
    def bstack1l1ll11lll_opy_(self, driver, platform_index):
        if self.bstack11llll11l1_opy_.bstack11l1ll11l1_opy_() is True or self.bstack11llll11l1_opy_.capturing() is True:
            return
        self.bstack11llll11l1_opy_.bstack11l111ll_opy_()
        while not self.bstack11llll11l1_opy_.bstack11l1ll11l1_opy_():
            bstack1l1ll1l11ll_opy_ = self.bstack11llll11l1_opy_.bstack1llll11lll_opy_()
            self.bstack11llll1l1_opy_(driver, bstack1l1ll1l11ll_opy_, platform_index)
        self.bstack11llll11l1_opy_.bstack11l1lllll1_opy_()
    def bstack11llll1l1_opy_(self, driver, bstack1l1ll1ll1l_opy_, platform_index, test=None):
        from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll111l1l_opy_
        bstack1ll1ll1l1ll_opy_ = bstack1llll111l1l_opy_.bstack1ll1l111lll_opy_(EVENTS.bstack1lll111l1_opy_.value)
        if test != None:
            bstack1l1ll1l1l1_opy_ = getattr(test, bstack11111ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪሻ"), None)
            bstack11111111_opy_ = getattr(test, bstack11111ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫሼ"), None)
            PercySDK.screenshot(driver, bstack1l1ll1ll1l_opy_, bstack1l1ll1l1l1_opy_=bstack1l1ll1l1l1_opy_, bstack11111111_opy_=bstack11111111_opy_, bstack1ll111ll11_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1l1ll1ll1l_opy_)
        bstack1llll111l1l_opy_.end(EVENTS.bstack1lll111l1_opy_.value, bstack1ll1ll1l1ll_opy_+bstack11111ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢሽ"), bstack1ll1ll1l1ll_opy_+bstack11111ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨሾ"), True, None, None, None, None, test_name=bstack1l1ll1ll1l_opy_)
    def bstack1l1ll1ll1ll_opy_(self):
        os.environ[bstack11111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧሿ")] = str(self.bstack1l1ll1lll1l_opy_.success)
        os.environ[bstack11111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧቀ")] = str(self.bstack1l1ll1lll1l_opy_.percy_capture_mode)
        self.percy.bstack1l1ll1l1l1l_opy_(self.bstack1l1ll1lll1l_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1ll1l1l11_opy_(self.bstack1l1ll1lll1l_opy_.percy_build_id)