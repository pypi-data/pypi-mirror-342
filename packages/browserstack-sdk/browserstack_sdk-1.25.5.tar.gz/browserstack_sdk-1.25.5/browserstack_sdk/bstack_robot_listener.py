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
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111ll1ll1l_opy_ import RobotHandler
from bstack_utils.capture import bstack11l111lll1_opy_
from bstack_utils.bstack111llll111_opy_ import bstack111lll1l1l_opy_, bstack11l11111l1_opy_, bstack11l11l1111_opy_
from bstack_utils.bstack11l1111l1l_opy_ import bstack1lll111111_opy_
from bstack_utils.bstack11l111l1ll_opy_ import bstack1ll1l11l1l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11ll111l1_opy_, bstack1lllllll11_opy_, Result, \
    bstack111l11lll1_opy_, bstack111l1l1ll1_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1ll1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ༗"): [],
        bstack1ll1l11_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ༘࠭"): [],
        bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷ༙ࠬ"): []
    }
    bstack111lll1l11_opy_ = []
    bstack111l11llll_opy_ = []
    @staticmethod
    def bstack11l1111ll1_opy_(log):
        if not ((isinstance(log[bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༚")], list) or (isinstance(log[bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༛")], dict)) and len(log[bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༜")])>0) or (isinstance(log[bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭༝")], str) and log[bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ༞")].strip())):
            return
        active = bstack1lll111111_opy_.bstack11l11l111l_opy_()
        log = {
            bstack1ll1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭༟"): log[bstack1ll1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ༠")],
            bstack1ll1l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ༡"): bstack111l1l1ll1_opy_().isoformat() + bstack1ll1l11_opy_ (u"ࠪ࡞ࠬ༢"),
            bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༣"): log[bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭༤")],
        }
        if active:
            if active[bstack1ll1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫ༥")] == bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ༦"):
                log[bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ༧")] = active[bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ༨")]
            elif active[bstack1ll1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ༩")] == bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ༪"):
                log[bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ༫")] = active[bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭༬")]
        bstack1ll1l11l1l_opy_.bstack1l1l11l1l_opy_([log])
    def __init__(self):
        self.messages = bstack111ll1ll11_opy_()
        self._111l1l1lll_opy_ = None
        self._111ll1l111_opy_ = None
        self._111lll1ll1_opy_ = OrderedDict()
        self.bstack111llllll1_opy_ = bstack11l111lll1_opy_(self.bstack11l1111ll1_opy_)
    @bstack111l11lll1_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111ll1lll1_opy_()
        if not self._111lll1ll1_opy_.get(attrs.get(bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪ༭")), None):
            self._111lll1ll1_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫ༮"))] = {}
        bstack111ll11l1l_opy_ = bstack11l11l1111_opy_(
                bstack111lll1lll_opy_=attrs.get(bstack1ll1l11_opy_ (u"ࠩ࡬ࡨࠬ༯")),
                name=name,
                started_at=bstack1lllllll11_opy_(),
                file_path=os.path.relpath(attrs[bstack1ll1l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ༰")], start=os.getcwd()) if attrs.get(bstack1ll1l11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ༱")) != bstack1ll1l11_opy_ (u"ࠬ࠭༲") else bstack1ll1l11_opy_ (u"࠭ࠧ༳"),
                framework=bstack1ll1l11_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭༴")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡫ࡧ༵ࠫ"), None)
        self._111lll1ll1_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠩ࡬ࡨࠬ༶"))][bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ༷࠭")] = bstack111ll11l1l_opy_
    @bstack111l11lll1_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111l1ll11l_opy_()
        self._111lll11l1_opy_(messages)
        for bstack111l11l1ll_opy_ in self.bstack111lll1l11_opy_:
            bstack111l11l1ll_opy_[bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭༸")][bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶ༹ࠫ")].extend(self.store[bstack1ll1l11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ༺")])
            bstack1ll1l11l1l_opy_.bstack11l1lll111_opy_(bstack111l11l1ll_opy_)
        self.bstack111lll1l11_opy_ = []
        self.store[bstack1ll1l11_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭༻")] = []
    @bstack111l11lll1_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack111llllll1_opy_.start()
        if not self._111lll1ll1_opy_.get(attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫ༼")), None):
            self._111lll1ll1_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠩ࡬ࡨࠬ༽"))] = {}
        driver = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ༾"), None)
        bstack111llll111_opy_ = bstack11l11l1111_opy_(
            bstack111lll1lll_opy_=attrs.get(bstack1ll1l11_opy_ (u"ࠫ࡮ࡪࠧ༿")),
            name=name,
            started_at=bstack1lllllll11_opy_(),
            file_path=os.path.relpath(attrs[bstack1ll1l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬཀ")], start=os.getcwd()),
            scope=RobotHandler.bstack111ll11ll1_opy_(attrs.get(bstack1ll1l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ཁ"), None)),
            framework=bstack1ll1l11_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ག"),
            tags=attrs[bstack1ll1l11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭གྷ")],
            hooks=self.store[bstack1ll1l11_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨང")],
            bstack11l1111lll_opy_=bstack1ll1l11l1l_opy_.bstack11l111ll11_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1ll1l11_opy_ (u"ࠥࡿࢂࠦ࡜࡯ࠢࡾࢁࠧཅ").format(bstack1ll1l11_opy_ (u"ࠦࠥࠨཆ").join(attrs[bstack1ll1l11_opy_ (u"ࠬࡺࡡࡨࡵࠪཇ")]), name) if attrs[bstack1ll1l11_opy_ (u"࠭ࡴࡢࡩࡶࠫ཈")] else name
        )
        self._111lll1ll1_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪཉ"))][bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫཊ")] = bstack111llll111_opy_
        threading.current_thread().current_test_uuid = bstack111llll111_opy_.bstack111l1ll1ll_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1ll1l11_opy_ (u"ࠩ࡬ࡨࠬཋ"), None)
        self.bstack111lllll1l_opy_(bstack1ll1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫཌ"), bstack111llll111_opy_)
    @bstack111l11lll1_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack111llllll1_opy_.reset()
        bstack111l1l111l_opy_ = bstack111ll1llll_opy_.get(attrs.get(bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫཌྷ")), bstack1ll1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ཎ"))
        self._111lll1ll1_opy_[attrs.get(bstack1ll1l11_opy_ (u"࠭ࡩࡥࠩཏ"))][bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪཐ")].stop(time=bstack1lllllll11_opy_(), duration=int(attrs.get(bstack1ll1l11_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ད"), bstack1ll1l11_opy_ (u"ࠩ࠳ࠫདྷ"))), result=Result(result=bstack111l1l111l_opy_, exception=attrs.get(bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫན")), bstack111llll1l1_opy_=[attrs.get(bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཔ"))]))
        self.bstack111lllll1l_opy_(bstack1ll1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧཕ"), self._111lll1ll1_opy_[attrs.get(bstack1ll1l11_opy_ (u"࠭ࡩࡥࠩབ"))][bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪབྷ")], True)
        self.store[bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬམ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack111l11lll1_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111ll1lll1_opy_()
        current_test_id = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫཙ"), None)
        bstack111l1ll111_opy_ = current_test_id if bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬཚ"), None) else bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧཛ"), None)
        if attrs.get(bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪཛྷ"), bstack1ll1l11_opy_ (u"࠭ࠧཝ")).lower() in [bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ཞ"), bstack1ll1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪཟ")]:
            hook_type = bstack111l1l1111_opy_(attrs.get(bstack1ll1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧའ")), bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧཡ"), None))
            hook_name = bstack1ll1l11_opy_ (u"ࠫࢀࢃࠧར").format(attrs.get(bstack1ll1l11_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬལ"), bstack1ll1l11_opy_ (u"࠭ࠧཤ")))
            if hook_type in [bstack1ll1l11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫཥ"), bstack1ll1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫས")]:
                hook_name = bstack1ll1l11_opy_ (u"ࠩ࡞ࡿࢂࡣࠠࡼࡿࠪཧ").format(bstack111l1l1l1l_opy_.get(hook_type), attrs.get(bstack1ll1l11_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪཨ"), bstack1ll1l11_opy_ (u"ࠫࠬཀྵ")))
            bstack111ll11lll_opy_ = bstack11l11111l1_opy_(
                bstack111lll1lll_opy_=bstack111l1ll111_opy_ + bstack1ll1l11_opy_ (u"ࠬ࠳ࠧཪ") + attrs.get(bstack1ll1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫཫ"), bstack1ll1l11_opy_ (u"ࠧࠨཬ")).lower(),
                name=hook_name,
                started_at=bstack1lllllll11_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1ll1l11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ཭")), start=os.getcwd()),
                framework=bstack1ll1l11_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ཮"),
                tags=attrs[bstack1ll1l11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ཯")],
                scope=RobotHandler.bstack111ll11ll1_opy_(attrs.get(bstack1ll1l11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ཰"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111ll11lll_opy_.bstack111l1ll1ll_opy_()
            threading.current_thread().current_hook_id = bstack111l1ll111_opy_ + bstack1ll1l11_opy_ (u"ࠬ࠳ཱࠧ") + attrs.get(bstack1ll1l11_opy_ (u"࠭ࡴࡺࡲࡨིࠫ"), bstack1ll1l11_opy_ (u"ࠧࠨཱི")).lower()
            self.store[bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨུࠬ")] = [bstack111ll11lll_opy_.bstack111l1ll1ll_opy_()]
            if bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩཱུ࠭"), None):
                self.store[bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧྲྀ")].append(bstack111ll11lll_opy_.bstack111l1ll1ll_opy_())
            else:
                self.store[bstack1ll1l11_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪཷ")].append(bstack111ll11lll_opy_.bstack111l1ll1ll_opy_())
            if bstack111l1ll111_opy_:
                self._111lll1ll1_opy_[bstack111l1ll111_opy_ + bstack1ll1l11_opy_ (u"ࠬ࠳ࠧླྀ") + attrs.get(bstack1ll1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫཹ"), bstack1ll1l11_opy_ (u"ࠧࠨེ")).lower()] = { bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤཻࠫ"): bstack111ll11lll_opy_ }
            bstack1ll1l11l1l_opy_.bstack111lllll1l_opy_(bstack1ll1l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦོࠪ"), bstack111ll11lll_opy_)
        else:
            bstack11l111llll_opy_ = {
                bstack1ll1l11_opy_ (u"ࠪ࡭ࡩཽ࠭"): uuid4().__str__(),
                bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡸࡵࠩཾ"): bstack1ll1l11_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫཿ").format(attrs.get(bstack1ll1l11_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪྀ࠭")), attrs.get(bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡷཱྀࠬ"), bstack1ll1l11_opy_ (u"ࠨࠩྂ"))) if attrs.get(bstack1ll1l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧྃ"), []) else attrs.get(bstack1ll1l11_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧ྄ࠪ")),
                bstack1ll1l11_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫ྅"): attrs.get(bstack1ll1l11_opy_ (u"ࠬࡧࡲࡨࡵࠪ྆"), []),
                bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ྇"): bstack1lllllll11_opy_(),
                bstack1ll1l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧྈ"): bstack1ll1l11_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩྉ"),
                bstack1ll1l11_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧྊ"): attrs.get(bstack1ll1l11_opy_ (u"ࠪࡨࡴࡩࠧྋ"), bstack1ll1l11_opy_ (u"ࠫࠬྌ"))
            }
            if attrs.get(bstack1ll1l11_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭ྍ"), bstack1ll1l11_opy_ (u"࠭ࠧྎ")) != bstack1ll1l11_opy_ (u"ࠧࠨྏ"):
                bstack11l111llll_opy_[bstack1ll1l11_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩྐ")] = attrs.get(bstack1ll1l11_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪྑ"))
            if not self.bstack111l11llll_opy_:
                self._111lll1ll1_opy_[self._111l11ll11_opy_()][bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྒ")].add_step(bstack11l111llll_opy_)
                threading.current_thread().current_step_uuid = bstack11l111llll_opy_[bstack1ll1l11_opy_ (u"ࠫ࡮ࡪࠧྒྷ")]
            self.bstack111l11llll_opy_.append(bstack11l111llll_opy_)
    @bstack111l11lll1_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111l1ll11l_opy_()
        self._111lll11l1_opy_(messages)
        current_test_id = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧྔ"), None)
        bstack111l1ll111_opy_ = current_test_id if current_test_id else bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩྕ"), None)
        bstack111ll1111l_opy_ = bstack111ll1llll_opy_.get(attrs.get(bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧྖ")), bstack1ll1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩྗ"))
        bstack111l11l1l1_opy_ = attrs.get(bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ྘"))
        if bstack111ll1111l_opy_ != bstack1ll1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫྙ") and not attrs.get(bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬྚ")) and self._111l1l1lll_opy_:
            bstack111l11l1l1_opy_ = self._111l1l1lll_opy_
        bstack11l111l111_opy_ = Result(result=bstack111ll1111l_opy_, exception=bstack111l11l1l1_opy_, bstack111llll1l1_opy_=[bstack111l11l1l1_opy_])
        if attrs.get(bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪྛ"), bstack1ll1l11_opy_ (u"࠭ࠧྜ")).lower() in [bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ྜྷ"), bstack1ll1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪྞ")]:
            bstack111l1ll111_opy_ = current_test_id if current_test_id else bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬྟ"), None)
            if bstack111l1ll111_opy_:
                bstack111llll1ll_opy_ = bstack111l1ll111_opy_ + bstack1ll1l11_opy_ (u"ࠥ࠱ࠧྠ") + attrs.get(bstack1ll1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩྡ"), bstack1ll1l11_opy_ (u"ࠬ࠭ྡྷ")).lower()
                self._111lll1ll1_opy_[bstack111llll1ll_opy_][bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩྣ")].stop(time=bstack1lllllll11_opy_(), duration=int(attrs.get(bstack1ll1l11_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬྤ"), bstack1ll1l11_opy_ (u"ࠨ࠲ࠪྥ"))), result=bstack11l111l111_opy_)
                bstack1ll1l11l1l_opy_.bstack111lllll1l_opy_(bstack1ll1l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫྦ"), self._111lll1ll1_opy_[bstack111llll1ll_opy_][bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྦྷ")])
        else:
            bstack111l1ll111_opy_ = current_test_id if current_test_id else bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢ࡭ࡩ࠭ྨ"), None)
            if bstack111l1ll111_opy_ and len(self.bstack111l11llll_opy_) == 1:
                current_step_uuid = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩྩ"), None)
                self._111lll1ll1_opy_[bstack111l1ll111_opy_][bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩྪ")].bstack111lllllll_opy_(current_step_uuid, duration=int(attrs.get(bstack1ll1l11_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬྫ"), bstack1ll1l11_opy_ (u"ࠨ࠲ࠪྫྷ"))), result=bstack11l111l111_opy_)
            else:
                self.bstack111l1l1l11_opy_(attrs)
            self.bstack111l11llll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1ll1l11_opy_ (u"ࠩ࡫ࡸࡲࡲࠧྭ"), bstack1ll1l11_opy_ (u"ࠪࡲࡴ࠭ྮ")) == bstack1ll1l11_opy_ (u"ࠫࡾ࡫ࡳࠨྯ"):
                return
            self.messages.push(message)
            logs = []
            if bstack1lll111111_opy_.bstack11l11l111l_opy_():
                logs.append({
                    bstack1ll1l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨྰ"): bstack1lllllll11_opy_(),
                    bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྱ"): message.get(bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨྲ")),
                    bstack1ll1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧླ"): message.get(bstack1ll1l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨྴ")),
                    **bstack1lll111111_opy_.bstack11l11l111l_opy_()
                })
                if len(logs) > 0:
                    bstack1ll1l11l1l_opy_.bstack1l1l11l1l_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack1ll1l11l1l_opy_.bstack111l1llll1_opy_()
    def bstack111l1l1l11_opy_(self, bstack111lll111l_opy_):
        if not bstack1lll111111_opy_.bstack11l11l111l_opy_():
            return
        kwname = bstack1ll1l11_opy_ (u"ࠪࡿࢂࠦࡻࡾࠩྵ").format(bstack111lll111l_opy_.get(bstack1ll1l11_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫྶ")), bstack111lll111l_opy_.get(bstack1ll1l11_opy_ (u"ࠬࡧࡲࡨࡵࠪྷ"), bstack1ll1l11_opy_ (u"࠭ࠧྸ"))) if bstack111lll111l_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡷࠬྐྵ"), []) else bstack111lll111l_opy_.get(bstack1ll1l11_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨྺ"))
        error_message = bstack1ll1l11_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠡࡾࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠ࡝ࠤࡾ࠶ࢂࡢࠢࠣྻ").format(kwname, bstack111lll111l_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪྼ")), str(bstack111lll111l_opy_.get(bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ྽"))))
        bstack111l1ll1l1_opy_ = bstack1ll1l11_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠦ྾").format(kwname, bstack111lll111l_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭྿")))
        bstack111l1l11ll_opy_ = error_message if bstack111lll111l_opy_.get(bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿀")) else bstack111l1ll1l1_opy_
        bstack111l1lll1l_opy_ = {
            bstack1ll1l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ࿁"): self.bstack111l11llll_opy_[-1].get(bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭࿂"), bstack1lllllll11_opy_()),
            bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿃"): bstack111l1l11ll_opy_,
            bstack1ll1l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ࿄"): bstack1ll1l11_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫ࿅") if bstack111lll111l_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࿆࠭")) == bstack1ll1l11_opy_ (u"ࠧࡇࡃࡌࡐࠬ࿇") else bstack1ll1l11_opy_ (u"ࠨࡋࡑࡊࡔ࠭࿈"),
            **bstack1lll111111_opy_.bstack11l11l111l_opy_()
        }
        bstack1ll1l11l1l_opy_.bstack1l1l11l1l_opy_([bstack111l1lll1l_opy_])
    def _111l11ll11_opy_(self):
        for bstack111lll1lll_opy_ in reversed(self._111lll1ll1_opy_):
            bstack111l11ll1l_opy_ = bstack111lll1lll_opy_
            data = self._111lll1ll1_opy_[bstack111lll1lll_opy_][bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ࿉")]
            if isinstance(data, bstack11l11111l1_opy_):
                if not bstack1ll1l11_opy_ (u"ࠪࡉࡆࡉࡈࠨ࿊") in data.bstack111l1lll11_opy_():
                    return bstack111l11ll1l_opy_
            else:
                return bstack111l11ll1l_opy_
    def _111lll11l1_opy_(self, messages):
        try:
            bstack111lll1111_opy_ = BuiltIn().get_variable_value(bstack1ll1l11_opy_ (u"ࠦࠩࢁࡌࡐࡉࠣࡐࡊ࡜ࡅࡍࡿࠥ࿋")) in (bstack111l1l11l1_opy_.DEBUG, bstack111l1l11l1_opy_.TRACE)
            for message, bstack111ll11111_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿌"))
                level = message.get(bstack1ll1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ࿍"))
                if level == bstack111l1l11l1_opy_.FAIL:
                    self._111l1l1lll_opy_ = name or self._111l1l1lll_opy_
                    self._111ll1l111_opy_ = bstack111ll11111_opy_.get(bstack1ll1l11_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣ࿎")) if bstack111lll1111_opy_ and bstack111ll11111_opy_ else self._111ll1l111_opy_
        except:
            pass
    @classmethod
    def bstack111lllll1l_opy_(self, event: str, bstack111ll1l1ll_opy_: bstack111lll1l1l_opy_, bstack111l11l11l_opy_=False):
        if event == bstack1ll1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ࿏"):
            bstack111ll1l1ll_opy_.set(hooks=self.store[bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭࿐")])
        if event == bstack1ll1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ࿑"):
            event = bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭࿒")
        if bstack111l11l11l_opy_:
            bstack111ll1l1l1_opy_ = {
                bstack1ll1l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ࿓"): event,
                bstack111ll1l1ll_opy_.bstack111l11l111_opy_(): bstack111ll1l1ll_opy_.bstack111ll1l11l_opy_(event)
            }
            self.bstack111lll1l11_opy_.append(bstack111ll1l1l1_opy_)
        else:
            bstack1ll1l11l1l_opy_.bstack111lllll1l_opy_(event, bstack111ll1l1ll_opy_)
class bstack111ll1ll11_opy_:
    def __init__(self):
        self._111ll111ll_opy_ = []
    def bstack111ll1lll1_opy_(self):
        self._111ll111ll_opy_.append([])
    def bstack111l1ll11l_opy_(self):
        return self._111ll111ll_opy_.pop() if self._111ll111ll_opy_ else list()
    def push(self, message):
        self._111ll111ll_opy_[-1].append(message) if self._111ll111ll_opy_ else self._111ll111ll_opy_.append([message])
class bstack111l1l11l1_opy_:
    FAIL = bstack1ll1l11_opy_ (u"࠭ࡆࡂࡋࡏࠫ࿔")
    ERROR = bstack1ll1l11_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭࿕")
    WARNING = bstack1ll1l11_opy_ (u"ࠨ࡙ࡄࡖࡓ࠭࿖")
    bstack111lll11ll_opy_ = bstack1ll1l11_opy_ (u"ࠩࡌࡒࡋࡕࠧ࿗")
    DEBUG = bstack1ll1l11_opy_ (u"ࠪࡈࡊࡈࡕࡈࠩ࿘")
    TRACE = bstack1ll1l11_opy_ (u"࡙ࠫࡘࡁࡄࡇࠪ࿙")
    bstack111ll11l11_opy_ = [FAIL, ERROR]
def bstack111l1lllll_opy_(bstack111ll111l1_opy_):
    if not bstack111ll111l1_opy_:
        return None
    if bstack111ll111l1_opy_.get(bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿚"), None):
        return getattr(bstack111ll111l1_opy_[bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿛")], bstack1ll1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ࿜"), None)
    return bstack111ll111l1_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭࿝"), None)
def bstack111l1l1111_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ࿞"), bstack1ll1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ࿟")]:
        return
    if hook_type.lower() == bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ࿠"):
        if current_test_uuid is None:
            return bstack1ll1l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ࿡")
        else:
            return bstack1ll1l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ࿢")
    elif hook_type.lower() == bstack1ll1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ࿣"):
        if current_test_uuid is None:
            return bstack1ll1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ࿤")
        else:
            return bstack1ll1l11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭࿥")