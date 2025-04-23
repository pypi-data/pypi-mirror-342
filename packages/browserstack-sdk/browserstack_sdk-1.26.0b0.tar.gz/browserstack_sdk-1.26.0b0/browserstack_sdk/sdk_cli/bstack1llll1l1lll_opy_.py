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
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import bstack1111l1111l_opy_, bstack1111l11l1l_opy_, bstack11111l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll11l1ll_opy_ import bstack1lllllll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lll11_opy_ import bstack1llll11llll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll11ll1_opy_ import bstack1ll1lllll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll1l11ll_opy_, bstack1lll1l1l1l1_opy_, bstack1llllll1l11_opy_, bstack1ll1lllllll_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1lllll11l_opy_, bstack1l1llll111l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1ll11111111_opy_ = [bstack11111ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆮ"), bstack11111ll_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧᆯ"), bstack11111ll_opy_ (u"ࠨࡣࡰࡰࡩ࡭࡬ࠨᆰ"), bstack11111ll_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࠣᆱ"), bstack11111ll_opy_ (u"ࠣࡲࡤࡸ࡭ࠨᆲ")]
bstack1ll1111111l_opy_ = bstack1l1llll111l_opy_()
bstack1l1ll1lllll_opy_ = bstack11111ll_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᆳ")
bstack1ll111111ll_opy_ = {
    bstack11111ll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡍࡹ࡫࡭ࠣᆴ"): bstack1ll11111111_opy_,
    bstack11111ll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡕࡧࡣ࡬ࡣࡪࡩࠧᆵ"): bstack1ll11111111_opy_,
    bstack11111ll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡓ࡯ࡥࡷ࡯ࡩࠧᆶ"): bstack1ll11111111_opy_,
    bstack11111ll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡃ࡭ࡣࡶࡷࠧᆷ"): bstack1ll11111111_opy_,
    bstack11111ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡇࡷࡱࡧࡹ࡯࡯࡯ࠤᆸ"): bstack1ll11111111_opy_
    + [
        bstack11111ll_opy_ (u"ࠣࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡱࡥࡲ࡫ࠢᆹ"),
        bstack11111ll_opy_ (u"ࠤ࡮ࡩࡾࡽ࡯ࡳࡦࡶࠦᆺ"),
        bstack11111ll_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨ࡭ࡳ࡬࡯ࠣᆻ"),
        bstack11111ll_opy_ (u"ࠦࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᆼ"),
        bstack11111ll_opy_ (u"ࠧࡩࡡ࡭࡮ࡶࡴࡪࡩࠢᆽ"),
        bstack11111ll_opy_ (u"ࠨࡣࡢ࡮࡯ࡳࡧࡰࠢᆾ"),
        bstack11111ll_opy_ (u"ࠢࡴࡶࡤࡶࡹࠨᆿ"),
        bstack11111ll_opy_ (u"ࠣࡵࡷࡳࡵࠨᇀ"),
        bstack11111ll_opy_ (u"ࠤࡧࡹࡷࡧࡴࡪࡱࡱࠦᇁ"),
        bstack11111ll_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᇂ"),
    ],
    bstack11111ll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡩ࡯࠰ࡖࡩࡸࡹࡩࡰࡰࠥᇃ"): [bstack11111ll_opy_ (u"ࠧࡹࡴࡢࡴࡷࡴࡦࡺࡨࠣᇄ"), bstack11111ll_opy_ (u"ࠨࡴࡦࡵࡷࡷ࡫ࡧࡩ࡭ࡧࡧࠦᇅ"), bstack11111ll_opy_ (u"ࠢࡵࡧࡶࡸࡸࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤࠣᇆ"), bstack11111ll_opy_ (u"ࠣ࡫ࡷࡩࡲࡹࠢᇇ")],
    bstack11111ll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡦࡳࡳ࡬ࡩࡨ࠰ࡆࡳࡳ࡬ࡩࡨࠤᇈ"): [bstack11111ll_opy_ (u"ࠥ࡭ࡳࡼ࡯ࡤࡣࡷ࡭ࡴࡴ࡟ࡱࡣࡵࡥࡲࡹࠢᇉ"), bstack11111ll_opy_ (u"ࠦࡦࡸࡧࡴࠤᇊ")],
    bstack11111ll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳࡬ࡩࡹࡶࡸࡶࡪࡹ࠮ࡇ࡫ࡻࡸࡺࡸࡥࡅࡧࡩࠦᇋ"): [bstack11111ll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᇌ"), bstack11111ll_opy_ (u"ࠢࡢࡴࡪࡲࡦࡳࡥࠣᇍ"), bstack11111ll_opy_ (u"ࠣࡨࡸࡲࡨࠨᇎ"), bstack11111ll_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᇏ"), bstack11111ll_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࠧᇐ"), bstack11111ll_opy_ (u"ࠦ࡮ࡪࡳࠣᇑ")],
    bstack11111ll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳࡬ࡩࡹࡶࡸࡶࡪࡹ࠮ࡔࡷࡥࡖࡪࡷࡵࡦࡵࡷࠦᇒ"): [bstack11111ll_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦᇓ"), bstack11111ll_opy_ (u"ࠢࡱࡣࡵࡥࡲࠨᇔ"), bstack11111ll_opy_ (u"ࠣࡲࡤࡶࡦࡳ࡟ࡪࡰࡧࡩࡽࠨᇕ")],
    bstack11111ll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡵࡹࡳࡴࡥࡳ࠰ࡆࡥࡱࡲࡉ࡯ࡨࡲࠦᇖ"): [bstack11111ll_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᇗ"), bstack11111ll_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࠦᇘ")],
    bstack11111ll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡳࡡࡳ࡭࠱ࡷࡹࡸࡵࡤࡶࡸࡶࡪࡹ࠮ࡏࡱࡧࡩࡐ࡫ࡹࡸࡱࡵࡨࡸࠨᇙ"): [bstack11111ll_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᇚ"), bstack11111ll_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢᇛ")],
    bstack11111ll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤࡶࡰ࠴ࡳࡵࡴࡸࡧࡹࡻࡲࡦࡵ࠱ࡑࡦࡸ࡫ࠣᇜ"): [bstack11111ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇝ"), bstack11111ll_opy_ (u"ࠥࡥࡷ࡭ࡳࠣᇞ"), bstack11111ll_opy_ (u"ࠦࡰࡽࡡࡳࡩࡶࠦᇟ")],
}
_1ll111ll111_opy_ = set()
class bstack1llll1l111l_opy_(bstack1lllllll11l_opy_):
    bstack1ll111lll11_opy_ = bstack11111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࠧᇠ")
    bstack1ll1111llll_opy_ = bstack11111ll_opy_ (u"ࠨࡉࡏࡈࡒࠦᇡ")
    bstack1ll1111ll11_opy_ = bstack11111ll_opy_ (u"ࠢࡆࡔࡕࡓࡗࠨᇢ")
    bstack1ll11111lll_opy_: Callable
    bstack1l1lll11l11_opy_: Callable
    def __init__(self, bstack1llll1l1l1l_opy_, bstack1lll1ll1lll_opy_):
        super().__init__()
        self.bstack1ll1l1lllll_opy_ = bstack1lll1ll1lll_opy_
        if os.getenv(bstack11111ll_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡐ࠳࠴࡝ࠧᇣ"), bstack11111ll_opy_ (u"ࠤ࠴ࠦᇤ")) != bstack11111ll_opy_ (u"ࠥ࠵ࠧᇥ") or not self.is_enabled():
            self.logger.warning(bstack11111ll_opy_ (u"ࠦࠧᇦ") + str(self.__class__.__name__) + bstack11111ll_opy_ (u"ࠧࠦࡤࡪࡵࡤࡦࡱ࡫ࡤࠣᇧ"))
            return
        TestFramework.bstack1ll1ll11l11_opy_((bstack1llll1l11ll_opy_.TEST, bstack1llllll1l11_opy_.PRE), self.bstack1ll1l1l1l11_opy_)
        TestFramework.bstack1ll1ll11l11_opy_((bstack1llll1l11ll_opy_.TEST, bstack1llllll1l11_opy_.POST), self.bstack1ll1l1ll1l1_opy_)
        for event in bstack1llll1l11ll_opy_:
            for state in bstack1llllll1l11_opy_:
                TestFramework.bstack1ll1ll11l11_opy_((event, state), self.bstack1l1llll1lll_opy_)
        bstack1llll1l1l1l_opy_.bstack1ll1ll11l11_opy_((bstack1111l11l1l_opy_.bstack1llllllll1l_opy_, bstack11111l1ll1_opy_.POST), self.bstack1l1lll11111_opy_)
        self.bstack1ll11111lll_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1ll11111l1l_opy_(bstack1llll1l111l_opy_.bstack1ll1111llll_opy_, self.bstack1ll11111lll_opy_)
        self.bstack1l1lll11l11_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1ll11111l1l_opy_(bstack1llll1l111l_opy_.bstack1ll1111ll11_opy_, self.bstack1l1lll11l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1llll1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1lll11l1l_opy_() and instance:
            bstack1ll111111l1_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack11111l111l_opy_
            if test_framework_state == bstack1llll1l11ll_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1llll1l11ll_opy_.LOG:
                bstack11ll111l1l_opy_ = datetime.now()
                entries = f.bstack1ll1111l1ll_opy_(instance, bstack11111l111l_opy_)
                if entries:
                    self.bstack1l1lll111l1_opy_(instance, entries)
                    instance.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࠨᇨ"), datetime.now() - bstack11ll111l1l_opy_)
                    f.bstack1ll111lll1l_opy_(instance, bstack11111l111l_opy_)
                instance.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥᇩ"), datetime.now() - bstack1ll111111l1_opy_)
                return # bstack1l1lllll1l1_opy_ not send this event with the bstack1ll111ll11l_opy_ bstack1ll111ll1l1_opy_
            elif (
                test_framework_state == bstack1llll1l11ll_opy_.TEST
                and test_hook_state == bstack1llllll1l11_opy_.POST
                and not f.bstack111111l111_opy_(instance, TestFramework.bstack1l1llll11ll_opy_)
            ):
                self.logger.warning(bstack11111ll_opy_ (u"ࠣࡦࡵࡳࡵࡶࡩ࡯ࡩࠣࡨࡺ࡫ࠠࡵࡱࠣࡰࡦࡩ࡫ࠡࡱࡩࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࠨᇪ") + str(TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1l1llll11ll_opy_)) + bstack11111ll_opy_ (u"ࠤࠥᇫ"))
                f.bstack11111l11ll_opy_(instance, bstack1llll1l111l_opy_.bstack1ll111lll11_opy_, True)
                return # bstack1l1lllll1l1_opy_ not send this event bstack1l1lll1lll1_opy_ bstack1ll111l11l1_opy_
            elif (
                f.bstack11111lll1l_opy_(instance, bstack1llll1l111l_opy_.bstack1ll111lll11_opy_, False)
                and test_framework_state == bstack1llll1l11ll_opy_.LOG_REPORT
                and test_hook_state == bstack1llllll1l11_opy_.POST
                and f.bstack111111l111_opy_(instance, TestFramework.bstack1l1llll11ll_opy_)
            ):
                self.logger.warning(bstack11111ll_opy_ (u"ࠥ࡭ࡳࡰࡥࡤࡶ࡬ࡲ࡬ࠦࡔࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡢࡶࡨ࠲࡙ࡋࡓࡕ࠮ࠣࡘࡪࡹࡴࡉࡱࡲ࡯ࡘࡺࡡࡵࡧ࠱ࡔࡔ࡙ࡔࠡࠤᇬ") + str(TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1l1llll11ll_opy_)) + bstack11111ll_opy_ (u"ࠦࠧᇭ"))
                self.bstack1l1llll1lll_opy_(f, instance, (bstack1llll1l11ll_opy_.TEST, bstack1llllll1l11_opy_.POST), *args, **kwargs)
            bstack11ll111l1l_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1ll1111l111_opy_ = sorted(
                filter(lambda x: x.get(bstack11111ll_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᇮ"), None), data.pop(bstack11111ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᇯ"), {}).values()),
                key=lambda x: x[bstack11111ll_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᇰ")],
            )
            if bstack1llll11llll_opy_.bstack1ll111l1l11_opy_ in data:
                data.pop(bstack1llll11llll_opy_.bstack1ll111l1l11_opy_)
            data.update({bstack11111ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᇱ"): bstack1ll1111l111_opy_})
            instance.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠤ࡭ࡷࡴࡴ࠺ࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᇲ"), datetime.now() - bstack11ll111l1l_opy_)
            bstack11ll111l1l_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1lll1l111_opy_)
            instance.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠥ࡮ࡸࡵ࡮࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨᇳ"), datetime.now() - bstack11ll111l1l_opy_)
            self.bstack1ll111ll1l1_opy_(instance, bstack11111l111l_opy_, event_json=event_json)
            instance.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢᇴ"), datetime.now() - bstack1ll111111l1_opy_)
    def bstack1ll1l1l1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll111l1l_opy_
        bstack1ll1ll1l1ll_opy_ = bstack1llll111l1l_opy_.bstack1ll1l111lll_opy_(EVENTS.bstack11l11llll_opy_.value)
        self.bstack1ll1l1lllll_opy_.bstack1l1lll1ll1l_opy_(instance, f, bstack11111l111l_opy_, *args, **kwargs)
        bstack1llll111l1l_opy_.end(EVENTS.bstack11l11llll_opy_.value, bstack1ll1ll1l1ll_opy_ + bstack11111ll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᇵ"), bstack1ll1ll1l1ll_opy_ + bstack11111ll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᇶ"), status=True, failure=None, test_name=None)
    def bstack1ll1l1ll1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll1l1lllll_opy_.bstack1l1llll1l11_opy_(instance, f, bstack11111l111l_opy_, *args, **kwargs)
        self.bstack1l1lll1llll_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1llll1ll1_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def bstack1l1lll1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack11111ll_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡗࡩࡸࡺࡓࡦࡵࡶ࡭ࡴࡴࡅࡷࡧࡱࡸࠥ࡭ࡒࡑࡅࠣࡧࡦࡲ࡬࠻ࠢࡑࡳࠥࡼࡡ࡭࡫ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡪࡡࡵࡣࠥᇷ"))
            return
        bstack11ll111l1l_opy_ = datetime.now()
        try:
            r = self.bstack1llll1l1111_opy_.TestSessionEvent(req)
            instance.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡩࡻ࡫࡮ࡵࠤᇸ"), datetime.now() - bstack11ll111l1l_opy_)
            f.bstack11111l11ll_opy_(instance, self.bstack1ll1l1lllll_opy_.bstack1l1lll1111l_opy_, r.success)
            if not r.success:
                self.logger.info(bstack11111ll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᇹ") + str(r) + bstack11111ll_opy_ (u"ࠥࠦᇺ"))
        except grpc.RpcError as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᇻ") + str(e) + bstack11111ll_opy_ (u"ࠧࠨᇼ"))
            traceback.print_exc()
            raise e
    def bstack1l1lll11111_opy_(
        self,
        f: bstack1ll1lllll11_opy_,
        _driver: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        _1ll11111ll1_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll1lllll11_opy_.bstack1ll1l1l11l1_opy_(method_name):
            return
        if f.bstack1ll11llll1l_opy_(*args) == bstack1ll1lllll11_opy_.bstack1l1llll1l1l_opy_:
            bstack1ll111111l1_opy_ = datetime.now()
            screenshot = result.get(bstack11111ll_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᇽ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack11111ll_opy_ (u"ࠢࡪࡰࡹࡥࡱ࡯ࡤࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥ࡯࡭ࡢࡩࡨࠤࡧࡧࡳࡦ࠸࠷ࠤࡸࡺࡲࠣᇾ"))
                return
            bstack1l1llll11l1_opy_ = self.bstack1l1lll1l1l1_opy_(instance)
            if bstack1l1llll11l1_opy_:
                entry = bstack1ll1lllllll_opy_(TestFramework.bstack1ll11l1111l_opy_, screenshot)
                self.bstack1l1lll111l1_opy_(bstack1l1llll11l1_opy_, [entry])
                instance.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡧࡻࡩࡨࡻࡴࡦࠤᇿ"), datetime.now() - bstack1ll111111l1_opy_)
            else:
                self.logger.warning(bstack11111ll_opy_ (u"ࠤࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡶࡨࡷࡹࠦࡦࡰࡴࠣࡻ࡭࡯ࡣࡩࠢࡷ࡬࡮ࡹࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡼࡧࡳࠡࡶࡤ࡯ࡪࡴࠠࡣࡻࠣࡨࡷ࡯ࡶࡦࡴࡀࠤࢀࢃࠢሀ").format(instance.ref()))
        event = {}
        bstack1l1llll11l1_opy_ = self.bstack1l1lll1l1l1_opy_(instance)
        if bstack1l1llll11l1_opy_:
            self.bstack1ll11111l11_opy_(event, bstack1l1llll11l1_opy_)
            if event.get(bstack11111ll_opy_ (u"ࠥࡰࡴ࡭ࡳࠣሁ")):
                self.bstack1l1lll111l1_opy_(bstack1l1llll11l1_opy_, event[bstack11111ll_opy_ (u"ࠦࡱࡵࡧࡴࠤሂ")])
            else:
                self.logger.info(bstack11111ll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡱࡵࡧࡴࠢࡩࡳࡷࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡩࡻ࡫࡮ࡵࠤሃ"))
    @measure(event_name=EVENTS.bstack1l1lllllll1_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def bstack1l1lll111l1_opy_(
        self,
        bstack1l1llll11l1_opy_: bstack1lll1l1l1l1_opy_,
        entries: List[bstack1ll1lllllll_opy_],
    ):
        self.bstack1ll1l1l1lll_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111lll1l_opy_(bstack1l1llll11l1_opy_, TestFramework.bstack1ll1ll111ll_opy_)
        req.execution_context.hash = str(bstack1l1llll11l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1llll11l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1llll11l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack11111lll1l_opy_(bstack1l1llll11l1_opy_, TestFramework.bstack1ll1ll1111l_opy_)
            log_entry.test_framework_version = TestFramework.bstack11111lll1l_opy_(bstack1l1llll11l1_opy_, TestFramework.bstack1ll111l1lll_opy_)
            log_entry.uuid = TestFramework.bstack11111lll1l_opy_(bstack1l1llll11l1_opy_, TestFramework.bstack1ll1ll1lll1_opy_)
            log_entry.test_framework_state = bstack1l1llll11l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11111ll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧሄ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11111ll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤህ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1ll1111l1l1_opy_
                log_entry.file_path = entry.bstack1l11ll_opy_
        def bstack1l1lll1l11l_opy_():
            bstack11ll111l1l_opy_ = datetime.now()
            try:
                self.bstack1llll1l1111_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1ll11l1111l_opy_:
                    bstack1l1llll11l1_opy_.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧሆ"), datetime.now() - bstack11ll111l1l_opy_)
                elif entry.kind == TestFramework.bstack1ll111lllll_opy_:
                    bstack1l1llll11l1_opy_.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨሇ"), datetime.now() - bstack11ll111l1l_opy_)
                else:
                    bstack1l1llll11l1_opy_.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡰࡴ࡭ࠢለ"), datetime.now() - bstack11ll111l1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11111ll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤሉ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111l1ll11_opy_.enqueue(bstack1l1lll1l11l_opy_)
    @measure(event_name=EVENTS.bstack1l1lllll111_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def bstack1ll111ll1l1_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        event_json=None,
    ):
        self.bstack1ll1l1l1lll_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll1ll111ll_opy_)
        req.test_framework_name = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll1ll1111l_opy_)
        req.test_framework_version = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll111l1lll_opy_)
        req.test_framework_state = bstack11111l111l_opy_[0].name
        req.test_hook_state = bstack11111l111l_opy_[1].name
        started_at = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll111l11ll_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll111l111l_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1lll1l111_opy_)).encode(bstack11111ll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦሊ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1lll1l11l_opy_():
            bstack11ll111l1l_opy_ = datetime.now()
            try:
                self.bstack1llll1l1111_opy_.TestFrameworkEvent(req)
                instance.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡩࡻ࡫࡮ࡵࠤላ"), datetime.now() - bstack11ll111l1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11111ll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧሌ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111l1ll11_opy_.enqueue(bstack1l1lll1l11l_opy_)
    def bstack1l1lll1l1l1_opy_(self, instance: bstack1111l1111l_opy_):
        bstack1ll1111lll1_opy_ = TestFramework.bstack111111l1l1_opy_(instance.context)
        for t in bstack1ll1111lll1_opy_:
            bstack1ll111l1111_opy_ = TestFramework.bstack11111lll1l_opy_(t, bstack1llll11llll_opy_.bstack1ll111l1l11_opy_, [])
            if any(instance is d[1] for d in bstack1ll111l1111_opy_):
                return t
    def bstack1ll1111l11l_opy_(self, message):
        self.bstack1ll11111lll_opy_(message + bstack11111ll_opy_ (u"ࠣ࡞ࡱࠦል"))
    def log_error(self, message):
        self.bstack1l1lll11l11_opy_(message + bstack11111ll_opy_ (u"ࠤ࡟ࡲࠧሎ"))
    def bstack1ll11111l1l_opy_(self, level, original_func):
        def bstack1l1llll1111_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1ll1111lll1_opy_ = TestFramework.bstack1l1llllllll_opy_()
            if not bstack1ll1111lll1_opy_:
                return return_value
            bstack1l1llll11l1_opy_ = next(
                (
                    instance
                    for instance in bstack1ll1111lll1_opy_
                    if TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1ll1ll1lll1_opy_)
                ),
                None,
            )
            if not bstack1l1llll11l1_opy_:
                return
            entry = bstack1ll1lllllll_opy_(TestFramework.bstack1l1llllll1l_opy_, message, level)
            self.bstack1l1lll111l1_opy_(bstack1l1llll11l1_opy_, [entry])
            return return_value
        return bstack1l1llll1111_opy_
    def bstack1ll11111l11_opy_(self, event: dict, instance=None) -> None:
        global _1ll111ll111_opy_
        levels = [bstack11111ll_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨሏ"), bstack11111ll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣሐ")]
        bstack1l1lll1ll11_opy_ = bstack11111ll_opy_ (u"ࠧࠨሑ")
        if instance is not None:
            try:
                bstack1l1lll1ll11_opy_ = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll1ll1lll1_opy_)
            except Exception as e:
                self.logger.warning(bstack11111ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡶ࡫ࡧࠤ࡫ࡸ࡯࡮ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠦሒ").format(e))
        bstack1l1lll111ll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack11111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧሓ")]
                bstack1ll11l11111_opy_ = os.path.join(bstack1ll1111111l_opy_, (bstack1l1ll1lllll_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1ll11l11111_opy_):
                    self.logger.info(bstack11111ll_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡳࡵࡴࠡࡲࡵࡩࡸ࡫࡮ࡵࠢࡩࡳࡷࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡘࡪࡹࡴࠡࡣࡱࡨࠥࡈࡵࡪ࡮ࡧࠤࡱ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠣሔ").format(bstack1ll11l11111_opy_))
                file_names = os.listdir(bstack1ll11l11111_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1ll11l11111_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1ll111ll111_opy_:
                        self.logger.info(bstack11111ll_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢሕ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1ll1111ll1l_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1ll1111ll1l_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack11111ll_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨሖ"):
                                entry = bstack1ll1lllllll_opy_(
                                    kind=bstack11111ll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨሗ"),
                                    message=bstack11111ll_opy_ (u"ࠧࠨመ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1ll1111l1l1_opy_=file_size,
                                    bstack1ll111l1l1l_opy_=bstack11111ll_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨሙ"),
                                    bstack1l11ll_opy_=os.path.abspath(file_path),
                                    bstack1l1111l11l_opy_=bstack1l1lll1ll11_opy_
                                )
                            elif level == bstack11111ll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦሚ"):
                                entry = bstack1ll1lllllll_opy_(
                                    kind=bstack11111ll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥማ"),
                                    message=bstack11111ll_opy_ (u"ࠤࠥሜ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1ll1111l1l1_opy_=file_size,
                                    bstack1ll111l1l1l_opy_=bstack11111ll_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥም"),
                                    bstack1l11ll_opy_=os.path.abspath(file_path),
                                    bstack1ll111llll1_opy_=bstack1l1lll1ll11_opy_
                                )
                            bstack1l1lll111ll_opy_.append(entry)
                            _1ll111ll111_opy_.add(abs_path)
                        except Exception as bstack1l1lllll1ll_opy_:
                            self.logger.error(bstack11111ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡳࡣ࡬ࡷࡪࡪࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠢሞ").format(bstack1l1lllll1ll_opy_))
        except Exception as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡴࡤ࡭ࡸ࡫ࡤࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠣሟ").format(e))
        event[bstack11111ll_opy_ (u"ࠨ࡬ࡰࡩࡶࠦሠ")] = bstack1l1lll111ll_opy_
class bstack1l1lll1l111_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1lll11ll1_opy_ = set()
        kwargs[bstack11111ll_opy_ (u"ࠢࡴ࡭࡬ࡴࡰ࡫ࡹࡴࠤሡ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1ll111l1ll1_opy_(obj, self.bstack1l1lll11ll1_opy_)
def bstack1l1lll1l1ll_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1ll111l1ll1_opy_(obj, bstack1l1lll11ll1_opy_=None, max_depth=3):
    if bstack1l1lll11ll1_opy_ is None:
        bstack1l1lll11ll1_opy_ = set()
    if id(obj) in bstack1l1lll11ll1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1lll11ll1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1llllll11_opy_ = TestFramework.bstack1ll111ll1ll_opy_(obj)
    bstack1l1lll11lll_opy_ = next((k.lower() in bstack1l1llllll11_opy_.lower() for k in bstack1ll111111ll_opy_.keys()), None)
    if bstack1l1lll11lll_opy_:
        obj = TestFramework.bstack1ll11l111l1_opy_(obj, bstack1ll111111ll_opy_[bstack1l1lll11lll_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack11111ll_opy_ (u"ࠣࡡࡢࡷࡱࡵࡴࡴࡡࡢࠦሢ")):
            keys = getattr(obj, bstack11111ll_opy_ (u"ࠤࡢࡣࡸࡲ࡯ࡵࡵࡢࡣࠧሣ"), [])
        elif hasattr(obj, bstack11111ll_opy_ (u"ࠥࡣࡤࡪࡩࡤࡶࡢࡣࠧሤ")):
            keys = getattr(obj, bstack11111ll_opy_ (u"ࠦࡤࡥࡤࡪࡥࡷࡣࡤࠨሥ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack11111ll_opy_ (u"ࠧࡥࠢሦ"))}
        if not obj and bstack1l1llllll11_opy_ == bstack11111ll_opy_ (u"ࠨࡰࡢࡶ࡫ࡰ࡮ࡨ࠮ࡑࡱࡶ࡭ࡽࡖࡡࡵࡪࠥሧ"):
            obj = {bstack11111ll_opy_ (u"ࠢࡱࡣࡷ࡬ࠧረ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1lll1l1ll_opy_(key) or str(key).startswith(bstack11111ll_opy_ (u"ࠣࡡࠥሩ")):
            continue
        if value is not None and bstack1l1lll1l1ll_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1ll111l1ll1_opy_(value, bstack1l1lll11ll1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1ll111l1ll1_opy_(o, bstack1l1lll11ll1_opy_, max_depth) for o in value]))
    return result or None