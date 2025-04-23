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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack111llll111_opy_ import bstack11l11111l1_opy_, bstack11l11l1111_opy_
from bstack_utils.bstack11l1111l1l_opy_ import bstack1lll111111_opy_
from bstack_utils.helper import bstack11ll111l1_opy_, bstack1lllllll11_opy_, Result
from bstack_utils.bstack11l111l1ll_opy_ import bstack1ll1l11l1l_opy_
from bstack_utils.capture import bstack11l111lll1_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack11111ll1l_opy_:
    def __init__(self):
        self.bstack111llllll1_opy_ = bstack11l111lll1_opy_(self.bstack11l1111ll1_opy_)
        self.tests = {}
    @staticmethod
    def bstack11l1111ll1_opy_(log):
        if not (log[bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫໊ࠧ")] and log[bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ໋")].strip()):
            return
        active = bstack1lll111111_opy_.bstack11l11l111l_opy_()
        log = {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ໌"): log[bstack1ll1l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨໍ")],
            bstack1ll1l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭໎"): bstack1lllllll11_opy_(),
            bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ໏"): log[bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭໐")],
        }
        if active:
            if active[bstack1ll1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫ໑")] == bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ໒"):
                log[bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ໓")] = active[bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ໔")]
            elif active[bstack1ll1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ໕")] == bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ໖"):
                log[bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ໗")] = active[bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭໘")]
        bstack1ll1l11l1l_opy_.bstack1l1l11l1l_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack111llllll1_opy_.start()
        driver = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭໙"), None)
        bstack111llll111_opy_ = bstack11l11l1111_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack1lllllll11_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1ll1l11_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤ໚"),
            framework=bstack1ll1l11_opy_ (u"ࠩࡅࡩ࡭ࡧࡶࡦࠩ໛"),
            scope=[attrs.feature.name],
            bstack11l1111lll_opy_=bstack1ll1l11l1l_opy_.bstack11l111ll11_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ໜ")] = bstack111llll111_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack1ll1l11l1l_opy_.bstack111lllll1l_opy_(bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬໝ"), bstack111llll111_opy_)
    def end_test(self, attrs):
        bstack11l111l11l_opy_ = {
            bstack1ll1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥໞ"): attrs.feature.name,
            bstack1ll1l11_opy_ (u"ࠨࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦໟ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack111llll111_opy_ = self.tests[current_test_uuid][bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ໠")]
        meta = {
            bstack1ll1l11_opy_ (u"ࠣࡨࡨࡥࡹࡻࡲࡦࠤ໡"): bstack11l111l11l_opy_,
            bstack1ll1l11_opy_ (u"ࠤࡶࡸࡪࡶࡳࠣ໢"): bstack111llll111_opy_.meta.get(bstack1ll1l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ໣"), []),
            bstack1ll1l11_opy_ (u"ࠦࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ໤"): {
                bstack1ll1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ໥"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack111llll111_opy_.bstack11l111l1l1_opy_(meta)
        bstack111llll111_opy_.bstack111llll11l_opy_(bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ໦"), []))
        bstack11l111ll1l_opy_, exception = self._11l11111ll_opy_(attrs)
        bstack11l111l111_opy_ = Result(result=attrs.status.name, exception=exception, bstack111llll1l1_opy_=[bstack11l111ll1l_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ໧")].stop(time=bstack1lllllll11_opy_(), duration=int(attrs.duration)*1000, result=bstack11l111l111_opy_)
        bstack1ll1l11l1l_opy_.bstack111lllll1l_opy_(bstack1ll1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ໨"), self.tests[threading.current_thread().current_test_uuid][bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ໩")])
    def bstack1l111ll1l_opy_(self, attrs):
        bstack11l111llll_opy_ = {
            bstack1ll1l11_opy_ (u"ࠪ࡭ࡩ࠭໪"): uuid4().__str__(),
            bstack1ll1l11_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬ໫"): attrs.keyword,
            bstack1ll1l11_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬ໬"): [],
            bstack1ll1l11_opy_ (u"࠭ࡴࡦࡺࡷࠫ໭"): attrs.name,
            bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ໮"): bstack1lllllll11_opy_(),
            bstack1ll1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ໯"): bstack1ll1l11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ໰"),
            bstack1ll1l11_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ໱"): bstack1ll1l11_opy_ (u"ࠫࠬ໲")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ໳")].add_step(bstack11l111llll_opy_)
        threading.current_thread().current_step_uuid = bstack11l111llll_opy_[bstack1ll1l11_opy_ (u"࠭ࡩࡥࠩ໴")]
    def bstack1llll11111_opy_(self, attrs):
        current_test_id = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ໵"), None)
        current_step_uuid = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬ໶"), None)
        bstack11l111ll1l_opy_, exception = self._11l11111ll_opy_(attrs)
        bstack11l111l111_opy_ = Result(result=attrs.status.name, exception=exception, bstack111llll1l1_opy_=[bstack11l111ll1l_opy_])
        self.tests[current_test_id][bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ໷")].bstack111lllllll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11l111l111_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1lll11ll1l_opy_(self, name, attrs):
        try:
            bstack11l1111111_opy_ = uuid4().__str__()
            self.tests[bstack11l1111111_opy_] = {}
            self.bstack111llllll1_opy_.start()
            scopes = []
            driver = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ໸"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ໹")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11l1111111_opy_)
            if name in [bstack1ll1l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ໺"), bstack1ll1l11_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤ໻")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1ll1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣ໼"), bstack1ll1l11_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠣ໽")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1ll1l11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ໾")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack11l11111l1_opy_(
                name=name,
                uuid=bstack11l1111111_opy_,
                started_at=bstack1lllllll11_opy_(),
                file_path=file_path,
                framework=bstack1ll1l11_opy_ (u"ࠥࡆࡪ࡮ࡡࡷࡧࠥ໿"),
                bstack11l1111lll_opy_=bstack1ll1l11l1l_opy_.bstack11l111ll11_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1ll1l11_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧༀ"),
                hook_type=name
            )
            self.tests[bstack11l1111111_opy_][bstack1ll1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡦࡺࡡࠣ༁")] = hook_data
            current_test_id = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥ༂"), None)
            if current_test_id:
                hook_data.bstack11l111111l_opy_(current_test_id)
            if name == bstack1ll1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ༃"):
                threading.current_thread().before_all_hook_uuid = bstack11l1111111_opy_
            threading.current_thread().current_hook_uuid = bstack11l1111111_opy_
            bstack1ll1l11l1l_opy_.bstack111lllll1l_opy_(bstack1ll1l11_opy_ (u"ࠣࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠤ༄"), hook_data)
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥ࡮࡯ࡰ࡭ࠣࡩࡻ࡫࡮ࡵࡵ࠯ࠤ࡭ࡵ࡯࡬ࠢࡱࡥࡲ࡫࠺ࠡࠧࡶ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠫࡳࠣ༅"), name, e)
    def bstack11l1ll11l1_opy_(self, attrs):
        bstack111llll1ll_opy_ = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ༆"), None)
        hook_data = self.tests[bstack111llll1ll_opy_][bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ༇")]
        status = bstack1ll1l11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ༈")
        exception = None
        bstack11l111ll1l_opy_ = None
        if hook_data.name == bstack1ll1l11_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤ༉"):
            self.bstack111llllll1_opy_.reset()
            bstack11l1111l11_opy_ = self.tests[bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ༊"), None)][bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ་")].result.result
            if bstack11l1111l11_opy_ == bstack1ll1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ༌"):
                if attrs.hook_failures == 1:
                    status = bstack1ll1l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ།")
                elif attrs.hook_failures == 2:
                    status = bstack1ll1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ༎")
            elif attrs.bstack111lllll11_opy_:
                status = bstack1ll1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ༏")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1ll1l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪ༐") and attrs.hook_failures == 1:
                status = bstack1ll1l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ༑")
            elif hasattr(attrs, bstack1ll1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨ༒")) and attrs.error_message:
                status = bstack1ll1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ༓")
            bstack11l111ll1l_opy_, exception = self._11l11111ll_opy_(attrs)
        bstack11l111l111_opy_ = Result(result=status, exception=exception, bstack111llll1l1_opy_=[bstack11l111ll1l_opy_])
        hook_data.stop(time=bstack1lllllll11_opy_(), duration=0, result=bstack11l111l111_opy_)
        bstack1ll1l11l1l_opy_.bstack111lllll1l_opy_(bstack1ll1l11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ༔"), self.tests[bstack111llll1ll_opy_][bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ༕")])
        threading.current_thread().current_hook_uuid = None
    def _11l11111ll_opy_(self, attrs):
        try:
            import traceback
            bstack1ll11ll1ll_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11l111ll1l_opy_ = bstack1ll11ll1ll_opy_[-1] if bstack1ll11ll1ll_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1ll1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡣࡶࡵࡷࡳࡲࠦࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࠤ༖"))
            bstack11l111ll1l_opy_ = None
            exception = None
        return bstack11l111ll1l_opy_, exception