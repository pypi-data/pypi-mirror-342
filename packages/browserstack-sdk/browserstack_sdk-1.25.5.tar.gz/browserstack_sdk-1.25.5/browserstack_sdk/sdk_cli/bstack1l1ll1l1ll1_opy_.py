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
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll111lll1l_opy_ import bstack1l1lll1ll11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1111l1l1_opy_ import bstack1l1llll11l1_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack11111ll1l1_opy_,
    bstack11111l111l_opy_,
    bstack1111111l1l_opy_,
    bstack1ll11l11111_opy_,
    bstack111111llll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1llllll111l_opy_
from bstack_utils.bstack1ll11l1lll_opy_ import bstack111111lll1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1llll11l111_opy_ import bstack1ll111ll1ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1111111l_opy_ import bstack1ll1111l1ll_opy_
from bstack_utils.bstack11l1111l1l_opy_ import bstack1lll111111_opy_
bstack1lllll1lll1_opy_ = bstack1llllll111l_opy_()
bstack1ll11l1l11l_opy_ = 1.0
bstack1lllllll1ll_opy_ = bstack1ll1l11_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧቺ")
bstack1l1ll1ll111_opy_ = bstack1ll1l11_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤቻ")
bstack1l1ll1l1l1l_opy_ = bstack1ll1l11_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦቼ")
bstack1l1ll1l1lll_opy_ = bstack1ll1l11_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦች")
bstack1l1ll1ll1ll_opy_ = bstack1ll1l11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣቾ")
_1lll1lll11l_opy_ = set()
class bstack1l1ll1ll11l_opy_(TestFramework):
    bstack1l1llllll11_opy_ = bstack1ll1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥቿ")
    bstack1ll111111ll_opy_ = bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤኀ")
    bstack1l1lll1ll1l_opy_ = bstack1ll1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦኁ")
    bstack1ll11l1lll1_opy_ = bstack1ll1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣኂ")
    bstack1l1lll11111_opy_ = bstack1ll1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥኃ")
    bstack1ll11l1ll11_opy_: bool
    bstack1llll11l111_opy_: bstack1ll111ll1ll_opy_  = None
    bstack1llll111lll_opy_ = None
    bstack1ll11ll1111_opy_ = [
        bstack11111ll1l1_opy_.BEFORE_ALL,
        bstack11111ll1l1_opy_.AFTER_ALL,
        bstack11111ll1l1_opy_.BEFORE_EACH,
        bstack11111ll1l1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1ll111ll111_opy_: Dict[str, str],
        bstack1l1lll11l1l_opy_: List[str]=[bstack1ll1l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣኄ")],
        bstack1llll11l111_opy_: bstack1ll111ll1ll_opy_=None,
        bstack1llll111lll_opy_=None
    ):
        super().__init__(bstack1l1lll11l1l_opy_, bstack1ll111ll111_opy_, bstack1llll11l111_opy_)
        self.bstack1ll11l1ll11_opy_ = any(bstack1ll1l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤኅ") in item.lower() for item in bstack1l1lll11l1l_opy_)
        self.bstack1llll111lll_opy_ = bstack1llll111lll_opy_
    def track_event(
        self,
        context: bstack1ll11l11111_opy_,
        test_framework_state: bstack11111ll1l1_opy_,
        test_hook_state: bstack1111111l1l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack11111ll1l1_opy_.TEST or test_framework_state in bstack1l1ll1ll11l_opy_.bstack1ll11ll1111_opy_:
            bstack1l1llll11l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack11111ll1l1_opy_.NONE:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦኆ") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠦࠧኇ"))
            return
        if not self.bstack1ll11l1ll11_opy_:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨኈ") + str(str(self.bstack1l1lll11l1l_opy_)) + bstack1ll1l11_opy_ (u"ࠨࠢ኉"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤኊ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠣࠤኋ"))
            return
        instance = self.__1ll111lll11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣኌ") + str(args) + bstack1ll1l11_opy_ (u"ࠥࠦኍ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1l1ll1ll11l_opy_.bstack1ll11ll1111_opy_ and test_hook_state == bstack1111111l1l_opy_.PRE:
                bstack11111l11ll_opy_ = bstack111111lll1_opy_.bstack11111l1111_opy_(EVENTS.bstack1l111l1l1_opy_.value)
                name = str(EVENTS.bstack1l111l1l1_opy_.name)+bstack1ll1l11_opy_ (u"ࠦ࠿ࠨ኎")+str(test_framework_state.name)
                TestFramework.bstack1ll11l1l1l1_opy_(instance, name, bstack11111l11ll_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤ኏").format(e))
        try:
            if not TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1l1lll1llll_opy_) and test_hook_state == bstack1111111l1l_opy_.PRE:
                test = bstack1l1ll1ll11l_opy_.__1ll11111l11_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1ll1l11_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨነ") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠢࠣኑ"))
            if test_framework_state == bstack11111ll1l1_opy_.TEST:
                if test_hook_state == bstack1111111l1l_opy_.PRE and not TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1llll11llll_opy_):
                    TestFramework.bstack1lllllll1l1_opy_(instance, TestFramework.bstack1llll11llll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨኒ") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠤࠥና"))
                elif test_hook_state == bstack1111111l1l_opy_.POST and not TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1lllll1l1l1_opy_):
                    TestFramework.bstack1lllllll1l1_opy_(instance, TestFramework.bstack1lllll1l1l1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨኔ") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠦࠧን"))
            elif test_framework_state == bstack11111ll1l1_opy_.LOG and test_hook_state == bstack1111111l1l_opy_.POST:
                bstack1l1ll1ll11l_opy_.__1l1ll1lll1l_opy_(instance, *args)
            elif test_framework_state == bstack11111ll1l1_opy_.LOG_REPORT and test_hook_state == bstack1111111l1l_opy_.POST:
                self.__1ll11l11l1l_opy_(instance, *args)
                self.__1l1lll11ll1_opy_(instance)
            elif test_framework_state in bstack1l1ll1ll11l_opy_.bstack1ll11ll1111_opy_:
                self.__1l1llll1l1l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨኖ") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠨࠢኗ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1ll111lllll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1l1ll1ll11l_opy_.bstack1ll11ll1111_opy_ and test_hook_state == bstack1111111l1l_opy_.POST:
                name = str(EVENTS.bstack1l111l1l1_opy_.name)+bstack1ll1l11_opy_ (u"ࠢ࠻ࠤኘ")+str(test_framework_state.name)
                bstack11111l11ll_opy_ = TestFramework.bstack1l1llll1ll1_opy_(instance, name)
                bstack111111lll1_opy_.end(EVENTS.bstack1l111l1l1_opy_.value, bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣኙ"), bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢኚ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥኛ").format(e))
    def bstack1lll1llll11_opy_(self):
        return self.bstack1ll11l1ll11_opy_
    def __1ll11111lll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1ll1l11_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣኜ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1llll1l111l_opy_(rep, [bstack1ll1l11_opy_ (u"ࠧࡽࡨࡦࡰࠥኝ"), bstack1ll1l11_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢኞ"), bstack1ll1l11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢኟ"), bstack1ll1l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣአ"), bstack1ll1l11_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥኡ"), bstack1ll1l11_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤኢ")])
        return None
    def __1ll11l11l1l_opy_(self, instance: bstack11111l111l_opy_, *args):
        result = self.__1ll11111lll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111ll1111_opy_ = None
        if result.get(bstack1ll1l11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧኣ"), None) == bstack1ll1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧኤ") and len(args) > 1 and getattr(args[1], bstack1ll1l11_opy_ (u"ࠨࡥࡹࡥ࡬ࡲ࡫ࡵࠢእ"), None) is not None:
            failure = [{bstack1ll1l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪኦ"): [args[1].excinfo.exconly(), result.get(bstack1ll1l11_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢኧ"), None)]}]
            bstack1111ll1111_opy_ = bstack1ll1l11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥከ") if bstack1ll1l11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨኩ") in getattr(args[1].excinfo, bstack1ll1l11_opy_ (u"ࠦࡹࡿࡰࡦࡰࡤࡱࡪࠨኪ"), bstack1ll1l11_opy_ (u"ࠧࠨካ")) else bstack1ll1l11_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢኬ")
        bstack1ll111l1l11_opy_ = result.get(bstack1ll1l11_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣክ"), TestFramework.bstack1ll11l11ll1_opy_)
        if bstack1ll111l1l11_opy_ != TestFramework.bstack1ll11l11ll1_opy_:
            TestFramework.bstack1lllllll1l1_opy_(instance, TestFramework.bstack1llll11l1ll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l1llllllll_opy_(instance, {
            TestFramework.bstack1lll11l1111_opy_: failure,
            TestFramework.bstack1ll111ll11l_opy_: bstack1111ll1111_opy_,
            TestFramework.bstack1lll111111l_opy_: bstack1ll111l1l11_opy_,
        })
    def __1ll111lll11_opy_(
        self,
        context: bstack1ll11l11111_opy_,
        test_framework_state: bstack11111ll1l1_opy_,
        test_hook_state: bstack1111111l1l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack11111ll1l1_opy_.SETUP_FIXTURE:
            instance = self.__1l1llll1l11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1ll11l111ll_opy_ bstack1ll1111ll11_opy_ this to be bstack1ll1l11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣኮ")
            if test_framework_state == bstack11111ll1l1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1ll1111llll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack11111ll1l1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1ll1l11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢኯ"), None), bstack1ll1l11_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥኰ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1ll1l11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦ኱"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1ll11ll11l1_opy_(target) if target else None
        return instance
    def __1l1llll1l1l_opy_(
        self,
        instance: bstack11111l111l_opy_,
        test_framework_state: bstack11111ll1l1_opy_,
        test_hook_state: bstack1111111l1l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1ll111l11l1_opy_ = TestFramework.bstack11111l11l1_opy_(instance, bstack1l1ll1ll11l_opy_.bstack1ll111111ll_opy_, {})
        if not key in bstack1ll111l11l1_opy_:
            bstack1ll111l11l1_opy_[key] = []
        bstack1l1lllll1l1_opy_ = TestFramework.bstack11111l11l1_opy_(instance, bstack1l1ll1ll11l_opy_.bstack1l1lll1ll1l_opy_, {})
        if not key in bstack1l1lllll1l1_opy_:
            bstack1l1lllll1l1_opy_[key] = []
        bstack1ll11ll1l11_opy_ = {
            bstack1l1ll1ll11l_opy_.bstack1ll111111ll_opy_: bstack1ll111l11l1_opy_,
            bstack1l1ll1ll11l_opy_.bstack1l1lll1ll1l_opy_: bstack1l1lllll1l1_opy_,
        }
        if test_hook_state == bstack1111111l1l_opy_.PRE:
            hook = {
                bstack1ll1l11_opy_ (u"ࠧࡱࡥࡺࠤኲ"): key,
                TestFramework.bstack1l1lll1l11l_opy_: uuid4().__str__(),
                TestFramework.bstack1l1lllllll1_opy_: TestFramework.bstack1l1lll111l1_opy_,
                TestFramework.bstack1l1lll1111l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1llll11ll_opy_: [],
                TestFramework.bstack1ll11111111_opy_: args[1] if len(args) > 1 else bstack1ll1l11_opy_ (u"࠭ࠧኳ"),
                TestFramework.bstack1ll11l11l11_opy_: bstack1ll1111l1ll_opy_.bstack1ll11ll111l_opy_()
            }
            bstack1ll111l11l1_opy_[key].append(hook)
            bstack1ll11ll1l11_opy_[bstack1l1ll1ll11l_opy_.bstack1ll11l1lll1_opy_] = key
        elif test_hook_state == bstack1111111l1l_opy_.POST:
            bstack1l1lll1l111_opy_ = bstack1ll111l11l1_opy_.get(key, [])
            hook = bstack1l1lll1l111_opy_.pop() if bstack1l1lll1l111_opy_ else None
            if hook:
                result = self.__1ll11111lll_opy_(*args)
                if result:
                    bstack1ll111llll1_opy_ = result.get(bstack1ll1l11_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣኴ"), TestFramework.bstack1l1lll111l1_opy_)
                    if bstack1ll111llll1_opy_ != TestFramework.bstack1l1lll111l1_opy_:
                        hook[TestFramework.bstack1l1lllllll1_opy_] = bstack1ll111llll1_opy_
                hook[TestFramework.bstack1ll11111ll1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1ll11l11l11_opy_]= bstack1ll1111l1ll_opy_.bstack1ll11ll111l_opy_()
                self.bstack1l1lllll111_opy_(hook)
                logs = hook.get(TestFramework.bstack1l1ll1lll11_opy_, [])
                if logs: self.bstack1llll1lll11_opy_(instance, logs)
                bstack1l1lllll1l1_opy_[key].append(hook)
                bstack1ll11ll1l11_opy_[bstack1l1ll1ll11l_opy_.bstack1l1lll11111_opy_] = key
        TestFramework.bstack1l1llllllll_opy_(instance, bstack1ll11ll1l11_opy_)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼ࡭ࡨࡽࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࡀࡿ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࠢኵ") + str(bstack1l1lllll1l1_opy_) + bstack1ll1l11_opy_ (u"ࠤࠥ኶"))
    def __1l1llll1l11_opy_(
        self,
        context: bstack1ll11l11111_opy_,
        test_framework_state: bstack11111ll1l1_opy_,
        test_hook_state: bstack1111111l1l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1llll1l111l_opy_(args[0], [bstack1ll1l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤ኷"), bstack1ll1l11_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧኸ"), bstack1ll1l11_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧኹ"), bstack1ll1l11_opy_ (u"ࠨࡩࡥࡵࠥኺ"), bstack1ll1l11_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤኻ"), bstack1ll1l11_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣኼ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1ll1l11_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣኽ")) else fixturedef.get(bstack1ll1l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤኾ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1ll1l11_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤ኿")) else None
        node = request.node if hasattr(request, bstack1ll1l11_opy_ (u"ࠧࡴ࡯ࡥࡧࠥዀ")) else None
        target = request.node.nodeid if hasattr(node, bstack1ll1l11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨ዁")) else None
        baseid = fixturedef.get(bstack1ll1l11_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢዂ"), None) or bstack1ll1l11_opy_ (u"ࠣࠤዃ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1ll1l11_opy_ (u"ࠤࡢࡴࡾ࡬ࡵ࡯ࡥ࡬ࡸࡪࡳࠢዄ")):
            target = bstack1l1ll1ll11l_opy_.__1l1lllll11l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1ll1l11_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧዅ")) else None
            if target and not TestFramework.bstack1ll11ll11l1_opy_(target):
                self.__1ll1111llll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦ࡮ࡰࡦࡨࡁࢀࡴ࡯ࡥࡧࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨ዆") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠧࠨ዇"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦወ") + str(target) + bstack1ll1l11_opy_ (u"ࠢࠣዉ"))
            return None
        instance = TestFramework.bstack1ll11ll11l1_opy_(target)
        if not instance:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡣࡣࡶࡩ࡮ࡪ࠽ࡼࡤࡤࡷࡪ࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥዊ") + str(target) + bstack1ll1l11_opy_ (u"ࠤࠥዋ"))
            return None
        bstack1ll111ll1l1_opy_ = TestFramework.bstack11111l11l1_opy_(instance, bstack1l1ll1ll11l_opy_.bstack1l1llllll11_opy_, {})
        if os.getenv(bstack1ll1l11_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡉࡍ࡝࡚ࡕࡓࡇࡖࠦዌ"), bstack1ll1l11_opy_ (u"ࠦ࠶ࠨው")) == bstack1ll1l11_opy_ (u"ࠧ࠷ࠢዎ"):
            bstack1ll1111ll1l_opy_ = bstack1ll1l11_opy_ (u"ࠨ࠺ࠣዏ").join((scope, fixturename))
            bstack1l1lll11lll_opy_ = datetime.now(tz=timezone.utc)
            bstack1ll11l1l1ll_opy_ = {
                bstack1ll1l11_opy_ (u"ࠢ࡬ࡧࡼࠦዐ"): bstack1ll1111ll1l_opy_,
                bstack1ll1l11_opy_ (u"ࠣࡶࡤ࡫ࡸࠨዑ"): bstack1l1ll1ll11l_opy_.__1ll11l1llll_opy_(request.node),
                bstack1ll1l11_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࠥዒ"): fixturedef,
                bstack1ll1l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤዓ"): scope,
                bstack1ll1l11_opy_ (u"ࠦࡹࡿࡰࡦࠤዔ"): None,
            }
            try:
                if test_hook_state == bstack1111111l1l_opy_.POST and callable(getattr(args[-1], bstack1ll1l11_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤዕ"), None)):
                    bstack1ll11l1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡴࡺࡲࡨࠦዖ")] = TestFramework.bstack1llll11ll1l_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1111111l1l_opy_.PRE:
                bstack1ll11l1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠢࡶࡷ࡬ࡨࠧ዗")] = uuid4().__str__()
                bstack1ll11l1l1ll_opy_[bstack1l1ll1ll11l_opy_.bstack1l1lll1111l_opy_] = bstack1l1lll11lll_opy_
            elif test_hook_state == bstack1111111l1l_opy_.POST:
                bstack1ll11l1l1ll_opy_[bstack1l1ll1ll11l_opy_.bstack1ll11111ll1_opy_] = bstack1l1lll11lll_opy_
            if bstack1ll1111ll1l_opy_ in bstack1ll111ll1l1_opy_:
                bstack1ll111ll1l1_opy_[bstack1ll1111ll1l_opy_].update(bstack1ll11l1l1ll_opy_)
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࠤዘ") + str(bstack1ll111ll1l1_opy_[bstack1ll1111ll1l_opy_]) + bstack1ll1l11_opy_ (u"ࠤࠥዙ"))
            else:
                bstack1ll111ll1l1_opy_[bstack1ll1111ll1l_opy_] = bstack1ll11l1l1ll_opy_
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡾࠢࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࠨዚ") + str(len(bstack1ll111ll1l1_opy_)) + bstack1ll1l11_opy_ (u"ࠦࠧዛ"))
        TestFramework.bstack1lllllll1l1_opy_(instance, bstack1l1ll1ll11l_opy_.bstack1l1llllll11_opy_, bstack1ll111ll1l1_opy_)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࡻ࡭ࡧࡱࠬࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧዜ") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠨࠢዝ"))
        return instance
    def __1ll1111llll_opy_(
        self,
        context: bstack1ll11l11111_opy_,
        test_framework_state: bstack11111ll1l1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1l1lll1ll11_opy_.create_context(target)
        ob = bstack11111l111l_opy_(ctx, self.bstack1l1lll11l1l_opy_, self.bstack1ll111ll111_opy_, test_framework_state)
        TestFramework.bstack1l1llllllll_opy_(ob, {
            TestFramework.bstack1llll1lllll_opy_: context.test_framework_name,
            TestFramework.bstack1lllllllll1_opy_: context.test_framework_version,
            TestFramework.bstack1l1llll111l_opy_: [],
            bstack1l1ll1ll11l_opy_.bstack1l1llllll11_opy_: {},
            bstack1l1ll1ll11l_opy_.bstack1l1lll1ll1l_opy_: {},
            bstack1l1ll1ll11l_opy_.bstack1ll111111ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lllllll1l1_opy_(ob, TestFramework.bstack1l1lllll1ll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lllllll1l1_opy_(ob, TestFramework.bstack1111l11ll1_opy_, context.platform_index)
        TestFramework.bstack1lll111l111_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢዞ") + str(TestFramework.bstack1lll111l111_opy_.keys()) + bstack1ll1l11_opy_ (u"ࠣࠤዟ"))
        return ob
    def bstack1llll111111_opy_(self, instance: bstack11111l111l_opy_, bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_]):
        bstack1ll111111l1_opy_ = (
            bstack1l1ll1ll11l_opy_.bstack1ll11l1lll1_opy_
            if bstack111111111l_opy_[1] == bstack1111111l1l_opy_.PRE
            else bstack1l1ll1ll11l_opy_.bstack1l1lll11111_opy_
        )
        hook = bstack1l1ll1ll11l_opy_.bstack1ll111l111l_opy_(instance, bstack1ll111111l1_opy_)
        entries = hook.get(TestFramework.bstack1l1llll11ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1l1llll111l_opy_, []))
        return entries
    def bstack1llll1l1111_opy_(self, instance: bstack11111l111l_opy_, bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_]):
        bstack1ll111111l1_opy_ = (
            bstack1l1ll1ll11l_opy_.bstack1ll11l1lll1_opy_
            if bstack111111111l_opy_[1] == bstack1111111l1l_opy_.PRE
            else bstack1l1ll1ll11l_opy_.bstack1l1lll11111_opy_
        )
        bstack1l1ll1ll11l_opy_.bstack1ll1111l11l_opy_(instance, bstack1ll111111l1_opy_)
        TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1l1llll111l_opy_, []).clear()
    def bstack1l1lllll111_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll1l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤࡹ࡮ࡥࠡࡌࡤࡺࡦࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬࡮ࡹࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡃࡩࡧࡦ࡯ࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡬ࡲࡸ࡯ࡤࡦࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠳࡚ࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡉࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠭ࠢࡵࡩࡵࡲࡡࡤࡧࡶࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦࠥ࡯࡮ࠡ࡫ࡷࡷࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡌࡪࠥࡧࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡯ࡤࡸࡨ࡮ࡥࡴࠢࡤࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࠦࡨࡰࡱ࡮࠱ࡱ࡫ࡶࡦ࡮ࠣࡪ࡮ࡲࡥ࠭ࠢ࡬ࡸࠥࡩࡲࡦࡣࡷࡩࡸࠦࡡࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࠣࡻ࡮ࡺࡨࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡙ࠥࡩ࡮࡫࡯ࡥࡷࡲࡹ࠭ࠢ࡬ࡸࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡴࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡥࡽࠥࡸࡥࡱ࡮ࡤࡧ࡮ࡴࡧࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡖ࡫ࡩࠥࡩࡲࡦࡣࡷࡩࡩࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡤࡶࡪࠦࡡࡥࡦࡨࡨࠥࡺ࡯ࠡࡶ࡫ࡩࠥ࡮࡯ࡰ࡭ࠪࡷࠥࠨ࡬ࡰࡩࡶࠦࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࠺ࠡࡖ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷࠥࡧ࡮ࡥࠢ࡫ࡳࡴࡱࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡘࡪࡹࡴࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣዠ")
        global _1lll1lll11l_opy_
        platform_index = os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪዡ")]
        bstack1llll111ll1_opy_ = os.path.join(bstack1lllll1lll1_opy_, (bstack1lllllll1ll_opy_ + str(platform_index)), bstack1l1ll1l1lll_opy_)
        if not os.path.exists(bstack1llll111ll1_opy_) or not os.path.isdir(bstack1llll111ll1_opy_):
            self.logger.info(bstack1ll1l11_opy_ (u"ࠦࡉ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴࡴࠢࡷࡳࠥࡶࡲࡰࡥࡨࡷࡸࠦࡻࡾࠤዢ").format(bstack1llll111ll1_opy_))
            return
        logs = hook.get(bstack1ll1l11_opy_ (u"ࠧࡲ࡯ࡨࡵࠥዣ"), [])
        with os.scandir(bstack1llll111ll1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1lll1lll11l_opy_:
                    self.logger.info(bstack1ll1l11_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦዤ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll1l11_opy_ (u"ࠢࠣዥ")
                    log_entry = bstack111111llll_opy_(
                        kind=bstack1ll1l11_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥዦ"),
                        message=bstack1ll1l11_opy_ (u"ࠤࠥዧ"),
                        level=bstack1ll1l11_opy_ (u"ࠥࠦየ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1llll1l1lll_opy_=entry.stat().st_size,
                        bstack1llll1ll1ll_opy_=bstack1ll1l11_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦዩ"),
                        bstack11l1ll1_opy_=os.path.abspath(entry.path),
                        bstack1l1llll1lll_opy_=hook.get(TestFramework.bstack1l1lll1l11l_opy_)
                    )
                    logs.append(log_entry)
                    _1lll1lll11l_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬዪ")]
        bstack1ll111l11ll_opy_ = os.path.join(bstack1lllll1lll1_opy_, (bstack1lllllll1ll_opy_ + str(platform_index)), bstack1l1ll1l1lll_opy_, bstack1l1ll1ll1ll_opy_)
        if not os.path.exists(bstack1ll111l11ll_opy_) or not os.path.isdir(bstack1ll111l11ll_opy_):
            self.logger.info(bstack1ll1l11_opy_ (u"ࠨࡎࡰࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤࠡࡣࡷ࠾ࠥࢁࡽࠣያ").format(bstack1ll111l11ll_opy_))
        else:
            self.logger.info(bstack1ll1l11_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡨࡵࡳࡲࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨዬ").format(bstack1ll111l11ll_opy_))
            with os.scandir(bstack1ll111l11ll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1lll1lll11l_opy_:
                        self.logger.info(bstack1ll1l11_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨይ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll1l11_opy_ (u"ࠤࠥዮ")
                        log_entry = bstack111111llll_opy_(
                            kind=bstack1ll1l11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧዯ"),
                            message=bstack1ll1l11_opy_ (u"ࠦࠧደ"),
                            level=bstack1ll1l11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤዱ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1llll1l1lll_opy_=entry.stat().st_size,
                            bstack1llll1ll1ll_opy_=bstack1ll1l11_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨዲ"),
                            bstack11l1ll1_opy_=os.path.abspath(entry.path),
                            bstack1lllll11lll_opy_=hook.get(TestFramework.bstack1l1lll1l11l_opy_)
                        )
                        logs.append(log_entry)
                        _1lll1lll11l_opy_.add(abs_path)
        hook[bstack1ll1l11_opy_ (u"ࠢ࡭ࡱࡪࡷࠧዳ")] = logs
    def bstack1llll1lll11_opy_(
        self,
        bstack1111l1ll11_opy_: bstack11111l111l_opy_,
        entries: List[bstack111111llll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll1l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧዴ"))
        req.platform_index = TestFramework.bstack11111l11l1_opy_(bstack1111l1ll11_opy_, TestFramework.bstack1111l11ll1_opy_)
        req.execution_context.hash = str(bstack1111l1ll11_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1111l1ll11_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1111l1ll11_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack11111l11l1_opy_(bstack1111l1ll11_opy_, TestFramework.bstack1llll1lllll_opy_)
            log_entry.test_framework_version = TestFramework.bstack11111l11l1_opy_(bstack1111l1ll11_opy_, TestFramework.bstack1lllllllll1_opy_)
            log_entry.uuid = entry.bstack1l1llll1lll_opy_
            log_entry.test_framework_state = bstack1111l1ll11_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll1l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣድ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1ll1l11_opy_ (u"ࠥࠦዶ")
            if entry.kind == bstack1ll1l11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨዷ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1llll1l1lll_opy_
                log_entry.file_path = entry.bstack11l1ll1_opy_
        def bstack1lll1lll1l1_opy_():
            bstack1l1l1lllll_opy_ = datetime.now()
            try:
                self.bstack1llll111lll_opy_.LogCreatedEvent(req)
                bstack1111l1ll11_opy_.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤዸ"), datetime.now() - bstack1l1l1lllll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1l11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧዹ").format(str(e)))
                traceback.print_exc()
        self.bstack1llll11l111_opy_.enqueue(bstack1lll1lll1l1_opy_)
    def __1l1lll11ll1_opy_(self, instance) -> None:
        bstack1ll1l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧዺ")
        bstack1ll11ll1l11_opy_ = {bstack1ll1l11_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥዻ"): bstack1ll1111l1ll_opy_.bstack1ll11ll111l_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l1llllllll_opy_(instance, bstack1ll11ll1l11_opy_)
    @staticmethod
    def bstack1ll111l111l_opy_(instance: bstack11111l111l_opy_, bstack1ll111111l1_opy_: str):
        bstack1ll111l1l1l_opy_ = (
            bstack1l1ll1ll11l_opy_.bstack1l1lll1ll1l_opy_
            if bstack1ll111111l1_opy_ == bstack1l1ll1ll11l_opy_.bstack1l1lll11111_opy_
            else bstack1l1ll1ll11l_opy_.bstack1ll111111ll_opy_
        )
        bstack1ll11ll11ll_opy_ = TestFramework.bstack11111l11l1_opy_(instance, bstack1ll111111l1_opy_, None)
        bstack1ll11l1111l_opy_ = TestFramework.bstack11111l11l1_opy_(instance, bstack1ll111l1l1l_opy_, None) if bstack1ll11ll11ll_opy_ else None
        return (
            bstack1ll11l1111l_opy_[bstack1ll11ll11ll_opy_][-1]
            if isinstance(bstack1ll11l1111l_opy_, dict) and len(bstack1ll11l1111l_opy_.get(bstack1ll11ll11ll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1ll1111l11l_opy_(instance: bstack11111l111l_opy_, bstack1ll111111l1_opy_: str):
        hook = bstack1l1ll1ll11l_opy_.bstack1ll111l111l_opy_(instance, bstack1ll111111l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1llll11ll_opy_, []).clear()
    @staticmethod
    def __1l1ll1lll1l_opy_(instance: bstack11111l111l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1ll1l11_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡥࡲࡶࡩࡹࠢዼ"), None)):
            return
        if os.getenv(bstack1ll1l11_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡏࡓࡌ࡙ࠢዽ"), bstack1ll1l11_opy_ (u"ࠦ࠶ࠨዾ")) != bstack1ll1l11_opy_ (u"ࠧ࠷ࠢዿ"):
            bstack1l1ll1ll11l_opy_.logger.warning(bstack1ll1l11_opy_ (u"ࠨࡩࡨࡰࡲࡶ࡮ࡴࡧࠡࡥࡤࡴࡱࡵࡧࠣጀ"))
            return
        bstack1ll11111l1l_opy_ = {
            bstack1ll1l11_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨጁ"): (bstack1l1ll1ll11l_opy_.bstack1ll11l1lll1_opy_, bstack1l1ll1ll11l_opy_.bstack1ll111111ll_opy_),
            bstack1ll1l11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥጂ"): (bstack1l1ll1ll11l_opy_.bstack1l1lll11111_opy_, bstack1l1ll1ll11l_opy_.bstack1l1lll1ll1l_opy_),
        }
        for when in (bstack1ll1l11_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣጃ"), bstack1ll1l11_opy_ (u"ࠥࡧࡦࡲ࡬ࠣጄ"), bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨጅ")):
            bstack1l1llll1111_opy_ = args[1].get_records(when)
            if not bstack1l1llll1111_opy_:
                continue
            records = [
                bstack111111llll_opy_(
                    kind=TestFramework.bstack1lllll11ll1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1ll1l11_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠣጆ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1ll1l11_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪࠢጇ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l1llll1111_opy_
                if isinstance(getattr(r, bstack1ll1l11_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣገ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l1llllll1l_opy_, bstack1ll111l1l1l_opy_ = bstack1ll11111l1l_opy_.get(when, (None, None))
            bstack1l1ll1llll1_opy_ = TestFramework.bstack11111l11l1_opy_(instance, bstack1l1llllll1l_opy_, None) if bstack1l1llllll1l_opy_ else None
            bstack1ll11l1111l_opy_ = TestFramework.bstack11111l11l1_opy_(instance, bstack1ll111l1l1l_opy_, None) if bstack1l1ll1llll1_opy_ else None
            if isinstance(bstack1ll11l1111l_opy_, dict) and len(bstack1ll11l1111l_opy_.get(bstack1l1ll1llll1_opy_, [])) > 0:
                hook = bstack1ll11l1111l_opy_[bstack1l1ll1llll1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l1llll11ll_opy_ in hook:
                    hook[TestFramework.bstack1l1llll11ll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1l1llll111l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1ll11111l11_opy_(test) -> Dict[str, Any]:
        bstack1l1llll111_opy_ = bstack1l1ll1ll11l_opy_.__1l1lllll11l_opy_(test.location) if hasattr(test, bstack1ll1l11_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥጉ")) else getattr(test, bstack1ll1l11_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤጊ"), None)
        test_name = test.name if hasattr(test, bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣጋ")) else None
        bstack1ll1111lll1_opy_ = test.fspath.strpath if hasattr(test, bstack1ll1l11_opy_ (u"ࠦ࡫ࡹࡰࡢࡶ࡫ࠦጌ")) and test.fspath else None
        if not bstack1l1llll111_opy_ or not test_name or not bstack1ll1111lll1_opy_:
            return None
        code = None
        if hasattr(test, bstack1ll1l11_opy_ (u"ࠧࡵࡢ࡫ࠤግ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l1ll1ll1l1_opy_ = []
        try:
            bstack1l1ll1ll1l1_opy_ = bstack1lll111111_opy_.bstack111ll11ll1_opy_(test)
        except:
            bstack1l1ll1ll11l_opy_.logger.warning(bstack1ll1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷ࠱ࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶࠤࡼ࡯࡬࡭ࠢࡥࡩࠥࡸࡥࡴࡱ࡯ࡺࡪࡪࠠࡪࡰࠣࡇࡑࡏࠢጎ"))
        return {
            TestFramework.bstack11111111ll_opy_: uuid4().__str__(),
            TestFramework.bstack1l1lll1llll_opy_: bstack1l1llll111_opy_,
            TestFramework.bstack1111l111ll_opy_: test_name,
            TestFramework.bstack11111lll1l_opy_: getattr(test, bstack1ll1l11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢጏ"), None),
            TestFramework.bstack1l1lll1l1l1_opy_: bstack1ll1111lll1_opy_,
            TestFramework.bstack1ll111l1ll1_opy_: bstack1l1ll1ll11l_opy_.__1ll11l1llll_opy_(test),
            TestFramework.bstack1l1lll111ll_opy_: code,
            TestFramework.bstack1lll111111l_opy_: TestFramework.bstack1ll11l11ll1_opy_,
            TestFramework.bstack1ll1l1l11ll_opy_: bstack1l1llll111_opy_,
            TestFramework.bstack1l1ll1l1l11_opy_: bstack1l1ll1ll1l1_opy_
        }
    @staticmethod
    def __1ll11l1llll_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1ll1l11_opy_ (u"ࠣࡱࡺࡲࡤࡳࡡࡳ࡭ࡨࡶࡸࠨጐ"), [])
            markers.extend([getattr(m, bstack1ll1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ጑"), None) for m in own_markers if getattr(m, bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣጒ"), None)])
            current = getattr(current, bstack1ll1l11_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦጓ"), None)
        return markers
    @staticmethod
    def __1l1lllll11l_opy_(location):
        return bstack1ll1l11_opy_ (u"ࠧࡀ࠺ࠣጔ").join(filter(lambda x: isinstance(x, str), location))