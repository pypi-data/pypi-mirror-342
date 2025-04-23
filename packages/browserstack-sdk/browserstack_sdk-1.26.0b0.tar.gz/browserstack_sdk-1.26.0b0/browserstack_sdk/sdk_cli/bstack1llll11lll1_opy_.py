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
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1111l11ll1_opy_ import bstack11111l1l11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1ll111_opy_ import bstack1l111ll1111_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1llll1l11ll_opy_,
    bstack1lll1l1l1l1_opy_,
    bstack1llllll1l11_opy_,
    bstack1l11ll1111l_opy_,
    bstack1ll1lllllll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1llll111l_opy_
from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll111l1l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1111l1ll11_opy_ import bstack1111l1l1ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll1lllll1_opy_ import bstack1lll11l1l1l_opy_
from bstack_utils.bstack11l11l11l1_opy_ import bstack11lll1l1_opy_
bstack1ll1111111l_opy_ = bstack1l1llll111l_opy_()
bstack1l11ll1l1l1_opy_ = 1.0
bstack1l1ll1lllll_opy_ = bstack11111ll_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᐖ")
bstack1l111l1l111_opy_ = bstack11111ll_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᐗ")
bstack1l111l11l11_opy_ = bstack11111ll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᐘ")
bstack1l111l11lll_opy_ = bstack11111ll_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥᐙ")
bstack1l111l11ll1_opy_ = bstack11111ll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢᐚ")
_1ll111ll111_opy_ = set()
class bstack1lll1ll1l11_opy_(TestFramework):
    bstack1l111l1l1l1_opy_ = bstack11111ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤᐛ")
    bstack1l111llllll_opy_ = bstack11111ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᐜ")
    bstack1l11l11ll11_opy_ = bstack11111ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᐝ")
    bstack1l11l1lllll_opy_ = bstack11111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪࠢᐞ")
    bstack1l11l11l1l1_opy_ = bstack11111ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᐟ")
    bstack1l11l1lll1l_opy_: bool
    bstack1111l1ll11_opy_: bstack1111l1l1ll_opy_  = None
    bstack1llll1l1111_opy_ = None
    bstack1l11ll1l111_opy_ = [
        bstack1llll1l11ll_opy_.BEFORE_ALL,
        bstack1llll1l11ll_opy_.AFTER_ALL,
        bstack1llll1l11ll_opy_.BEFORE_EACH,
        bstack1llll1l11ll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111lllll1_opy_: Dict[str, str],
        bstack1ll1l111ll1_opy_: List[str]=[bstack11111ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᐠ")],
        bstack1111l1ll11_opy_: bstack1111l1l1ll_opy_=None,
        bstack1llll1l1111_opy_=None
    ):
        super().__init__(bstack1ll1l111ll1_opy_, bstack1l111lllll1_opy_, bstack1111l1ll11_opy_)
        self.bstack1l11l1lll1l_opy_ = any(bstack11111ll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᐡ") in item.lower() for item in bstack1ll1l111ll1_opy_)
        self.bstack1llll1l1111_opy_ = bstack1llll1l1111_opy_
    def track_event(
        self,
        context: bstack1l11ll1111l_opy_,
        test_framework_state: bstack1llll1l11ll_opy_,
        test_hook_state: bstack1llllll1l11_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1llll1l11ll_opy_.TEST or test_framework_state in bstack1lll1ll1l11_opy_.bstack1l11ll1l111_opy_:
            bstack1l111ll1111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1llll1l11ll_opy_.NONE:
            self.logger.warning(bstack11111ll_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࠥᐢ") + str(test_hook_state) + bstack11111ll_opy_ (u"ࠥࠦᐣ"))
            return
        if not self.bstack1l11l1lll1l_opy_:
            self.logger.warning(bstack11111ll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡁࠧᐤ") + str(str(self.bstack1ll1l111ll1_opy_)) + bstack11111ll_opy_ (u"ࠧࠨᐥ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11111ll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᐦ") + str(kwargs) + bstack11111ll_opy_ (u"ࠢࠣᐧ"))
            return
        instance = self.__1l11l11111l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11111ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡣࡵ࡫ࡸࡃࠢᐨ") + str(args) + bstack11111ll_opy_ (u"ࠤࠥᐩ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1lll1ll1l11_opy_.bstack1l11ll1l111_opy_ and test_hook_state == bstack1llllll1l11_opy_.PRE:
                bstack1ll1ll1l1ll_opy_ = bstack1llll111l1l_opy_.bstack1ll1l111lll_opy_(EVENTS.bstack111l1111_opy_.value)
                name = str(EVENTS.bstack111l1111_opy_.name)+bstack11111ll_opy_ (u"ࠥ࠾ࠧᐪ")+str(test_framework_state.name)
                TestFramework.bstack1l11l1l11ll_opy_(instance, name, bstack1ll1ll1l1ll_opy_)
        except Exception as e:
            self.logger.debug(bstack11111ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣᐫ").format(e))
        try:
            if not TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1l11ll11ll1_opy_) and test_hook_state == bstack1llllll1l11_opy_.PRE:
                test = bstack1lll1ll1l11_opy_.__1l11lll1l1l_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11111ll_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᐬ") + str(test_hook_state) + bstack11111ll_opy_ (u"ࠨࠢᐭ"))
            if test_framework_state == bstack1llll1l11ll_opy_.TEST:
                if test_hook_state == bstack1llllll1l11_opy_.PRE and not TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1ll111l11ll_opy_):
                    TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1ll111l11ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11111ll_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᐮ") + str(test_hook_state) + bstack11111ll_opy_ (u"ࠣࠤᐯ"))
                elif test_hook_state == bstack1llllll1l11_opy_.POST and not TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1ll111l111l_opy_):
                    TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1ll111l111l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11111ll_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᐰ") + str(test_hook_state) + bstack11111ll_opy_ (u"ࠥࠦᐱ"))
            elif test_framework_state == bstack1llll1l11ll_opy_.LOG and test_hook_state == bstack1llllll1l11_opy_.POST:
                bstack1lll1ll1l11_opy_.__1l111llll1l_opy_(instance, *args)
            elif test_framework_state == bstack1llll1l11ll_opy_.LOG_REPORT and test_hook_state == bstack1llllll1l11_opy_.POST:
                self.__1l11l111lll_opy_(instance, *args)
                self.__1l11lll1ll1_opy_(instance)
            elif test_framework_state in bstack1lll1ll1l11_opy_.bstack1l11ll1l111_opy_:
                self.__1l11l1l1111_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11111ll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᐲ") + str(instance.ref()) + bstack11111ll_opy_ (u"ࠧࠨᐳ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11l11l1ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1lll1ll1l11_opy_.bstack1l11ll1l111_opy_ and test_hook_state == bstack1llllll1l11_opy_.POST:
                name = str(EVENTS.bstack111l1111_opy_.name)+bstack11111ll_opy_ (u"ࠨ࠺ࠣᐴ")+str(test_framework_state.name)
                bstack1ll1ll1l1ll_opy_ = TestFramework.bstack1l11ll1lll1_opy_(instance, name)
                bstack1llll111l1l_opy_.end(EVENTS.bstack111l1111_opy_.value, bstack1ll1ll1l1ll_opy_+bstack11111ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᐵ"), bstack1ll1ll1l1ll_opy_+bstack11111ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᐶ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11111ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᐷ").format(e))
    def bstack1l1lll11l1l_opy_(self):
        return self.bstack1l11l1lll1l_opy_
    def __1l11lll1l11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11111ll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᐸ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll11l111l1_opy_(rep, [bstack11111ll_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤᐹ"), bstack11111ll_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᐺ"), bstack11111ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᐻ"), bstack11111ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᐼ"), bstack11111ll_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤᐽ"), bstack11111ll_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᐾ")])
        return None
    def __1l11l111lll_opy_(self, instance: bstack1lll1l1l1l1_opy_, *args):
        result = self.__1l11lll1l11_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111ll1l11_opy_ = None
        if result.get(bstack11111ll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᐿ"), None) == bstack11111ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᑀ") and len(args) > 1 and getattr(args[1], bstack11111ll_opy_ (u"ࠧ࡫ࡸࡤ࡫ࡱࡪࡴࠨᑁ"), None) is not None:
            failure = [{bstack11111ll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᑂ"): [args[1].excinfo.exconly(), result.get(bstack11111ll_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᑃ"), None)]}]
            bstack1111ll1l11_opy_ = bstack11111ll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᑄ") if bstack11111ll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᑅ") in getattr(args[1].excinfo, bstack11111ll_opy_ (u"ࠥࡸࡾࡶࡥ࡯ࡣࡰࡩࠧᑆ"), bstack11111ll_opy_ (u"ࠦࠧᑇ")) else bstack11111ll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᑈ")
        bstack1l11llll1l1_opy_ = result.get(bstack11111ll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᑉ"), TestFramework.bstack1l11l1l111l_opy_)
        if bstack1l11llll1l1_opy_ != TestFramework.bstack1l11l1l111l_opy_:
            TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1l1llll11ll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11lll111l_opy_(instance, {
            TestFramework.bstack1l1l1llll11_opy_: failure,
            TestFramework.bstack1l11l11lll1_opy_: bstack1111ll1l11_opy_,
            TestFramework.bstack1l1l1lll1l1_opy_: bstack1l11llll1l1_opy_,
        })
    def __1l11l11111l_opy_(
        self,
        context: bstack1l11ll1111l_opy_,
        test_framework_state: bstack1llll1l11ll_opy_,
        test_hook_state: bstack1llllll1l11_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1llll1l11ll_opy_.SETUP_FIXTURE:
            instance = self.__1l111ll1ll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11l1111l1_opy_ bstack1l111lll1l1_opy_ this to be bstack11111ll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᑊ")
            if test_framework_state == bstack1llll1l11ll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11ll1l1ll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1llll1l11ll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11111ll_opy_ (u"ࠣࡰࡲࡨࡪࠨᑋ"), None), bstack11111ll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᑌ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11111ll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᑍ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1111l111ll_opy_(target) if target else None
        return instance
    def __1l11l1l1111_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        test_framework_state: bstack1llll1l11ll_opy_,
        test_hook_state: bstack1llllll1l11_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11lll11ll_opy_ = TestFramework.bstack11111lll1l_opy_(instance, bstack1lll1ll1l11_opy_.bstack1l111llllll_opy_, {})
        if not key in bstack1l11lll11ll_opy_:
            bstack1l11lll11ll_opy_[key] = []
        bstack1l11l11ll1l_opy_ = TestFramework.bstack11111lll1l_opy_(instance, bstack1lll1ll1l11_opy_.bstack1l11l11ll11_opy_, {})
        if not key in bstack1l11l11ll1l_opy_:
            bstack1l11l11ll1l_opy_[key] = []
        bstack1l111ll11ll_opy_ = {
            bstack1lll1ll1l11_opy_.bstack1l111llllll_opy_: bstack1l11lll11ll_opy_,
            bstack1lll1ll1l11_opy_.bstack1l11l11ll11_opy_: bstack1l11l11ll1l_opy_,
        }
        if test_hook_state == bstack1llllll1l11_opy_.PRE:
            hook = {
                bstack11111ll_opy_ (u"ࠦࡰ࡫ࡹࠣᑎ"): key,
                TestFramework.bstack1l11l1l1l1l_opy_: uuid4().__str__(),
                TestFramework.bstack1l11l1l1ll1_opy_: TestFramework.bstack1l11l1l1lll_opy_,
                TestFramework.bstack1l11l111111_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11ll1l11l_opy_: [],
                TestFramework.bstack1l111lll1ll_opy_: args[1] if len(args) > 1 else bstack11111ll_opy_ (u"ࠬ࠭ᑏ"),
                TestFramework.bstack1l11lll11l1_opy_: bstack1lll11l1l1l_opy_.bstack1l11l11llll_opy_()
            }
            bstack1l11lll11ll_opy_[key].append(hook)
            bstack1l111ll11ll_opy_[bstack1lll1ll1l11_opy_.bstack1l11l1lllll_opy_] = key
        elif test_hook_state == bstack1llllll1l11_opy_.POST:
            bstack1l111ll11l1_opy_ = bstack1l11lll11ll_opy_.get(key, [])
            hook = bstack1l111ll11l1_opy_.pop() if bstack1l111ll11l1_opy_ else None
            if hook:
                result = self.__1l11lll1l11_opy_(*args)
                if result:
                    bstack1l111ll1l1l_opy_ = result.get(bstack11111ll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᑐ"), TestFramework.bstack1l11l1l1lll_opy_)
                    if bstack1l111ll1l1l_opy_ != TestFramework.bstack1l11l1l1lll_opy_:
                        hook[TestFramework.bstack1l11l1l1ll1_opy_] = bstack1l111ll1l1l_opy_
                hook[TestFramework.bstack1l11l1llll1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11lll11l1_opy_]= bstack1lll11l1l1l_opy_.bstack1l11l11llll_opy_()
                self.bstack1l11l1l11l1_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11l1lll11_opy_, [])
                if logs: self.bstack1l1lll111l1_opy_(instance, logs)
                bstack1l11l11ll1l_opy_[key].append(hook)
                bstack1l111ll11ll_opy_[bstack1lll1ll1l11_opy_.bstack1l11l11l1l1_opy_] = key
        TestFramework.bstack1l11lll111l_opy_(instance, bstack1l111ll11ll_opy_)
        self.logger.debug(bstack11111ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻ࡬ࡧࡼࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥ࠿ࡾ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࡂࠨᑑ") + str(bstack1l11l11ll1l_opy_) + bstack11111ll_opy_ (u"ࠣࠤᑒ"))
    def __1l111ll1ll1_opy_(
        self,
        context: bstack1l11ll1111l_opy_,
        test_framework_state: bstack1llll1l11ll_opy_,
        test_hook_state: bstack1llllll1l11_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll11l111l1_opy_(args[0], [bstack11111ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᑓ"), bstack11111ll_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦᑔ"), bstack11111ll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᑕ"), bstack11111ll_opy_ (u"ࠧ࡯ࡤࡴࠤᑖ"), bstack11111ll_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣᑗ"), bstack11111ll_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᑘ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack11111ll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᑙ")) else fixturedef.get(bstack11111ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᑚ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11111ll_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣᑛ")) else None
        node = request.node if hasattr(request, bstack11111ll_opy_ (u"ࠦࡳࡵࡤࡦࠤᑜ")) else None
        target = request.node.nodeid if hasattr(node, bstack11111ll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᑝ")) else None
        baseid = fixturedef.get(bstack11111ll_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᑞ"), None) or bstack11111ll_opy_ (u"ࠢࠣᑟ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11111ll_opy_ (u"ࠣࡡࡳࡽ࡫ࡻ࡮ࡤ࡫ࡷࡩࡲࠨᑠ")):
            target = bstack1lll1ll1l11_opy_.__1l111lll11l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11111ll_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᑡ")) else None
            if target and not TestFramework.bstack1111l111ll_opy_(target):
                self.__1l11ll1l1ll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11111ll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡴ࡯ࡥࡧࡀࡿࡳࡵࡤࡦࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᑢ") + str(test_hook_state) + bstack11111ll_opy_ (u"ࠦࠧᑣ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11111ll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᑤ") + str(target) + bstack11111ll_opy_ (u"ࠨࠢᑥ"))
            return None
        instance = TestFramework.bstack1111l111ll_opy_(target)
        if not instance:
            self.logger.warning(bstack11111ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡢࡢࡵࡨ࡭ࡩࡃࡻࡣࡣࡶࡩ࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᑦ") + str(target) + bstack11111ll_opy_ (u"ࠣࠤᑧ"))
            return None
        bstack1l11llll111_opy_ = TestFramework.bstack11111lll1l_opy_(instance, bstack1lll1ll1l11_opy_.bstack1l111l1l1l1_opy_, {})
        if os.getenv(bstack11111ll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡈࡌ࡜࡙࡛ࡒࡆࡕࠥᑨ"), bstack11111ll_opy_ (u"ࠥ࠵ࠧᑩ")) == bstack11111ll_opy_ (u"ࠦ࠶ࠨᑪ"):
            bstack1l11l11l11l_opy_ = bstack11111ll_opy_ (u"ࠧࡀࠢᑫ").join((scope, fixturename))
            bstack1l11l1ll111_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11ll11l11_opy_ = {
                bstack11111ll_opy_ (u"ࠨ࡫ࡦࡻࠥᑬ"): bstack1l11l11l11l_opy_,
                bstack11111ll_opy_ (u"ࠢࡵࡣࡪࡷࠧᑭ"): bstack1lll1ll1l11_opy_.__1l11ll1ll11_opy_(request.node),
                bstack11111ll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࠤᑮ"): fixturedef,
                bstack11111ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᑯ"): scope,
                bstack11111ll_opy_ (u"ࠥࡸࡾࡶࡥࠣᑰ"): None,
            }
            try:
                if test_hook_state == bstack1llllll1l11_opy_.POST and callable(getattr(args[-1], bstack11111ll_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᑱ"), None)):
                    bstack1l11ll11l11_opy_[bstack11111ll_opy_ (u"ࠧࡺࡹࡱࡧࠥᑲ")] = TestFramework.bstack1ll111ll1ll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1llllll1l11_opy_.PRE:
                bstack1l11ll11l11_opy_[bstack11111ll_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᑳ")] = uuid4().__str__()
                bstack1l11ll11l11_opy_[bstack1lll1ll1l11_opy_.bstack1l11l111111_opy_] = bstack1l11l1ll111_opy_
            elif test_hook_state == bstack1llllll1l11_opy_.POST:
                bstack1l11ll11l11_opy_[bstack1lll1ll1l11_opy_.bstack1l11l1llll1_opy_] = bstack1l11l1ll111_opy_
            if bstack1l11l11l11l_opy_ in bstack1l11llll111_opy_:
                bstack1l11llll111_opy_[bstack1l11l11l11l_opy_].update(bstack1l11ll11l11_opy_)
                self.logger.debug(bstack11111ll_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࠣᑴ") + str(bstack1l11llll111_opy_[bstack1l11l11l11l_opy_]) + bstack11111ll_opy_ (u"ࠣࠤᑵ"))
            else:
                bstack1l11llll111_opy_[bstack1l11l11l11l_opy_] = bstack1l11ll11l11_opy_
                self.logger.debug(bstack11111ll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡽࠡࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࠧᑶ") + str(len(bstack1l11llll111_opy_)) + bstack11111ll_opy_ (u"ࠥࠦᑷ"))
        TestFramework.bstack11111l11ll_opy_(instance, bstack1lll1ll1l11_opy_.bstack1l111l1l1l1_opy_, bstack1l11llll111_opy_)
        self.logger.debug(bstack11111ll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࢁ࡬ࡦࡰࠫࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᑸ") + str(instance.ref()) + bstack11111ll_opy_ (u"ࠧࠨᑹ"))
        return instance
    def __1l11ll1l1ll_opy_(
        self,
        context: bstack1l11ll1111l_opy_,
        test_framework_state: bstack1llll1l11ll_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack11111l1l11_opy_.create_context(target)
        ob = bstack1lll1l1l1l1_opy_(ctx, self.bstack1ll1l111ll1_opy_, self.bstack1l111lllll1_opy_, test_framework_state)
        TestFramework.bstack1l11lll111l_opy_(ob, {
            TestFramework.bstack1ll1ll1111l_opy_: context.test_framework_name,
            TestFramework.bstack1ll111l1lll_opy_: context.test_framework_version,
            TestFramework.bstack1l11l1ll1l1_opy_: [],
            bstack1lll1ll1l11_opy_.bstack1l111l1l1l1_opy_: {},
            bstack1lll1ll1l11_opy_.bstack1l11l11ll11_opy_: {},
            bstack1lll1ll1l11_opy_.bstack1l111llllll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack11111l11ll_opy_(ob, TestFramework.bstack1l111l1ll11_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack11111l11ll_opy_(ob, TestFramework.bstack1ll1ll111ll_opy_, context.platform_index)
        TestFramework.bstack11111llll1_opy_[ctx.id] = ob
        self.logger.debug(bstack11111ll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᑺ") + str(TestFramework.bstack11111llll1_opy_.keys()) + bstack11111ll_opy_ (u"ࠢࠣᑻ"))
        return ob
    def bstack1ll1111l1ll_opy_(self, instance: bstack1lll1l1l1l1_opy_, bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_]):
        bstack1l11lll1lll_opy_ = (
            bstack1lll1ll1l11_opy_.bstack1l11l1lllll_opy_
            if bstack11111l111l_opy_[1] == bstack1llllll1l11_opy_.PRE
            else bstack1lll1ll1l11_opy_.bstack1l11l11l1l1_opy_
        )
        hook = bstack1lll1ll1l11_opy_.bstack1l111ll1lll_opy_(instance, bstack1l11lll1lll_opy_)
        entries = hook.get(TestFramework.bstack1l11ll1l11l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1l11l1ll1l1_opy_, []))
        return entries
    def bstack1ll111lll1l_opy_(self, instance: bstack1lll1l1l1l1_opy_, bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_]):
        bstack1l11lll1lll_opy_ = (
            bstack1lll1ll1l11_opy_.bstack1l11l1lllll_opy_
            if bstack11111l111l_opy_[1] == bstack1llllll1l11_opy_.PRE
            else bstack1lll1ll1l11_opy_.bstack1l11l11l1l1_opy_
        )
        bstack1lll1ll1l11_opy_.bstack1l11ll111ll_opy_(instance, bstack1l11lll1lll_opy_)
        TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1l11l1ll1l1_opy_, []).clear()
    def bstack1l11l1l11l1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11111ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡸ࡭ࡱࡪ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᑼ")
        global _1ll111ll111_opy_
        platform_index = os.environ[bstack11111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᑽ")]
        bstack1ll11l11111_opy_ = os.path.join(bstack1ll1111111l_opy_, (bstack1l1ll1lllll_opy_ + str(platform_index)), bstack1l111l11lll_opy_)
        if not os.path.exists(bstack1ll11l11111_opy_) or not os.path.isdir(bstack1ll11l11111_opy_):
            self.logger.info(bstack11111ll_opy_ (u"ࠥࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺࡳࠡࡶࡲࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࢁࡽࠣᑾ").format(bstack1ll11l11111_opy_))
            return
        logs = hook.get(bstack11111ll_opy_ (u"ࠦࡱࡵࡧࡴࠤᑿ"), [])
        with os.scandir(bstack1ll11l11111_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1ll111ll111_opy_:
                    self.logger.info(bstack11111ll_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᒀ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11111ll_opy_ (u"ࠨࠢᒁ")
                    log_entry = bstack1ll1lllllll_opy_(
                        kind=bstack11111ll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᒂ"),
                        message=bstack11111ll_opy_ (u"ࠣࠤᒃ"),
                        level=bstack11111ll_opy_ (u"ࠤࠥᒄ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1ll1111l1l1_opy_=entry.stat().st_size,
                        bstack1ll111l1l1l_opy_=bstack11111ll_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᒅ"),
                        bstack1l11ll_opy_=os.path.abspath(entry.path),
                        bstack1l111llll11_opy_=hook.get(TestFramework.bstack1l11l1l1l1l_opy_)
                    )
                    logs.append(log_entry)
                    _1ll111ll111_opy_.add(abs_path)
        platform_index = os.environ[bstack11111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᒆ")]
        bstack1l11l111l1l_opy_ = os.path.join(bstack1ll1111111l_opy_, (bstack1l1ll1lllll_opy_ + str(platform_index)), bstack1l111l11lll_opy_, bstack1l111l11ll1_opy_)
        if not os.path.exists(bstack1l11l111l1l_opy_) or not os.path.isdir(bstack1l11l111l1l_opy_):
            self.logger.info(bstack11111ll_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢᒇ").format(bstack1l11l111l1l_opy_))
        else:
            self.logger.info(bstack11111ll_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᒈ").format(bstack1l11l111l1l_opy_))
            with os.scandir(bstack1l11l111l1l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1ll111ll111_opy_:
                        self.logger.info(bstack11111ll_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᒉ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11111ll_opy_ (u"ࠣࠤᒊ")
                        log_entry = bstack1ll1lllllll_opy_(
                            kind=bstack11111ll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᒋ"),
                            message=bstack11111ll_opy_ (u"ࠥࠦᒌ"),
                            level=bstack11111ll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᒍ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1ll1111l1l1_opy_=entry.stat().st_size,
                            bstack1ll111l1l1l_opy_=bstack11111ll_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᒎ"),
                            bstack1l11ll_opy_=os.path.abspath(entry.path),
                            bstack1ll111llll1_opy_=hook.get(TestFramework.bstack1l11l1l1l1l_opy_)
                        )
                        logs.append(log_entry)
                        _1ll111ll111_opy_.add(abs_path)
        hook[bstack11111ll_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᒏ")] = logs
    def bstack1l1lll111l1_opy_(
        self,
        bstack1l1llll11l1_opy_: bstack1lll1l1l1l1_opy_,
        entries: List[bstack1ll1lllllll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11111ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᒐ"))
        req.platform_index = TestFramework.bstack11111lll1l_opy_(bstack1l1llll11l1_opy_, TestFramework.bstack1ll1ll111ll_opy_)
        req.execution_context.hash = str(bstack1l1llll11l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1llll11l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1llll11l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack11111lll1l_opy_(bstack1l1llll11l1_opy_, TestFramework.bstack1ll1ll1111l_opy_)
            log_entry.test_framework_version = TestFramework.bstack11111lll1l_opy_(bstack1l1llll11l1_opy_, TestFramework.bstack1ll111l1lll_opy_)
            log_entry.uuid = entry.bstack1l111llll11_opy_
            log_entry.test_framework_state = bstack1l1llll11l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11111ll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᒑ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11111ll_opy_ (u"ࠤࠥᒒ")
            if entry.kind == bstack11111ll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᒓ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1ll1111l1l1_opy_
                log_entry.file_path = entry.bstack1l11ll_opy_
        def bstack1l1lll1l11l_opy_():
            bstack11ll111l1l_opy_ = datetime.now()
            try:
                self.bstack1llll1l1111_opy_.LogCreatedEvent(req)
                bstack1l1llll11l1_opy_.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᒔ"), datetime.now() - bstack11ll111l1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11111ll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࢀࠦᒕ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l1ll11_opy_.enqueue(bstack1l1lll1l11l_opy_)
    def __1l11lll1ll1_opy_(self, instance) -> None:
        bstack11111ll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᒖ")
        bstack1l111ll11ll_opy_ = {bstack11111ll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᒗ"): bstack1lll11l1l1l_opy_.bstack1l11l11llll_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l11lll111l_opy_(instance, bstack1l111ll11ll_opy_)
    @staticmethod
    def bstack1l111ll1lll_opy_(instance: bstack1lll1l1l1l1_opy_, bstack1l11lll1lll_opy_: str):
        bstack1l111l1l1ll_opy_ = (
            bstack1lll1ll1l11_opy_.bstack1l11l11ll11_opy_
            if bstack1l11lll1lll_opy_ == bstack1lll1ll1l11_opy_.bstack1l11l11l1l1_opy_
            else bstack1lll1ll1l11_opy_.bstack1l111llllll_opy_
        )
        bstack1l11ll11lll_opy_ = TestFramework.bstack11111lll1l_opy_(instance, bstack1l11lll1lll_opy_, None)
        bstack1l111l1ll1l_opy_ = TestFramework.bstack11111lll1l_opy_(instance, bstack1l111l1l1ll_opy_, None) if bstack1l11ll11lll_opy_ else None
        return (
            bstack1l111l1ll1l_opy_[bstack1l11ll11lll_opy_][-1]
            if isinstance(bstack1l111l1ll1l_opy_, dict) and len(bstack1l111l1ll1l_opy_.get(bstack1l11ll11lll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l11ll111ll_opy_(instance: bstack1lll1l1l1l1_opy_, bstack1l11lll1lll_opy_: str):
        hook = bstack1lll1ll1l11_opy_.bstack1l111ll1lll_opy_(instance, bstack1l11lll1lll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11ll1l11l_opy_, []).clear()
    @staticmethod
    def __1l111llll1l_opy_(instance: bstack1lll1l1l1l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11111ll_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡤࡱࡵࡨࡸࠨᒘ"), None)):
            return
        if os.getenv(bstack11111ll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨᒙ"), bstack11111ll_opy_ (u"ࠥ࠵ࠧᒚ")) != bstack11111ll_opy_ (u"ࠦ࠶ࠨᒛ"):
            bstack1lll1ll1l11_opy_.logger.warning(bstack11111ll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡤࡣࡳࡰࡴ࡭ࠢᒜ"))
            return
        bstack1l11l1ll1ll_opy_ = {
            bstack11111ll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᒝ"): (bstack1lll1ll1l11_opy_.bstack1l11l1lllll_opy_, bstack1lll1ll1l11_opy_.bstack1l111llllll_opy_),
            bstack11111ll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᒞ"): (bstack1lll1ll1l11_opy_.bstack1l11l11l1l1_opy_, bstack1lll1ll1l11_opy_.bstack1l11l11ll11_opy_),
        }
        for when in (bstack11111ll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᒟ"), bstack11111ll_opy_ (u"ࠤࡦࡥࡱࡲࠢᒠ"), bstack11111ll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᒡ")):
            bstack1l111l1llll_opy_ = args[1].get_records(when)
            if not bstack1l111l1llll_opy_:
                continue
            records = [
                bstack1ll1lllllll_opy_(
                    kind=TestFramework.bstack1l1llllll1l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11111ll_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠢᒢ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11111ll_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠨᒣ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111l1llll_opy_
                if isinstance(getattr(r, bstack11111ll_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᒤ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11ll1ll1l_opy_, bstack1l111l1l1ll_opy_ = bstack1l11l1ll1ll_opy_.get(when, (None, None))
            bstack1l11ll11111_opy_ = TestFramework.bstack11111lll1l_opy_(instance, bstack1l11ll1ll1l_opy_, None) if bstack1l11ll1ll1l_opy_ else None
            bstack1l111l1ll1l_opy_ = TestFramework.bstack11111lll1l_opy_(instance, bstack1l111l1l1ll_opy_, None) if bstack1l11ll11111_opy_ else None
            if isinstance(bstack1l111l1ll1l_opy_, dict) and len(bstack1l111l1ll1l_opy_.get(bstack1l11ll11111_opy_, [])) > 0:
                hook = bstack1l111l1ll1l_opy_[bstack1l11ll11111_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11ll1l11l_opy_ in hook:
                    hook[TestFramework.bstack1l11ll1l11l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1l11l1ll1l1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l11lll1l1l_opy_(test) -> Dict[str, Any]:
        bstack11lll111l_opy_ = bstack1lll1ll1l11_opy_.__1l111lll11l_opy_(test.location) if hasattr(test, bstack11111ll_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᒥ")) else getattr(test, bstack11111ll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᒦ"), None)
        test_name = test.name if hasattr(test, bstack11111ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᒧ")) else None
        bstack1l111ll1l11_opy_ = test.fspath.strpath if hasattr(test, bstack11111ll_opy_ (u"ࠥࡪࡸࡶࡡࡵࡪࠥᒨ")) and test.fspath else None
        if not bstack11lll111l_opy_ or not test_name or not bstack1l111ll1l11_opy_:
            return None
        code = None
        if hasattr(test, bstack11111ll_opy_ (u"ࠦࡴࡨࡪࠣᒩ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l111l1l11l_opy_ = []
        try:
            bstack1l111l1l11l_opy_ = bstack11lll1l1_opy_.bstack111l1l111l_opy_(test)
        except:
            bstack1lll1ll1l11_opy_.logger.warning(bstack11111ll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶ࠰ࠥࡺࡥࡴࡶࠣࡷࡨࡵࡰࡦࡵࠣࡻ࡮ࡲ࡬ࠡࡤࡨࠤࡷ࡫ࡳࡰ࡮ࡹࡩࡩࠦࡩ࡯ࠢࡆࡐࡎࠨᒪ"))
        return {
            TestFramework.bstack1ll1ll1lll1_opy_: uuid4().__str__(),
            TestFramework.bstack1l11ll11ll1_opy_: bstack11lll111l_opy_,
            TestFramework.bstack1ll1lll111l_opy_: test_name,
            TestFramework.bstack1l1ll1ll111_opy_: getattr(test, bstack11111ll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᒫ"), None),
            TestFramework.bstack1l11l111l11_opy_: bstack1l111ll1l11_opy_,
            TestFramework.bstack1l11llll11l_opy_: bstack1lll1ll1l11_opy_.__1l11ll1ll11_opy_(test),
            TestFramework.bstack1l11l111ll1_opy_: code,
            TestFramework.bstack1l1l1lll1l1_opy_: TestFramework.bstack1l11l1l111l_opy_,
            TestFramework.bstack1l1l1111lll_opy_: bstack11lll111l_opy_,
            TestFramework.bstack1l111l11l1l_opy_: bstack1l111l1l11l_opy_
        }
    @staticmethod
    def __1l11ll1ll11_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack11111ll_opy_ (u"ࠢࡰࡹࡱࡣࡲࡧࡲ࡬ࡧࡵࡷࠧᒬ"), [])
            markers.extend([getattr(m, bstack11111ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᒭ"), None) for m in own_markers if getattr(m, bstack11111ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᒮ"), None)])
            current = getattr(current, bstack11111ll_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥᒯ"), None)
        return markers
    @staticmethod
    def __1l111lll11l_opy_(location):
        return bstack11111ll_opy_ (u"ࠦ࠿ࡀࠢᒰ").join(filter(lambda x: isinstance(x, str), location))