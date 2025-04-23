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
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack11111l1lll_opy_,
    bstack111111ll1l_opy_,
    bstack1ll1l1l1111_opy_,
    bstack1111l1lll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import bstack1111111ll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack11111ll1l1_opy_, bstack1111111l1l_opy_, bstack11111l111l_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack11111lllll_opy_
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import bstack1111l11lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll111ll11_opy_ import bstack1lll11ll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11lll_opy_ import bstack1lll1l111l1_opy_
from bstack_utils.helper import bstack1l111lll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1ll11l1lll_opy_ import bstack111111lll1_opy_
import grpc
import traceback
import json
class bstack1l11ll111l1_opy_(bstack11111lllll_opy_):
    bstack1l111ll1111_opy_ = False
    bstack1l111l1l111_opy_ = bstack1ll1l11_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࠨᑧ")
    bstack1l111l11ll1_opy_ = bstack1ll1l11_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦ࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶࠧᑨ")
    bstack1l111l11lll_opy_ = bstack1ll1l11_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢ࡭ࡳ࡯ࡴࠣᑩ")
    bstack1l111ll1lll_opy_ = bstack1ll1l11_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣ࡮ࡹ࡟ࡴࡥࡤࡲࡳ࡯࡮ࡨࠤᑪ")
    bstack1l111l1llll_opy_ = bstack1ll1l11_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶࡤ࡮ࡡࡴࡡࡸࡶࡱࠨᑫ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1llll11lll1_opy_, bstack1lll1ll1lll_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        if not self.is_enabled():
            return
        self.bstack1llll111l1l_opy_ = bstack1lll1ll1lll_opy_
        bstack1llll11lll1_opy_.bstack111111l1l1_opy_((bstack11111l1lll_opy_.bstack1111l1l1l1_opy_, bstack111111ll1l_opy_.PRE), self.bstack1l111l1l11l_opy_)
        TestFramework.bstack111111l1l1_opy_((bstack11111ll1l1_opy_.TEST, bstack1111111l1l_opy_.PRE), self.bstack1llll11ll11_opy_)
        TestFramework.bstack111111l1l1_opy_((bstack11111ll1l1_opy_.TEST, bstack1111111l1l_opy_.POST), self.bstack1111111l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1llll11ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1l111l1l1l1_opy_(instance, args)
        test_framework = f.bstack11111l11l1_opy_(instance, TestFramework.bstack1llll1lllll_opy_)
        if bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᑬ") in instance.bstack1l1lll11l1l_opy_:
            platform_index = f.bstack11111l11l1_opy_(instance, TestFramework.bstack1111l11ll1_opy_)
            self.accessibility = self.bstack1l111lll111_opy_(tags, self.config[bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᑭ")][platform_index])
        else:
            capabilities = self.bstack1llll111l1l_opy_.bstack1ll1lllllll_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᑮ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠤࠥᑯ"))
                return
            self.accessibility = self.bstack1l111lll111_opy_(tags, capabilities)
        if self.bstack1llll111l1l_opy_.pages and self.bstack1llll111l1l_opy_.pages.values():
            bstack1l11l111111_opy_ = list(self.bstack1llll111l1l_opy_.pages.values())
            if bstack1l11l111111_opy_ and isinstance(bstack1l11l111111_opy_[0], (list, tuple)) and bstack1l11l111111_opy_[0]:
                bstack1l111llll11_opy_ = bstack1l11l111111_opy_[0][0]
                if callable(bstack1l111llll11_opy_):
                    page = bstack1l111llll11_opy_()
                    def bstack1l1ll1llll_opy_():
                        self.get_accessibility_results(page, bstack1ll1l11_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᑰ"))
                    def bstack1l111lll1l1_opy_():
                        self.get_accessibility_results_summary(page, bstack1ll1l11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᑱ"))
                    setattr(page, bstack1ll1l11_opy_ (u"ࠧ࡭ࡥࡵࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡓࡧࡶࡹࡱࡺࡳࠣᑲ"), bstack1l1ll1llll_opy_)
                    setattr(page, bstack1ll1l11_opy_ (u"ࠨࡧࡦࡶࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡔࡨࡷࡺࡲࡴࡔࡷࡰࡱࡦࡸࡹࠣᑳ"), bstack1l111lll1l1_opy_)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡴࡪࡲࡹࡱࡪࠠࡳࡷࡱࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡻࡧ࡬ࡶࡧࡀࠦᑴ") + str(self.accessibility) + bstack1ll1l11_opy_ (u"ࠣࠤᑵ"))
    def bstack1l111l1l11l_opy_(
        self,
        f: bstack1111111ll1_opy_,
        driver: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1l1l1lllll_opy_ = datetime.now()
            self.bstack1l111ll111l_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡪࡰ࡬ࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡩ࡯࡯ࡨ࡬࡫ࠧᑶ"), datetime.now() - bstack1l1l1lllll_opy_)
            if (
                not f.bstack1111l11111_opy_(method_name)
                or f.bstack1ll1l111lll_opy_(method_name, *args)
                or f.bstack1ll1l111l1l_opy_(method_name, *args)
            ):
                return
            if not f.bstack11111l11l1_opy_(instance, bstack1l11ll111l1_opy_.bstack1l111l11lll_opy_, False):
                if not bstack1l11ll111l1_opy_.bstack1l111ll1111_opy_:
                    self.logger.warning(bstack1ll1l11_opy_ (u"ࠥ࡟ࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨᑷ") + str(f.platform_index) + bstack1ll1l11_opy_ (u"ࠦࡢࠦࡡ࠲࠳ࡼࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣ࡬ࡦࡼࡥࠡࡰࡲࡸࠥࡨࡥࡦࡰࠣࡷࡪࡺࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡶࡩࡸࡹࡩࡰࡰࠥᑸ"))
                    bstack1l11ll111l1_opy_.bstack1l111ll1111_opy_ = True
                return
            bstack1l111llll1l_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l111llll1l_opy_:
                platform_index = f.bstack11111l11l1_opy_(instance, bstack1111111ll1_opy_.bstack1111l11ll1_opy_, 0)
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡴ࡯ࠡࡣ࠴࠵ࡾࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࢁࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᑹ") + str(f.framework_name) + bstack1ll1l11_opy_ (u"ࠨࠢᑺ"))
                return
            bstack1l1ll11l11l_opy_ = f.bstack111111l11l_opy_(*args)
            if not bstack1l1ll11l11l_opy_:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫ࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࠤᑻ") + str(method_name) + bstack1ll1l11_opy_ (u"ࠣࠤᑼ"))
                return
            bstack1l111l1ll11_opy_ = f.bstack11111l11l1_opy_(instance, bstack1l11ll111l1_opy_.bstack1l111l1llll_opy_, False)
            if bstack1l1ll11l11l_opy_ == bstack1ll1l11_opy_ (u"ࠤࡪࡩࡹࠨᑽ") and not bstack1l111l1ll11_opy_:
                f.bstack1lllllll1l1_opy_(instance, bstack1l11ll111l1_opy_.bstack1l111l1llll_opy_, True)
            if not bstack1l111l1ll11_opy_:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡲࡴࠦࡕࡓࡎࠣࡰࡴࡧࡤࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥ࠾ࠤᑾ") + str(bstack1l1ll11l11l_opy_) + bstack1ll1l11_opy_ (u"ࠦࠧᑿ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1l1ll11l11l_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡴ࡯ࠡࡣ࠴࠵ࡾࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦ࠿ࠥᒀ") + str(bstack1l1ll11l11l_opy_) + bstack1ll1l11_opy_ (u"ࠨࠢᒁ"))
                return
            self.logger.info(bstack1ll1l11_opy_ (u"ࠢࡳࡷࡱࡲ࡮ࡴࡧࠡࡽ࡯ࡩࡳ࠮ࡳࡤࡴ࡬ࡴࡹࡹ࡟ࡵࡱࡢࡶࡺࡴࠩࡾࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥ࠾ࠤᒂ") + str(bstack1l1ll11l11l_opy_) + bstack1ll1l11_opy_ (u"ࠣࠤᒃ"))
            scripts = [(s, bstack1l111llll1l_opy_[s]) for s in scripts_to_run if s in bstack1l111llll1l_opy_]
            for script_name, bstack1lll1111lll_opy_ in scripts:
                try:
                    bstack1l1l1lllll_opy_ = datetime.now()
                    if script_name == bstack1ll1l11_opy_ (u"ࠤࡶࡧࡦࡴࠢᒄ"):
                        result = self.perform_scan(driver, method=bstack1l1ll11l11l_opy_, framework_name=f.framework_name)
                    instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࠤᒅ") + script_name, datetime.now() - bstack1l1l1lllll_opy_)
                    if isinstance(result, dict) and not result.get(bstack1ll1l11_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᒆ"), True):
                        self.logger.warning(bstack1ll1l11_opy_ (u"ࠧࡹ࡫ࡪࡲࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡲࡦ࡯ࡤ࡭ࡳ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵࡵ࠽ࠤࠧᒇ") + str(result) + bstack1ll1l11_opy_ (u"ࠨࠢᒈ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵ࠿ࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾࠢࡨࡶࡷࡵࡲ࠾ࠤᒉ") + str(e) + bstack1ll1l11_opy_ (u"ࠣࠤᒊ"))
        except Exception as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡥࡳࡴࡲࡶࡂࠨᒋ") + str(e) + bstack1ll1l11_opy_ (u"ࠥࠦᒌ"))
    def bstack1111111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1l111l1l1l1_opy_(instance, args)
        capabilities = self.bstack1llll111l1l_opy_.bstack1ll1lllllll_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        self.accessibility = self.bstack1l111lll111_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠣᒍ"))
            return
        driver = self.bstack1llll111l1l_opy_.bstack1lll11111ll_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        test_name = f.bstack11111l11l1_opy_(instance, TestFramework.bstack1111l111ll_opy_)
        if not test_name:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥᒎ"))
            return
        test_uuid = f.bstack11111l11l1_opy_(instance, TestFramework.bstack11111111ll_opy_)
        if not test_uuid:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡵࡶ࡫ࡧࠦᒏ"))
            return
        if isinstance(self.bstack1llll111l1l_opy_, bstack1lll11ll11l_opy_):
            framework_name = bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᒐ")
        else:
            framework_name = bstack1ll1l11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪᒑ")
        self.bstack11111lll_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack11111l11ll_opy_ = bstack111111lll1_opy_.bstack11111l1111_opy_(EVENTS.bstack11l1l1l11l_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࠥᒒ"))
            return
        bstack1l1l1lllll_opy_ = datetime.now()
        bstack1lll1111lll_opy_ = self.scripts.get(framework_name, {}).get(bstack1ll1l11_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᒓ"), None)
        if not bstack1lll1111lll_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡳࡤࡣࡱࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᒔ") + str(framework_name) + bstack1ll1l11_opy_ (u"ࠧࠦࠢᒕ"))
            return
        instance = bstack1ll1l1l1111_opy_.bstack1ll11ll11l1_opy_(driver)
        if instance:
            if not bstack1ll1l1l1111_opy_.bstack11111l11l1_opy_(instance, bstack1l11ll111l1_opy_.bstack1l111ll1lll_opy_, False):
                bstack1ll1l1l1111_opy_.bstack1lllllll1l1_opy_(instance, bstack1l11ll111l1_opy_.bstack1l111ll1lll_opy_, True)
            else:
                self.logger.info(bstack1ll1l11_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡪࡰࠣࡴࡷࡵࡧࡳࡧࡶࡷࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡰࡩࡹ࡮࡯ࡥ࠿ࠥᒖ") + str(method) + bstack1ll1l11_opy_ (u"ࠢࠣᒗ"))
                return
        self.logger.info(bstack1ll1l11_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡂࠨᒘ") + str(method) + bstack1ll1l11_opy_ (u"ࠤࠥᒙ"))
        if framework_name == bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᒚ"):
            result = self.bstack1llll111l1l_opy_.bstack1lll1111l1l_opy_(driver, bstack1lll1111lll_opy_)
        else:
            result = driver.execute_async_script(bstack1lll1111lll_opy_, {bstack1ll1l11_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᒛ"): method if method else bstack1ll1l11_opy_ (u"ࠧࠨᒜ")})
        bstack111111lll1_opy_.end(EVENTS.bstack11l1l1l11l_opy_.value, bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᒝ"), bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᒞ"), True, None, command=method)
        if instance:
            bstack1ll1l1l1111_opy_.bstack1lllllll1l1_opy_(instance, bstack1l11ll111l1_opy_.bstack1l111ll1lll_opy_, False)
            instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲࠧᒟ"), datetime.now() - bstack1l1l1lllll_opy_)
        return result
    @measure(event_name=EVENTS.bstack111l111l1_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠦᒠ"))
            return
        bstack1lll1111lll_opy_ = self.scripts.get(framework_name, {}).get(bstack1ll1l11_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢᒡ"), None)
        if not bstack1lll1111lll_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᒢ") + str(framework_name) + bstack1ll1l11_opy_ (u"ࠧࠨᒣ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l1l1lllll_opy_ = datetime.now()
        if framework_name == bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᒤ"):
            result = self.bstack1llll111l1l_opy_.bstack1lll1111l1l_opy_(driver, bstack1lll1111lll_opy_)
        else:
            result = driver.execute_async_script(bstack1lll1111lll_opy_)
        instance = bstack1ll1l1l1111_opy_.bstack1ll11ll11l1_opy_(driver)
        if instance:
            instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࠥᒥ"), datetime.now() - bstack1l1l1lllll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll11lll11_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠦᒦ"))
            return
        bstack1lll1111lll_opy_ = self.scripts.get(framework_name, {}).get(bstack1ll1l11_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨᒧ"), None)
        if not bstack1lll1111lll_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᒨ") + str(framework_name) + bstack1ll1l11_opy_ (u"ࠦࠧᒩ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l1l1lllll_opy_ = datetime.now()
        if framework_name == bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᒪ"):
            result = self.bstack1llll111l1l_opy_.bstack1lll1111l1l_opy_(driver, bstack1lll1111lll_opy_)
        else:
            result = driver.execute_async_script(bstack1lll1111lll_opy_)
        instance = bstack1ll1l1l1111_opy_.bstack1ll11ll11l1_opy_(driver)
        if instance:
            instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻࠥᒫ"), datetime.now() - bstack1l1l1lllll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l111ll1l11_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def bstack1l111l1lll1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1lll1lll1ll_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1llll111lll_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᒬ") + str(r) + bstack1ll1l11_opy_ (u"ࠣࠤᒭ"))
            else:
                self.bstack1l111lllll1_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᒮ") + str(e) + bstack1ll1l11_opy_ (u"ࠥࠦᒯ"))
            traceback.print_exc()
            raise e
    def bstack1l111lllll1_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡱࡵࡡࡥࡡࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦᒰ"))
            return False
        if result.accessibility.options:
            options = result.accessibility.options
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l111ll1l1l_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1l111l1l111_opy_ and command.module == self.bstack1l111l11ll1_opy_:
                        if command.method and not command.method in bstack1l111ll1l1l_opy_:
                            bstack1l111ll1l1l_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1l111ll1l1l_opy_[command.method]:
                            bstack1l111ll1l1l_opy_[command.method][command.name] = list()
                        bstack1l111ll1l1l_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l111ll1l1l_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l111ll111l_opy_(
        self,
        f: bstack1111111ll1_opy_,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1llll111l1l_opy_, bstack1lll11ll11l_opy_) and method_name != bstack1ll1l11_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹ࠭ᒱ"):
            return
        if bstack1ll1l1l1111_opy_.bstack1llllll11l1_opy_(instance, bstack1l11ll111l1_opy_.bstack1l111l11lll_opy_):
            return
        if not f.bstack1ll1l11ll1l_opy_(instance):
            if not bstack1l11ll111l1_opy_.bstack1l111ll1111_opy_:
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠨࡡ࠲࠳ࡼࠤ࡫ࡲ࡯ࡸࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡰࡲࡲ࠲ࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤ࡮ࡴࡦࡳࡣࠥᒲ"))
                bstack1l11ll111l1_opy_.bstack1l111ll1111_opy_ = True
            return
        if f.bstack1ll1l1ll1ll_opy_(method_name, *args):
            bstack1l111ll11l1_opy_ = False
            desired_capabilities = f.bstack1ll1l1111ll_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll1l111ll1_opy_(instance)
                platform_index = f.bstack11111l11l1_opy_(instance, bstack1111111ll1_opy_.bstack1111l11ll1_opy_, 0)
                bstack1l111l11l1l_opy_ = datetime.now()
                r = self.bstack1l111l1lll1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡩ࡯࡯ࡨ࡬࡫ࠧᒳ"), datetime.now() - bstack1l111l11l1l_opy_)
                bstack1l111ll11l1_opy_ = r.success
            else:
                self.logger.error(bstack1ll1l11_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡧࡩࡸ࡯ࡲࡦࡦࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠿ࠥᒴ") + str(desired_capabilities) + bstack1ll1l11_opy_ (u"ࠤࠥᒵ"))
            f.bstack1lllllll1l1_opy_(instance, bstack1l11ll111l1_opy_.bstack1l111l11lll_opy_, bstack1l111ll11l1_opy_)
    def bstack11ll1ll1l1_opy_(self, test_tags):
        bstack1l111l1lll1_opy_ = self.config.get(bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᒶ"))
        if not bstack1l111l1lll1_opy_:
            return True
        try:
            include_tags = bstack1l111l1lll1_opy_[bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᒷ")] if bstack1ll1l11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᒸ") in bstack1l111l1lll1_opy_ and isinstance(bstack1l111l1lll1_opy_[bstack1ll1l11_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᒹ")], list) else []
            exclude_tags = bstack1l111l1lll1_opy_[bstack1ll1l11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᒺ")] if bstack1ll1l11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᒻ") in bstack1l111l1lll1_opy_ and isinstance(bstack1l111l1lll1_opy_[bstack1ll1l11_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᒼ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥᒽ") + str(error))
        return False
    def bstack1l111ll111_opy_(self, caps):
        try:
            bstack1l111lll11l_opy_ = caps.get(bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᒾ"), {}).get(bstack1ll1l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᒿ"), caps.get(bstack1ll1l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ᓀ"), bstack1ll1l11_opy_ (u"ࠧࠨᓁ")))
            if bstack1l111lll11l_opy_:
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡆࡨࡷࡰࡺ࡯ࡱࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧᓂ"))
                return False
            browser = caps.get(bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᓃ"), bstack1ll1l11_opy_ (u"ࠪࠫᓄ")).lower()
            if browser != bstack1ll1l11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᓅ"):
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᓆ"))
                return False
            browser_version = caps.get(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᓇ"))
            if browser_version and browser_version != bstack1ll1l11_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧᓈ") and int(browser_version.split(bstack1ll1l11_opy_ (u"ࠨ࠰ࠪᓉ"))[0]) <= 98:
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣ࠽࠽࠴ࠢᓊ"))
                return False
            bstack1l111ll1ll1_opy_ = caps.get(bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᓋ"), {}).get(bstack1ll1l11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᓌ"))
            if bstack1l111ll1ll1_opy_ and bstack1ll1l11_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩᓍ") in bstack1l111ll1ll1_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫᓎ"), []):
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤᓏ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥᓐ") + str(error))
            return False
    def bstack1l111llllll_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l11l11111l_opy_ = {
            bstack1ll1l11_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩᓑ"): test_uuid,
        }
        bstack1l111ll11ll_opy_ = {}
        if result.success:
            bstack1l111ll11ll_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l111lll1ll_opy_(bstack1l11l11111l_opy_, bstack1l111ll11ll_opy_)
    def bstack11111lll_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack11111l11ll_opy_ = None
        try:
            self.bstack1lll1lll1ll_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1ll1l11_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥᓒ")
            req.script_name = bstack1ll1l11_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤᓓ")
            r = self.bstack1llll111lll_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡥࡴ࡬ࡺࡪࡸࠠࡦࡺࡨࡧࡺࡺࡥࠡࡲࡤࡶࡦࡳࡳࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᓔ") + str(r.error) + bstack1ll1l11_opy_ (u"ࠨࠢᓕ"))
            else:
                bstack1l11l11111l_opy_ = self.bstack1l111llllll_opy_(test_uuid, r)
                bstack1lll1111lll_opy_ = r.script
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪᓖ") + str(bstack1l11l11111l_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1lll1111lll_opy_:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᓗ") + str(framework_name) + bstack1ll1l11_opy_ (u"ࠤࠣࠦᓘ"))
                return
            bstack11111l11ll_opy_ = bstack111111lll1_opy_.bstack11111l1111_opy_(EVENTS.bstack1l111l1l1ll_opy_.value)
            self.bstack1l111l11l11_opy_(driver, bstack1lll1111lll_opy_, bstack1l11l11111l_opy_, framework_name)
            self.logger.info(bstack1ll1l11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨᓙ"))
            bstack111111lll1_opy_.end(EVENTS.bstack1l111l1l1ll_opy_.value, bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᓚ"), bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᓛ"), True, None, command=bstack1ll1l11_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫᓜ"),test_name=name)
        except Exception as bstack1l111l1ll1l_opy_:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᓝ") + bstack1ll1l11_opy_ (u"ࠣࡵࡷࡶ࠭ࡶࡡࡵࡪࠬࠦᓞ") + bstack1ll1l11_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦᓟ") + str(bstack1l111l1ll1l_opy_))
            bstack111111lll1_opy_.end(EVENTS.bstack1l111l1l1ll_opy_.value, bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᓠ"), bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᓡ"), False, bstack1l111l1ll1l_opy_, command=bstack1ll1l11_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᓢ"),test_name=name)
    def bstack1l111l11l11_opy_(self, driver, bstack1lll1111lll_opy_, bstack1l11l11111l_opy_, framework_name):
        if framework_name == bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᓣ"):
            self.bstack1llll111l1l_opy_.bstack1lll1111l1l_opy_(driver, bstack1lll1111lll_opy_, bstack1l11l11111l_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1lll1111lll_opy_, bstack1l11l11111l_opy_))
    def _1l111l1l1l1_opy_(self, instance: bstack11111l111l_opy_, args: Tuple) -> list:
        bstack1ll1l11_opy_ (u"ࠢࠣࠤࡈࡼࡹࡸࡡࡤࡶࠣࡸࡦ࡭ࡳࠡࡤࡤࡷࡪࡪࠠࡰࡰࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࠤࠥࠦᓤ")
        if bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᓥ") in instance.bstack1l1lll11l1l_opy_:
            return args[2].tags if hasattr(args[2], bstack1ll1l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᓦ")) else []
        if hasattr(args[0], bstack1ll1l11_opy_ (u"ࠪࡳࡼࡴ࡟࡮ࡣࡵ࡯ࡪࡸࡳࠨᓧ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1l111lll111_opy_(self, tags, capabilities):
        return self.bstack11ll1ll1l1_opy_(tags) and self.bstack1l111ll111_opy_(capabilities)