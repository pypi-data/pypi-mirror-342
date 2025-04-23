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
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack11111ll1l1_opy_,
    bstack11111l111l_opy_,
    bstack1111111l1l_opy_,
    bstack1ll11l11111_opy_,
    bstack111111llll_opy_,
)
import traceback
from bstack_utils.helper import bstack1llllll111l_opy_
from bstack_utils.bstack1ll11l1lll_opy_ import bstack111111lll1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1ll1111111l_opy_ import bstack1ll1111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll11l111_opy_ import bstack1ll111ll1ll_opy_
bstack1lllll1lll1_opy_ = bstack1llllll111l_opy_()
bstack1lllllll1ll_opy_ = bstack1ll1l11_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᇆ")
bstack1ll111l1111_opy_ = bstack1ll1l11_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦᇇ")
bstack1ll11l1l111_opy_ = bstack1ll1l11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣᇈ")
bstack1ll11l1l11l_opy_ = 1.0
_1lll1lll11l_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l1llllll11_opy_ = bstack1ll1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᇉ")
    bstack1ll111111ll_opy_ = bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤᇊ")
    bstack1l1lll1ll1l_opy_ = bstack1ll1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᇋ")
    bstack1ll11l1lll1_opy_ = bstack1ll1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᇌ")
    bstack1l1lll11111_opy_ = bstack1ll1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᇍ")
    bstack1ll11l1ll11_opy_: bool
    bstack1llll11l111_opy_: bstack1ll111ll1ll_opy_  = None
    bstack1ll11ll1111_opy_ = [
        bstack11111ll1l1_opy_.BEFORE_ALL,
        bstack11111ll1l1_opy_.AFTER_ALL,
        bstack11111ll1l1_opy_.BEFORE_EACH,
        bstack11111ll1l1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1ll111ll111_opy_: Dict[str, str],
        bstack1l1lll11l1l_opy_: List[str]=[bstack1ll1l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᇎ")],
        bstack1llll11l111_opy_: bstack1ll111ll1ll_opy_ = None,
        bstack1llll111lll_opy_=None
    ):
        super().__init__(bstack1l1lll11l1l_opy_, bstack1ll111ll111_opy_, bstack1llll11l111_opy_)
        self.bstack1ll11l1ll11_opy_ = any(bstack1ll1l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᇏ") in item.lower() for item in bstack1l1lll11l1l_opy_)
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
        if test_framework_state == bstack11111ll1l1_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1ll11ll1111_opy_:
            bstack1l1llll11l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack11111ll1l1_opy_.NONE:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦᇐ") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠦࠧᇑ"))
            return
        if not self.bstack1ll11l1ll11_opy_:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨᇒ") + str(str(self.bstack1l1lll11l1l_opy_)) + bstack1ll1l11_opy_ (u"ࠨࠢᇓ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᇔ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠣࠤᇕ"))
            return
        instance = self.__1ll111lll11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣᇖ") + str(args) + bstack1ll1l11_opy_ (u"ࠥࠦᇗ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1ll11ll1111_opy_ and test_hook_state == bstack1111111l1l_opy_.PRE:
                bstack11111l11ll_opy_ = bstack111111lll1_opy_.bstack11111l1111_opy_(EVENTS.bstack1l111l1l1_opy_.value)
                name = str(EVENTS.bstack1l111l1l1_opy_.name)+bstack1ll1l11_opy_ (u"ࠦ࠿ࠨᇘ")+str(test_framework_state.name)
                TestFramework.bstack1ll11l1l1l1_opy_(instance, name, bstack11111l11ll_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤᇙ").format(e))
        try:
            if test_framework_state == bstack11111ll1l1_opy_.TEST:
                if not TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1l1lll1llll_opy_) and test_hook_state == bstack1111111l1l_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1ll11111l11_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1ll1l11_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᇚ") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠢࠣᇛ"))
                if test_hook_state == bstack1111111l1l_opy_.PRE and not TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1llll11llll_opy_):
                    TestFramework.bstack1lllllll1l1_opy_(instance, TestFramework.bstack1llll11llll_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l1ll1lllll_opy_(instance, args)
                    self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᇜ") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠤࠥᇝ"))
                elif test_hook_state == bstack1111111l1l_opy_.POST and not TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1lllll1l1l1_opy_):
                    TestFramework.bstack1lllllll1l1_opy_(instance, TestFramework.bstack1lllll1l1l1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᇞ") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠦࠧᇟ"))
            elif test_framework_state == bstack11111ll1l1_opy_.STEP:
                if test_hook_state == bstack1111111l1l_opy_.PRE:
                    PytestBDDFramework.__1ll11l1ll1l_opy_(instance, args)
                elif test_hook_state == bstack1111111l1l_opy_.POST:
                    PytestBDDFramework.__1ll111l1lll_opy_(instance, args)
            elif test_framework_state == bstack11111ll1l1_opy_.LOG and test_hook_state == bstack1111111l1l_opy_.POST:
                PytestBDDFramework.__1l1ll1lll1l_opy_(instance, *args)
            elif test_framework_state == bstack11111ll1l1_opy_.LOG_REPORT and test_hook_state == bstack1111111l1l_opy_.POST:
                self.__1ll11l11l1l_opy_(instance, *args)
                self.__1l1lll11ll1_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1ll11ll1111_opy_:
                self.__1l1llll1l1l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᇠ") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠨࠢᇡ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1ll111lllll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1ll11ll1111_opy_ and test_hook_state == bstack1111111l1l_opy_.POST:
                name = str(EVENTS.bstack1l111l1l1_opy_.name)+bstack1ll1l11_opy_ (u"ࠢ࠻ࠤᇢ")+str(test_framework_state.name)
                bstack11111l11ll_opy_ = TestFramework.bstack1l1llll1ll1_opy_(instance, name)
                bstack111111lll1_opy_.end(EVENTS.bstack1l111l1l1_opy_.value, bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᇣ"), bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᇤ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᇥ").format(e))
    def bstack1lll1llll11_opy_(self):
        return self.bstack1ll11l1ll11_opy_
    def __1ll11111lll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1ll1l11_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᇦ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1llll1l111l_opy_(rep, [bstack1ll1l11_opy_ (u"ࠧࡽࡨࡦࡰࠥᇧ"), bstack1ll1l11_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᇨ"), bstack1ll1l11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᇩ"), bstack1ll1l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᇪ"), bstack1ll1l11_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥᇫ"), bstack1ll1l11_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᇬ")])
        return None
    def __1ll11l11l1l_opy_(self, instance: bstack11111l111l_opy_, *args):
        result = self.__1ll11111lll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111ll1111_opy_ = None
        if result.get(bstack1ll1l11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᇭ"), None) == bstack1ll1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᇮ") and len(args) > 1 and getattr(args[1], bstack1ll1l11_opy_ (u"ࠨࡥࡹࡥ࡬ࡲ࡫ࡵࠢᇯ"), None) is not None:
            failure = [{bstack1ll1l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᇰ"): [args[1].excinfo.exconly(), result.get(bstack1ll1l11_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᇱ"), None)]}]
            bstack1111ll1111_opy_ = bstack1ll1l11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᇲ") if bstack1ll1l11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᇳ") in getattr(args[1].excinfo, bstack1ll1l11_opy_ (u"ࠦࡹࡿࡰࡦࡰࡤࡱࡪࠨᇴ"), bstack1ll1l11_opy_ (u"ࠧࠨᇵ")) else bstack1ll1l11_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᇶ")
        bstack1ll111l1l11_opy_ = result.get(bstack1ll1l11_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᇷ"), TestFramework.bstack1ll11l11ll1_opy_)
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
            target = None # bstack1ll11l111ll_opy_ bstack1ll1111ll11_opy_ this to be bstack1ll1l11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᇸ")
            if test_framework_state == bstack11111ll1l1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1ll1111llll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack11111ll1l1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1ll1l11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᇹ"), None), bstack1ll1l11_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᇺ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1ll1l11_opy_ (u"ࠦࡳࡵࡤࡦࠤᇻ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1ll1l11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᇼ"), None):
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
        bstack1ll111l11l1_opy_ = TestFramework.bstack11111l11l1_opy_(instance, PytestBDDFramework.bstack1ll111111ll_opy_, {})
        if not key in bstack1ll111l11l1_opy_:
            bstack1ll111l11l1_opy_[key] = []
        bstack1l1lllll1l1_opy_ = TestFramework.bstack11111l11l1_opy_(instance, PytestBDDFramework.bstack1l1lll1ll1l_opy_, {})
        if not key in bstack1l1lllll1l1_opy_:
            bstack1l1lllll1l1_opy_[key] = []
        bstack1ll11ll1l11_opy_ = {
            PytestBDDFramework.bstack1ll111111ll_opy_: bstack1ll111l11l1_opy_,
            PytestBDDFramework.bstack1l1lll1ll1l_opy_: bstack1l1lllll1l1_opy_,
        }
        if test_hook_state == bstack1111111l1l_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1ll1l11_opy_ (u"ࠨ࡫ࡦࡻࠥᇽ"): key,
                TestFramework.bstack1l1lll1l11l_opy_: uuid4().__str__(),
                TestFramework.bstack1l1lllllll1_opy_: TestFramework.bstack1l1lll111l1_opy_,
                TestFramework.bstack1l1lll1111l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1llll11ll_opy_: [],
                TestFramework.bstack1ll11111111_opy_: hook_name,
                TestFramework.bstack1ll11l11l11_opy_: bstack1ll1111l1ll_opy_.bstack1ll11ll111l_opy_()
            }
            bstack1ll111l11l1_opy_[key].append(hook)
            bstack1ll11ll1l11_opy_[PytestBDDFramework.bstack1ll11l1lll1_opy_] = key
        elif test_hook_state == bstack1111111l1l_opy_.POST:
            bstack1l1lll1l111_opy_ = bstack1ll111l11l1_opy_.get(key, [])
            hook = bstack1l1lll1l111_opy_.pop() if bstack1l1lll1l111_opy_ else None
            if hook:
                result = self.__1ll11111lll_opy_(*args)
                if result:
                    bstack1ll111llll1_opy_ = result.get(bstack1ll1l11_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᇾ"), TestFramework.bstack1l1lll111l1_opy_)
                    if bstack1ll111llll1_opy_ != TestFramework.bstack1l1lll111l1_opy_:
                        hook[TestFramework.bstack1l1lllllll1_opy_] = bstack1ll111llll1_opy_
                hook[TestFramework.bstack1ll11111ll1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1ll11l11l11_opy_] = bstack1ll1111l1ll_opy_.bstack1ll11ll111l_opy_()
                self.bstack1l1lllll111_opy_(hook)
                logs = hook.get(TestFramework.bstack1l1ll1lll11_opy_, [])
                self.bstack1llll1lll11_opy_(instance, logs)
                bstack1l1lllll1l1_opy_[key].append(hook)
                bstack1ll11ll1l11_opy_[PytestBDDFramework.bstack1l1lll11111_opy_] = key
        TestFramework.bstack1l1llllllll_opy_(instance, bstack1ll11ll1l11_opy_)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼ࡭ࡨࡽࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࡀࡿ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࠢᇿ") + str(bstack1l1lllll1l1_opy_) + bstack1ll1l11_opy_ (u"ࠤࠥሀ"))
    def __1l1llll1l11_opy_(
        self,
        context: bstack1ll11l11111_opy_,
        test_framework_state: bstack11111ll1l1_opy_,
        test_hook_state: bstack1111111l1l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1llll1l111l_opy_(args[0], [bstack1ll1l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤሁ"), bstack1ll1l11_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧሂ"), bstack1ll1l11_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧሃ"), bstack1ll1l11_opy_ (u"ࠨࡩࡥࡵࠥሄ"), bstack1ll1l11_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤህ"), bstack1ll1l11_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣሆ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1ll1l11_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣሇ")) else fixturedef.get(bstack1ll1l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤለ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1ll1l11_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤሉ")) else None
        node = request.node if hasattr(request, bstack1ll1l11_opy_ (u"ࠧࡴ࡯ࡥࡧࠥሊ")) else None
        target = request.node.nodeid if hasattr(node, bstack1ll1l11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨላ")) else None
        baseid = fixturedef.get(bstack1ll1l11_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢሌ"), None) or bstack1ll1l11_opy_ (u"ࠣࠤል")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1ll1l11_opy_ (u"ࠤࡢࡴࡾ࡬ࡵ࡯ࡥ࡬ࡸࡪࡳࠢሎ")):
            target = PytestBDDFramework.__1l1lllll11l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1ll1l11_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧሏ")) else None
            if target and not TestFramework.bstack1ll11ll11l1_opy_(target):
                self.__1ll1111llll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦ࡮ࡰࡦࡨࡁࢀࡴ࡯ࡥࡧࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨሐ") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠧࠨሑ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦሒ") + str(target) + bstack1ll1l11_opy_ (u"ࠢࠣሓ"))
            return None
        instance = TestFramework.bstack1ll11ll11l1_opy_(target)
        if not instance:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡣࡣࡶࡩ࡮ࡪ࠽ࡼࡤࡤࡷࡪ࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥሔ") + str(target) + bstack1ll1l11_opy_ (u"ࠤࠥሕ"))
            return None
        bstack1ll111ll1l1_opy_ = TestFramework.bstack11111l11l1_opy_(instance, PytestBDDFramework.bstack1l1llllll11_opy_, {})
        if os.getenv(bstack1ll1l11_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡉࡍ࡝࡚ࡕࡓࡇࡖࠦሖ"), bstack1ll1l11_opy_ (u"ࠦ࠶ࠨሗ")) == bstack1ll1l11_opy_ (u"ࠧ࠷ࠢመ"):
            bstack1ll1111ll1l_opy_ = bstack1ll1l11_opy_ (u"ࠨ࠺ࠣሙ").join((scope, fixturename))
            bstack1l1lll11lll_opy_ = datetime.now(tz=timezone.utc)
            bstack1ll11l1l1ll_opy_ = {
                bstack1ll1l11_opy_ (u"ࠢ࡬ࡧࡼࠦሚ"): bstack1ll1111ll1l_opy_,
                bstack1ll1l11_opy_ (u"ࠣࡶࡤ࡫ࡸࠨማ"): PytestBDDFramework.__1ll11l1llll_opy_(request.node, scenario),
                bstack1ll1l11_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࠥሜ"): fixturedef,
                bstack1ll1l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤም"): scope,
                bstack1ll1l11_opy_ (u"ࠦࡹࡿࡰࡦࠤሞ"): None,
            }
            try:
                if test_hook_state == bstack1111111l1l_opy_.POST and callable(getattr(args[-1], bstack1ll1l11_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤሟ"), None)):
                    bstack1ll11l1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡴࡺࡲࡨࠦሠ")] = TestFramework.bstack1llll11ll1l_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1111111l1l_opy_.PRE:
                bstack1ll11l1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠢࡶࡷ࡬ࡨࠧሡ")] = uuid4().__str__()
                bstack1ll11l1l1ll_opy_[PytestBDDFramework.bstack1l1lll1111l_opy_] = bstack1l1lll11lll_opy_
            elif test_hook_state == bstack1111111l1l_opy_.POST:
                bstack1ll11l1l1ll_opy_[PytestBDDFramework.bstack1ll11111ll1_opy_] = bstack1l1lll11lll_opy_
            if bstack1ll1111ll1l_opy_ in bstack1ll111ll1l1_opy_:
                bstack1ll111ll1l1_opy_[bstack1ll1111ll1l_opy_].update(bstack1ll11l1l1ll_opy_)
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࠤሢ") + str(bstack1ll111ll1l1_opy_[bstack1ll1111ll1l_opy_]) + bstack1ll1l11_opy_ (u"ࠤࠥሣ"))
            else:
                bstack1ll111ll1l1_opy_[bstack1ll1111ll1l_opy_] = bstack1ll11l1l1ll_opy_
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡾࠢࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࠨሤ") + str(len(bstack1ll111ll1l1_opy_)) + bstack1ll1l11_opy_ (u"ࠦࠧሥ"))
        TestFramework.bstack1lllllll1l1_opy_(instance, PytestBDDFramework.bstack1l1llllll11_opy_, bstack1ll111ll1l1_opy_)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࡻ࡭ࡧࡱࠬࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧሦ") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠨࠢሧ"))
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
            PytestBDDFramework.bstack1l1llllll11_opy_: {},
            PytestBDDFramework.bstack1l1lll1ll1l_opy_: {},
            PytestBDDFramework.bstack1ll111111ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lllllll1l1_opy_(ob, TestFramework.bstack1l1lllll1ll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lllllll1l1_opy_(ob, TestFramework.bstack1111l11ll1_opy_, context.platform_index)
        TestFramework.bstack1lll111l111_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢረ") + str(TestFramework.bstack1lll111l111_opy_.keys()) + bstack1ll1l11_opy_ (u"ࠣࠤሩ"))
        return ob
    @staticmethod
    def __1l1ll1lllll_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll1l11_opy_ (u"ࠩ࡬ࡨࠬሪ"): id(step),
                bstack1ll1l11_opy_ (u"ࠪࡸࡪࡾࡴࠨራ"): step.name,
                bstack1ll1l11_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬሬ"): step.keyword,
            })
        meta = {
            bstack1ll1l11_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭ር"): {
                bstack1ll1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫሮ"): feature.name,
                bstack1ll1l11_opy_ (u"ࠧࡱࡣࡷ࡬ࠬሯ"): feature.filename,
                bstack1ll1l11_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ሰ"): feature.description
            },
            bstack1ll1l11_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫሱ"): {
                bstack1ll1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨሲ"): scenario.name
            },
            bstack1ll1l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪሳ"): steps,
            bstack1ll1l11_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧሴ"): PytestBDDFramework.__1ll11l11lll_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1ll11l111l1_opy_: meta
            }
        )
    def bstack1l1lllll111_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧስ")
        global _1lll1lll11l_opy_
        platform_index = os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧሶ")]
        bstack1llll111ll1_opy_ = os.path.join(bstack1lllll1lll1_opy_, (bstack1lllllll1ll_opy_ + str(platform_index)), bstack1ll111l1111_opy_)
        if not os.path.exists(bstack1llll111ll1_opy_) or not os.path.isdir(bstack1llll111ll1_opy_):
            return
        logs = hook.get(bstack1ll1l11_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨሷ"), [])
        with os.scandir(bstack1llll111ll1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1lll1lll11l_opy_:
                    self.logger.info(bstack1ll1l11_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢሸ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll1l11_opy_ (u"ࠥࠦሹ")
                    log_entry = bstack111111llll_opy_(
                        kind=bstack1ll1l11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨሺ"),
                        message=bstack1ll1l11_opy_ (u"ࠧࠨሻ"),
                        level=bstack1ll1l11_opy_ (u"ࠨࠢሼ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1llll1l1lll_opy_=entry.stat().st_size,
                        bstack1llll1ll1ll_opy_=bstack1ll1l11_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢሽ"),
                        bstack11l1ll1_opy_=os.path.abspath(entry.path),
                        bstack1l1llll1lll_opy_=hook.get(TestFramework.bstack1l1lll1l11l_opy_)
                    )
                    logs.append(log_entry)
                    _1lll1lll11l_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨሾ")]
        bstack1ll111l11ll_opy_ = os.path.join(bstack1lllll1lll1_opy_, (bstack1lllllll1ll_opy_ + str(platform_index)), bstack1ll111l1111_opy_, bstack1ll11l1l111_opy_)
        if not os.path.exists(bstack1ll111l11ll_opy_) or not os.path.isdir(bstack1ll111l11ll_opy_):
            self.logger.info(bstack1ll1l11_opy_ (u"ࠤࡑࡳࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡬࡯ࡶࡰࡧࠤࡦࡺ࠺ࠡࡽࢀࠦሿ").format(bstack1ll111l11ll_opy_))
        else:
            self.logger.info(bstack1ll1l11_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤቀ").format(bstack1ll111l11ll_opy_))
            with os.scandir(bstack1ll111l11ll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1lll1lll11l_opy_:
                        self.logger.info(bstack1ll1l11_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤቁ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll1l11_opy_ (u"ࠧࠨቂ")
                        log_entry = bstack111111llll_opy_(
                            kind=bstack1ll1l11_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣቃ"),
                            message=bstack1ll1l11_opy_ (u"ࠢࠣቄ"),
                            level=bstack1ll1l11_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧቅ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1llll1l1lll_opy_=entry.stat().st_size,
                            bstack1llll1ll1ll_opy_=bstack1ll1l11_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤቆ"),
                            bstack11l1ll1_opy_=os.path.abspath(entry.path),
                            bstack1lllll11lll_opy_=hook.get(TestFramework.bstack1l1lll1l11l_opy_)
                        )
                        logs.append(log_entry)
                        _1lll1lll11l_opy_.add(abs_path)
        hook[bstack1ll1l11_opy_ (u"ࠥࡰࡴ࡭ࡳࠣቇ")] = logs
    def bstack1llll1lll11_opy_(
        self,
        bstack1111l1ll11_opy_: bstack11111l111l_opy_,
        entries: List[bstack111111llll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣቈ"))
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
            log_entry.message = entry.message.encode(bstack1ll1l11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ቉"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1ll1l11_opy_ (u"ࠨࠢቊ")
            if entry.kind == bstack1ll1l11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤቋ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1llll1l1lll_opy_
                log_entry.file_path = entry.bstack11l1ll1_opy_
        def bstack1lll1lll1l1_opy_():
            bstack1l1l1lllll_opy_ = datetime.now()
            try:
                self.bstack1llll111lll_opy_.LogCreatedEvent(req)
                bstack1111l1ll11_opy_.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧቌ"), datetime.now() - bstack1l1l1lllll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1l11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡽࠣቍ").format(str(e)))
                traceback.print_exc()
        self.bstack1llll11l111_opy_.enqueue(bstack1lll1lll1l1_opy_)
    def __1l1lll11ll1_opy_(self, instance) -> None:
        bstack1ll1l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ቎")
        bstack1ll11ll1l11_opy_ = {bstack1ll1l11_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨ቏"): bstack1ll1111l1ll_opy_.bstack1ll11ll111l_opy_()}
        TestFramework.bstack1l1llllllll_opy_(instance, bstack1ll11ll1l11_opy_)
    @staticmethod
    def __1ll11l1ll1l_opy_(instance, args):
        request, bstack1l1lll1l1ll_opy_ = args
        bstack1ll1111l111_opy_ = id(bstack1l1lll1l1ll_opy_)
        bstack1l1lll11l11_opy_ = instance.data[TestFramework.bstack1ll11l111l1_opy_]
        step = next(filter(lambda st: st[bstack1ll1l11_opy_ (u"ࠬ࡯ࡤࠨቐ")] == bstack1ll1111l111_opy_, bstack1l1lll11l11_opy_[bstack1ll1l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬቑ")]), None)
        step.update({
            bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫቒ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l1lll11l11_opy_[bstack1ll1l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧቓ")]) if st[bstack1ll1l11_opy_ (u"ࠩ࡬ࡨࠬቔ")] == step[bstack1ll1l11_opy_ (u"ࠪ࡭ࡩ࠭ቕ")]), None)
        if index is not None:
            bstack1l1lll11l11_opy_[bstack1ll1l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪቖ")][index] = step
        instance.data[TestFramework.bstack1ll11l111l1_opy_] = bstack1l1lll11l11_opy_
    @staticmethod
    def __1ll111l1lll_opy_(instance, args):
        bstack1ll1l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡬ࡪࡴࠠ࡭ࡧࡱࠤࡦࡸࡧࡴࠢ࡬ࡷࠥ࠸ࠬࠡ࡫ࡷࠤࡸ࡯ࡧ࡯࡫ࡩ࡭ࡪࡹࠠࡵࡪࡨࡶࡪࠦࡩࡴࠢࡱࡳࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡡࡳࡩࡶࠤࡦࡸࡥࠡ࠯ࠣ࡟ࡷ࡫ࡱࡶࡧࡶࡸ࠱ࠦࡳࡵࡧࡳࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࡩࡧࠢࡤࡶ࡬ࡹࠠࡢࡴࡨࠤ࠸ࠦࡴࡩࡧࡱࠤࡹ࡮ࡥࠡ࡮ࡤࡷࡹࠦࡶࡢ࡮ࡸࡩࠥ࡯ࡳࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ቗")
        bstack1l1lll1lll1_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l1lll1l1ll_opy_ = args[1]
        bstack1ll1111l111_opy_ = id(bstack1l1lll1l1ll_opy_)
        bstack1l1lll11l11_opy_ = instance.data[TestFramework.bstack1ll11l111l1_opy_]
        step = None
        if bstack1ll1111l111_opy_ is not None and bstack1l1lll11l11_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬቘ")):
            step = next(filter(lambda st: st[bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪ቙")] == bstack1ll1111l111_opy_, bstack1l1lll11l11_opy_[bstack1ll1l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧቚ")]), None)
            step.update({
                bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧቛ"): bstack1l1lll1lll1_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1ll1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪቜ"): bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫቝ"),
                bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭቞"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1ll1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭቟"): bstack1ll1l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧበ"),
                })
        index = next((i for i, st in enumerate(bstack1l1lll11l11_opy_[bstack1ll1l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧቡ")]) if st[bstack1ll1l11_opy_ (u"ࠩ࡬ࡨࠬቢ")] == step[bstack1ll1l11_opy_ (u"ࠪ࡭ࡩ࠭ባ")]), None)
        if index is not None:
            bstack1l1lll11l11_opy_[bstack1ll1l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪቤ")][index] = step
        instance.data[TestFramework.bstack1ll11l111l1_opy_] = bstack1l1lll11l11_opy_
    @staticmethod
    def __1ll11l11lll_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1ll1l11_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧብ")):
                examples = list(node.callspec.params[bstack1ll1l11_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬቦ")].values())
            return examples
        except:
            return []
    def bstack1llll111111_opy_(self, instance: bstack11111l111l_opy_, bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_]):
        bstack1ll111111l1_opy_ = (
            PytestBDDFramework.bstack1ll11l1lll1_opy_
            if bstack111111111l_opy_[1] == bstack1111111l1l_opy_.PRE
            else PytestBDDFramework.bstack1l1lll11111_opy_
        )
        hook = PytestBDDFramework.bstack1ll111l111l_opy_(instance, bstack1ll111111l1_opy_)
        entries = hook.get(TestFramework.bstack1l1llll11ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1l1llll111l_opy_, []))
        return entries
    def bstack1llll1l1111_opy_(self, instance: bstack11111l111l_opy_, bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_]):
        bstack1ll111111l1_opy_ = (
            PytestBDDFramework.bstack1ll11l1lll1_opy_
            if bstack111111111l_opy_[1] == bstack1111111l1l_opy_.PRE
            else PytestBDDFramework.bstack1l1lll11111_opy_
        )
        PytestBDDFramework.bstack1ll1111l11l_opy_(instance, bstack1ll111111l1_opy_)
        TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1l1llll111l_opy_, []).clear()
    @staticmethod
    def bstack1ll111l111l_opy_(instance: bstack11111l111l_opy_, bstack1ll111111l1_opy_: str):
        bstack1ll111l1l1l_opy_ = (
            PytestBDDFramework.bstack1l1lll1ll1l_opy_
            if bstack1ll111111l1_opy_ == PytestBDDFramework.bstack1l1lll11111_opy_
            else PytestBDDFramework.bstack1ll111111ll_opy_
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
        hook = PytestBDDFramework.bstack1ll111l111l_opy_(instance, bstack1ll111111l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1llll11ll_opy_, []).clear()
    @staticmethod
    def __1l1ll1lll1l_opy_(instance: bstack11111l111l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1ll1l11_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡣࡰࡴࡧࡷࠧቧ"), None)):
            return
        if os.getenv(bstack1ll1l11_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧቨ"), bstack1ll1l11_opy_ (u"ࠤ࠴ࠦቩ")) != bstack1ll1l11_opy_ (u"ࠥ࠵ࠧቪ"):
            PytestBDDFramework.logger.warning(bstack1ll1l11_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡣࡢࡲ࡯ࡳ࡬ࠨቫ"))
            return
        bstack1ll11111l1l_opy_ = {
            bstack1ll1l11_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦቬ"): (PytestBDDFramework.bstack1ll11l1lll1_opy_, PytestBDDFramework.bstack1ll111111ll_opy_),
            bstack1ll1l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣቭ"): (PytestBDDFramework.bstack1l1lll11111_opy_, PytestBDDFramework.bstack1l1lll1ll1l_opy_),
        }
        for when in (bstack1ll1l11_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨቮ"), bstack1ll1l11_opy_ (u"ࠣࡥࡤࡰࡱࠨቯ"), bstack1ll1l11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦተ")):
            bstack1l1llll1111_opy_ = args[1].get_records(when)
            if not bstack1l1llll1111_opy_:
                continue
            records = [
                bstack111111llll_opy_(
                    kind=TestFramework.bstack1lllll11ll1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1ll1l11_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࡰࡤࡱࡪࠨቱ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1ll1l11_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࠧቲ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l1llll1111_opy_
                if isinstance(getattr(r, bstack1ll1l11_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨታ"), None), str) and r.message.strip()
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
    def __1ll11111l11_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1l1llll111_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1ll1111l1l1_opy_(request.node, scenario)
        bstack1ll1111lll1_opy_ = feature.filename
        if not bstack1l1llll111_opy_ or not test_name or not bstack1ll1111lll1_opy_:
            return None
        code = None
        return {
            TestFramework.bstack11111111ll_opy_: uuid4().__str__(),
            TestFramework.bstack1l1lll1llll_opy_: bstack1l1llll111_opy_,
            TestFramework.bstack1111l111ll_opy_: test_name,
            TestFramework.bstack11111lll1l_opy_: bstack1l1llll111_opy_,
            TestFramework.bstack1l1lll1l1l1_opy_: bstack1ll1111lll1_opy_,
            TestFramework.bstack1ll111l1ll1_opy_: PytestBDDFramework.__1ll11l1llll_opy_(feature, scenario),
            TestFramework.bstack1l1lll111ll_opy_: code,
            TestFramework.bstack1lll111111l_opy_: TestFramework.bstack1ll11l11ll1_opy_,
            TestFramework.bstack1ll1l1l11ll_opy_: test_name
        }
    @staticmethod
    def __1ll1111l1l1_opy_(node, scenario):
        if hasattr(node, bstack1ll1l11_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨቴ")):
            parts = node.nodeid.rsplit(bstack1ll1l11_opy_ (u"ࠢ࡜ࠤት"))
            params = parts[-1]
            return bstack1ll1l11_opy_ (u"ࠣࡽࢀࠤࡠࢁࡽࠣቶ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1ll11l1llll_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1ll1l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧቷ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1ll1l11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨቸ")) else [])
    @staticmethod
    def __1l1lllll11l_opy_(location):
        return bstack1ll1l11_opy_ (u"ࠦ࠿ࡀࠢቹ").join(filter(lambda x: isinstance(x, str), location))