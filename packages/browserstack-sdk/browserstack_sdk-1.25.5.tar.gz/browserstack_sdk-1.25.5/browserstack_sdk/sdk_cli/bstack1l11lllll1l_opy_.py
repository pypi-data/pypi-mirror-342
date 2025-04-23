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
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack11111lllll_opy_
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack11111l1lll_opy_,
    bstack111111ll1l_opy_,
    bstack1111l1lll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import bstack1111111ll1_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack11111lllll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1l11lll1l11_opy_(bstack11111lllll_opy_):
    bstack1l111ll1111_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1111111ll1_opy_.bstack111111l1l1_opy_((bstack11111l1lll_opy_.bstack1111l1l1l1_opy_, bstack111111ll1l_opy_.PRE), self.bstack1ll1lll1111_opy_)
    def is_enabled(self) -> bool:
        return True
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
        hub_url = f.hub_url(driver)
        if f.bstack1l1ll11l1ll_opy_(hub_url):
            if not bstack1l11lll1l11_opy_.bstack1l111ll1111_opy_:
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠦࡱࡵࡣࡢ࡮ࠣࡷࡪࡲࡦ࠮ࡪࡨࡥࡱࠦࡦ࡭ࡱࡺࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢ࡬ࡲ࡫ࡸࡡࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧᓨ") + str(hub_url) + bstack1ll1l11_opy_ (u"ࠧࠨᓩ"))
                bstack1l11lll1l11_opy_.bstack1l111ll1111_opy_ = True
            return
        bstack1l1ll11l11l_opy_ = f.bstack111111l11l_opy_(*args)
        bstack1ll1l1111l1_opy_ = f.bstack1ll1l11111l_opy_(*args)
        if bstack1l1ll11l11l_opy_ and bstack1l1ll11l11l_opy_.lower() == bstack1ll1l11_opy_ (u"ࠨࡦࡪࡰࡧࡩࡱ࡫࡭ࡦࡰࡷࠦᓪ") and bstack1ll1l1111l1_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll1l1111l1_opy_.get(bstack1ll1l11_opy_ (u"ࠢࡶࡵ࡬ࡲ࡬ࠨᓫ"), None), bstack1ll1l1111l1_opy_.get(bstack1ll1l11_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᓬ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠤࡾࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦࡿ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡵࡲࠡࡣࡵ࡫ࡸ࠴ࡵࡴ࡫ࡱ࡫ࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡷࡣ࡯ࡹࡪࡃࠢᓭ") + str(locator_value) + bstack1ll1l11_opy_ (u"ࠥࠦᓮ"))
                return
            def bstack1l1l1l1lll1_opy_(driver, bstack1l111l111ll_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l111l111ll_opy_(driver, *args, **kwargs)
                    response = self.bstack1l111l111l1_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1ll1l11_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࠢᓯ") + str(locator_value) + bstack1ll1l11_opy_ (u"ࠧࠨᓰ"))
                    else:
                        self.logger.warning(bstack1ll1l11_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹ࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤᓱ") + str(response) + bstack1ll1l11_opy_ (u"ࠢࠣᓲ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l1111llll1_opy_(
                        driver, bstack1l111l111ll_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1l1l1l1lll1_opy_.__name__ = bstack1l1ll11l11l_opy_
            return bstack1l1l1l1lll1_opy_
    def __1l1111llll1_opy_(
        self,
        driver,
        bstack1l111l111ll_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l111l111l1_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1ll1l11_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡸࡷ࡯ࡧࡨࡧࡵࡩࡩࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣᓳ") + str(locator_value) + bstack1ll1l11_opy_ (u"ࠤࠥᓴ"))
                bstack1l111l1111l_opy_ = self.bstack1l1111lllll_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1ll1l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡪࡨࡥࡱ࡯࡮ࡨࡡࡵࡩࡸࡻ࡬ࡵ࠿ࠥᓵ") + str(bstack1l111l1111l_opy_) + bstack1ll1l11_opy_ (u"ࠦࠧᓶ"))
                if bstack1l111l1111l_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1ll1l11_opy_ (u"ࠧࡻࡳࡪࡰࡪࠦᓷ"): bstack1l111l1111l_opy_.locator_type,
                            bstack1ll1l11_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᓸ"): bstack1l111l1111l_opy_.locator_value,
                        }
                    )
                    return bstack1l111l111ll_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1ll1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡊࡡࡇࡉࡇ࡛ࡇࠣᓹ"), False):
                    self.logger.info(bstack1lll1111ll1_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠰ࡱ࡮ࡹࡳࡪࡰࡪ࠾ࠥࡹ࡬ࡦࡧࡳࠬ࠸࠶ࠩࠡ࡮ࡨࡸࡹ࡯࡮ࡨࠢࡼࡳࡺࠦࡩ࡯ࡵࡳࡩࡨࡺࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࡸࠨᓺ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰ࡲࡴ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࡁࠧᓻ") + str(response) + bstack1ll1l11_opy_ (u"ࠥࠦᓼ"))
        except Exception as err:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠࡦࡴࡵࡳࡷࡀࠠࠣᓽ") + str(err) + bstack1ll1l11_opy_ (u"ࠧࠨᓾ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l111l11111_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def bstack1l111l111l1_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1ll1l11_opy_ (u"ࠨ࠰ࠣᓿ"),
    ):
        self.bstack1lll1lll1ll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1ll1l11_opy_ (u"ࠢࠣᔀ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1llll111lll_opy_.AISelfHealStep(req)
            self.logger.info(bstack1ll1l11_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᔁ") + str(r) + bstack1ll1l11_opy_ (u"ࠤࠥᔂ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᔃ") + str(e) + bstack1ll1l11_opy_ (u"ࠦࠧᔄ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1111lll1l_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def bstack1l1111lllll_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1ll1l11_opy_ (u"ࠧ࠶ࠢᔅ")):
        self.bstack1lll1lll1ll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1llll111lll_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1ll1l11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᔆ") + str(r) + bstack1ll1l11_opy_ (u"ࠢࠣᔇ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᔈ") + str(e) + bstack1ll1l11_opy_ (u"ࠤࠥᔉ"))
            traceback.print_exc()
            raise e