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
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack11111lllll_opy_
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack11111l1lll_opy_,
    bstack111111ll1l_opy_,
    bstack1111l1lll1_opy_,
)
from bstack_utils.helper import  bstack11ll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import bstack1111111ll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack11111ll1l1_opy_, bstack11111l111l_opy_, bstack1111111l1l_opy_, bstack111111llll_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1lll1l1ll_opy_ import bstack1ll111111_opy_
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import bstack1111l11lll_opy_
from bstack_utils.percy import bstack111l111l_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack111111ll11_opy_(bstack11111lllll_opy_):
    def __init__(self, bstack11111ll1ll_opy_: Dict[str, str]):
        super().__init__()
        self.bstack11111ll1ll_opy_ = bstack11111ll1ll_opy_
        self.percy = bstack111l111l_opy_()
        self.bstack111ll1l1l_opy_ = bstack1ll111111_opy_()
        self.bstack1111l1llll_opy_()
        bstack1111111ll1_opy_.bstack111111l1l1_opy_((bstack11111l1lll_opy_.bstack1111l1l1l1_opy_, bstack111111ll1l_opy_.PRE), self.bstack11111llll1_opy_)
        TestFramework.bstack111111l1l1_opy_((bstack11111ll1l1_opy_.TEST, bstack1111111l1l_opy_.POST), self.bstack1111111l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11111lll11_opy_(self, instance: bstack1111l1lll1_opy_, driver: object):
        bstack1111111lll_opy_ = TestFramework.bstack1111l1ll1l_opy_(instance.context)
        for t in bstack1111111lll_opy_:
            bstack11111ll11l_opy_ = TestFramework.bstack11111l11l1_opy_(t, bstack1111l11lll_opy_.bstack1111l1l11l_opy_, [])
            if any(instance is d[1] for d in bstack11111ll11l_opy_) or instance == driver:
                return t
    def bstack11111llll1_opy_(
        self,
        f: bstack1111111ll1_opy_,
        driver: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1111111ll1_opy_.bstack1111l11111_opy_(method_name):
                return
            platform_index = f.bstack11111l11l1_opy_(instance, bstack1111111ll1_opy_.bstack1111l11ll1_opy_, 0)
            bstack1111l1ll11_opy_ = self.bstack11111lll11_opy_(instance, driver)
            bstack1111l11l1l_opy_ = TestFramework.bstack11111l11l1_opy_(bstack1111l1ll11_opy_, TestFramework.bstack11111lll1l_opy_, None)
            if not bstack1111l11l1l_opy_:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡵ࡮ࡠࡲࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡳࡧࡷࡹࡷࡴࡩ࡯ࡩࠣࡥࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡪࡵࠣࡲࡴࡺࠠࡺࡧࡷࠤࡸࡺࡡࡳࡶࡨࡨࠧဒ"))
                return
            driver_command = f.bstack111111l11l_opy_(*args)
            for command in bstack1ll11ll1_opy_:
                if command == driver_command:
                    self.bstack1l111l1l_opy_(driver, platform_index)
            bstack1l1lllll11_opy_ = self.percy.bstack111llll11_opy_()
            if driver_command in bstack1lll11ll_opy_[bstack1l1lllll11_opy_]:
                self.bstack111ll1l1l_opy_.bstack111111111_opy_(bstack1111l11l1l_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠨ࡯࡯ࡡࡳࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡧࡵࡶࡴࡸࠢဓ"), e)
    def bstack1111111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll11l1lll_opy_ import bstack111111lll1_opy_
        bstack11111ll11l_opy_ = f.bstack11111l11l1_opy_(instance, bstack1111l11lll_opy_.bstack1111l1l11l_opy_, [])
        if not bstack11111ll11l_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤန") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠣࠤပ"))
            return
        if len(bstack11111ll11l_opy_) > 1:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦဖ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠥࠦဗ"))
        bstack11111111l1_opy_, bstack11111l1l1l_opy_ = bstack11111ll11l_opy_[0]
        driver = bstack11111111l1_opy_()
        if not driver:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧဘ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠧࠨမ"))
            return
        bstack11111ll111_opy_ = {
            TestFramework.bstack1111l111ll_opy_: bstack1ll1l11_opy_ (u"ࠨࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤယ"),
            TestFramework.bstack11111111ll_opy_: bstack1ll1l11_opy_ (u"ࠢࡵࡧࡶࡸࠥࡻࡵࡪࡦࠥရ"),
            TestFramework.bstack11111lll1l_opy_: bstack1ll1l11_opy_ (u"ࠣࡶࡨࡷࡹࠦࡲࡦࡴࡸࡲࠥࡴࡡ࡮ࡧࠥလ")
        }
        bstack11111l1ll1_opy_ = { key: f.bstack11111l11l1_opy_(instance, key) for key in bstack11111ll111_opy_ }
        bstack1111l1l1ll_opy_ = [key for key, value in bstack11111l1ll1_opy_.items() if not value]
        if bstack1111l1l1ll_opy_:
            for key in bstack1111l1l1ll_opy_:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࠧဝ") + str(key) + bstack1ll1l11_opy_ (u"ࠥࠦသ"))
            return
        platform_index = f.bstack11111l11l1_opy_(instance, bstack1111111ll1_opy_.bstack1111l11ll1_opy_, 0)
        if self.bstack11111ll1ll_opy_.percy_capture_mode == bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨဟ"):
            bstack1ll1l111_opy_ = bstack11111l1ll1_opy_.get(TestFramework.bstack11111lll1l_opy_) + bstack1ll1l11_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣဠ")
            bstack11111l11ll_opy_ = bstack111111lll1_opy_.bstack11111l1111_opy_(EVENTS.bstack1111l111l1_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1ll1l111_opy_,
                bstack1l1111ll1l_opy_=bstack11111l1ll1_opy_[TestFramework.bstack1111l111ll_opy_],
                bstack1lllll1111_opy_=bstack11111l1ll1_opy_[TestFramework.bstack11111111ll_opy_],
                bstack1ll11lll_opy_=platform_index
            )
            bstack111111lll1_opy_.end(EVENTS.bstack1111l111l1_opy_.value, bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨအ"), bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧဢ"), True, None, None, None, None, test_name=bstack1ll1l111_opy_)
    def bstack1l111l1l_opy_(self, driver, platform_index):
        if self.bstack111ll1l1l_opy_.bstack11l1l1lll1_opy_() is True or self.bstack111ll1l1l_opy_.capturing() is True:
            return
        self.bstack111ll1l1l_opy_.bstack1lll1l1l1_opy_()
        while not self.bstack111ll1l1l_opy_.bstack11l1l1lll1_opy_():
            bstack1111l11l1l_opy_ = self.bstack111ll1l1l_opy_.bstack11l1lll11_opy_()
            self.bstack11llll1l_opy_(driver, bstack1111l11l1l_opy_, platform_index)
        self.bstack111ll1l1l_opy_.bstack1llllll11l_opy_()
    def bstack11llll1l_opy_(self, driver, bstack1ll11l1l1_opy_, platform_index, test=None):
        from bstack_utils.bstack1ll11l1lll_opy_ import bstack111111lll1_opy_
        bstack11111l11ll_opy_ = bstack111111lll1_opy_.bstack11111l1111_opy_(EVENTS.bstack1ll1111l_opy_.value)
        if test != None:
            bstack1l1111ll1l_opy_ = getattr(test, bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ဣ"), None)
            bstack1lllll1111_opy_ = getattr(test, bstack1ll1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧဤ"), None)
            PercySDK.screenshot(driver, bstack1ll11l1l1_opy_, bstack1l1111ll1l_opy_=bstack1l1111ll1l_opy_, bstack1lllll1111_opy_=bstack1lllll1111_opy_, bstack1ll11lll_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1ll11l1l1_opy_)
        bstack111111lll1_opy_.end(EVENTS.bstack1ll1111l_opy_.value, bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥဥ"), bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤဦ"), True, None, None, None, None, test_name=bstack1ll11l1l1_opy_)
    def bstack1111l1llll_opy_(self):
        os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪဧ")] = str(self.bstack11111ll1ll_opy_.success)
        os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪဨ")] = str(self.bstack11111ll1ll_opy_.percy_capture_mode)
        self.percy.bstack111111l111_opy_(self.bstack11111ll1ll_opy_.is_percy_auto_enabled)
        self.percy.bstack1111l1l111_opy_(self.bstack11111ll1ll_opy_.percy_build_id)