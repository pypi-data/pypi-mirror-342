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
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import (
    bstack1111l11l1l_opy_,
    bstack11111l1ll1_opy_,
    bstack1111l1111l_opy_,
    bstack111111l1ll_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1lllll11l_opy_, bstack1ll1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll11ll1_opy_ import bstack1ll1lllll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_, bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1llll1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l1l1l1_opy_ import bstack1ll11l11lll_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack11lll111ll_opy_ import bstack1l1l1ll1l_opy_, bstack1l1l11l111_opy_, bstack1lllll11l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1llll11l1l1_opy_(bstack1ll11l11lll_opy_):
    bstack1l1l1lllll1_opy_ = bstack11111ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡲࡪࡸࡨࡶࡸࠨበ")
    bstack1ll111l1l11_opy_ = bstack11111ll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢቡ")
    bstack1l1l1ll1ll1_opy_ = bstack11111ll_opy_ (u"ࠤࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦቢ")
    bstack1l1l1l1lll1_opy_ = bstack11111ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥባ")
    bstack1l1l1ll11ll_opy_ = bstack11111ll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡶࡪ࡬ࡳࠣቤ")
    bstack1l1lll1111l_opy_ = bstack11111ll_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦብ")
    bstack1l1l1ll11l1_opy_ = bstack11111ll_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤቦ")
    bstack1l1l1ll111l_opy_ = bstack11111ll_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠧቧ")
    def __init__(self):
        super().__init__(bstack1ll11l1ll1l_opy_=self.bstack1l1l1lllll1_opy_, frameworks=[bstack1ll1lllll11_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1ll11l11_opy_((bstack1llll1l11ll_opy_.BEFORE_EACH, bstack1llllll1l11_opy_.POST), self.bstack1l1l1ll1l1l_opy_)
        if bstack1ll1ll1l_opy_():
            TestFramework.bstack1ll1ll11l11_opy_((bstack1llll1l11ll_opy_.TEST, bstack1llllll1l11_opy_.POST), self.bstack1ll1l1l1l11_opy_)
        else:
            TestFramework.bstack1ll1ll11l11_opy_((bstack1llll1l11ll_opy_.TEST, bstack1llllll1l11_opy_.PRE), self.bstack1ll1l1l1l11_opy_)
        TestFramework.bstack1ll1ll11l11_opy_((bstack1llll1l11ll_opy_.TEST, bstack1llllll1l11_opy_.POST), self.bstack1ll1l1ll1l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1ll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l1ll1l11_opy_ = self.bstack1l1l1lll1ll_opy_(instance.context)
        if not bstack1l1l1ll1l11_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡶࡡࡨࡧ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨቨ") + str(bstack11111l111l_opy_) + bstack11111ll_opy_ (u"ࠤࠥቩ"))
            return
        f.bstack11111l11ll_opy_(instance, bstack1llll11l1l1_opy_.bstack1ll111l1l11_opy_, bstack1l1l1ll1l11_opy_)
    def bstack1l1l1lll1ll_opy_(self, context: bstack111111l1ll_opy_, bstack1l1l1l1ll1l_opy_= True):
        if bstack1l1l1l1ll1l_opy_:
            bstack1l1l1ll1l11_opy_ = self.bstack1ll11l1lll1_opy_(context, reverse=True)
        else:
            bstack1l1l1ll1l11_opy_ = self.bstack1ll11l1ll11_opy_(context, reverse=True)
        return [f for f in bstack1l1l1ll1l11_opy_ if f[1].state != bstack1111l11l1l_opy_.QUIT]
    def bstack1ll1l1l1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll1l1l_opy_(f, instance, bstack11111l111l_opy_, *args, **kwargs)
        if not bstack1l1lllll11l_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨቪ") + str(kwargs) + bstack11111ll_opy_ (u"ࠦࠧቫ"))
            return
        bstack1l1l1ll1l11_opy_ = f.bstack11111lll1l_opy_(instance, bstack1llll11l1l1_opy_.bstack1ll111l1l11_opy_, [])
        if not bstack1l1l1ll1l11_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣቬ") + str(kwargs) + bstack11111ll_opy_ (u"ࠨࠢቭ"))
            return
        if len(bstack1l1l1ll1l11_opy_) > 1:
            self.logger.debug(
                bstack1lllll1l111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤቮ"))
        bstack1l1l1lll11l_opy_, bstack1l1ll1l1ll1_opy_ = bstack1l1l1ll1l11_opy_[0]
        page = bstack1l1l1lll11l_opy_()
        if not page:
            self.logger.debug(bstack11111ll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣቯ") + str(kwargs) + bstack11111ll_opy_ (u"ࠤࠥተ"))
            return
        bstack1l1l1l11_opy_ = getattr(args[0], bstack11111ll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥቱ"), None)
        try:
            page.evaluate(bstack11111ll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧቲ"),
                        bstack11111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩታ") + json.dumps(
                            bstack1l1l1l11_opy_) + bstack11111ll_opy_ (u"ࠨࡽࡾࠤቴ"))
        except Exception as e:
            self.logger.debug(bstack11111ll_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧት"), e)
    def bstack1ll1l1ll1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll1l1l_opy_(f, instance, bstack11111l111l_opy_, *args, **kwargs)
        if not bstack1l1lllll11l_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦቶ") + str(kwargs) + bstack11111ll_opy_ (u"ࠤࠥቷ"))
            return
        bstack1l1l1ll1l11_opy_ = f.bstack11111lll1l_opy_(instance, bstack1llll11l1l1_opy_.bstack1ll111l1l11_opy_, [])
        if not bstack1l1l1ll1l11_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨቸ") + str(kwargs) + bstack11111ll_opy_ (u"ࠦࠧቹ"))
            return
        if len(bstack1l1l1ll1l11_opy_) > 1:
            self.logger.debug(
                bstack1lllll1l111_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢቺ"))
        bstack1l1l1lll11l_opy_, bstack1l1ll1l1ll1_opy_ = bstack1l1l1ll1l11_opy_[0]
        page = bstack1l1l1lll11l_opy_()
        if not page:
            self.logger.debug(bstack11111ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨቻ") + str(kwargs) + bstack11111ll_opy_ (u"ࠢࠣቼ"))
            return
        status = f.bstack11111lll1l_opy_(instance, TestFramework.bstack1l1l1lll1l1_opy_, None)
        if not status:
            self.logger.debug(bstack11111ll_opy_ (u"ࠣࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦች") + str(bstack11111l111l_opy_) + bstack11111ll_opy_ (u"ࠤࠥቾ"))
            return
        bstack1l1l1ll1111_opy_ = {bstack11111ll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥቿ"): status.lower()}
        bstack1l1l1llll1l_opy_ = f.bstack11111lll1l_opy_(instance, TestFramework.bstack1l1l1llll11_opy_, None)
        if status.lower() == bstack11111ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫኀ") and bstack1l1l1llll1l_opy_ is not None:
            bstack1l1l1ll1111_opy_[bstack11111ll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬኁ")] = bstack1l1l1llll1l_opy_[0][bstack11111ll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩኂ")][0] if isinstance(bstack1l1l1llll1l_opy_, list) else str(bstack1l1l1llll1l_opy_)
        try:
              page.evaluate(
                    bstack11111ll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣኃ"),
                    bstack11111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥ࠭ኄ")
                    + json.dumps(bstack1l1l1ll1111_opy_)
                    + bstack11111ll_opy_ (u"ࠤࢀࠦኅ")
                )
        except Exception as e:
            self.logger.debug(bstack11111ll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠥኆ"), e)
    def bstack1l1lll1ll1l_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        f: TestFramework,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll1l1l_opy_(f, instance, bstack11111l111l_opy_, *args, **kwargs)
        if not bstack1l1lllll11l_opy_:
            self.logger.debug(
                bstack1lllll1l111_opy_ (u"ࠦࡲࡧࡲ࡬ࡡࡲ࠵࠶ࡿ࡟ࡴࡻࡱࡧ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧኇ"))
            return
        bstack1l1l1ll1l11_opy_ = f.bstack11111lll1l_opy_(instance, bstack1llll11l1l1_opy_.bstack1ll111l1l11_opy_, [])
        if not bstack1l1l1ll1l11_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣኈ") + str(kwargs) + bstack11111ll_opy_ (u"ࠨࠢ኉"))
            return
        if len(bstack1l1l1ll1l11_opy_) > 1:
            self.logger.debug(
                bstack1lllll1l111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤኊ"))
        bstack1l1l1lll11l_opy_, bstack1l1ll1l1ll1_opy_ = bstack1l1l1ll1l11_opy_[0]
        page = bstack1l1l1lll11l_opy_()
        if not page:
            self.logger.debug(bstack11111ll_opy_ (u"ࠣ࡯ࡤࡶࡰࡥ࡯࠲࠳ࡼࡣࡸࡿ࡮ࡤ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣኋ") + str(kwargs) + bstack11111ll_opy_ (u"ࠤࠥኌ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack11111ll_opy_ (u"ࠥࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡖࡽࡳࡩ࠺ࠣኍ") + str(timestamp)
        try:
            page.evaluate(
                bstack11111ll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ኎"),
                bstack11111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ኏").format(
                    json.dumps(
                        {
                            bstack11111ll_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨነ"): bstack11111ll_opy_ (u"ࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤኑ"),
                            bstack11111ll_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦኒ"): {
                                bstack11111ll_opy_ (u"ࠤࡷࡽࡵ࡫ࠢና"): bstack11111ll_opy_ (u"ࠥࡅࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠢኔ"),
                                bstack11111ll_opy_ (u"ࠦࡩࡧࡴࡢࠤን"): data,
                                bstack11111ll_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࠦኖ"): bstack11111ll_opy_ (u"ࠨࡤࡦࡤࡸ࡫ࠧኗ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack11111ll_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡳ࠶࠷ࡹࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡻࡾࠤኘ"), e)
    def bstack1l1llll1l11_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        f: TestFramework,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll1l1l_opy_(f, instance, bstack11111l111l_opy_, *args, **kwargs)
        if f.bstack11111lll1l_opy_(instance, bstack1llll11l1l1_opy_.bstack1l1lll1111l_opy_, False):
            return
        self.bstack1ll1l1l1lll_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll1ll111ll_opy_)
        req.test_framework_name = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll1ll1111l_opy_)
        req.test_framework_version = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll111l1lll_opy_)
        req.test_framework_state = bstack11111l111l_opy_[0].name
        req.test_hook_state = bstack11111l111l_opy_[1].name
        req.test_uuid = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll1ll1lll1_opy_)
        for bstack1l1l1ll1lll_opy_ in bstack1llll1ll1ll_opy_.bstack11111llll1_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack11111ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠢኙ")
                if bstack1l1lllll11l_opy_
                else bstack11111ll_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠣኚ")
            )
            session.ref = bstack1l1l1ll1lll_opy_.ref()
            session.hub_url = bstack1llll1ll1ll_opy_.bstack11111lll1l_opy_(bstack1l1l1ll1lll_opy_, bstack1llll1ll1ll_opy_.bstack1l1ll11l1ll_opy_, bstack11111ll_opy_ (u"ࠥࠦኛ"))
            session.framework_name = bstack1l1l1ll1lll_opy_.framework_name
            session.framework_version = bstack1l1l1ll1lll_opy_.framework_version
            session.framework_session_id = bstack1llll1ll1ll_opy_.bstack11111lll1l_opy_(bstack1l1l1ll1lll_opy_, bstack1llll1ll1ll_opy_.bstack1l1ll11l111_opy_, bstack11111ll_opy_ (u"ࠦࠧኜ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11lllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l1ll1l11_opy_ = f.bstack11111lll1l_opy_(instance, bstack1llll11l1l1_opy_.bstack1ll111l1l11_opy_, [])
        if not bstack1l1l1ll1l11_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨኝ") + str(kwargs) + bstack11111ll_opy_ (u"ࠨࠢኞ"))
            return
        if len(bstack1l1l1ll1l11_opy_) > 1:
            self.logger.debug(bstack11111ll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣኟ") + str(kwargs) + bstack11111ll_opy_ (u"ࠣࠤአ"))
        bstack1l1l1lll11l_opy_, bstack1l1ll1l1ll1_opy_ = bstack1l1l1ll1l11_opy_[0]
        page = bstack1l1l1lll11l_opy_()
        if not page:
            self.logger.debug(bstack11111ll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤኡ") + str(kwargs) + bstack11111ll_opy_ (u"ࠥࠦኢ"))
            return
        return page
    def bstack1ll1l1llll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l1l1llll_opy_ = {}
        for bstack1l1l1ll1lll_opy_ in bstack1llll1ll1ll_opy_.bstack11111llll1_opy_.values():
            caps = bstack1llll1ll1ll_opy_.bstack11111lll1l_opy_(bstack1l1l1ll1lll_opy_, bstack1llll1ll1ll_opy_.bstack1l1ll111l1l_opy_, bstack11111ll_opy_ (u"ࠦࠧኣ"))
        bstack1l1l1l1llll_opy_[bstack11111ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥኤ")] = caps.get(bstack11111ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢእ"), bstack11111ll_opy_ (u"ࠢࠣኦ"))
        bstack1l1l1l1llll_opy_[bstack11111ll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢኧ")] = caps.get(bstack11111ll_opy_ (u"ࠤࡲࡷࠧከ"), bstack11111ll_opy_ (u"ࠥࠦኩ"))
        bstack1l1l1l1llll_opy_[bstack11111ll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨኪ")] = caps.get(bstack11111ll_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤካ"), bstack11111ll_opy_ (u"ࠨࠢኬ"))
        bstack1l1l1l1llll_opy_[bstack11111ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣክ")] = caps.get(bstack11111ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥኮ"), bstack11111ll_opy_ (u"ࠤࠥኯ"))
        return bstack1l1l1l1llll_opy_
    def bstack1ll1l1lll11_opy_(self, page: object, bstack1ll1l1lll1l_opy_, args={}):
        try:
            bstack1l1l1lll111_opy_ = bstack11111ll_opy_ (u"ࠥࠦࠧ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࠪ࠱࠲࠳ࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡳ࡫ࡷࠡࡒࡵࡳࡲ࡯ࡳࡦࠪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠰ࠥࡸࡥ࡫ࡧࡦࡸ࠮ࠦ࠽࠿ࠢࡾࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶ࠲ࡵࡻࡳࡩࠪࡵࡩࡸࡵ࡬ࡷࡧࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢀ࡬࡮ࡠࡤࡲࡨࡾࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࡽࠪࠪࡾࡥࡷ࡭࡟࡫ࡵࡲࡲࢂ࠯ࠢࠣࠤኰ")
            bstack1ll1l1lll1l_opy_ = bstack1ll1l1lll1l_opy_.replace(bstack11111ll_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ኱"), bstack11111ll_opy_ (u"ࠧࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷࠧኲ"))
            script = bstack1l1l1lll111_opy_.format(fn_body=bstack1ll1l1lll1l_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠨࡡ࠲࠳ࡼࡣࡸࡩࡲࡪࡲࡷࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡅࡳࡴࡲࡶࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶ࠯ࠤࠧኳ") + str(e) + bstack11111ll_opy_ (u"ࠢࠣኴ"))