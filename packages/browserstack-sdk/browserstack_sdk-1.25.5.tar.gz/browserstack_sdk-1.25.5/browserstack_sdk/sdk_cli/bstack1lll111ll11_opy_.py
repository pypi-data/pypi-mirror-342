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
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack11111l1lll_opy_,
    bstack111111ll1l_opy_,
    bstack1111l1lll1_opy_,
    bstack1lll11l1ll1_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1llll1l1l11_opy_, bstack1l1l1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import bstack1111111ll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack11111ll1l1_opy_, bstack1111111l1l_opy_, bstack11111l111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11lll_opy_ import bstack1lll1l111l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l1l11_opy_ import bstack1lll111lll1_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack11111l11_opy_ import bstack111lll111_opy_, bstack11lll1l11_opy_, bstack11llllll1_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1lll11ll11l_opy_(bstack1lll111lll1_opy_):
    bstack1lll11l11l1_opy_ = bstack1ll1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢჄ")
    bstack1111l1l11l_opy_ = bstack1ll1l11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣჅ")
    bstack1ll1llll1ll_opy_ = bstack1ll1l11_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧ჆")
    bstack1ll1llllll1_opy_ = bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦჇ")
    bstack1lll111llll_opy_ = bstack1ll1l11_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤ჈")
    bstack1lll1lllll1_opy_ = bstack1ll1l11_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧ჉")
    bstack1lll1111l11_opy_ = bstack1ll1l11_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥ჊")
    bstack1lll11l111l_opy_ = bstack1ll1l11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨ჋")
    def __init__(self):
        super().__init__(bstack1lll11l11ll_opy_=self.bstack1lll11l11l1_opy_, frameworks=[bstack1111111ll1_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack111111l1l1_opy_((bstack11111ll1l1_opy_.BEFORE_EACH, bstack1111111l1l_opy_.POST), self.bstack1lll11l1l1l_opy_)
        if bstack1l1l1ll1l_opy_():
            TestFramework.bstack111111l1l1_opy_((bstack11111ll1l1_opy_.TEST, bstack1111111l1l_opy_.POST), self.bstack1llll11ll11_opy_)
        else:
            TestFramework.bstack111111l1l1_opy_((bstack11111ll1l1_opy_.TEST, bstack1111111l1l_opy_.PRE), self.bstack1llll11ll11_opy_)
        TestFramework.bstack111111l1l1_opy_((bstack11111ll1l1_opy_.TEST, bstack1111111l1l_opy_.POST), self.bstack1111111l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1lll11l1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1ll1lllll11_opy_ = self.bstack1lll11111l1_opy_(instance.context)
        if not bstack1ll1lllll11_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡰࡢࡩࡨ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢ჌") + str(bstack111111111l_opy_) + bstack1ll1l11_opy_ (u"ࠥࠦჍ"))
            return
        f.bstack1lllllll1l1_opy_(instance, bstack1lll11ll11l_opy_.bstack1111l1l11l_opy_, bstack1ll1lllll11_opy_)
    def bstack1lll11111l1_opy_(self, context: bstack1lll11l1ll1_opy_, bstack1lll11l1lll_opy_= True):
        if bstack1lll11l1lll_opy_:
            bstack1ll1lllll11_opy_ = self.bstack1lll111l1l1_opy_(context, reverse=True)
        else:
            bstack1ll1lllll11_opy_ = self.bstack1lll111l11l_opy_(context, reverse=True)
        return [f for f in bstack1ll1lllll11_opy_ if f[1].state != bstack11111l1lll_opy_.QUIT]
    def bstack1llll11ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1lll11l1l1l_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        if not bstack1llll1l1l11_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ჎") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠧࠨ჏"))
            return
        bstack1ll1lllll11_opy_ = f.bstack11111l11l1_opy_(instance, bstack1lll11ll11l_opy_.bstack1111l1l11l_opy_, [])
        if not bstack1ll1lllll11_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤა") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠢࠣბ"))
            return
        if len(bstack1ll1lllll11_opy_) > 1:
            self.logger.debug(
                bstack1lll1111ll1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥგ"))
        bstack1lll11ll111_opy_, bstack11111l1l1l_opy_ = bstack1ll1lllll11_opy_[0]
        page = bstack1lll11ll111_opy_()
        if not page:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤდ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠥࠦე"))
            return
        bstack1l1ll111l1_opy_ = getattr(args[0], bstack1ll1l11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦვ"), None)
        try:
            page.evaluate(bstack1ll1l11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨზ"),
                        bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪთ") + json.dumps(
                            bstack1l1ll111l1_opy_) + bstack1ll1l11_opy_ (u"ࠢࡾࡿࠥი"))
        except Exception as e:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨკ"), e)
    def bstack1111111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1lll11l1l1l_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        if not bstack1llll1l1l11_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧლ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠥࠦმ"))
            return
        bstack1ll1lllll11_opy_ = f.bstack11111l11l1_opy_(instance, bstack1lll11ll11l_opy_.bstack1111l1l11l_opy_, [])
        if not bstack1ll1lllll11_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢნ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠧࠨო"))
            return
        if len(bstack1ll1lllll11_opy_) > 1:
            self.logger.debug(
                bstack1lll1111ll1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣპ"))
        bstack1lll11ll111_opy_, bstack11111l1l1l_opy_ = bstack1ll1lllll11_opy_[0]
        page = bstack1lll11ll111_opy_()
        if not page:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢჟ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠣࠤრ"))
            return
        status = f.bstack11111l11l1_opy_(instance, TestFramework.bstack1lll111111l_opy_, None)
        if not status:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧს") + str(bstack111111111l_opy_) + bstack1ll1l11_opy_ (u"ࠥࠦტ"))
            return
        bstack1lll111ll1l_opy_ = {bstack1ll1l11_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦუ"): status.lower()}
        bstack1ll1llll1l1_opy_ = f.bstack11111l11l1_opy_(instance, TestFramework.bstack1lll11l1111_opy_, None)
        if status.lower() == bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬფ") and bstack1ll1llll1l1_opy_ is not None:
            bstack1lll111ll1l_opy_[bstack1ll1l11_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ქ")] = bstack1ll1llll1l1_opy_[0][bstack1ll1l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪღ")][0] if isinstance(bstack1ll1llll1l1_opy_, list) else str(bstack1ll1llll1l1_opy_)
        try:
              page.evaluate(
                    bstack1ll1l11_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤყ"),
                    bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࠧშ")
                    + json.dumps(bstack1lll111ll1l_opy_)
                    + bstack1ll1l11_opy_ (u"ࠥࢁࠧჩ")
                )
        except Exception as e:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀࠦც"), e)
    def bstack1lllll1ll1l_opy_(
        self,
        instance: bstack11111l111l_opy_,
        f: TestFramework,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1lll11l1l1l_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        if not bstack1llll1l1l11_opy_:
            self.logger.debug(
                bstack1lll1111ll1_opy_ (u"ࠧࡳࡡࡳ࡭ࡢࡳ࠶࠷ࡹࡠࡵࡼࡲࡨࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨძ"))
            return
        bstack1ll1lllll11_opy_ = f.bstack11111l11l1_opy_(instance, bstack1lll11ll11l_opy_.bstack1111l1l11l_opy_, [])
        if not bstack1ll1lllll11_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤწ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠢࠣჭ"))
            return
        if len(bstack1ll1lllll11_opy_) > 1:
            self.logger.debug(
                bstack1lll1111ll1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥხ"))
        bstack1lll11ll111_opy_, bstack11111l1l1l_opy_ = bstack1ll1lllll11_opy_[0]
        page = bstack1lll11ll111_opy_()
        if not page:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡰࡥࡷࡱ࡟ࡰ࠳࠴ࡽࡤࡹࡹ࡯ࡥ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤჯ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠥࠦჰ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1ll1l11_opy_ (u"ࠦࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡗࡾࡴࡣ࠻ࠤჱ") + str(timestamp)
        try:
            page.evaluate(
                bstack1ll1l11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨჲ"),
                bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫჳ").format(
                    json.dumps(
                        {
                            bstack1ll1l11_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢჴ"): bstack1ll1l11_opy_ (u"ࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥჵ"),
                            bstack1ll1l11_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧჶ"): {
                                bstack1ll1l11_opy_ (u"ࠥࡸࡾࡶࡥࠣჷ"): bstack1ll1l11_opy_ (u"ࠦࡆࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠣჸ"),
                                bstack1ll1l11_opy_ (u"ࠧࡪࡡࡵࡣࠥჹ"): data,
                                bstack1ll1l11_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࠧჺ"): bstack1ll1l11_opy_ (u"ࠢࡥࡧࡥࡹ࡬ࠨ჻")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡴ࠷࠱ࡺࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡼࡿࠥჼ"), e)
    def bstack1llll11l11l_opy_(
        self,
        instance: bstack11111l111l_opy_,
        f: TestFramework,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1lll11l1l1l_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        if f.bstack11111l11l1_opy_(instance, bstack1lll11ll11l_opy_.bstack1lll1lllll1_opy_, False):
            return
        self.bstack1lll1lll1ll_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1111l11ll1_opy_)
        req.test_framework_name = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1llll1lllll_opy_)
        req.test_framework_version = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1lllllllll1_opy_)
        req.test_framework_state = bstack111111111l_opy_[0].name
        req.test_hook_state = bstack111111111l_opy_[1].name
        req.test_uuid = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack11111111ll_opy_)
        for bstack1lll111l1ll_opy_ in bstack1lll1l111l1_opy_.bstack1lll111l111_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack1ll1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣჽ")
                if bstack1llll1l1l11_opy_
                else bstack1ll1l11_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠤჾ")
            )
            session.ref = bstack1lll111l1ll_opy_.ref()
            session.hub_url = bstack1lll1l111l1_opy_.bstack11111l11l1_opy_(bstack1lll111l1ll_opy_, bstack1lll1l111l1_opy_.bstack1lll1l1111l_opy_, bstack1ll1l11_opy_ (u"ࠦࠧჿ"))
            session.framework_name = bstack1lll111l1ll_opy_.framework_name
            session.framework_version = bstack1lll111l1ll_opy_.framework_version
            session.framework_session_id = bstack1lll1l111l1_opy_.bstack11111l11l1_opy_(bstack1lll111l1ll_opy_, bstack1lll1l111l1_opy_.bstack1lll1l11ll1_opy_, bstack1ll1l11_opy_ (u"ࠧࠨᄀ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1lll11111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs
    ):
        bstack1ll1lllll11_opy_ = f.bstack11111l11l1_opy_(instance, bstack1lll11ll11l_opy_.bstack1111l1l11l_opy_, [])
        if not bstack1ll1lllll11_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᄁ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠢࠣᄂ"))
            return
        if len(bstack1ll1lllll11_opy_) > 1:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᄃ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠤࠥᄄ"))
        bstack1lll11ll111_opy_, bstack11111l1l1l_opy_ = bstack1ll1lllll11_opy_[0]
        page = bstack1lll11ll111_opy_()
        if not page:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᄅ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠦࠧᄆ"))
            return
        return page
    def bstack1ll1lllllll_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1lll1111111_opy_ = {}
        for bstack1lll111l1ll_opy_ in bstack1lll1l111l1_opy_.bstack1lll111l111_opy_.values():
            caps = bstack1lll1l111l1_opy_.bstack11111l11l1_opy_(bstack1lll111l1ll_opy_, bstack1lll1l111l1_opy_.bstack1lll1l1l1ll_opy_, bstack1ll1l11_opy_ (u"ࠧࠨᄇ"))
        bstack1lll1111111_opy_[bstack1ll1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦᄈ")] = caps.get(bstack1ll1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣᄉ"), bstack1ll1l11_opy_ (u"ࠣࠤᄊ"))
        bstack1lll1111111_opy_[bstack1ll1l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣᄋ")] = caps.get(bstack1ll1l11_opy_ (u"ࠥࡳࡸࠨᄌ"), bstack1ll1l11_opy_ (u"ࠦࠧᄍ"))
        bstack1lll1111111_opy_[bstack1ll1l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᄎ")] = caps.get(bstack1ll1l11_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥᄏ"), bstack1ll1l11_opy_ (u"ࠢࠣᄐ"))
        bstack1lll1111111_opy_[bstack1ll1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤᄑ")] = caps.get(bstack1ll1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦᄒ"), bstack1ll1l11_opy_ (u"ࠥࠦᄓ"))
        return bstack1lll1111111_opy_
    def bstack1lll1111l1l_opy_(self, page: object, bstack1lll1111lll_opy_, args={}):
        try:
            bstack1ll1lllll1l_opy_ = bstack1ll1l11_opy_ (u"ࠦࠧࠨࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫ࠲࠳࠴ࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡴࡥࡸࠢࡓࡶࡴࡳࡩࡴࡧࠫࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠱ࠦࡲࡦ࡬ࡨࡧࡹ࠯ࠠ࠾ࡀࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠳ࡶࡵࡴࡪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢁࡦ࡯ࡡࡥࡳࡩࡿࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫࠫࡿࡦࡸࡧࡠ࡬ࡶࡳࡳࢃࠩࠣࠤࠥᄔ")
            bstack1lll1111lll_opy_ = bstack1lll1111lll_opy_.replace(bstack1ll1l11_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣᄕ"), bstack1ll1l11_opy_ (u"ࠨࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸࠨᄖ"))
            script = bstack1ll1lllll1l_opy_.format(fn_body=bstack1lll1111lll_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡢ࠳࠴ࡽࡤࡹࡣࡳ࡫ࡳࡸࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡆࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷ࠰ࠥࠨᄗ") + str(e) + bstack1ll1l11_opy_ (u"ࠣࠤᄘ"))