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
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import (
    bstack1111l11l1l_opy_,
    bstack11111l1ll1_opy_,
    bstack1111l1l11l_opy_,
    bstack1111l1111l_opy_,
    bstack111111l1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lllll11ll1_opy_ import bstack1ll1lllll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_, bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l1l1l1_opy_ import bstack1ll11l11lll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1lllll11l_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1llll11llll_opy_(bstack1ll11l11lll_opy_):
    bstack1l1l1lllll1_opy_ = bstack11111ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡵ࡭ࡻ࡫ࡲࡴࠤጄ")
    bstack1ll111l1l11_opy_ = bstack11111ll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥጅ")
    bstack1l1l1ll1ll1_opy_ = bstack11111ll_opy_ (u"ࠧࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢጆ")
    bstack1l1l1l1lll1_opy_ = bstack11111ll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨጇ")
    bstack1l1l1ll11ll_opy_ = bstack11111ll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡲࡦࡨࡶࠦገ")
    bstack1l1lll1111l_opy_ = bstack11111ll_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪࠢጉ")
    bstack1l1l1ll11l1_opy_ = bstack11111ll_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧጊ")
    bstack1l1l1ll111l_opy_ = bstack11111ll_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠣጋ")
    def __init__(self):
        super().__init__(bstack1ll11l1ll1l_opy_=self.bstack1l1l1lllll1_opy_, frameworks=[bstack1ll1lllll11_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1ll11l11_opy_((bstack1llll1l11ll_opy_.BEFORE_EACH, bstack1llllll1l11_opy_.POST), self.bstack1l1l111l1l1_opy_)
        TestFramework.bstack1ll1ll11l11_opy_((bstack1llll1l11ll_opy_.TEST, bstack1llllll1l11_opy_.PRE), self.bstack1ll1l1l1l11_opy_)
        TestFramework.bstack1ll1ll11l11_opy_((bstack1llll1l11ll_opy_.TEST, bstack1llllll1l11_opy_.POST), self.bstack1ll1l1ll1l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs,
    ):
        bstack1ll111l1111_opy_ = self.bstack1l1l111l11l_opy_(instance.context)
        if not bstack1ll111l1111_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢጌ") + str(bstack11111l111l_opy_) + bstack11111ll_opy_ (u"ࠧࠨግ"))
        f.bstack11111l11ll_opy_(instance, bstack1llll11llll_opy_.bstack1ll111l1l11_opy_, bstack1ll111l1111_opy_)
        bstack1l1l1111ll1_opy_ = self.bstack1l1l111l11l_opy_(instance.context, bstack1l1l111l111_opy_=False)
        f.bstack11111l11ll_opy_(instance, bstack1llll11llll_opy_.bstack1l1l1ll1ll1_opy_, bstack1l1l1111ll1_opy_)
    def bstack1ll1l1l1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1l1_opy_(f, instance, bstack11111l111l_opy_, *args, **kwargs)
        if not f.bstack11111lll1l_opy_(instance, bstack1llll11llll_opy_.bstack1l1l1ll11l1_opy_, False):
            self.__1l1l111l1ll_opy_(f,instance,bstack11111l111l_opy_)
    def bstack1ll1l1ll1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1l1_opy_(f, instance, bstack11111l111l_opy_, *args, **kwargs)
        if not f.bstack11111lll1l_opy_(instance, bstack1llll11llll_opy_.bstack1l1l1ll11l1_opy_, False):
            self.__1l1l111l1ll_opy_(f, instance, bstack11111l111l_opy_)
        if not f.bstack11111lll1l_opy_(instance, bstack1llll11llll_opy_.bstack1l1l1ll111l_opy_, False):
            self.__1l1l111lll1_opy_(f, instance, bstack11111l111l_opy_)
    def bstack1l1l111llll_opy_(
        self,
        f: bstack1ll1lllll11_opy_,
        driver: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll1l1l1ll1_opy_(instance):
            return
        if f.bstack11111lll1l_opy_(instance, bstack1llll11llll_opy_.bstack1l1l1ll111l_opy_, False):
            return
        driver.execute_script(
            bstack11111ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦጎ").format(
                json.dumps(
                    {
                        bstack11111ll_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢጏ"): bstack11111ll_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦጐ"),
                        bstack11111ll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧ጑"): {bstack11111ll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥጒ"): result},
                    }
                )
            )
        )
        f.bstack11111l11ll_opy_(instance, bstack1llll11llll_opy_.bstack1l1l1ll111l_opy_, True)
    def bstack1l1l111l11l_opy_(self, context: bstack111111l1ll_opy_, bstack1l1l111l111_opy_= True):
        if bstack1l1l111l111_opy_:
            bstack1ll111l1111_opy_ = self.bstack1ll11l1lll1_opy_(context, reverse=True)
        else:
            bstack1ll111l1111_opy_ = self.bstack1ll11l1ll11_opy_(context, reverse=True)
        return [f for f in bstack1ll111l1111_opy_ if f[1].state != bstack1111l11l1l_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1ll1l11ll_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def __1l1l111lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
    ):
        bstack1ll111l1111_opy_ = f.bstack11111lll1l_opy_(instance, bstack1llll11llll_opy_.bstack1ll111l1l11_opy_, [])
        if not bstack1ll111l1111_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢጓ") + str(bstack11111l111l_opy_) + bstack11111ll_opy_ (u"ࠧࠨጔ"))
            return
        driver = bstack1ll111l1111_opy_[0][0]()
        status = f.bstack11111lll1l_opy_(instance, TestFramework.bstack1l1l1lll1l1_opy_, None)
        if not status:
            self.logger.debug(bstack11111ll_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣጕ") + str(bstack11111l111l_opy_) + bstack11111ll_opy_ (u"ࠢࠣ጖"))
            return
        bstack1l1l1ll1111_opy_ = {bstack11111ll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ጗"): status.lower()}
        bstack1l1l1llll1l_opy_ = f.bstack11111lll1l_opy_(instance, TestFramework.bstack1l1l1llll11_opy_, None)
        if status.lower() == bstack11111ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩጘ") and bstack1l1l1llll1l_opy_ is not None:
            bstack1l1l1ll1111_opy_[bstack11111ll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪጙ")] = bstack1l1l1llll1l_opy_[0][bstack11111ll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧጚ")][0] if isinstance(bstack1l1l1llll1l_opy_, list) else str(bstack1l1l1llll1l_opy_)
        driver.execute_script(
            bstack11111ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥጛ").format(
                json.dumps(
                    {
                        bstack11111ll_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨጜ"): bstack11111ll_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥጝ"),
                        bstack11111ll_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦጞ"): bstack1l1l1ll1111_opy_,
                    }
                )
            )
        )
        f.bstack11111l11ll_opy_(instance, bstack1llll11llll_opy_.bstack1l1l1ll111l_opy_, True)
    @measure(event_name=EVENTS.bstack1lll1llll1_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def __1l1l111l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_]
    ):
        test_name = f.bstack11111lll1l_opy_(instance, TestFramework.bstack1l1l1111lll_opy_, None)
        if not test_name:
            self.logger.debug(bstack11111ll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣጟ"))
            return
        bstack1ll111l1111_opy_ = f.bstack11111lll1l_opy_(instance, bstack1llll11llll_opy_.bstack1ll111l1l11_opy_, [])
        if not bstack1ll111l1111_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧጠ") + str(bstack11111l111l_opy_) + bstack11111ll_opy_ (u"ࠦࠧጡ"))
            return
        for bstack1l1ll1ll11l_opy_, bstack1l1l11l1111_opy_ in bstack1ll111l1111_opy_:
            if not bstack1ll1lllll11_opy_.bstack1ll1l1l1ll1_opy_(bstack1l1l11l1111_opy_):
                continue
            driver = bstack1l1ll1ll11l_opy_()
            if not driver:
                continue
            driver.execute_script(
                bstack11111ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥጢ").format(
                    json.dumps(
                        {
                            bstack11111ll_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨጣ"): bstack11111ll_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣጤ"),
                            bstack11111ll_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦጥ"): {bstack11111ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢጦ"): test_name},
                        }
                    )
                )
            )
        f.bstack11111l11ll_opy_(instance, bstack1llll11llll_opy_.bstack1l1l1ll11l1_opy_, True)
    def bstack1l1lll1ll1l_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        f: TestFramework,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1l1_opy_(f, instance, bstack11111l111l_opy_, *args, **kwargs)
        bstack1ll111l1111_opy_ = [d for d, _ in f.bstack11111lll1l_opy_(instance, bstack1llll11llll_opy_.bstack1ll111l1l11_opy_, [])]
        if not bstack1ll111l1111_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢࡷࡳࠥࡲࡩ࡯࡭ࠥጧ"))
            return
        if not bstack1l1lllll11l_opy_():
            self.logger.debug(bstack11111ll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤጨ"))
            return
        for bstack1l1l111ll11_opy_ in bstack1ll111l1111_opy_:
            driver = bstack1l1l111ll11_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack11111ll_opy_ (u"ࠧࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡘࡿ࡮ࡤ࠼ࠥጩ") + str(timestamp)
            driver.execute_script(
                bstack11111ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦጪ").format(
                    json.dumps(
                        {
                            bstack11111ll_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢጫ"): bstack11111ll_opy_ (u"ࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥጬ"),
                            bstack11111ll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧጭ"): {
                                bstack11111ll_opy_ (u"ࠥࡸࡾࡶࡥࠣጮ"): bstack11111ll_opy_ (u"ࠦࡆࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠣጯ"),
                                bstack11111ll_opy_ (u"ࠧࡪࡡࡵࡣࠥጰ"): data,
                                bstack11111ll_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࠧጱ"): bstack11111ll_opy_ (u"ࠢࡥࡧࡥࡹ࡬ࠨጲ")
                            }
                        }
                    )
                )
            )
    def bstack1l1llll1l11_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        f: TestFramework,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1l1_opy_(f, instance, bstack11111l111l_opy_, *args, **kwargs)
        bstack1ll111l1111_opy_ = [d for _, d in f.bstack11111lll1l_opy_(instance, bstack1llll11llll_opy_.bstack1ll111l1l11_opy_, [])] + [d for _, d in f.bstack11111lll1l_opy_(instance, bstack1llll11llll_opy_.bstack1l1l1ll1ll1_opy_, [])]
        keys = [
            bstack1llll11llll_opy_.bstack1ll111l1l11_opy_,
            bstack1llll11llll_opy_.bstack1l1l1ll1ll1_opy_,
        ]
        bstack1ll111l1111_opy_ = [
            d for key in keys for _, d in f.bstack11111lll1l_opy_(instance, key, [])
        ]
        if not bstack1ll111l1111_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡳࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢࡷࡳࠥࡲࡩ࡯࡭ࠥጳ"))
            return
        if f.bstack11111lll1l_opy_(instance, bstack1llll11llll_opy_.bstack1l1lll1111l_opy_, False):
            self.logger.debug(bstack11111ll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡇࡇ࡚ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡥࡵࡩࡦࡺࡥࡥࠤጴ"))
            return
        self.bstack1ll1l1l1lll_opy_()
        bstack11ll111l1l_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll1ll111ll_opy_)
        req.test_framework_name = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll1ll1111l_opy_)
        req.test_framework_version = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll111l1lll_opy_)
        req.test_framework_state = bstack11111l111l_opy_[0].name
        req.test_hook_state = bstack11111l111l_opy_[1].name
        req.test_uuid = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll1ll1lll1_opy_)
        for driver in bstack1ll111l1111_opy_:
            session = req.automation_sessions.add()
            session.provider = (
                bstack11111ll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤጵ")
                if bstack1ll1lllll11_opy_.bstack11111lll1l_opy_(driver, bstack1ll1lllll11_opy_.bstack1l1l111ll1l_opy_, False)
                else bstack11111ll_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥጶ")
            )
            session.ref = driver.ref()
            session.hub_url = bstack1ll1lllll11_opy_.bstack11111lll1l_opy_(driver, bstack1ll1lllll11_opy_.bstack1l1ll11l1ll_opy_, bstack11111ll_opy_ (u"ࠧࠨጷ"))
            session.framework_name = driver.framework_name
            session.framework_version = driver.framework_version
            session.framework_session_id = bstack1ll1lllll11_opy_.bstack11111lll1l_opy_(driver, bstack1ll1lllll11_opy_.bstack1l1ll11l111_opy_, bstack11111ll_opy_ (u"ࠨࠢጸ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l1llll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs
    ):
        bstack1ll111l1111_opy_ = f.bstack11111lll1l_opy_(instance, bstack1llll11llll_opy_.bstack1ll111l1l11_opy_, [])
        if not bstack1ll111l1111_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥጹ") + str(kwargs) + bstack11111ll_opy_ (u"ࠣࠤጺ"))
            return {}
        if len(bstack1ll111l1111_opy_) > 1:
            self.logger.debug(bstack11111ll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጻ") + str(kwargs) + bstack11111ll_opy_ (u"ࠥࠦጼ"))
            return {}
        bstack1l1ll1ll11l_opy_, bstack1l1ll1l1ll1_opy_ = bstack1ll111l1111_opy_[0]
        driver = bstack1l1ll1ll11l_opy_()
        if not driver:
            self.logger.debug(bstack11111ll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨጽ") + str(kwargs) + bstack11111ll_opy_ (u"ࠧࠨጾ"))
            return {}
        capabilities = f.bstack11111lll1l_opy_(bstack1l1ll1l1ll1_opy_, bstack1ll1lllll11_opy_.bstack1l1ll111l1l_opy_)
        if not capabilities:
            self.logger.debug(bstack11111ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨጿ") + str(kwargs) + bstack11111ll_opy_ (u"ࠢࠣፀ"))
            return {}
        return capabilities.get(bstack11111ll_opy_ (u"ࠣࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭ࠨፁ"), {})
    def bstack1ll11lllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs
    ):
        bstack1ll111l1111_opy_ = f.bstack11111lll1l_opy_(instance, bstack1llll11llll_opy_.bstack1ll111l1l11_opy_, [])
        if not bstack1ll111l1111_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧፂ") + str(kwargs) + bstack11111ll_opy_ (u"ࠥࠦፃ"))
            return
        if len(bstack1ll111l1111_opy_) > 1:
            self.logger.debug(bstack11111ll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢፄ") + str(kwargs) + bstack11111ll_opy_ (u"ࠧࠨፅ"))
        bstack1l1ll1ll11l_opy_, bstack1l1ll1l1ll1_opy_ = bstack1ll111l1111_opy_[0]
        driver = bstack1l1ll1ll11l_opy_()
        if not driver:
            self.logger.debug(bstack11111ll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣፆ") + str(kwargs) + bstack11111ll_opy_ (u"ࠢࠣፇ"))
            return
        return driver