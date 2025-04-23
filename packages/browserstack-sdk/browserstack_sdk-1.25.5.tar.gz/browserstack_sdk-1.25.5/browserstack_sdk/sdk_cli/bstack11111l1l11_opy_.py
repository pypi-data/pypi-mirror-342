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
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack11111l1lll_opy_,
    bstack111111ll1l_opy_,
    bstack1ll1l1l1111_opy_,
    bstack1111l1lll1_opy_,
    bstack1lll11l1ll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import bstack1111111ll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack11111ll1l1_opy_, bstack1111111l1l_opy_, bstack11111l111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l1l11_opy_ import bstack1lll111lll1_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1llll1l1l11_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1111l11lll_opy_(bstack1lll111lll1_opy_):
    bstack1lll11l11l1_opy_ = bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡶ࡮ࡼࡥࡳࡵࠥᅨ")
    bstack1111l1l11l_opy_ = bstack1ll1l11_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᅩ")
    bstack1ll1llll1ll_opy_ = bstack1ll1l11_opy_ (u"ࠨ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᅪ")
    bstack1ll1llllll1_opy_ = bstack1ll1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᅫ")
    bstack1lll111llll_opy_ = bstack1ll1l11_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡳࡧࡩࡷࠧᅬ")
    bstack1lll1lllll1_opy_ = bstack1ll1l11_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡤࡴࡨࡥࡹ࡫ࡤࠣᅭ")
    bstack1lll1111l11_opy_ = bstack1ll1l11_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᅮ")
    bstack1lll11l111l_opy_ = bstack1ll1l11_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠤᅯ")
    def __init__(self):
        super().__init__(bstack1lll11l11ll_opy_=self.bstack1lll11l11l1_opy_, frameworks=[bstack1111111ll1_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack111111l1l1_opy_((bstack11111ll1l1_opy_.BEFORE_EACH, bstack1111111l1l_opy_.POST), self.bstack1ll1l11llll_opy_)
        TestFramework.bstack111111l1l1_opy_((bstack11111ll1l1_opy_.TEST, bstack1111111l1l_opy_.PRE), self.bstack1llll11ll11_opy_)
        TestFramework.bstack111111l1l1_opy_((bstack11111ll1l1_opy_.TEST, bstack1111111l1l_opy_.POST), self.bstack1111111l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1l11llll_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        bstack11111ll11l_opy_ = self.bstack1ll1l11lll1_opy_(instance.context)
        if not bstack11111ll11l_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᅰ") + str(bstack111111111l_opy_) + bstack1ll1l11_opy_ (u"ࠨࠢᅱ"))
        f.bstack1lllllll1l1_opy_(instance, bstack1111l11lll_opy_.bstack1111l1l11l_opy_, bstack11111ll11l_opy_)
        bstack1ll1l1l111l_opy_ = self.bstack1ll1l11lll1_opy_(instance.context, bstack1ll1l11ll11_opy_=False)
        f.bstack1lllllll1l1_opy_(instance, bstack1111l11lll_opy_.bstack1ll1llll1ll_opy_, bstack1ll1l1l111l_opy_)
    def bstack1llll11ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1ll1l11llll_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        if not f.bstack11111l11l1_opy_(instance, bstack1111l11lll_opy_.bstack1lll1111l11_opy_, False):
            self.__1ll1l1l1lll_opy_(f,instance,bstack111111111l_opy_)
    def bstack1111111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1ll1l11llll_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        if not f.bstack11111l11l1_opy_(instance, bstack1111l11lll_opy_.bstack1lll1111l11_opy_, False):
            self.__1ll1l1l1lll_opy_(f, instance, bstack111111111l_opy_)
        if not f.bstack11111l11l1_opy_(instance, bstack1111l11lll_opy_.bstack1lll11l111l_opy_, False):
            self.__1ll1l1l1ll1_opy_(f, instance, bstack111111111l_opy_)
    def bstack1ll1l1l1l1l_opy_(
        self,
        f: bstack1111111ll1_opy_,
        driver: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll1l11ll1l_opy_(instance):
            return
        if f.bstack11111l11l1_opy_(instance, bstack1111l11lll_opy_.bstack1lll11l111l_opy_, False):
            return
        driver.execute_script(
            bstack1ll1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᅲ").format(
                json.dumps(
                    {
                        bstack1ll1l11_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᅳ"): bstack1ll1l11_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᅴ"),
                        bstack1ll1l11_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᅵ"): {bstack1ll1l11_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᅶ"): result},
                    }
                )
            )
        )
        f.bstack1lllllll1l1_opy_(instance, bstack1111l11lll_opy_.bstack1lll11l111l_opy_, True)
    def bstack1ll1l11lll1_opy_(self, context: bstack1lll11l1ll1_opy_, bstack1ll1l11ll11_opy_= True):
        if bstack1ll1l11ll11_opy_:
            bstack11111ll11l_opy_ = self.bstack1lll111l1l1_opy_(context, reverse=True)
        else:
            bstack11111ll11l_opy_ = self.bstack1lll111l11l_opy_(context, reverse=True)
        return [f for f in bstack11111ll11l_opy_ if f[1].state != bstack11111l1lll_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11llll1l11_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def __1ll1l1l1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
    ):
        bstack11111ll11l_opy_ = f.bstack11111l11l1_opy_(instance, bstack1111l11lll_opy_.bstack1111l1l11l_opy_, [])
        if not bstack11111ll11l_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᅷ") + str(bstack111111111l_opy_) + bstack1ll1l11_opy_ (u"ࠨࠢᅸ"))
            return
        driver = bstack11111ll11l_opy_[0][0]()
        status = f.bstack11111l11l1_opy_(instance, TestFramework.bstack1lll111111l_opy_, None)
        if not status:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᅹ") + str(bstack111111111l_opy_) + bstack1ll1l11_opy_ (u"ࠣࠤᅺ"))
            return
        bstack1lll111ll1l_opy_ = {bstack1ll1l11_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᅻ"): status.lower()}
        bstack1ll1llll1l1_opy_ = f.bstack11111l11l1_opy_(instance, TestFramework.bstack1lll11l1111_opy_, None)
        if status.lower() == bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᅼ") and bstack1ll1llll1l1_opy_ is not None:
            bstack1lll111ll1l_opy_[bstack1ll1l11_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫᅽ")] = bstack1ll1llll1l1_opy_[0][bstack1ll1l11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᅾ")][0] if isinstance(bstack1ll1llll1l1_opy_, list) else str(bstack1ll1llll1l1_opy_)
        driver.execute_script(
            bstack1ll1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᅿ").format(
                json.dumps(
                    {
                        bstack1ll1l11_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᆀ"): bstack1ll1l11_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᆁ"),
                        bstack1ll1l11_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᆂ"): bstack1lll111ll1l_opy_,
                    }
                )
            )
        )
        f.bstack1lllllll1l1_opy_(instance, bstack1111l11lll_opy_.bstack1lll11l111l_opy_, True)
    @measure(event_name=EVENTS.bstack1l1l1111_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def __1ll1l1l1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_]
    ):
        test_name = f.bstack11111l11l1_opy_(instance, TestFramework.bstack1ll1l1l11ll_opy_, None)
        if not test_name:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤᆃ"))
            return
        bstack11111ll11l_opy_ = f.bstack11111l11l1_opy_(instance, bstack1111l11lll_opy_.bstack1111l1l11l_opy_, [])
        if not bstack11111ll11l_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᆄ") + str(bstack111111111l_opy_) + bstack1ll1l11_opy_ (u"ࠧࠨᆅ"))
            return
        for bstack11111111l1_opy_, bstack1ll1l1l11l1_opy_ in bstack11111ll11l_opy_:
            if not bstack1111111ll1_opy_.bstack1ll1l11ll1l_opy_(bstack1ll1l1l11l1_opy_):
                continue
            driver = bstack11111111l1_opy_()
            if not driver:
                continue
            driver.execute_script(
                bstack1ll1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᆆ").format(
                    json.dumps(
                        {
                            bstack1ll1l11_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᆇ"): bstack1ll1l11_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤᆈ"),
                            bstack1ll1l11_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᆉ"): {bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᆊ"): test_name},
                        }
                    )
                )
            )
        f.bstack1lllllll1l1_opy_(instance, bstack1111l11lll_opy_.bstack1lll1111l11_opy_, True)
    def bstack1lllll1ll1l_opy_(
        self,
        instance: bstack11111l111l_opy_,
        f: TestFramework,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1ll1l11llll_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        bstack11111ll11l_opy_ = [d for d, _ in f.bstack11111l11l1_opy_(instance, bstack1111l11lll_opy_.bstack1111l1l11l_opy_, [])]
        if not bstack11111ll11l_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦᆋ"))
            return
        if not bstack1llll1l1l11_opy_():
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᆌ"))
            return
        for bstack1ll1l11l1ll_opy_ in bstack11111ll11l_opy_:
            driver = bstack1ll1l11l1ll_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1ll1l11_opy_ (u"ࠨࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࡙ࡹ࡯ࡥ࠽ࠦᆍ") + str(timestamp)
            driver.execute_script(
                bstack1ll1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᆎ").format(
                    json.dumps(
                        {
                            bstack1ll1l11_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᆏ"): bstack1ll1l11_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦᆐ"),
                            bstack1ll1l11_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᆑ"): {
                                bstack1ll1l11_opy_ (u"ࠦࡹࡿࡰࡦࠤᆒ"): bstack1ll1l11_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤᆓ"),
                                bstack1ll1l11_opy_ (u"ࠨࡤࡢࡶࡤࠦᆔ"): data,
                                bstack1ll1l11_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨᆕ"): bstack1ll1l11_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢᆖ")
                            }
                        }
                    )
                )
            )
    def bstack1llll11l11l_opy_(
        self,
        instance: bstack11111l111l_opy_,
        f: TestFramework,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1ll1l11llll_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        bstack11111ll11l_opy_ = [d for _, d in f.bstack11111l11l1_opy_(instance, bstack1111l11lll_opy_.bstack1111l1l11l_opy_, [])] + [d for _, d in f.bstack11111l11l1_opy_(instance, bstack1111l11lll_opy_.bstack1ll1llll1ll_opy_, [])]
        keys = [
            bstack1111l11lll_opy_.bstack1111l1l11l_opy_,
            bstack1111l11lll_opy_.bstack1ll1llll1ll_opy_,
        ]
        bstack11111ll11l_opy_ = [
            d for key in keys for _, d in f.bstack11111l11l1_opy_(instance, key, [])
        ]
        if not bstack11111ll11l_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡴࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦᆗ"))
            return
        if f.bstack11111l11l1_opy_(instance, bstack1111l11lll_opy_.bstack1lll1lllll1_opy_, False):
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡈࡈࡔࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡦࡶࡪࡧࡴࡦࡦࠥᆘ"))
            return
        self.bstack1lll1lll1ll_opy_()
        bstack1l1l1lllll_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1111l11ll1_opy_)
        req.test_framework_name = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1llll1lllll_opy_)
        req.test_framework_version = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1lllllllll1_opy_)
        req.test_framework_state = bstack111111111l_opy_[0].name
        req.test_hook_state = bstack111111111l_opy_[1].name
        req.test_uuid = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack11111111ll_opy_)
        for driver in bstack11111ll11l_opy_:
            session = req.automation_sessions.add()
            session.provider = (
                bstack1ll1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠥᆙ")
                if bstack1111111ll1_opy_.bstack11111l11l1_opy_(driver, bstack1111111ll1_opy_.bstack1ll1l1l1l11_opy_, False)
                else bstack1ll1l11_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠦᆚ")
            )
            session.ref = driver.ref()
            session.hub_url = bstack1111111ll1_opy_.bstack11111l11l1_opy_(driver, bstack1111111ll1_opy_.bstack1lll1l1111l_opy_, bstack1ll1l11_opy_ (u"ࠨࠢᆛ"))
            session.framework_name = driver.framework_name
            session.framework_version = driver.framework_version
            session.framework_session_id = bstack1111111ll1_opy_.bstack11111l11l1_opy_(driver, bstack1111111ll1_opy_.bstack1lll1l11ll1_opy_, bstack1ll1l11_opy_ (u"ࠢࠣᆜ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1lllllll_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs
    ):
        bstack11111ll11l_opy_ = f.bstack11111l11l1_opy_(instance, bstack1111l11lll_opy_.bstack1111l1l11l_opy_, [])
        if not bstack11111ll11l_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᆝ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠤࠥᆞ"))
            return {}
        if len(bstack11111ll11l_opy_) > 1:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᆟ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠦࠧᆠ"))
            return {}
        bstack11111111l1_opy_, bstack11111l1l1l_opy_ = bstack11111ll11l_opy_[0]
        driver = bstack11111111l1_opy_()
        if not driver:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᆡ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠨࠢᆢ"))
            return {}
        capabilities = f.bstack11111l11l1_opy_(bstack11111l1l1l_opy_, bstack1111111ll1_opy_.bstack1lll1l1l1ll_opy_)
        if not capabilities:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᆣ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠣࠤᆤ"))
            return {}
        return capabilities.get(bstack1ll1l11_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢᆥ"), {})
    def bstack1lll11111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs
    ):
        bstack11111ll11l_opy_ = f.bstack11111l11l1_opy_(instance, bstack1111l11lll_opy_.bstack1111l1l11l_opy_, [])
        if not bstack11111ll11l_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᆦ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠦࠧᆧ"))
            return
        if len(bstack11111ll11l_opy_) > 1:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᆨ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠨࠢᆩ"))
        bstack11111111l1_opy_, bstack11111l1l1l_opy_ = bstack11111ll11l_opy_[0]
        driver = bstack11111111l1_opy_()
        if not driver:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᆪ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠣࠤᆫ"))
            return
        return driver