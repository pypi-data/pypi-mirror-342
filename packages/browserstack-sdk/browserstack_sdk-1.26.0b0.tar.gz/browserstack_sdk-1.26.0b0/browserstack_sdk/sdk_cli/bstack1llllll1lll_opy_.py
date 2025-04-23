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
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll11l1ll_opy_ import bstack1lllllll11l_opy_
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import (
    bstack1111l11l1l_opy_,
    bstack11111l1ll1_opy_,
    bstack1111l1111l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lllll11ll1_opy_ import bstack1ll1lllll11_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11l1111l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll111l1l_opy_
class bstack1lllll1l11l_opy_(bstack1lllllll11l_opy_):
    bstack1l1l11l111l_opy_ = bstack11111ll_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣኵ")
    bstack1l1l1l11ll1_opy_ = bstack11111ll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶࠥ኶")
    bstack1l1l1l1l1ll_opy_ = bstack11111ll_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲࠥ኷")
    def __init__(self, bstack1lllll1llll_opy_):
        super().__init__()
        bstack1ll1lllll11_opy_.bstack1ll1ll11l11_opy_((bstack1111l11l1l_opy_.bstack1111111l11_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1l1l11ll111_opy_)
        bstack1ll1lllll11_opy_.bstack1ll1ll11l11_opy_((bstack1111l11l1l_opy_.bstack1llllllll1l_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1ll11ll1lll_opy_)
        bstack1ll1lllll11_opy_.bstack1ll1ll11l11_opy_((bstack1111l11l1l_opy_.bstack1llllllll1l_opy_, bstack11111l1ll1_opy_.POST), self.bstack1l1l1l1l11l_opy_)
        bstack1ll1lllll11_opy_.bstack1ll1ll11l11_opy_((bstack1111l11l1l_opy_.bstack1llllllll1l_opy_, bstack11111l1ll1_opy_.POST), self.bstack1l1l1l11l1l_opy_)
        bstack1ll1lllll11_opy_.bstack1ll1ll11l11_opy_((bstack1111l11l1l_opy_.QUIT, bstack11111l1ll1_opy_.POST), self.bstack1l1l1l1ll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11ll111_opy_(
        self,
        f: bstack1ll1lllll11_opy_,
        driver: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11111ll_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨኸ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            self.bstack1l1l1l111ll_opy_(instance, f, kwargs)
            self.logger.debug(bstack11111ll_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠳ࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࡻࡧ࠰ࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࢀ࠾ࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦኹ") + str(kwargs) + bstack11111ll_opy_ (u"ࠨࠢኺ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll11ll1lll_opy_(
        self,
        f: bstack1ll1lllll11_opy_,
        driver: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack11111lll1l_opy_(instance, bstack1lllll1l11l_opy_.bstack1l1l11l111l_opy_, False):
            return
        if not f.bstack111111l111_opy_(instance, bstack1ll1lllll11_opy_.bstack1ll1ll111ll_opy_):
            return
        platform_index = f.bstack11111lll1l_opy_(instance, bstack1ll1lllll11_opy_.bstack1ll1ll111ll_opy_)
        if f.bstack1ll1l1l1111_opy_(method_name, *args) and len(args) > 1:
            bstack11ll111l1l_opy_ = datetime.now()
            hub_url = bstack1ll1lllll11_opy_.hub_url(driver)
            self.logger.warning(bstack11111ll_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬࠾ࠤኻ") + str(hub_url) + bstack11111ll_opy_ (u"ࠣࠤኼ"))
            bstack1l1l1l1111l_opy_ = args[1][bstack11111ll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣኽ")] if isinstance(args[1], dict) and bstack11111ll_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤኾ") in args[1] else None
            bstack1l1l11lll1l_opy_ = bstack11111ll_opy_ (u"ࠦࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠤ኿")
            if isinstance(bstack1l1l1l1111l_opy_, dict):
                bstack11ll111l1l_opy_ = datetime.now()
                r = self.bstack1l1l11l1l1l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶࠥዀ"), datetime.now() - bstack11ll111l1l_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11111ll_opy_ (u"ࠨࡳࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࡀࠠࠣ዁") + str(r) + bstack11111ll_opy_ (u"ࠢࠣዂ"))
                        return
                    if r.hub_url:
                        f.bstack1l1l11l1ll1_opy_(instance, driver, r.hub_url)
                        f.bstack11111l11ll_opy_(instance, bstack1lllll1l11l_opy_.bstack1l1l11l111l_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11111ll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢዃ"), e)
    def bstack1l1l1l1l11l_opy_(
        self,
        f: bstack1ll1lllll11_opy_,
        driver: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll1lllll11_opy_.session_id(driver)
            if session_id:
                bstack1l1l11ll1ll_opy_ = bstack11111ll_opy_ (u"ࠤࡾࢁ࠿ࡹࡴࡢࡴࡷࠦዄ").format(session_id)
                bstack1llll111l1l_opy_.mark(bstack1l1l11ll1ll_opy_)
    def bstack1l1l1l11l1l_opy_(
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
        if f.bstack11111lll1l_opy_(instance, bstack1lllll1l11l_opy_.bstack1l1l1l11ll1_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll1lllll11_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11111ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡮ࡵࡣࡡࡸࡶࡱࡃࠢዅ") + str(hub_url) + bstack11111ll_opy_ (u"ࠦࠧ዆"))
            return
        framework_session_id = bstack1ll1lllll11_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11111ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣ዇") + str(framework_session_id) + bstack11111ll_opy_ (u"ࠨࠢወ"))
            return
        if bstack1ll1lllll11_opy_.bstack1l1l11ll1l1_opy_(*args) == bstack1ll1lllll11_opy_.bstack1l1l1l11lll_opy_:
            bstack1l1l11l11ll_opy_ = bstack11111ll_opy_ (u"ࠢࡼࡿ࠽ࡩࡳࡪࠢዉ").format(framework_session_id)
            bstack1l1l11ll1ll_opy_ = bstack11111ll_opy_ (u"ࠣࡽࢀ࠾ࡸࡺࡡࡳࡶࠥዊ").format(framework_session_id)
            bstack1llll111l1l_opy_.end(
                label=bstack11111ll_opy_ (u"ࠤࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡰࡵࡷ࠱࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠧዋ"),
                start=bstack1l1l11ll1ll_opy_,
                end=bstack1l1l11l11ll_opy_,
                status=True,
                failure=None
            )
            bstack11ll111l1l_opy_ = datetime.now()
            r = self.bstack1l1l1l11l11_opy_(
                ref,
                f.bstack11111lll1l_opy_(instance, bstack1ll1lllll11_opy_.bstack1ll1ll111ll_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵࠤዌ"), datetime.now() - bstack11ll111l1l_opy_)
            f.bstack11111l11ll_opy_(instance, bstack1lllll1l11l_opy_.bstack1l1l1l11ll1_opy_, r.success)
    def bstack1l1l1l1ll11_opy_(
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
        if f.bstack11111lll1l_opy_(instance, bstack1lllll1l11l_opy_.bstack1l1l1l1l1ll_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll1lllll11_opy_.session_id(driver)
        hub_url = bstack1ll1lllll11_opy_.hub_url(driver)
        bstack11ll111l1l_opy_ = datetime.now()
        r = self.bstack1l1l11llll1_opy_(
            ref,
            f.bstack11111lll1l_opy_(instance, bstack1ll1lllll11_opy_.bstack1ll1ll111ll_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱࠤው"), datetime.now() - bstack11ll111l1l_opy_)
        f.bstack11111l11ll_opy_(instance, bstack1lllll1l11l_opy_.bstack1l1l1l1l1ll_opy_, r.success)
    @measure(event_name=EVENTS.bstack1l111ll1_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def bstack1l1ll1111ll_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack11111ll_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࠥዎ") + str(req) + bstack11111ll_opy_ (u"ࠨࠢዏ"))
        try:
            r = self.bstack1llll1l1111_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11111ll_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥዐ") + str(r.success) + bstack11111ll_opy_ (u"ࠣࠤዑ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢዒ") + str(e) + bstack11111ll_opy_ (u"ࠥࠦዓ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1l111l1_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def bstack1l1l11l1l1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll1l1l1lll_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack11111ll_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥࠨዔ") + str(req) + bstack11111ll_opy_ (u"ࠧࠨዕ"))
        try:
            r = self.bstack1llll1l1111_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11111ll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤዖ") + str(r.success) + bstack11111ll_opy_ (u"ࠢࠣ዗"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨዘ") + str(e) + bstack11111ll_opy_ (u"ࠤࠥዙ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11l11l1_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def bstack1l1l1l11l11_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l1l1lll_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11111ll_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷ࠾ࠥࠨዚ") + str(req) + bstack11111ll_opy_ (u"ࠦࠧዛ"))
        try:
            r = self.bstack1llll1l1111_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11111ll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢዜ") + str(r) + bstack11111ll_opy_ (u"ࠨࠢዝ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧዞ") + str(e) + bstack11111ll_opy_ (u"ࠣࠤዟ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11lllll_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def bstack1l1l11llll1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l1l1lll_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11111ll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱ࠼ࠣࠦዠ") + str(req) + bstack11111ll_opy_ (u"ࠥࠦዡ"))
        try:
            r = self.bstack1llll1l1111_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11111ll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨዢ") + str(r) + bstack11111ll_opy_ (u"ࠧࠨዣ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦዤ") + str(e) + bstack11111ll_opy_ (u"ࠢࠣዥ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l1l1l11_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def bstack1l1l1l111ll_opy_(self, instance: bstack1111l1111l_opy_, f: bstack1ll1lllll11_opy_, kwargs):
        bstack1l1l11lll11_opy_ = version.parse(f.framework_version)
        bstack1l1l1l1l111_opy_ = kwargs.get(bstack11111ll_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤዦ"))
        bstack1l1l11l1lll_opy_ = kwargs.get(bstack11111ll_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤዧ"))
        bstack1l1ll111111_opy_ = {}
        bstack1l1l1l1l1l1_opy_ = {}
        bstack1l1l11ll11l_opy_ = None
        bstack1l1l1l11111_opy_ = {}
        if bstack1l1l11l1lll_opy_ is not None or bstack1l1l1l1l111_opy_ is not None: # check top level caps
            if bstack1l1l11l1lll_opy_ is not None:
                bstack1l1l1l11111_opy_[bstack11111ll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪየ")] = bstack1l1l11l1lll_opy_
            if bstack1l1l1l1l111_opy_ is not None and callable(getattr(bstack1l1l1l1l111_opy_, bstack11111ll_opy_ (u"ࠦࡹࡵ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨዩ"))):
                bstack1l1l1l11111_opy_[bstack11111ll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸࡥࡡࡴࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨዪ")] = bstack1l1l1l1l111_opy_.to_capabilities()
        response = self.bstack1l1ll1111ll_opy_(f.platform_index, instance.ref(), json.dumps(bstack1l1l1l11111_opy_).encode(bstack11111ll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧያ")))
        if response is not None and response.capabilities:
            bstack1l1ll111111_opy_ = json.loads(response.capabilities.decode(bstack11111ll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨዬ")))
            if not bstack1l1ll111111_opy_: # empty caps bstack1l1ll11ll1l_opy_ bstack1l1ll11ll11_opy_ bstack1l1ll111l11_opy_ bstack1llllll1l1l_opy_ or error in processing
                return
            bstack1l1l11ll11l_opy_ = f.bstack1lll111ll11_opy_[bstack11111ll_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡩࡶࡴࡳ࡟ࡤࡣࡳࡷࠧይ")](bstack1l1ll111111_opy_)
        if bstack1l1l1l1l111_opy_ is not None and bstack1l1l11lll11_opy_ >= version.parse(bstack11111ll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨዮ")):
            bstack1l1l1l1l1l1_opy_ = None
        if (
                not bstack1l1l1l1l111_opy_ and not bstack1l1l11l1lll_opy_
        ) or (
                bstack1l1l11lll11_opy_ < version.parse(bstack11111ll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩዯ"))
        ):
            bstack1l1l1l1l1l1_opy_ = {}
            bstack1l1l1l1l1l1_opy_.update(bstack1l1ll111111_opy_)
        self.logger.info(bstack11l1111l1_opy_)
        if os.environ.get(bstack11111ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠢደ")).lower().__eq__(bstack11111ll_opy_ (u"ࠧࡺࡲࡶࡧࠥዱ")):
            kwargs.update(
                {
                    bstack11111ll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤዲ"): f.bstack1l1l11l1l11_opy_,
                }
            )
        if bstack1l1l11lll11_opy_ >= version.parse(bstack11111ll_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧዳ")):
            if bstack1l1l11l1lll_opy_ is not None:
                del kwargs[bstack11111ll_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣዴ")]
            kwargs.update(
                {
                    bstack11111ll_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥድ"): bstack1l1l11ll11l_opy_,
                    bstack11111ll_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢዶ"): True,
                    bstack11111ll_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦዷ"): None,
                }
            )
        elif bstack1l1l11lll11_opy_ >= version.parse(bstack11111ll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫዸ")):
            kwargs.update(
                {
                    bstack11111ll_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨዹ"): bstack1l1l1l1l1l1_opy_,
                    bstack11111ll_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣዺ"): bstack1l1l11ll11l_opy_,
                    bstack11111ll_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧዻ"): True,
                    bstack11111ll_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤዼ"): None,
                }
            )
        elif bstack1l1l11lll11_opy_ >= version.parse(bstack11111ll_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪዽ")):
            kwargs.update(
                {
                    bstack11111ll_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦዾ"): bstack1l1l1l1l1l1_opy_,
                    bstack11111ll_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤዿ"): True,
                    bstack11111ll_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨጀ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11111ll_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢጁ"): bstack1l1l1l1l1l1_opy_,
                    bstack11111ll_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧጂ"): True,
                    bstack11111ll_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤጃ"): None,
                }
            )