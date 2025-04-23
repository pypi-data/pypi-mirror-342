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
from browserstack_sdk.sdk_cli.bstack1llll11l1ll_opy_ import bstack1lllllll11l_opy_
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import (
    bstack1111l11l1l_opy_,
    bstack11111l1ll1_opy_,
    bstack1111l1111l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lllll11ll1_opy_ import bstack1ll1lllll11_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll11l1ll_opy_ import bstack1lllllll11l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1lll1ll11ll_opy_(bstack1lllllll11l_opy_):
    bstack1ll1l111l1l_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1ll1lllll11_opy_.bstack1ll1ll11l11_opy_((bstack1111l11l1l_opy_.bstack1llllllll1l_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1ll11ll1lll_opy_)
    def is_enabled(self) -> bool:
        return True
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
        hub_url = f.hub_url(driver)
        if f.bstack1ll11ll1ll1_opy_(hub_url):
            if not bstack1lll1ll11ll_opy_.bstack1ll1l111l1l_opy_:
                self.logger.warning(bstack11111ll_opy_ (u"ࠤ࡯ࡳࡨࡧ࡬ࠡࡵࡨࡰ࡫࠳ࡨࡦࡣ࡯ࠤ࡫ࡲ࡯ࡸࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡪࡰࡩࡶࡦࠦࡳࡦࡵࡶ࡭ࡴࡴࡳࠡࡪࡸࡦࡤࡻࡲ࡭࠿ࠥᅻ") + str(hub_url) + bstack11111ll_opy_ (u"ࠥࠦᅼ"))
                bstack1lll1ll11ll_opy_.bstack1ll1l111l1l_opy_ = True
            return
        bstack1ll1ll1ll11_opy_ = f.bstack1ll11llll1l_opy_(*args)
        bstack1ll11ll11ll_opy_ = f.bstack1ll11lll11l_opy_(*args)
        if bstack1ll1ll1ll11_opy_ and bstack1ll1ll1ll11_opy_.lower() == bstack11111ll_opy_ (u"ࠦ࡫࡯࡮ࡥࡧ࡯ࡩࡲ࡫࡮ࡵࠤᅽ") and bstack1ll11ll11ll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll11ll11ll_opy_.get(bstack11111ll_opy_ (u"ࠧࡻࡳࡪࡰࡪࠦᅾ"), None), bstack1ll11ll11ll_opy_.get(bstack11111ll_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᅿ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack11111ll_opy_ (u"ࠢࡼࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫ࡽ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠣࡳࡷࠦࡡࡳࡩࡶ࠲ࡺࡹࡩ࡯ࡩࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡴࡸࠠࡢࡴࡪࡷ࠳ࡼࡡ࡭ࡷࡨࡁࠧᆀ") + str(locator_value) + bstack11111ll_opy_ (u"ࠣࠤᆁ"))
                return
            def bstack11111l1111_opy_(driver, bstack1ll11lll1l1_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll11lll1l1_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll11ll111l_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack11111ll_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࠧᆂ") + str(locator_value) + bstack11111ll_opy_ (u"ࠥࠦᆃ"))
                    else:
                        self.logger.warning(bstack11111ll_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷ࠲ࡴ࡯࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡃࠢᆄ") + str(response) + bstack11111ll_opy_ (u"ࠧࠨᆅ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll11ll1l11_opy_(
                        driver, bstack1ll11lll1l1_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack11111l1111_opy_.__name__ = bstack1ll1ll1ll11_opy_
            return bstack11111l1111_opy_
    def __1ll11ll1l11_opy_(
        self,
        driver,
        bstack1ll11lll1l1_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll11ll111l_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack11111ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡶࡵ࡭࡬࡭ࡥࡳࡧࡧ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࠨᆆ") + str(locator_value) + bstack11111ll_opy_ (u"ࠢࠣᆇ"))
                bstack1ll11ll1111_opy_ = self.bstack1ll11ll11l1_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack11111ll_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡨࡦࡣ࡯࡭ࡳ࡭࡟ࡳࡧࡶࡹࡱࡺ࠽ࠣᆈ") + str(bstack1ll11ll1111_opy_) + bstack11111ll_opy_ (u"ࠤࠥᆉ"))
                if bstack1ll11ll1111_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack11111ll_opy_ (u"ࠥࡹࡸ࡯࡮ࡨࠤᆊ"): bstack1ll11ll1111_opy_.locator_type,
                            bstack11111ll_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᆋ"): bstack1ll11ll1111_opy_.locator_value,
                        }
                    )
                    return bstack1ll11lll1l1_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack11111ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡏ࡟ࡅࡇࡅ࡙ࡌࠨᆌ"), False):
                    self.logger.info(bstack1lllll1l111_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠮࡯࡬ࡷࡸ࡯࡮ࡨ࠼ࠣࡷࡱ࡫ࡥࡱࠪ࠶࠴࠮ࠦ࡬ࡦࡶࡷ࡭ࡳ࡭ࠠࡺࡱࡸࠤ࡮ࡴࡳࡱࡧࡦࡸࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࠦ࡬ࡰࡩࡶࠦᆍ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack11111ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡰࡲ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠿ࠥᆎ") + str(response) + bstack11111ll_opy_ (u"ࠣࠤᆏ"))
        except Exception as err:
            self.logger.warning(bstack11111ll_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠾ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨᆐ") + str(err) + bstack11111ll_opy_ (u"ࠥࠦᆑ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll11lll111_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def bstack1ll11ll111l_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack11111ll_opy_ (u"ࠦ࠵ࠨᆒ"),
    ):
        self.bstack1ll1l1l1lll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack11111ll_opy_ (u"ࠧࠨᆓ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1llll1l1111_opy_.AISelfHealStep(req)
            self.logger.info(bstack11111ll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᆔ") + str(r) + bstack11111ll_opy_ (u"ࠢࠣᆕ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᆖ") + str(e) + bstack11111ll_opy_ (u"ࠤࠥᆗ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11ll1l1l_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def bstack1ll11ll11l1_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack11111ll_opy_ (u"ࠥ࠴ࠧᆘ")):
        self.bstack1ll1l1l1lll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1llll1l1111_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack11111ll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᆙ") + str(r) + bstack11111ll_opy_ (u"ࠧࠨᆚ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᆛ") + str(e) + bstack11111ll_opy_ (u"ࠢࠣᆜ"))
            traceback.print_exc()
            raise e