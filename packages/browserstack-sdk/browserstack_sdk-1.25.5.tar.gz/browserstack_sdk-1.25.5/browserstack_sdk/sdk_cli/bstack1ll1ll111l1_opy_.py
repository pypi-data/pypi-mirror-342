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
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack11111lllll_opy_
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack11111l1lll_opy_,
    bstack111111ll1l_opy_,
    bstack1111l1lll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import bstack1111111ll1_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1lll1ll11l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1ll11l1lll_opy_ import bstack111111lll1_opy_
class bstack1ll1ll1ll11_opy_(bstack11111lllll_opy_):
    bstack1ll1lll1l11_opy_ = bstack1ll1l11_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵࠤᄙ")
    bstack1ll1llll11l_opy_ = bstack1ll1l11_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦᄚ")
    bstack1ll1ll11ll1_opy_ = bstack1ll1l11_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦᄛ")
    def __init__(self, bstack1ll1ll1ll1l_opy_):
        super().__init__()
        bstack1111111ll1_opy_.bstack111111l1l1_opy_((bstack11111l1lll_opy_.bstack1lll11llll1_opy_, bstack111111ll1l_opy_.PRE), self.bstack1ll1lll1lll_opy_)
        bstack1111111ll1_opy_.bstack111111l1l1_opy_((bstack11111l1lll_opy_.bstack1111l1l1l1_opy_, bstack111111ll1l_opy_.PRE), self.bstack1ll1lll1111_opy_)
        bstack1111111ll1_opy_.bstack111111l1l1_opy_((bstack11111l1lll_opy_.bstack1111l1l1l1_opy_, bstack111111ll1l_opy_.POST), self.bstack1ll1lll111l_opy_)
        bstack1111111ll1_opy_.bstack111111l1l1_opy_((bstack11111l1lll_opy_.bstack1111l1l1l1_opy_, bstack111111ll1l_opy_.POST), self.bstack1ll1l1lll1l_opy_)
        bstack1111111ll1_opy_.bstack111111l1l1_opy_((bstack11111l1lll_opy_.QUIT, bstack111111ll1l_opy_.POST), self.bstack1ll1ll1l11l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1lll1lll_opy_(
        self,
        f: bstack1111111ll1_opy_,
        driver: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1l11_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᄜ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            self.bstack1ll1l1lllll_opy_(instance, f, kwargs)
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷ࠴ࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࡼࡨ࠱ࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁ࠿ࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᄝ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠢࠣᄞ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll1lll1111_opy_(
        self,
        f: bstack1111111ll1_opy_,
        driver: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack11111l11l1_opy_(instance, bstack1ll1ll1ll11_opy_.bstack1ll1lll1l11_opy_, False):
            return
        if not f.bstack1llllll11l1_opy_(instance, bstack1111111ll1_opy_.bstack1111l11ll1_opy_):
            return
        platform_index = f.bstack11111l11l1_opy_(instance, bstack1111111ll1_opy_.bstack1111l11ll1_opy_)
        if f.bstack1ll1l1ll1ll_opy_(method_name, *args) and len(args) > 1:
            bstack1l1l1lllll_opy_ = datetime.now()
            hub_url = bstack1111111ll1_opy_.hub_url(driver)
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭࠿ࠥᄟ") + str(hub_url) + bstack1ll1l11_opy_ (u"ࠤࠥᄠ"))
            bstack1ll1lll1ll1_opy_ = args[1][bstack1ll1l11_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᄡ")] if isinstance(args[1], dict) and bstack1ll1l11_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᄢ") in args[1] else None
            bstack1ll1l1llll1_opy_ = bstack1ll1l11_opy_ (u"ࠧࡧ࡬ࡸࡣࡼࡷࡒࡧࡴࡤࡪࠥᄣ")
            if isinstance(bstack1ll1lll1ll1_opy_, dict):
                bstack1l1l1lllll_opy_ = datetime.now()
                r = self.bstack1ll1l1ll11l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷࠦᄤ"), datetime.now() - bstack1l1l1lllll_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1ll1l11_opy_ (u"ࠢࡴࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭࠺ࠡࠤᄥ") + str(r) + bstack1ll1l11_opy_ (u"ࠣࠤᄦ"))
                        return
                    if r.hub_url:
                        f.bstack1ll1ll1l1ll_opy_(instance, driver, r.hub_url)
                        f.bstack1lllllll1l1_opy_(instance, bstack1ll1ll1ll11_opy_.bstack1ll1lll1l11_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1ll1l11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣᄧ"), e)
    def bstack1ll1lll111l_opy_(
        self,
        f: bstack1111111ll1_opy_,
        driver: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1111111ll1_opy_.session_id(driver)
            if session_id:
                bstack1ll1ll111ll_opy_ = bstack1ll1l11_opy_ (u"ࠥࡿࢂࡀࡳࡵࡣࡵࡸࠧᄨ").format(session_id)
                bstack111111lll1_opy_.mark(bstack1ll1ll111ll_opy_)
    def bstack1ll1l1lll1l_opy_(
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
        if f.bstack11111l11l1_opy_(instance, bstack1ll1ll1ll11_opy_.bstack1ll1llll11l_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1111111ll1_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࠣᄩ") + str(hub_url) + bstack1ll1l11_opy_ (u"ࠧࠨᄪ"))
            return
        framework_session_id = bstack1111111ll1_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࠤᄫ") + str(framework_session_id) + bstack1ll1l11_opy_ (u"ࠢࠣᄬ"))
            return
        if bstack1111111ll1_opy_.bstack1ll1ll1l1l1_opy_(*args) == bstack1111111ll1_opy_.bstack1ll1ll1llll_opy_:
            bstack1ll1ll11lll_opy_ = bstack1ll1l11_opy_ (u"ࠣࡽࢀ࠾ࡪࡴࡤࠣᄭ").format(framework_session_id)
            bstack1ll1ll111ll_opy_ = bstack1ll1l11_opy_ (u"ࠤࡾࢁ࠿ࡹࡴࡢࡴࡷࠦᄮ").format(framework_session_id)
            bstack111111lll1_opy_.end(
                label=bstack1ll1l11_opy_ (u"ࠥࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡱࡶࡸ࠲࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳࠨᄯ"),
                start=bstack1ll1ll111ll_opy_,
                end=bstack1ll1ll11lll_opy_,
                status=True,
                failure=None
            )
            bstack1l1l1lllll_opy_ = datetime.now()
            r = self.bstack1ll1l1ll1l1_opy_(
                ref,
                f.bstack11111l11l1_opy_(instance, bstack1111111ll1_opy_.bstack1111l11ll1_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶࠥᄰ"), datetime.now() - bstack1l1l1lllll_opy_)
            f.bstack1lllllll1l1_opy_(instance, bstack1ll1ll1ll11_opy_.bstack1ll1llll11l_opy_, r.success)
    def bstack1ll1ll1l11l_opy_(
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
        if f.bstack11111l11l1_opy_(instance, bstack1ll1ll1ll11_opy_.bstack1ll1ll11ll1_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1111111ll1_opy_.session_id(driver)
        hub_url = bstack1111111ll1_opy_.hub_url(driver)
        bstack1l1l1lllll_opy_ = datetime.now()
        r = self.bstack1ll1ll11l1l_opy_(
            ref,
            f.bstack11111l11l1_opy_(instance, bstack1111111ll1_opy_.bstack1111l11ll1_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲࠥᄱ"), datetime.now() - bstack1l1l1lllll_opy_)
        f.bstack1lllllll1l1_opy_(instance, bstack1ll1ll1ll11_opy_.bstack1ll1ll11ll1_opy_, r.success)
    @measure(event_name=EVENTS.bstack11ll1l11l1_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def bstack1lll11lll1l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡹࡨࡦࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦᄲ") + str(req) + bstack1ll1l11_opy_ (u"ࠢࠣᄳ"))
        try:
            r = self.bstack1llll111lll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦᄴ") + str(r.success) + bstack1ll1l11_opy_ (u"ࠤࠥᄵ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᄶ") + str(e) + bstack1ll1l11_opy_ (u"ࠦࠧᄷ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1ll1l111_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def bstack1ll1l1ll11l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1lll1lll1ll_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࠢᄸ") + str(req) + bstack1ll1l11_opy_ (u"ࠨࠢᄹ"))
        try:
            r = self.bstack1llll111lll_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥᄺ") + str(r.success) + bstack1ll1l11_opy_ (u"ࠣࠤᄻ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᄼ") + str(e) + bstack1ll1l11_opy_ (u"ࠥࠦᄽ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1llll111_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def bstack1ll1l1ll1l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1lll1lll1ll_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸ࠿ࠦࠢᄾ") + str(req) + bstack1ll1l11_opy_ (u"ࠧࠨᄿ"))
        try:
            r = self.bstack1llll111lll_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᅀ") + str(r) + bstack1ll1l11_opy_ (u"ࠢࠣᅁ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᅂ") + str(e) + bstack1ll1l11_opy_ (u"ࠤࠥᅃ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1ll1111l_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def bstack1ll1ll11l1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1lll1lll1ll_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲ࠽ࠤࠧᅄ") + str(req) + bstack1ll1l11_opy_ (u"ࠦࠧᅅ"))
        try:
            r = self.bstack1llll111lll_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᅆ") + str(r) + bstack1ll1l11_opy_ (u"ࠨࠢᅇ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᅈ") + str(e) + bstack1ll1l11_opy_ (u"ࠣࠤᅉ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1111ll_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def bstack1ll1l1lllll_opy_(self, instance: bstack1111l1lll1_opy_, f: bstack1111111ll1_opy_, kwargs):
        bstack1ll1ll1lll1_opy_ = version.parse(f.framework_version)
        bstack1ll1lll11l1_opy_ = kwargs.get(bstack1ll1l11_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᅊ"))
        bstack1ll1l1lll11_opy_ = kwargs.get(bstack1ll1l11_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᅋ"))
        bstack1lll1l1l1l1_opy_ = {}
        bstack1ll1ll11l11_opy_ = {}
        bstack1ll1lll1l1l_opy_ = None
        bstack1ll1ll11111_opy_ = {}
        if bstack1ll1l1lll11_opy_ is not None or bstack1ll1lll11l1_opy_ is not None: # check top level caps
            if bstack1ll1l1lll11_opy_ is not None:
                bstack1ll1ll11111_opy_[bstack1ll1l11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᅌ")] = bstack1ll1l1lll11_opy_
            if bstack1ll1lll11l1_opy_ is not None and callable(getattr(bstack1ll1lll11l1_opy_, bstack1ll1l11_opy_ (u"ࠧࡺ࡯ࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᅍ"))):
                bstack1ll1ll11111_opy_[bstack1ll1l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡢࡵࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᅎ")] = bstack1ll1lll11l1_opy_.to_capabilities()
        response = self.bstack1lll11lll1l_opy_(f.platform_index, instance.ref(), json.dumps(bstack1ll1ll11111_opy_).encode(bstack1ll1l11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᅏ")))
        if response is not None and response.capabilities:
            bstack1lll1l1l1l1_opy_ = json.loads(response.capabilities.decode(bstack1ll1l11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᅐ")))
            if not bstack1lll1l1l1l1_opy_: # empty caps bstack1lll1l1lll1_opy_ bstack1lll1l1ll11_opy_ bstack1lll1l11l11_opy_ bstack1lll1l11111_opy_ or error in processing
                return
            bstack1ll1lll1l1l_opy_ = f.bstack1ll1l1ll111_opy_[bstack1ll1l11_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࡢࡪࡷࡵ࡭ࡠࡥࡤࡴࡸࠨᅑ")](bstack1lll1l1l1l1_opy_)
        if bstack1ll1lll11l1_opy_ is not None and bstack1ll1ll1lll1_opy_ >= version.parse(bstack1ll1l11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᅒ")):
            bstack1ll1ll11l11_opy_ = None
        if (
                not bstack1ll1lll11l1_opy_ and not bstack1ll1l1lll11_opy_
        ) or (
                bstack1ll1ll1lll1_opy_ < version.parse(bstack1ll1l11_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᅓ"))
        ):
            bstack1ll1ll11l11_opy_ = {}
            bstack1ll1ll11l11_opy_.update(bstack1lll1l1l1l1_opy_)
        self.logger.info(bstack1lll1ll11l_opy_)
        if os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠣᅔ")).lower().__eq__(bstack1ll1l11_opy_ (u"ࠨࡴࡳࡷࡨࠦᅕ")):
            kwargs.update(
                {
                    bstack1ll1l11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᅖ"): f.bstack1ll1lll11ll_opy_,
                }
            )
        if bstack1ll1ll1lll1_opy_ >= version.parse(bstack1ll1l11_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨᅗ")):
            if bstack1ll1l1lll11_opy_ is not None:
                del kwargs[bstack1ll1l11_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᅘ")]
            kwargs.update(
                {
                    bstack1ll1l11_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦᅙ"): bstack1ll1lll1l1l_opy_,
                    bstack1ll1l11_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣᅚ"): True,
                    bstack1ll1l11_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧᅛ"): None,
                }
            )
        elif bstack1ll1ll1lll1_opy_ >= version.parse(bstack1ll1l11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᅜ")):
            kwargs.update(
                {
                    bstack1ll1l11_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᅝ"): bstack1ll1ll11l11_opy_,
                    bstack1ll1l11_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᅞ"): bstack1ll1lll1l1l_opy_,
                    bstack1ll1l11_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᅟ"): True,
                    bstack1ll1l11_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᅠ"): None,
                }
            )
        elif bstack1ll1ll1lll1_opy_ >= version.parse(bstack1ll1l11_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫᅡ")):
            kwargs.update(
                {
                    bstack1ll1l11_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᅢ"): bstack1ll1ll11l11_opy_,
                    bstack1ll1l11_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥᅣ"): True,
                    bstack1ll1l11_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᅤ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1ll1l11_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᅥ"): bstack1ll1ll11l11_opy_,
                    bstack1ll1l11_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᅦ"): True,
                    bstack1ll1l11_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᅧ"): None,
                }
            )