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
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import bstack1111l1lll1_opy_, bstack11111l1lll_opy_, bstack111111ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack11111lllll_opy_
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import bstack1111l11lll_opy_
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import bstack1111111ll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack11111ll1l1_opy_, bstack11111l111l_opy_, bstack1111111l1l_opy_, bstack111111llll_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1llll1l1l11_opy_, bstack1llllll111l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1llll11111l_opy_ = [bstack1ll1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧဩ"), bstack1ll1l11_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣဪ"), bstack1ll1l11_opy_ (u"ࠤࡦࡳࡳ࡬ࡩࡨࠤါ"), bstack1ll1l11_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࠦာ"), bstack1ll1l11_opy_ (u"ࠦࡵࡧࡴࡩࠤိ")]
bstack1lllll1lll1_opy_ = bstack1llllll111l_opy_()
bstack1lllllll1ll_opy_ = bstack1ll1l11_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧီ")
bstack1llllll1l1l_opy_ = {
    bstack1ll1l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡉࡵࡧࡰࠦု"): bstack1llll11111l_opy_,
    bstack1ll1l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡑࡣࡦ࡯ࡦ࡭ࡥࠣူ"): bstack1llll11111l_opy_,
    bstack1ll1l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡏࡲࡨࡺࡲࡥࠣေ"): bstack1llll11111l_opy_,
    bstack1ll1l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡆࡰࡦࡹࡳࠣဲ"): bstack1llll11111l_opy_,
    bstack1ll1l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡊࡺࡴࡣࡵ࡫ࡲࡲࠧဳ"): bstack1llll11111l_opy_
    + [
        bstack1ll1l11_opy_ (u"ࠦࡴࡸࡩࡨ࡫ࡱࡥࡱࡴࡡ࡮ࡧࠥဴ"),
        bstack1ll1l11_opy_ (u"ࠧࡱࡥࡺࡹࡲࡶࡩࡹࠢဵ"),
        bstack1ll1l11_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࡩ࡯ࡨࡲࠦံ"),
        bstack1ll1l11_opy_ (u"ࠢ࡬ࡧࡼࡻࡴࡸࡤࡴࠤ့"),
        bstack1ll1l11_opy_ (u"ࠣࡥࡤࡰࡱࡹࡰࡦࡥࠥး"),
        bstack1ll1l11_opy_ (u"ࠤࡦࡥࡱࡲ࡯ࡣ࡬္ࠥ"),
        bstack1ll1l11_opy_ (u"ࠥࡷࡹࡧࡲࡵࠤ်"),
        bstack1ll1l11_opy_ (u"ࠦࡸࡺ࡯ࡱࠤျ"),
        bstack1ll1l11_opy_ (u"ࠧࡪࡵࡳࡣࡷ࡭ࡴࡴࠢြ"),
        bstack1ll1l11_opy_ (u"ࠨࡷࡩࡧࡱࠦွ"),
    ],
    bstack1ll1l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣ࡬ࡲ࠳࡙ࡥࡴࡵ࡬ࡳࡳࠨှ"): [bstack1ll1l11_opy_ (u"ࠣࡵࡷࡥࡷࡺࡰࡢࡶ࡫ࠦဿ"), bstack1ll1l11_opy_ (u"ࠤࡷࡩࡸࡺࡳࡧࡣ࡬ࡰࡪࡪࠢ၀"), bstack1ll1l11_opy_ (u"ࠥࡸࡪࡹࡴࡴࡥࡲࡰࡱ࡫ࡣࡵࡧࡧࠦ၁"), bstack1ll1l11_opy_ (u"ࠦ࡮ࡺࡥ࡮ࡵࠥ၂")],
    bstack1ll1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡩ࡯࡯ࡨ࡬࡫࠳ࡉ࡯࡯ࡨ࡬࡫ࠧ၃"): [bstack1ll1l11_opy_ (u"ࠨࡩ࡯ࡸࡲࡧࡦࡺࡩࡰࡰࡢࡴࡦࡸࡡ࡮ࡵࠥ၄"), bstack1ll1l11_opy_ (u"ࠢࡢࡴࡪࡷࠧ၅")],
    bstack1ll1l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡊ࡮ࡾࡴࡶࡴࡨࡈࡪ࡬ࠢ၆"): [bstack1ll1l11_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣ၇"), bstack1ll1l11_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦ၈"), bstack1ll1l11_opy_ (u"ࠦ࡫ࡻ࡮ࡤࠤ၉"), bstack1ll1l11_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧ၊"), bstack1ll1l11_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣ။"), bstack1ll1l11_opy_ (u"ࠢࡪࡦࡶࠦ၌")],
    bstack1ll1l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡗࡺࡨࡒࡦࡳࡸࡩࡸࡺࠢ၍"): [bstack1ll1l11_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢ၎"), bstack1ll1l11_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࠤ၏"), bstack1ll1l11_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡢ࡭ࡳࡪࡥࡹࠤၐ")],
    bstack1ll1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡸࡵ࡯ࡰࡨࡶ࠳ࡉࡡ࡭࡮ࡌࡲ࡫ࡵࠢၑ"): [bstack1ll1l11_opy_ (u"ࠨࡷࡩࡧࡱࠦၒ"), bstack1ll1l11_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࠢၓ")],
    bstack1ll1l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤࡶࡰ࠴ࡳࡵࡴࡸࡧࡹࡻࡲࡦࡵ࠱ࡒࡴࡪࡥࡌࡧࡼࡻࡴࡸࡤࡴࠤၔ"): [bstack1ll1l11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢၕ"), bstack1ll1l11_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥၖ")],
    bstack1ll1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡲ࡬࠰ࡶࡸࡷࡻࡣࡵࡷࡵࡩࡸ࠴ࡍࡢࡴ࡮ࠦၗ"): [bstack1ll1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥၘ"), bstack1ll1l11_opy_ (u"ࠨࡡࡳࡩࡶࠦၙ"), bstack1ll1l11_opy_ (u"ࠢ࡬ࡹࡤࡶ࡬ࡹࠢၚ")],
}
_1lll1lll11l_opy_ = set()
class bstack1llllll11ll_opy_(bstack11111lllll_opy_):
    bstack1lllll111l1_opy_ = bstack1ll1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࠣၛ")
    bstack1lllll1111l_opy_ = bstack1ll1l11_opy_ (u"ࠤࡌࡒࡋࡕࠢၜ")
    bstack1lllll1l111_opy_ = bstack1ll1l11_opy_ (u"ࠥࡉࡗࡘࡏࡓࠤၝ")
    bstack1lllll1l11l_opy_: Callable
    bstack1llll1111l1_opy_: Callable
    def __init__(self, bstack1llll11lll1_opy_, bstack1lll1ll1lll_opy_):
        super().__init__()
        self.bstack1llll111l1l_opy_ = bstack1lll1ll1lll_opy_
        if os.getenv(bstack1ll1l11_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡓ࠶࠷࡙ࠣၞ"), bstack1ll1l11_opy_ (u"ࠧ࠷ࠢၟ")) != bstack1ll1l11_opy_ (u"ࠨ࠱ࠣၠ") or not self.is_enabled():
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠢࠣၡ") + str(self.__class__.__name__) + bstack1ll1l11_opy_ (u"ࠣࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧࠦၢ"))
            return
        TestFramework.bstack111111l1l1_opy_((bstack11111ll1l1_opy_.TEST, bstack1111111l1l_opy_.PRE), self.bstack1llll11ll11_opy_)
        TestFramework.bstack111111l1l1_opy_((bstack11111ll1l1_opy_.TEST, bstack1111111l1l_opy_.POST), self.bstack1111111l11_opy_)
        for event in bstack11111ll1l1_opy_:
            for state in bstack1111111l1l_opy_:
                TestFramework.bstack111111l1l1_opy_((event, state), self.bstack1lll1ll1l1l_opy_)
        bstack1llll11lll1_opy_.bstack111111l1l1_opy_((bstack11111l1lll_opy_.bstack1111l1l1l1_opy_, bstack111111ll1l_opy_.POST), self.bstack1llll1111ll_opy_)
        self.bstack1lllll1l11l_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1lllll1ll11_opy_(bstack1llllll11ll_opy_.bstack1lllll1111l_opy_, self.bstack1lllll1l11l_opy_)
        self.bstack1llll1111l1_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1lllll1ll11_opy_(bstack1llllll11ll_opy_.bstack1lllll1l111_opy_, self.bstack1llll1111l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1lll1ll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1lll1llll11_opy_() and instance:
            bstack1lllll1l1ll_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack111111111l_opy_
            if test_framework_state == bstack11111ll1l1_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack11111ll1l1_opy_.LOG:
                bstack1l1l1lllll_opy_ = datetime.now()
                entries = f.bstack1llll111111_opy_(instance, bstack111111111l_opy_)
                if entries:
                    self.bstack1llll1lll11_opy_(instance, entries)
                    instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࠤၣ"), datetime.now() - bstack1l1l1lllll_opy_)
                    f.bstack1llll1l1111_opy_(instance, bstack111111111l_opy_)
                instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨၤ"), datetime.now() - bstack1lllll1l1ll_opy_)
                return # bstack1llllllll11_opy_ not send this event with the bstack1lllll11l11_opy_ bstack1lll1lll111_opy_
            elif (
                test_framework_state == bstack11111ll1l1_opy_.TEST
                and test_hook_state == bstack1111111l1l_opy_.POST
                and not f.bstack1llllll11l1_opy_(instance, TestFramework.bstack1llll11l1ll_opy_)
            ):
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠦࡩࡸ࡯ࡱࡲ࡬ࡲ࡬ࠦࡤࡶࡧࠣࡸࡴࠦ࡬ࡢࡥ࡮ࠤࡴ࡬ࠠࡳࡧࡶࡹࡱࡺࡳࠡࠤၥ") + str(TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1llll11l1ll_opy_)) + bstack1ll1l11_opy_ (u"ࠧࠨၦ"))
                f.bstack1lllllll1l1_opy_(instance, bstack1llllll11ll_opy_.bstack1lllll111l1_opy_, True)
                return # bstack1llllllll11_opy_ not send this event bstack1lllll1llll_opy_ bstack1llllll1111_opy_
            elif (
                f.bstack11111l11l1_opy_(instance, bstack1llllll11ll_opy_.bstack1lllll111l1_opy_, False)
                and test_framework_state == bstack11111ll1l1_opy_.LOG_REPORT
                and test_hook_state == bstack1111111l1l_opy_.POST
                and f.bstack1llllll11l1_opy_(instance, TestFramework.bstack1llll11l1ll_opy_)
            ):
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠨࡩ࡯࡬ࡨࡧࡹ࡯࡮ࡨࠢࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡕࡇࡖࡘ࠱ࠦࡔࡦࡵࡷࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡐࡐࡕࡗࠤࠧၧ") + str(TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack1llll11l1ll_opy_)) + bstack1ll1l11_opy_ (u"ࠢࠣၨ"))
                self.bstack1lll1ll1l1l_opy_(f, instance, (bstack11111ll1l1_opy_.TEST, bstack1111111l1l_opy_.POST), *args, **kwargs)
            bstack1l1l1lllll_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1llll1ll111_opy_ = sorted(
                filter(lambda x: x.get(bstack1ll1l11_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦၩ"), None), data.pop(bstack1ll1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤၪ"), {}).values()),
                key=lambda x: x[bstack1ll1l11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨၫ")],
            )
            if bstack1111l11lll_opy_.bstack1111l1l11l_opy_ in data:
                data.pop(bstack1111l11lll_opy_.bstack1111l1l11l_opy_)
            data.update({bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦၬ"): bstack1llll1ll111_opy_})
            instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠧࡰࡳࡰࡰ࠽ࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥၭ"), datetime.now() - bstack1l1l1lllll_opy_)
            bstack1l1l1lllll_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1llllll1lll_opy_)
            instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤၮ"), datetime.now() - bstack1l1l1lllll_opy_)
            self.bstack1lll1lll111_opy_(instance, bstack111111111l_opy_, event_json=event_json)
            instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥၯ"), datetime.now() - bstack1lllll1l1ll_opy_)
    def bstack1llll11ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll11l1lll_opy_ import bstack111111lll1_opy_
        bstack11111l11ll_opy_ = bstack111111lll1_opy_.bstack11111l1111_opy_(EVENTS.bstack1ll111lll1_opy_.value)
        self.bstack1llll111l1l_opy_.bstack1lllll1ll1l_opy_(instance, f, bstack111111111l_opy_, *args, **kwargs)
        bstack111111lll1_opy_.end(EVENTS.bstack1ll111lll1_opy_.value, bstack11111l11ll_opy_ + bstack1ll1l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣၰ"), bstack11111l11ll_opy_ + bstack1ll1l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢၱ"), status=True, failure=None, test_name=None)
    def bstack1111111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1llll111l1l_opy_.bstack1llll11l11l_opy_(instance, f, bstack111111111l_opy_, *args, **kwargs)
        self.bstack1lll1ll1ll1_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1llllll1l11_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def bstack1lll1ll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫࡚ࠥࡥࡴࡶࡖࡩࡸࡹࡩࡰࡰࡈࡺࡪࡴࡴࠡࡩࡕࡔࡈࠦࡣࡢ࡮࡯࠾ࠥࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡦࡤࡸࡦࠨၲ"))
            return
        bstack1l1l1lllll_opy_ = datetime.now()
        try:
            r = self.bstack1llll111lll_opy_.TestSessionEvent(req)
            instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡥࡷࡧࡱࡸࠧၳ"), datetime.now() - bstack1l1l1lllll_opy_)
            f.bstack1lllllll1l1_opy_(instance, self.bstack1llll111l1l_opy_.bstack1lll1lllll1_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1ll1l11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢၴ") + str(r) + bstack1ll1l11_opy_ (u"ࠨࠢၵ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧၶ") + str(e) + bstack1ll1l11_opy_ (u"ࠣࠤၷ"))
            traceback.print_exc()
            raise e
    def bstack1llll1111ll_opy_(
        self,
        f: bstack1111111ll1_opy_,
        _driver: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        _1lllll11l1l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1111111ll1_opy_.bstack1111l11111_opy_(method_name):
            return
        if f.bstack111111l11l_opy_(*args) == bstack1111111ll1_opy_.bstack1lllllll11l_opy_:
            bstack1lllll1l1ll_opy_ = datetime.now()
            screenshot = result.get(bstack1ll1l11_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣၸ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠥ࡭ࡳࡼࡡ࡭࡫ࡧࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡ࡫ࡰࡥ࡬࡫ࠠࡣࡣࡶࡩ࠻࠺ࠠࡴࡶࡵࠦၹ"))
                return
            bstack1111l1ll11_opy_ = self.bstack11111lll11_opy_(instance)
            if bstack1111l1ll11_opy_:
                entry = bstack111111llll_opy_(TestFramework.bstack1llll1ll11l_opy_, screenshot)
                self.bstack1llll1lll11_opy_(bstack1111l1ll11_opy_, [entry])
                instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧࡦࡵࡧࡵࡣࡪࡾࡥࡤࡷࡷࡩࠧၺ"), datetime.now() - bstack1lllll1l1ll_opy_)
            else:
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠧࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡹ࡫ࡳࡵࠢࡩࡳࡷࠦࡷࡩ࡫ࡦ࡬ࠥࡺࡨࡪࡵࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡸࡣࡶࠤࡹࡧ࡫ࡦࡰࠣࡦࡾࠦࡤࡳ࡫ࡹࡩࡷࡃࠠࡼࡿࠥၻ").format(instance.ref()))
        event = {}
        bstack1111l1ll11_opy_ = self.bstack11111lll11_opy_(instance)
        if bstack1111l1ll11_opy_:
            self.bstack1llllll1ll1_opy_(event, bstack1111l1ll11_opy_)
            if event.get(bstack1ll1l11_opy_ (u"ࠨ࡬ࡰࡩࡶࠦၼ")):
                self.bstack1llll1lll11_opy_(bstack1111l1ll11_opy_, event[bstack1ll1l11_opy_ (u"ࠢ࡭ࡱࡪࡷࠧၽ")])
            else:
                self.logger.info(bstack1ll1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠ࡭ࡱࡪࡷࠥ࡬࡯ࡳࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡥࡷࡧࡱࡸࠧၾ"))
    @measure(event_name=EVENTS.bstack1llll11l1l1_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def bstack1llll1lll11_opy_(
        self,
        bstack1111l1ll11_opy_: bstack11111l111l_opy_,
        entries: List[bstack111111llll_opy_],
    ):
        self.bstack1lll1lll1ll_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111l11l1_opy_(bstack1111l1ll11_opy_, TestFramework.bstack1111l11ll1_opy_)
        req.execution_context.hash = str(bstack1111l1ll11_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1111l1ll11_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1111l1ll11_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack11111l11l1_opy_(bstack1111l1ll11_opy_, TestFramework.bstack1llll1lllll_opy_)
            log_entry.test_framework_version = TestFramework.bstack11111l11l1_opy_(bstack1111l1ll11_opy_, TestFramework.bstack1lllllllll1_opy_)
            log_entry.uuid = TestFramework.bstack11111l11l1_opy_(bstack1111l1ll11_opy_, TestFramework.bstack11111111ll_opy_)
            log_entry.test_framework_state = bstack1111l1ll11_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll1l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣၿ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1ll1l11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧႀ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1llll1l1lll_opy_
                log_entry.file_path = entry.bstack11l1ll1_opy_
        def bstack1lll1lll1l1_opy_():
            bstack1l1l1lllll_opy_ = datetime.now()
            try:
                self.bstack1llll111lll_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1llll1ll11l_opy_:
                    bstack1111l1ll11_opy_.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣႁ"), datetime.now() - bstack1l1l1lllll_opy_)
                elif entry.kind == TestFramework.bstack1lllllll111_opy_:
                    bstack1111l1ll11_opy_.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤႂ"), datetime.now() - bstack1l1l1lllll_opy_)
                else:
                    bstack1111l1ll11_opy_.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥ࡬ࡰࡩࠥႃ"), datetime.now() - bstack1l1l1lllll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1l11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧႄ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1llll11l111_opy_.enqueue(bstack1lll1lll1l1_opy_)
    @measure(event_name=EVENTS.bstack1llll111l11_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def bstack1lll1lll111_opy_(
        self,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        event_json=None,
    ):
        self.bstack1lll1lll1ll_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1111l11ll1_opy_)
        req.test_framework_name = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1llll1lllll_opy_)
        req.test_framework_version = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1lllllllll1_opy_)
        req.test_framework_state = bstack111111111l_opy_[0].name
        req.test_hook_state = bstack111111111l_opy_[1].name
        started_at = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1llll11llll_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1lllll1l1l1_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1llllll1lll_opy_)).encode(bstack1ll1l11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢႅ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1lll1lll1l1_opy_():
            bstack1l1l1lllll_opy_ = datetime.now()
            try:
                self.bstack1llll111lll_opy_.TestFrameworkEvent(req)
                instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡥࡷࡧࡱࡸࠧႆ"), datetime.now() - bstack1l1l1lllll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1l11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣႇ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1llll11l111_opy_.enqueue(bstack1lll1lll1l1_opy_)
    def bstack11111lll11_opy_(self, instance: bstack1111l1lll1_opy_):
        bstack1111111lll_opy_ = TestFramework.bstack1111l1ll1l_opy_(instance.context)
        for t in bstack1111111lll_opy_:
            bstack11111ll11l_opy_ = TestFramework.bstack11111l11l1_opy_(t, bstack1111l11lll_opy_.bstack1111l1l11l_opy_, [])
            if any(instance is d[1] for d in bstack11111ll11l_opy_):
                return t
    def bstack1lllll111ll_opy_(self, message):
        self.bstack1lllll1l11l_opy_(message + bstack1ll1l11_opy_ (u"ࠦࡡࡴࠢႈ"))
    def log_error(self, message):
        self.bstack1llll1111l1_opy_(message + bstack1ll1l11_opy_ (u"ࠧࡢ࡮ࠣႉ"))
    def bstack1lllll1ll11_opy_(self, level, original_func):
        def bstack1lllll11111_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1111111lll_opy_ = TestFramework.bstack1llllllllll_opy_()
            if not bstack1111111lll_opy_:
                return return_value
            bstack1111l1ll11_opy_ = next(
                (
                    instance
                    for instance in bstack1111111lll_opy_
                    if TestFramework.bstack1llllll11l1_opy_(instance, TestFramework.bstack11111111ll_opy_)
                ),
                None,
            )
            if not bstack1111l1ll11_opy_:
                return
            entry = bstack111111llll_opy_(TestFramework.bstack1lllll11ll1_opy_, message, level)
            self.bstack1llll1lll11_opy_(bstack1111l1ll11_opy_, [entry])
            return return_value
        return bstack1lllll11111_opy_
    def bstack1llllll1ll1_opy_(self, event: dict, instance=None) -> None:
        global _1lll1lll11l_opy_
        levels = [bstack1ll1l11_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤႊ"), bstack1ll1l11_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦႋ")]
        bstack1lll1llll1l_opy_ = bstack1ll1l11_opy_ (u"ࠣࠤႌ")
        if instance is not None:
            try:
                bstack1lll1llll1l_opy_ = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack11111111ll_opy_)
            except Exception as e:
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡸࡹ࡮ࡪࠠࡧࡴࡲࡱࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ႍࠢ").format(e))
        bstack1llll1l11l1_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪႎ")]
                bstack1llll111ll1_opy_ = os.path.join(bstack1lllll1lll1_opy_, (bstack1lllllll1ll_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1llll111ll1_opy_):
                    self.logger.info(bstack1ll1l11_opy_ (u"ࠦࡉ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡯ࡱࡷࠤࡵࡸࡥࡴࡧࡱࡸࠥ࡬࡯ࡳࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡔࡦࡵࡷࠤࡦࡴࡤࠡࡄࡸ࡭ࡱࡪࠠ࡭ࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠦႏ").format(bstack1llll111ll1_opy_))
                file_names = os.listdir(bstack1llll111ll1_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1llll111ll1_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1lll1lll11l_opy_:
                        self.logger.info(bstack1ll1l11_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥ႐").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1llll1l1l1l_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1llll1l1l1l_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1ll1l11_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤ႑"):
                                entry = bstack111111llll_opy_(
                                    kind=bstack1ll1l11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤ႒"),
                                    message=bstack1ll1l11_opy_ (u"ࠣࠤ႓"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1llll1l1lll_opy_=file_size,
                                    bstack1llll1ll1ll_opy_=bstack1ll1l11_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤ႔"),
                                    bstack11l1ll1_opy_=os.path.abspath(file_path),
                                    bstack111l1l111_opy_=bstack1lll1llll1l_opy_
                                )
                            elif level == bstack1ll1l11_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢ႕"):
                                entry = bstack111111llll_opy_(
                                    kind=bstack1ll1l11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨ႖"),
                                    message=bstack1ll1l11_opy_ (u"ࠧࠨ႗"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1llll1l1lll_opy_=file_size,
                                    bstack1llll1ll1ll_opy_=bstack1ll1l11_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨ႘"),
                                    bstack11l1ll1_opy_=os.path.abspath(file_path),
                                    bstack1lllll11lll_opy_=bstack1lll1llll1l_opy_
                                )
                            bstack1llll1l11l1_opy_.append(entry)
                            _1lll1lll11l_opy_.add(abs_path)
                        except Exception as bstack1llllllll1l_opy_:
                            self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡶࡦ࡯ࡳࡦࡦࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠥ႙").format(bstack1llllllll1l_opy_))
        except Exception as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡷࡧࡩࡴࡧࡧࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠦႚ").format(e))
        event[bstack1ll1l11_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢႛ")] = bstack1llll1l11l1_opy_
class bstack1llllll1lll_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1llll1llll1_opy_ = set()
        kwargs[bstack1ll1l11_opy_ (u"ࠥࡷࡰ࡯ࡰ࡬ࡧࡼࡷࠧႜ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1lll1llllll_opy_(obj, self.bstack1llll1llll1_opy_)
def bstack1llll1ll1l1_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1lll1llllll_opy_(obj, bstack1llll1llll1_opy_=None, max_depth=3):
    if bstack1llll1llll1_opy_ is None:
        bstack1llll1llll1_opy_ = set()
    if id(obj) in bstack1llll1llll1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1llll1llll1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1llll1l11ll_opy_ = TestFramework.bstack1llll11ll1l_opy_(obj)
    bstack1llll1lll1l_opy_ = next((k.lower() in bstack1llll1l11ll_opy_.lower() for k in bstack1llllll1l1l_opy_.keys()), None)
    if bstack1llll1lll1l_opy_:
        obj = TestFramework.bstack1llll1l111l_opy_(obj, bstack1llllll1l1l_opy_[bstack1llll1lll1l_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1ll1l11_opy_ (u"ࠦࡤࡥࡳ࡭ࡱࡷࡷࡤࡥࠢႝ")):
            keys = getattr(obj, bstack1ll1l11_opy_ (u"ࠧࡥ࡟ࡴ࡮ࡲࡸࡸࡥ࡟ࠣ႞"), [])
        elif hasattr(obj, bstack1ll1l11_opy_ (u"ࠨ࡟ࡠࡦ࡬ࡧࡹࡥ࡟ࠣ႟")):
            keys = getattr(obj, bstack1ll1l11_opy_ (u"ࠢࡠࡡࡧ࡭ࡨࡺ࡟ࡠࠤႠ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1ll1l11_opy_ (u"ࠣࡡࠥႡ"))}
        if not obj and bstack1llll1l11ll_opy_ == bstack1ll1l11_opy_ (u"ࠤࡳࡥࡹ࡮࡬ࡪࡤ࠱ࡔࡴࡹࡩࡹࡒࡤࡸ࡭ࠨႢ"):
            obj = {bstack1ll1l11_opy_ (u"ࠥࡴࡦࡺࡨࠣႣ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1llll1ll1l1_opy_(key) or str(key).startswith(bstack1ll1l11_opy_ (u"ࠦࡤࠨႤ")):
            continue
        if value is not None and bstack1llll1ll1l1_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1lll1llllll_opy_(value, bstack1llll1llll1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1lll1llllll_opy_(o, bstack1llll1llll1_opy_, max_depth) for o in value]))
    return result or None