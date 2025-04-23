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
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1llll1l11ll_opy_,
    bstack1lll1l1l1l1_opy_,
    bstack1llllll1l11_opy_,
    bstack1l11ll1111l_opy_,
    bstack1ll1lllllll_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1llll111l_opy_
from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll111l1l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1lll1lllll1_opy_ import bstack1lll11l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1111l1ll11_opy_ import bstack1111l1l1ll_opy_
bstack1ll1111111l_opy_ = bstack1l1llll111l_opy_()
bstack1l1ll1lllll_opy_ = bstack11111ll_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨ።")
bstack1l11l1ll11l_opy_ = bstack11111ll_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥ፣")
bstack1l111lll111_opy_ = bstack11111ll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ፤")
bstack1l11ll1l1l1_opy_ = 1.0
_1ll111ll111_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l111l1l1l1_opy_ = bstack11111ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤ፥")
    bstack1l111llllll_opy_ = bstack11111ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣ፦")
    bstack1l11l11ll11_opy_ = bstack11111ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥ፧")
    bstack1l11l1lllll_opy_ = bstack11111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪࠢ፨")
    bstack1l11l11l1l1_opy_ = bstack11111ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤ፩")
    bstack1l11l1lll1l_opy_: bool
    bstack1111l1ll11_opy_: bstack1111l1l1ll_opy_  = None
    bstack1l11ll1l111_opy_ = [
        bstack1llll1l11ll_opy_.BEFORE_ALL,
        bstack1llll1l11ll_opy_.AFTER_ALL,
        bstack1llll1l11ll_opy_.BEFORE_EACH,
        bstack1llll1l11ll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111lllll1_opy_: Dict[str, str],
        bstack1ll1l111ll1_opy_: List[str]=[bstack11111ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦ፪")],
        bstack1111l1ll11_opy_: bstack1111l1l1ll_opy_ = None,
        bstack1llll1l1111_opy_=None
    ):
        super().__init__(bstack1ll1l111ll1_opy_, bstack1l111lllll1_opy_, bstack1111l1ll11_opy_)
        self.bstack1l11l1lll1l_opy_ = any(bstack11111ll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧ፫") in item.lower() for item in bstack1ll1l111ll1_opy_)
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
        if test_framework_state == bstack1llll1l11ll_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l11ll1l111_opy_:
            bstack1l111ll1111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1llll1l11ll_opy_.NONE:
            self.logger.warning(bstack11111ll_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࠥ፬") + str(test_hook_state) + bstack11111ll_opy_ (u"ࠥࠦ፭"))
            return
        if not self.bstack1l11l1lll1l_opy_:
            self.logger.warning(bstack11111ll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡁࠧ፮") + str(str(self.bstack1ll1l111ll1_opy_)) + bstack11111ll_opy_ (u"ࠧࠨ፯"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11111ll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ፰") + str(kwargs) + bstack11111ll_opy_ (u"ࠢࠣ፱"))
            return
        instance = self.__1l11l11111l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11111ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡣࡵ࡫ࡸࡃࠢ፲") + str(args) + bstack11111ll_opy_ (u"ࠤࠥ፳"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11ll1l111_opy_ and test_hook_state == bstack1llllll1l11_opy_.PRE:
                bstack1ll1ll1l1ll_opy_ = bstack1llll111l1l_opy_.bstack1ll1l111lll_opy_(EVENTS.bstack111l1111_opy_.value)
                name = str(EVENTS.bstack111l1111_opy_.name)+bstack11111ll_opy_ (u"ࠥ࠾ࠧ፴")+str(test_framework_state.name)
                TestFramework.bstack1l11l1l11ll_opy_(instance, name, bstack1ll1ll1l1ll_opy_)
        except Exception as e:
            self.logger.debug(bstack11111ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣ፵").format(e))
        try:
            if test_framework_state == bstack1llll1l11ll_opy_.TEST:
                if not TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1l11ll11ll1_opy_) and test_hook_state == bstack1llllll1l11_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l11lll1l1l_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack11111ll_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧ፶") + str(test_hook_state) + bstack11111ll_opy_ (u"ࠨࠢ፷"))
                if test_hook_state == bstack1llllll1l11_opy_.PRE and not TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1ll111l11ll_opy_):
                    TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1ll111l11ll_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11lll1111_opy_(instance, args)
                    self.logger.debug(bstack11111ll_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧ፸") + str(test_hook_state) + bstack11111ll_opy_ (u"ࠣࠤ፹"))
                elif test_hook_state == bstack1llllll1l11_opy_.POST and not TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1ll111l111l_opy_):
                    TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1ll111l111l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11111ll_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧ፺") + str(test_hook_state) + bstack11111ll_opy_ (u"ࠥࠦ፻"))
            elif test_framework_state == bstack1llll1l11ll_opy_.STEP:
                if test_hook_state == bstack1llllll1l11_opy_.PRE:
                    PytestBDDFramework.__1l11ll111l1_opy_(instance, args)
                elif test_hook_state == bstack1llllll1l11_opy_.POST:
                    PytestBDDFramework.__1l11l1l1l11_opy_(instance, args)
            elif test_framework_state == bstack1llll1l11ll_opy_.LOG and test_hook_state == bstack1llllll1l11_opy_.POST:
                PytestBDDFramework.__1l111llll1l_opy_(instance, *args)
            elif test_framework_state == bstack1llll1l11ll_opy_.LOG_REPORT and test_hook_state == bstack1llllll1l11_opy_.POST:
                self.__1l11l111lll_opy_(instance, *args)
                self.__1l11lll1ll1_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l11ll1l111_opy_:
                self.__1l11l1l1111_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11111ll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧ፼") + str(instance.ref()) + bstack11111ll_opy_ (u"ࠧࠨ፽"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11l11l1ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11ll1l111_opy_ and test_hook_state == bstack1llllll1l11_opy_.POST:
                name = str(EVENTS.bstack111l1111_opy_.name)+bstack11111ll_opy_ (u"ࠨ࠺ࠣ፾")+str(test_framework_state.name)
                bstack1ll1ll1l1ll_opy_ = TestFramework.bstack1l11ll1lll1_opy_(instance, name)
                bstack1llll111l1l_opy_.end(EVENTS.bstack111l1111_opy_.value, bstack1ll1ll1l1ll_opy_+bstack11111ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ፿"), bstack1ll1ll1l1ll_opy_+bstack11111ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᎀ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11111ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᎁ").format(e))
    def bstack1l1lll11l1l_opy_(self):
        return self.bstack1l11l1lll1l_opy_
    def __1l11lll1l11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11111ll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᎂ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll11l111l1_opy_(rep, [bstack11111ll_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤᎃ"), bstack11111ll_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᎄ"), bstack11111ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᎅ"), bstack11111ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᎆ"), bstack11111ll_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤᎇ"), bstack11111ll_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᎈ")])
        return None
    def __1l11l111lll_opy_(self, instance: bstack1lll1l1l1l1_opy_, *args):
        result = self.__1l11lll1l11_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111ll1l11_opy_ = None
        if result.get(bstack11111ll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᎉ"), None) == bstack11111ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᎊ") and len(args) > 1 and getattr(args[1], bstack11111ll_opy_ (u"ࠧ࡫ࡸࡤ࡫ࡱࡪࡴࠨᎋ"), None) is not None:
            failure = [{bstack11111ll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᎌ"): [args[1].excinfo.exconly(), result.get(bstack11111ll_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᎍ"), None)]}]
            bstack1111ll1l11_opy_ = bstack11111ll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᎎ") if bstack11111ll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᎏ") in getattr(args[1].excinfo, bstack11111ll_opy_ (u"ࠥࡸࡾࡶࡥ࡯ࡣࡰࡩࠧ᎐"), bstack11111ll_opy_ (u"ࠦࠧ᎑")) else bstack11111ll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ᎒")
        bstack1l11llll1l1_opy_ = result.get(bstack11111ll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢ᎓"), TestFramework.bstack1l11l1l111l_opy_)
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
            target = None # bstack1l11l1111l1_opy_ bstack1l111lll1l1_opy_ this to be bstack11111ll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢ᎔")
            if test_framework_state == bstack1llll1l11ll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11ll1l1ll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1llll1l11ll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11111ll_opy_ (u"ࠣࡰࡲࡨࡪࠨ᎕"), None), bstack11111ll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ᎖"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11111ll_opy_ (u"ࠥࡲࡴࡪࡥࠣ᎗"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack11111ll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦ᎘"), None):
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
        bstack1l11lll11ll_opy_ = TestFramework.bstack11111lll1l_opy_(instance, PytestBDDFramework.bstack1l111llllll_opy_, {})
        if not key in bstack1l11lll11ll_opy_:
            bstack1l11lll11ll_opy_[key] = []
        bstack1l11l11ll1l_opy_ = TestFramework.bstack11111lll1l_opy_(instance, PytestBDDFramework.bstack1l11l11ll11_opy_, {})
        if not key in bstack1l11l11ll1l_opy_:
            bstack1l11l11ll1l_opy_[key] = []
        bstack1l111ll11ll_opy_ = {
            PytestBDDFramework.bstack1l111llllll_opy_: bstack1l11lll11ll_opy_,
            PytestBDDFramework.bstack1l11l11ll11_opy_: bstack1l11l11ll1l_opy_,
        }
        if test_hook_state == bstack1llllll1l11_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack11111ll_opy_ (u"ࠧࡱࡥࡺࠤ᎙"): key,
                TestFramework.bstack1l11l1l1l1l_opy_: uuid4().__str__(),
                TestFramework.bstack1l11l1l1ll1_opy_: TestFramework.bstack1l11l1l1lll_opy_,
                TestFramework.bstack1l11l111111_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11ll1l11l_opy_: [],
                TestFramework.bstack1l111lll1ll_opy_: hook_name,
                TestFramework.bstack1l11lll11l1_opy_: bstack1lll11l1l1l_opy_.bstack1l11l11llll_opy_()
            }
            bstack1l11lll11ll_opy_[key].append(hook)
            bstack1l111ll11ll_opy_[PytestBDDFramework.bstack1l11l1lllll_opy_] = key
        elif test_hook_state == bstack1llllll1l11_opy_.POST:
            bstack1l111ll11l1_opy_ = bstack1l11lll11ll_opy_.get(key, [])
            hook = bstack1l111ll11l1_opy_.pop() if bstack1l111ll11l1_opy_ else None
            if hook:
                result = self.__1l11lll1l11_opy_(*args)
                if result:
                    bstack1l111ll1l1l_opy_ = result.get(bstack11111ll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢ᎚"), TestFramework.bstack1l11l1l1lll_opy_)
                    if bstack1l111ll1l1l_opy_ != TestFramework.bstack1l11l1l1lll_opy_:
                        hook[TestFramework.bstack1l11l1l1ll1_opy_] = bstack1l111ll1l1l_opy_
                hook[TestFramework.bstack1l11l1llll1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11lll11l1_opy_] = bstack1lll11l1l1l_opy_.bstack1l11l11llll_opy_()
                self.bstack1l11l1l11l1_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11l1lll11_opy_, [])
                self.bstack1l1lll111l1_opy_(instance, logs)
                bstack1l11l11ll1l_opy_[key].append(hook)
                bstack1l111ll11ll_opy_[PytestBDDFramework.bstack1l11l11l1l1_opy_] = key
        TestFramework.bstack1l11lll111l_opy_(instance, bstack1l111ll11ll_opy_)
        self.logger.debug(bstack11111ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻ࡬ࡧࡼࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥ࠿ࡾ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࡂࠨ᎛") + str(bstack1l11l11ll1l_opy_) + bstack11111ll_opy_ (u"ࠣࠤ᎜"))
    def __1l111ll1ll1_opy_(
        self,
        context: bstack1l11ll1111l_opy_,
        test_framework_state: bstack1llll1l11ll_opy_,
        test_hook_state: bstack1llllll1l11_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll11l111l1_opy_(args[0], [bstack11111ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣ᎝"), bstack11111ll_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦ᎞"), bstack11111ll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦ᎟"), bstack11111ll_opy_ (u"ࠧ࡯ࡤࡴࠤᎠ"), bstack11111ll_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣᎡ"), bstack11111ll_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᎢ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack11111ll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᎣ")) else fixturedef.get(bstack11111ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᎤ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11111ll_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣᎥ")) else None
        node = request.node if hasattr(request, bstack11111ll_opy_ (u"ࠦࡳࡵࡤࡦࠤᎦ")) else None
        target = request.node.nodeid if hasattr(node, bstack11111ll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᎧ")) else None
        baseid = fixturedef.get(bstack11111ll_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᎨ"), None) or bstack11111ll_opy_ (u"ࠢࠣᎩ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11111ll_opy_ (u"ࠣࡡࡳࡽ࡫ࡻ࡮ࡤ࡫ࡷࡩࡲࠨᎪ")):
            target = PytestBDDFramework.__1l111lll11l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11111ll_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᎫ")) else None
            if target and not TestFramework.bstack1111l111ll_opy_(target):
                self.__1l11ll1l1ll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11111ll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡴ࡯ࡥࡧࡀࡿࡳࡵࡤࡦࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᎬ") + str(test_hook_state) + bstack11111ll_opy_ (u"ࠦࠧᎭ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11111ll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᎮ") + str(target) + bstack11111ll_opy_ (u"ࠨࠢᎯ"))
            return None
        instance = TestFramework.bstack1111l111ll_opy_(target)
        if not instance:
            self.logger.warning(bstack11111ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡢࡢࡵࡨ࡭ࡩࡃࡻࡣࡣࡶࡩ࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᎰ") + str(target) + bstack11111ll_opy_ (u"ࠣࠤᎱ"))
            return None
        bstack1l11llll111_opy_ = TestFramework.bstack11111lll1l_opy_(instance, PytestBDDFramework.bstack1l111l1l1l1_opy_, {})
        if os.getenv(bstack11111ll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡈࡌ࡜࡙࡛ࡒࡆࡕࠥᎲ"), bstack11111ll_opy_ (u"ࠥ࠵ࠧᎳ")) == bstack11111ll_opy_ (u"ࠦ࠶ࠨᎴ"):
            bstack1l11l11l11l_opy_ = bstack11111ll_opy_ (u"ࠧࡀࠢᎵ").join((scope, fixturename))
            bstack1l11l1ll111_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11ll11l11_opy_ = {
                bstack11111ll_opy_ (u"ࠨ࡫ࡦࡻࠥᎶ"): bstack1l11l11l11l_opy_,
                bstack11111ll_opy_ (u"ࠢࡵࡣࡪࡷࠧᎷ"): PytestBDDFramework.__1l11ll1ll11_opy_(request.node, scenario),
                bstack11111ll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࠤᎸ"): fixturedef,
                bstack11111ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᎹ"): scope,
                bstack11111ll_opy_ (u"ࠥࡸࡾࡶࡥࠣᎺ"): None,
            }
            try:
                if test_hook_state == bstack1llllll1l11_opy_.POST and callable(getattr(args[-1], bstack11111ll_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᎻ"), None)):
                    bstack1l11ll11l11_opy_[bstack11111ll_opy_ (u"ࠧࡺࡹࡱࡧࠥᎼ")] = TestFramework.bstack1ll111ll1ll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1llllll1l11_opy_.PRE:
                bstack1l11ll11l11_opy_[bstack11111ll_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᎽ")] = uuid4().__str__()
                bstack1l11ll11l11_opy_[PytestBDDFramework.bstack1l11l111111_opy_] = bstack1l11l1ll111_opy_
            elif test_hook_state == bstack1llllll1l11_opy_.POST:
                bstack1l11ll11l11_opy_[PytestBDDFramework.bstack1l11l1llll1_opy_] = bstack1l11l1ll111_opy_
            if bstack1l11l11l11l_opy_ in bstack1l11llll111_opy_:
                bstack1l11llll111_opy_[bstack1l11l11l11l_opy_].update(bstack1l11ll11l11_opy_)
                self.logger.debug(bstack11111ll_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࠣᎾ") + str(bstack1l11llll111_opy_[bstack1l11l11l11l_opy_]) + bstack11111ll_opy_ (u"ࠣࠤᎿ"))
            else:
                bstack1l11llll111_opy_[bstack1l11l11l11l_opy_] = bstack1l11ll11l11_opy_
                self.logger.debug(bstack11111ll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡽࠡࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࠧᏀ") + str(len(bstack1l11llll111_opy_)) + bstack11111ll_opy_ (u"ࠥࠦᏁ"))
        TestFramework.bstack11111l11ll_opy_(instance, PytestBDDFramework.bstack1l111l1l1l1_opy_, bstack1l11llll111_opy_)
        self.logger.debug(bstack11111ll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࢁ࡬ࡦࡰࠫࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᏂ") + str(instance.ref()) + bstack11111ll_opy_ (u"ࠧࠨᏃ"))
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
            PytestBDDFramework.bstack1l111l1l1l1_opy_: {},
            PytestBDDFramework.bstack1l11l11ll11_opy_: {},
            PytestBDDFramework.bstack1l111llllll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack11111l11ll_opy_(ob, TestFramework.bstack1l111l1ll11_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack11111l11ll_opy_(ob, TestFramework.bstack1ll1ll111ll_opy_, context.platform_index)
        TestFramework.bstack11111llll1_opy_[ctx.id] = ob
        self.logger.debug(bstack11111ll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᏄ") + str(TestFramework.bstack11111llll1_opy_.keys()) + bstack11111ll_opy_ (u"ࠢࠣᏅ"))
        return ob
    @staticmethod
    def __1l11lll1111_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11111ll_opy_ (u"ࠨ࡫ࡧࠫᏆ"): id(step),
                bstack11111ll_opy_ (u"ࠩࡷࡩࡽࡺࠧᏇ"): step.name,
                bstack11111ll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᏈ"): step.keyword,
            })
        meta = {
            bstack11111ll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᏉ"): {
                bstack11111ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᏊ"): feature.name,
                bstack11111ll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᏋ"): feature.filename,
                bstack11111ll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᏌ"): feature.description
            },
            bstack11111ll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᏍ"): {
                bstack11111ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᏎ"): scenario.name
            },
            bstack11111ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᏏ"): steps,
            bstack11111ll_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭Ꮠ"): PytestBDDFramework.__1l11l1111ll_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l11l11l111_opy_: meta
            }
        )
    def bstack1l11l1l11l1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11111ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡵࡪࡨࠤࡏࡧࡶࡢࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡆ࡬ࡪࡩ࡫ࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡯࡮ࡴ࡫ࡧࡩࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠯ࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌ࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠰ࠥࡸࡥࡱ࡮ࡤࡧࡪࡹࠠࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢࠡ࡫ࡱࠤ࡮ࡺࡳࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡏࡦࠡࡣࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡲࡧࡴࡤࡪࡨࡷࠥࡧࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࠢ࡫ࡳࡴࡱ࠭࡭ࡧࡹࡩࡱࠦࡦࡪ࡮ࡨ࠰ࠥ࡯ࡴࠡࡥࡵࡩࡦࡺࡥࡴࠢࡤࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡷࡪࡶ࡫ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡕ࡬ࡱ࡮ࡲࡡࡳ࡮ࡼ࠰ࠥ࡯ࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦ࡬ࡰࡥࡤࡸࡪࡪࠠࡪࡰࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡨࡹࠡࡴࡨࡴࡱࡧࡣࡪࡰࡪࠤࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤ࡙࡮ࡥࠡࡥࡵࡩࡦࡺࡥࡥࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࡷࠥࡧࡲࡦࠢࡤࡨࡩ࡫ࡤࠡࡶࡲࠤࡹ࡮ࡥࠡࡪࡲࡳࡰ࠭ࡳࠡࠤ࡯ࡳ࡬ࡹࠢࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭࠽ࠤ࡙࡮ࡥࠡࡧࡹࡩࡳࡺࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴ࡭ࡳࠡࡣࡱࡨࠥ࡮࡯ࡰ࡭ࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡵࡪ࡮ࡧࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᏑ")
        global _1ll111ll111_opy_
        platform_index = os.environ[bstack11111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭Ꮢ")]
        bstack1ll11l11111_opy_ = os.path.join(bstack1ll1111111l_opy_, (bstack1l1ll1lllll_opy_ + str(platform_index)), bstack1l11l1ll11l_opy_)
        if not os.path.exists(bstack1ll11l11111_opy_) or not os.path.isdir(bstack1ll11l11111_opy_):
            return
        logs = hook.get(bstack11111ll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᏓ"), [])
        with os.scandir(bstack1ll11l11111_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1ll111ll111_opy_:
                    self.logger.info(bstack11111ll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᏔ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11111ll_opy_ (u"ࠤࠥᏕ")
                    log_entry = bstack1ll1lllllll_opy_(
                        kind=bstack11111ll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᏖ"),
                        message=bstack11111ll_opy_ (u"ࠦࠧᏗ"),
                        level=bstack11111ll_opy_ (u"ࠧࠨᏘ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1ll1111l1l1_opy_=entry.stat().st_size,
                        bstack1ll111l1l1l_opy_=bstack11111ll_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᏙ"),
                        bstack1l11ll_opy_=os.path.abspath(entry.path),
                        bstack1l111llll11_opy_=hook.get(TestFramework.bstack1l11l1l1l1l_opy_)
                    )
                    logs.append(log_entry)
                    _1ll111ll111_opy_.add(abs_path)
        platform_index = os.environ[bstack11111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᏚ")]
        bstack1l11l111l1l_opy_ = os.path.join(bstack1ll1111111l_opy_, (bstack1l1ll1lllll_opy_ + str(platform_index)), bstack1l11l1ll11l_opy_, bstack1l111lll111_opy_)
        if not os.path.exists(bstack1l11l111l1l_opy_) or not os.path.isdir(bstack1l11l111l1l_opy_):
            self.logger.info(bstack11111ll_opy_ (u"ࠣࡐࡲࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣࡥࡹࡀࠠࡼࡿࠥᏛ").format(bstack1l11l111l1l_opy_))
        else:
            self.logger.info(bstack11111ll_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡪࡷࡵ࡭ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᏜ").format(bstack1l11l111l1l_opy_))
            with os.scandir(bstack1l11l111l1l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1ll111ll111_opy_:
                        self.logger.info(bstack11111ll_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᏝ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11111ll_opy_ (u"ࠦࠧᏞ")
                        log_entry = bstack1ll1lllllll_opy_(
                            kind=bstack11111ll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᏟ"),
                            message=bstack11111ll_opy_ (u"ࠨࠢᏠ"),
                            level=bstack11111ll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᏡ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1ll1111l1l1_opy_=entry.stat().st_size,
                            bstack1ll111l1l1l_opy_=bstack11111ll_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᏢ"),
                            bstack1l11ll_opy_=os.path.abspath(entry.path),
                            bstack1ll111llll1_opy_=hook.get(TestFramework.bstack1l11l1l1l1l_opy_)
                        )
                        logs.append(log_entry)
                        _1ll111ll111_opy_.add(abs_path)
        hook[bstack11111ll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᏣ")] = logs
    def bstack1l1lll111l1_opy_(
        self,
        bstack1l1llll11l1_opy_: bstack1lll1l1l1l1_opy_,
        entries: List[bstack1ll1lllllll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11111ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢᏤ"))
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
            log_entry.message = entry.message.encode(bstack11111ll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᏥ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11111ll_opy_ (u"ࠧࠨᏦ")
            if entry.kind == bstack11111ll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᏧ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1ll1111l1l1_opy_
                log_entry.file_path = entry.bstack1l11ll_opy_
        def bstack1l1lll1l11l_opy_():
            bstack11ll111l1l_opy_ = datetime.now()
            try:
                self.bstack1llll1l1111_opy_.LogCreatedEvent(req)
                bstack1l1llll11l1_opy_.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦᏨ"), datetime.now() - bstack11ll111l1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11111ll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࢀࢃࠢᏩ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l1ll11_opy_.enqueue(bstack1l1lll1l11l_opy_)
    def __1l11lll1ll1_opy_(self, instance) -> None:
        bstack11111ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡌࡰࡣࡧࡷࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࠤࡩ࡯ࡣࡵࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡨࡵࡳࡲࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡥࡳࡪࠠࡶࡲࡧࡥࡹ࡫ࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡴࡶࡤࡸࡪࠦࡵࡴ࡫ࡱ࡫ࠥࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᏪ")
        bstack1l111ll11ll_opy_ = {bstack11111ll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧᏫ"): bstack1lll11l1l1l_opy_.bstack1l11l11llll_opy_()}
        TestFramework.bstack1l11lll111l_opy_(instance, bstack1l111ll11ll_opy_)
    @staticmethod
    def __1l11ll111l1_opy_(instance, args):
        request, bstack1l11ll11l1l_opy_ = args
        bstack1l11ll1llll_opy_ = id(bstack1l11ll11l1l_opy_)
        bstack1l111l1lll1_opy_ = instance.data[TestFramework.bstack1l11l11l111_opy_]
        step = next(filter(lambda st: st[bstack11111ll_opy_ (u"ࠫ࡮ࡪࠧᏬ")] == bstack1l11ll1llll_opy_, bstack1l111l1lll1_opy_[bstack11111ll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᏭ")]), None)
        step.update({
            bstack11111ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᏮ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l111l1lll1_opy_[bstack11111ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭Ꮿ")]) if st[bstack11111ll_opy_ (u"ࠨ࡫ࡧࠫᏰ")] == step[bstack11111ll_opy_ (u"ࠩ࡬ࡨࠬᏱ")]), None)
        if index is not None:
            bstack1l111l1lll1_opy_[bstack11111ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᏲ")][index] = step
        instance.data[TestFramework.bstack1l11l11l111_opy_] = bstack1l111l1lll1_opy_
    @staticmethod
    def __1l11l1l1l11_opy_(instance, args):
        bstack11111ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡫ࡩࡳࠦ࡬ࡦࡰࠣࡥࡷ࡭ࡳࠡ࡫ࡶࠤ࠷࠲ࠠࡪࡶࠣࡷ࡮࡭࡮ࡪࡨ࡬ࡩࡸࠦࡴࡩࡧࡵࡩࠥ࡯ࡳࠡࡰࡲࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡧࡲࡨࡵࠣࡥࡷ࡫ࠠ࠮ࠢ࡞ࡶࡪࡷࡵࡦࡵࡷ࠰ࠥࡹࡴࡦࡲࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡯ࡦࠡࡣࡵ࡫ࡸࠦࡡࡳࡧࠣ࠷ࠥࡺࡨࡦࡰࠣࡸ࡭࡫ࠠ࡭ࡣࡶࡸࠥࡼࡡ࡭ࡷࡨࠤ࡮ࡹࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᏳ")
        bstack1l111ll111l_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l11ll11l1l_opy_ = args[1]
        bstack1l11ll1llll_opy_ = id(bstack1l11ll11l1l_opy_)
        bstack1l111l1lll1_opy_ = instance.data[TestFramework.bstack1l11l11l111_opy_]
        step = None
        if bstack1l11ll1llll_opy_ is not None and bstack1l111l1lll1_opy_.get(bstack11111ll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᏴ")):
            step = next(filter(lambda st: st[bstack11111ll_opy_ (u"࠭ࡩࡥࠩᏵ")] == bstack1l11ll1llll_opy_, bstack1l111l1lll1_opy_[bstack11111ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭᏶")]), None)
            step.update({
                bstack11111ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᏷"): bstack1l111ll111l_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack11111ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᏸ"): bstack11111ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᏹ"),
                bstack11111ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᏺ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack11111ll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᏻ"): bstack11111ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᏼ"),
                })
        index = next((i for i, st in enumerate(bstack1l111l1lll1_opy_[bstack11111ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᏽ")]) if st[bstack11111ll_opy_ (u"ࠨ࡫ࡧࠫ᏾")] == step[bstack11111ll_opy_ (u"ࠩ࡬ࡨࠬ᏿")]), None)
        if index is not None:
            bstack1l111l1lll1_opy_[bstack11111ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ᐀")][index] = step
        instance.data[TestFramework.bstack1l11l11l111_opy_] = bstack1l111l1lll1_opy_
    @staticmethod
    def __1l11l1111ll_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack11111ll_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᐁ")):
                examples = list(node.callspec.params[bstack11111ll_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫᐂ")].values())
            return examples
        except:
            return []
    def bstack1ll1111l1ll_opy_(self, instance: bstack1lll1l1l1l1_opy_, bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_]):
        bstack1l11lll1lll_opy_ = (
            PytestBDDFramework.bstack1l11l1lllll_opy_
            if bstack11111l111l_opy_[1] == bstack1llllll1l11_opy_.PRE
            else PytestBDDFramework.bstack1l11l11l1l1_opy_
        )
        hook = PytestBDDFramework.bstack1l111ll1lll_opy_(instance, bstack1l11lll1lll_opy_)
        entries = hook.get(TestFramework.bstack1l11ll1l11l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1l11l1ll1l1_opy_, []))
        return entries
    def bstack1ll111lll1l_opy_(self, instance: bstack1lll1l1l1l1_opy_, bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_]):
        bstack1l11lll1lll_opy_ = (
            PytestBDDFramework.bstack1l11l1lllll_opy_
            if bstack11111l111l_opy_[1] == bstack1llllll1l11_opy_.PRE
            else PytestBDDFramework.bstack1l11l11l1l1_opy_
        )
        PytestBDDFramework.bstack1l11ll111ll_opy_(instance, bstack1l11lll1lll_opy_)
        TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1l11l1ll1l1_opy_, []).clear()
    @staticmethod
    def bstack1l111ll1lll_opy_(instance: bstack1lll1l1l1l1_opy_, bstack1l11lll1lll_opy_: str):
        bstack1l111l1l1ll_opy_ = (
            PytestBDDFramework.bstack1l11l11ll11_opy_
            if bstack1l11lll1lll_opy_ == PytestBDDFramework.bstack1l11l11l1l1_opy_
            else PytestBDDFramework.bstack1l111llllll_opy_
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
        hook = PytestBDDFramework.bstack1l111ll1lll_opy_(instance, bstack1l11lll1lll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11ll1l11l_opy_, []).clear()
    @staticmethod
    def __1l111llll1l_opy_(instance: bstack1lll1l1l1l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11111ll_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡩ࡯ࡳࡦࡶࠦᐃ"), None)):
            return
        if os.getenv(bstack11111ll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᐄ"), bstack11111ll_opy_ (u"ࠣ࠳ࠥᐅ")) != bstack11111ll_opy_ (u"ࠤ࠴ࠦᐆ"):
            PytestBDDFramework.logger.warning(bstack11111ll_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡩࡡࡱ࡮ࡲ࡫ࠧᐇ"))
            return
        bstack1l11l1ll1ll_opy_ = {
            bstack11111ll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᐈ"): (PytestBDDFramework.bstack1l11l1lllll_opy_, PytestBDDFramework.bstack1l111llllll_opy_),
            bstack11111ll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᐉ"): (PytestBDDFramework.bstack1l11l11l1l1_opy_, PytestBDDFramework.bstack1l11l11ll11_opy_),
        }
        for when in (bstack11111ll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᐊ"), bstack11111ll_opy_ (u"ࠢࡤࡣ࡯ࡰࠧᐋ"), bstack11111ll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᐌ")):
            bstack1l111l1llll_opy_ = args[1].get_records(when)
            if not bstack1l111l1llll_opy_:
                continue
            records = [
                bstack1ll1lllllll_opy_(
                    kind=TestFramework.bstack1l1llllll1l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11111ll_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩࠧᐍ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11111ll_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠦᐎ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111l1llll_opy_
                if isinstance(getattr(r, bstack11111ll_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᐏ"), None), str) and r.message.strip()
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
    def __1l11lll1l1l_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack11lll111l_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l11llll1ll_opy_(request.node, scenario)
        bstack1l111ll1l11_opy_ = feature.filename
        if not bstack11lll111l_opy_ or not test_name or not bstack1l111ll1l11_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll1ll1lll1_opy_: uuid4().__str__(),
            TestFramework.bstack1l11ll11ll1_opy_: bstack11lll111l_opy_,
            TestFramework.bstack1ll1lll111l_opy_: test_name,
            TestFramework.bstack1l1ll1ll111_opy_: bstack11lll111l_opy_,
            TestFramework.bstack1l11l111l11_opy_: bstack1l111ll1l11_opy_,
            TestFramework.bstack1l11llll11l_opy_: PytestBDDFramework.__1l11ll1ll11_opy_(feature, scenario),
            TestFramework.bstack1l11l111ll1_opy_: code,
            TestFramework.bstack1l1l1lll1l1_opy_: TestFramework.bstack1l11l1l111l_opy_,
            TestFramework.bstack1l1l1111lll_opy_: test_name
        }
    @staticmethod
    def __1l11llll1ll_opy_(node, scenario):
        if hasattr(node, bstack11111ll_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᐐ")):
            parts = node.nodeid.rsplit(bstack11111ll_opy_ (u"ࠨ࡛ࠣᐑ"))
            params = parts[-1]
            return bstack11111ll_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢᐒ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l11ll1ll11_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack11111ll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᐓ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack11111ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᐔ")) else [])
    @staticmethod
    def __1l111lll11l_opy_(location):
        return bstack11111ll_opy_ (u"ࠥ࠾࠿ࠨᐕ").join(filter(lambda x: isinstance(x, str), location))