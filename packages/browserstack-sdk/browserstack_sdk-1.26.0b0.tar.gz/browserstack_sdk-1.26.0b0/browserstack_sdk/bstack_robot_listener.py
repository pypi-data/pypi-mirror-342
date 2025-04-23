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
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111l1l1111_opy_ import RobotHandler
from bstack_utils.capture import bstack11l111ll11_opy_
from bstack_utils.bstack111llll11l_opy_ import bstack111l11ll1l_opy_, bstack11l111llll_opy_, bstack111llll1ll_opy_
from bstack_utils.bstack11l11l11l1_opy_ import bstack11lll1l1_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack1l1l1l1111_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l1llll11l_opy_, bstack11lllll1l_opy_, Result, \
    bstack111ll1ll11_opy_, bstack111l1ll11l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11111ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ༖"): [],
        bstack11111ll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ༗"): [],
        bstack11111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶ༘ࠫ"): []
    }
    bstack111l1l1l11_opy_ = []
    bstack111ll111l1_opy_ = []
    @staticmethod
    def bstack11l111l1l1_opy_(log):
        if not ((isinstance(log[bstack11111ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦ༙ࠩ")], list) or (isinstance(log[bstack11111ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༚")], dict)) and len(log[bstack11111ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༛")])>0) or (isinstance(log[bstack11111ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༜")], str) and log[bstack11111ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭༝")].strip())):
            return
        active = bstack11lll1l1_opy_.bstack11l11111l1_opy_()
        log = {
            bstack11111ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ༞"): log[bstack11111ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭༟")],
            bstack11111ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ༠"): bstack111l1ll11l_opy_().isoformat() + bstack11111ll_opy_ (u"ࠩ࡝ࠫ༡"),
            bstack11111ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༢"): log[bstack11111ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༣")],
        }
        if active:
            if active[bstack11111ll_opy_ (u"ࠬࡺࡹࡱࡧࠪ༤")] == bstack11111ll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ༥"):
                log[bstack11111ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ༦")] = active[bstack11111ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ༧")]
            elif active[bstack11111ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ༨")] == bstack11111ll_opy_ (u"ࠪࡸࡪࡹࡴࠨ༩"):
                log[bstack11111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ༪")] = active[bstack11111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ༫")]
        bstack1l1l1l1111_opy_.bstack1llllll1l_opy_([log])
    def __init__(self):
        self.messages = bstack111ll1l1ll_opy_()
        self._111ll11l11_opy_ = None
        self._111ll111ll_opy_ = None
        self._111l11l1ll_opy_ = OrderedDict()
        self.bstack11l111l1ll_opy_ = bstack11l111ll11_opy_(self.bstack11l111l1l1_opy_)
    @bstack111ll1ll11_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111l1ll111_opy_()
        if not self._111l11l1ll_opy_.get(attrs.get(bstack11111ll_opy_ (u"࠭ࡩࡥࠩ༬")), None):
            self._111l11l1ll_opy_[attrs.get(bstack11111ll_opy_ (u"ࠧࡪࡦࠪ༭"))] = {}
        bstack111lll111l_opy_ = bstack111llll1ll_opy_(
                bstack111ll11l1l_opy_=attrs.get(bstack11111ll_opy_ (u"ࠨ࡫ࡧࠫ༮")),
                name=name,
                started_at=bstack11lllll1l_opy_(),
                file_path=os.path.relpath(attrs[bstack11111ll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ༯")], start=os.getcwd()) if attrs.get(bstack11111ll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ༰")) != bstack11111ll_opy_ (u"ࠫࠬ༱") else bstack11111ll_opy_ (u"ࠬ࠭༲"),
                framework=bstack11111ll_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬ༳")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11111ll_opy_ (u"ࠧࡪࡦࠪ༴"), None)
        self._111l11l1ll_opy_[attrs.get(bstack11111ll_opy_ (u"ࠨ࡫ࡧ༵ࠫ"))][bstack11111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༶")] = bstack111lll111l_opy_
    @bstack111ll1ll11_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111l1ll1ll_opy_()
        self._111l1lll1l_opy_(messages)
        for bstack111llll111_opy_ in self.bstack111l1l1l11_opy_:
            bstack111llll111_opy_[bstack11111ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲ༷ࠬ")][bstack11111ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ༸")].extend(self.store[bstack11111ll_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶ༹ࠫ")])
            bstack1l1l1l1111_opy_.bstack1111l11l_opy_(bstack111llll111_opy_)
        self.bstack111l1l1l11_opy_ = []
        self.store[bstack11111ll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ༺")] = []
    @bstack111ll1ll11_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11l111l1ll_opy_.start()
        if not self._111l11l1ll_opy_.get(attrs.get(bstack11111ll_opy_ (u"ࠧࡪࡦࠪ༻")), None):
            self._111l11l1ll_opy_[attrs.get(bstack11111ll_opy_ (u"ࠨ࡫ࡧࠫ༼"))] = {}
        driver = bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ༽"), None)
        bstack111llll11l_opy_ = bstack111llll1ll_opy_(
            bstack111ll11l1l_opy_=attrs.get(bstack11111ll_opy_ (u"ࠪ࡭ࡩ࠭༾")),
            name=name,
            started_at=bstack11lllll1l_opy_(),
            file_path=os.path.relpath(attrs[bstack11111ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ༿")], start=os.getcwd()),
            scope=RobotHandler.bstack111l1l111l_opy_(attrs.get(bstack11111ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬཀ"), None)),
            framework=bstack11111ll_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬཁ"),
            tags=attrs[bstack11111ll_opy_ (u"ࠧࡵࡣࡪࡷࠬག")],
            hooks=self.store[bstack11111ll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧགྷ")],
            bstack11l1111111_opy_=bstack1l1l1l1111_opy_.bstack111llllll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11111ll_opy_ (u"ࠤࡾࢁࠥࡢ࡮ࠡࡽࢀࠦང").format(bstack11111ll_opy_ (u"ࠥࠤࠧཅ").join(attrs[bstack11111ll_opy_ (u"ࠫࡹࡧࡧࡴࠩཆ")]), name) if attrs[bstack11111ll_opy_ (u"ࠬࡺࡡࡨࡵࠪཇ")] else name
        )
        self._111l11l1ll_opy_[attrs.get(bstack11111ll_opy_ (u"࠭ࡩࡥࠩ཈"))][bstack11111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪཉ")] = bstack111llll11l_opy_
        threading.current_thread().current_test_uuid = bstack111llll11l_opy_.bstack111lll1l1l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11111ll_opy_ (u"ࠨ࡫ࡧࠫཊ"), None)
        self.bstack11l11l1111_opy_(bstack11111ll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪཋ"), bstack111llll11l_opy_)
    @bstack111ll1ll11_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11l111l1ll_opy_.reset()
        bstack111lll1111_opy_ = bstack111l1ll1l1_opy_.get(attrs.get(bstack11111ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪཌ")), bstack11111ll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬཌྷ"))
        self._111l11l1ll_opy_[attrs.get(bstack11111ll_opy_ (u"ࠬ࡯ࡤࠨཎ"))][bstack11111ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩཏ")].stop(time=bstack11lllll1l_opy_(), duration=int(attrs.get(bstack11111ll_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬཐ"), bstack11111ll_opy_ (u"ࠨ࠲ࠪད"))), result=Result(result=bstack111lll1111_opy_, exception=attrs.get(bstack11111ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪདྷ")), bstack11l1111l11_opy_=[attrs.get(bstack11111ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫན"))]))
        self.bstack11l11l1111_opy_(bstack11111ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭པ"), self._111l11l1ll_opy_[attrs.get(bstack11111ll_opy_ (u"ࠬ࡯ࡤࠨཕ"))][bstack11111ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩབ")], True)
        self.store[bstack11111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫབྷ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack111ll1ll11_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111l1ll111_opy_()
        current_test_id = bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪམ"), None)
        bstack111lll11l1_opy_ = current_test_id if bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫཙ"), None) else bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ཚ"), None)
        if attrs.get(bstack11111ll_opy_ (u"ࠫࡹࡿࡰࡦࠩཛ"), bstack11111ll_opy_ (u"ࠬ࠭ཛྷ")).lower() in [bstack11111ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬཝ"), bstack11111ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩཞ")]:
            hook_type = bstack111l1l1lll_opy_(attrs.get(bstack11111ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ཟ")), bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭འ"), None))
            hook_name = bstack11111ll_opy_ (u"ࠪࡿࢂ࠭ཡ").format(attrs.get(bstack11111ll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫར"), bstack11111ll_opy_ (u"ࠬ࠭ལ")))
            if hook_type in [bstack11111ll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪཤ"), bstack11111ll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪཥ")]:
                hook_name = bstack11111ll_opy_ (u"ࠨ࡝ࡾࢁࡢࠦࡻࡾࠩས").format(bstack111ll1l111_opy_.get(hook_type), attrs.get(bstack11111ll_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩཧ"), bstack11111ll_opy_ (u"ࠪࠫཨ")))
            bstack111l1l11l1_opy_ = bstack11l111llll_opy_(
                bstack111ll11l1l_opy_=bstack111lll11l1_opy_ + bstack11111ll_opy_ (u"ࠫ࠲࠭ཀྵ") + attrs.get(bstack11111ll_opy_ (u"ࠬࡺࡹࡱࡧࠪཪ"), bstack11111ll_opy_ (u"࠭ࠧཫ")).lower(),
                name=hook_name,
                started_at=bstack11lllll1l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11111ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧཬ")), start=os.getcwd()),
                framework=bstack11111ll_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ཭"),
                tags=attrs[bstack11111ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ཮")],
                scope=RobotHandler.bstack111l1l111l_opy_(attrs.get(bstack11111ll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ཯"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111l1l11l1_opy_.bstack111lll1l1l_opy_()
            threading.current_thread().current_hook_id = bstack111lll11l1_opy_ + bstack11111ll_opy_ (u"ࠫ࠲࠭཰") + attrs.get(bstack11111ll_opy_ (u"ࠬࡺࡹࡱࡧཱࠪ"), bstack11111ll_opy_ (u"ི࠭ࠧ")).lower()
            self.store[bstack11111ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧཱིࠫ")] = [bstack111l1l11l1_opy_.bstack111lll1l1l_opy_()]
            if bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨུࠬ"), None):
                self.store[bstack11111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸཱུ࠭")].append(bstack111l1l11l1_opy_.bstack111lll1l1l_opy_())
            else:
                self.store[bstack11111ll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩྲྀ")].append(bstack111l1l11l1_opy_.bstack111lll1l1l_opy_())
            if bstack111lll11l1_opy_:
                self._111l11l1ll_opy_[bstack111lll11l1_opy_ + bstack11111ll_opy_ (u"ࠫ࠲࠭ཷ") + attrs.get(bstack11111ll_opy_ (u"ࠬࡺࡹࡱࡧࠪླྀ"), bstack11111ll_opy_ (u"࠭ࠧཹ")).lower()] = { bstack11111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣེࠪ"): bstack111l1l11l1_opy_ }
            bstack1l1l1l1111_opy_.bstack11l11l1111_opy_(bstack11111ll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥཻࠩ"), bstack111l1l11l1_opy_)
        else:
            bstack111lllll1l_opy_ = {
                bstack11111ll_opy_ (u"ࠩ࡬ࡨོࠬ"): uuid4().__str__(),
                bstack11111ll_opy_ (u"ࠪࡸࡪࡾࡴࠨཽ"): bstack11111ll_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪཾ").format(attrs.get(bstack11111ll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬཿ")), attrs.get(bstack11111ll_opy_ (u"࠭ࡡࡳࡩࡶྀࠫ"), bstack11111ll_opy_ (u"ࠧࠨཱྀ"))) if attrs.get(bstack11111ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ྂ"), []) else attrs.get(bstack11111ll_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩྃ")),
                bstack11111ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶ྄ࠪ"): attrs.get(bstack11111ll_opy_ (u"ࠫࡦࡸࡧࡴࠩ྅"), []),
                bstack11111ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ྆"): bstack11lllll1l_opy_(),
                bstack11111ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭྇"): bstack11111ll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨྈ"),
                bstack11111ll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ྉ"): attrs.get(bstack11111ll_opy_ (u"ࠩࡧࡳࡨ࠭ྊ"), bstack11111ll_opy_ (u"ࠪࠫྋ"))
            }
            if attrs.get(bstack11111ll_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬྌ"), bstack11111ll_opy_ (u"ࠬ࠭ྍ")) != bstack11111ll_opy_ (u"࠭ࠧྎ"):
                bstack111lllll1l_opy_[bstack11111ll_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨྏ")] = attrs.get(bstack11111ll_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩྐ"))
            if not self.bstack111ll111l1_opy_:
                self._111l11l1ll_opy_[self._111ll11lll_opy_()][bstack11111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬྑ")].add_step(bstack111lllll1l_opy_)
                threading.current_thread().current_step_uuid = bstack111lllll1l_opy_[bstack11111ll_opy_ (u"ࠪ࡭ࡩ࠭ྒ")]
            self.bstack111ll111l1_opy_.append(bstack111lllll1l_opy_)
    @bstack111ll1ll11_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111l1ll1ll_opy_()
        self._111l1lll1l_opy_(messages)
        current_test_id = bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ྒྷ"), None)
        bstack111lll11l1_opy_ = current_test_id if current_test_id else bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨྔ"), None)
        bstack111l1l1l1l_opy_ = bstack111l1ll1l1_opy_.get(attrs.get(bstack11111ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ྕ")), bstack11111ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨྖ"))
        bstack111l11lll1_opy_ = attrs.get(bstack11111ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྗ"))
        if bstack111l1l1l1l_opy_ != bstack11111ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ྘") and not attrs.get(bstack11111ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྙ")) and self._111ll11l11_opy_:
            bstack111l11lll1_opy_ = self._111ll11l11_opy_
        bstack111lllll11_opy_ = Result(result=bstack111l1l1l1l_opy_, exception=bstack111l11lll1_opy_, bstack11l1111l11_opy_=[bstack111l11lll1_opy_])
        if attrs.get(bstack11111ll_opy_ (u"ࠫࡹࡿࡰࡦࠩྚ"), bstack11111ll_opy_ (u"ࠬ࠭ྛ")).lower() in [bstack11111ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬྜ"), bstack11111ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩྜྷ")]:
            bstack111lll11l1_opy_ = current_test_id if current_test_id else bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫྞ"), None)
            if bstack111lll11l1_opy_:
                bstack11l111l111_opy_ = bstack111lll11l1_opy_ + bstack11111ll_opy_ (u"ࠤ࠰ࠦྟ") + attrs.get(bstack11111ll_opy_ (u"ࠪࡸࡾࡶࡥࠨྠ"), bstack11111ll_opy_ (u"ࠫࠬྡ")).lower()
                self._111l11l1ll_opy_[bstack11l111l111_opy_][bstack11111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨྡྷ")].stop(time=bstack11lllll1l_opy_(), duration=int(attrs.get(bstack11111ll_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫྣ"), bstack11111ll_opy_ (u"ࠧ࠱ࠩྤ"))), result=bstack111lllll11_opy_)
                bstack1l1l1l1111_opy_.bstack11l11l1111_opy_(bstack11111ll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪྥ"), self._111l11l1ll_opy_[bstack11l111l111_opy_][bstack11111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬྦ")])
        else:
            bstack111lll11l1_opy_ = current_test_id if current_test_id else bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡ࡬ࡨࠬྦྷ"), None)
            if bstack111lll11l1_opy_ and len(self.bstack111ll111l1_opy_) == 1:
                current_step_uuid = bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨྨ"), None)
                self._111l11l1ll_opy_[bstack111lll11l1_opy_][bstack11111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨྩ")].bstack11l111ll1l_opy_(current_step_uuid, duration=int(attrs.get(bstack11111ll_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫྪ"), bstack11111ll_opy_ (u"ࠧ࠱ࠩྫ"))), result=bstack111lllll11_opy_)
            else:
                self.bstack111lll11ll_opy_(attrs)
            self.bstack111ll111l1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11111ll_opy_ (u"ࠨࡪࡷࡱࡱ࠭ྫྷ"), bstack11111ll_opy_ (u"ࠩࡱࡳࠬྭ")) == bstack11111ll_opy_ (u"ࠪࡽࡪࡹࠧྮ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11lll1l1_opy_.bstack11l11111l1_opy_():
                logs.append({
                    bstack11111ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧྯ"): bstack11lllll1l_opy_(),
                    bstack11111ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ྰ"): message.get(bstack11111ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྱ")),
                    bstack11111ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ྲ"): message.get(bstack11111ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧླ")),
                    **bstack11lll1l1_opy_.bstack11l11111l1_opy_()
                })
                if len(logs) > 0:
                    bstack1l1l1l1111_opy_.bstack1llllll1l_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack1l1l1l1111_opy_.bstack111l1lll11_opy_()
    def bstack111lll11ll_opy_(self, bstack111lll1l11_opy_):
        if not bstack11lll1l1_opy_.bstack11l11111l1_opy_():
            return
        kwname = bstack11111ll_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨྴ").format(bstack111lll1l11_opy_.get(bstack11111ll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪྵ")), bstack111lll1l11_opy_.get(bstack11111ll_opy_ (u"ࠫࡦࡸࡧࡴࠩྶ"), bstack11111ll_opy_ (u"ࠬ࠭ྷ"))) if bstack111lll1l11_opy_.get(bstack11111ll_opy_ (u"࠭ࡡࡳࡩࡶࠫྸ"), []) else bstack111lll1l11_opy_.get(bstack11111ll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧྐྵ"))
        error_message = bstack11111ll_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠠࡽࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦ࡜ࠣࡽ࠵ࢁࡡࠨࠢྺ").format(kwname, bstack111lll1l11_opy_.get(bstack11111ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩྻ")), str(bstack111lll1l11_opy_.get(bstack11111ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྼ"))))
        bstack111ll11ll1_opy_ = bstack11111ll_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠥ྽").format(kwname, bstack111lll1l11_opy_.get(bstack11111ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ྾")))
        bstack111ll1l11l_opy_ = error_message if bstack111lll1l11_opy_.get(bstack11111ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ྿")) else bstack111ll11ll1_opy_
        bstack111ll1lll1_opy_ = {
            bstack11111ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ࿀"): self.bstack111ll111l1_opy_[-1].get(bstack11111ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ࿁"), bstack11lllll1l_opy_()),
            bstack11111ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿂"): bstack111ll1l11l_opy_,
            bstack11111ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ࿃"): bstack11111ll_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ࿄") if bstack111lll1l11_opy_.get(bstack11111ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ࿅")) == bstack11111ll_opy_ (u"࠭ࡆࡂࡋࡏ࿆ࠫ") else bstack11111ll_opy_ (u"ࠧࡊࡐࡉࡓࠬ࿇"),
            **bstack11lll1l1_opy_.bstack11l11111l1_opy_()
        }
        bstack1l1l1l1111_opy_.bstack1llllll1l_opy_([bstack111ll1lll1_opy_])
    def _111ll11lll_opy_(self):
        for bstack111ll11l1l_opy_ in reversed(self._111l11l1ll_opy_):
            bstack111l11ll11_opy_ = bstack111ll11l1l_opy_
            data = self._111l11l1ll_opy_[bstack111ll11l1l_opy_][bstack11111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ࿈")]
            if isinstance(data, bstack11l111llll_opy_):
                if not bstack11111ll_opy_ (u"ࠩࡈࡅࡈࡎࠧ࿉") in data.bstack111lll1ll1_opy_():
                    return bstack111l11ll11_opy_
            else:
                return bstack111l11ll11_opy_
    def _111l1lll1l_opy_(self, messages):
        try:
            bstack111l1llll1_opy_ = BuiltIn().get_variable_value(bstack11111ll_opy_ (u"ࠥࠨࢀࡒࡏࡈࠢࡏࡉ࡛ࡋࡌࡾࠤ࿊")) in (bstack111l1l11ll_opy_.DEBUG, bstack111l1l11ll_opy_.TRACE)
            for message, bstack111l11llll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11111ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ࿋"))
                level = message.get(bstack11111ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ࿌"))
                if level == bstack111l1l11ll_opy_.FAIL:
                    self._111ll11l11_opy_ = name or self._111ll11l11_opy_
                    self._111ll111ll_opy_ = bstack111l11llll_opy_.get(bstack11111ll_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢ࿍")) if bstack111l1llll1_opy_ and bstack111l11llll_opy_ else self._111ll111ll_opy_
        except:
            pass
    @classmethod
    def bstack11l11l1111_opy_(self, event: str, bstack111ll1ll1l_opy_: bstack111l11ll1l_opy_, bstack111l1l1ll1_opy_=False):
        if event == bstack11111ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ࿎"):
            bstack111ll1ll1l_opy_.set(hooks=self.store[bstack11111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ࿏")])
        if event == bstack11111ll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ࿐"):
            event = bstack11111ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ࿑")
        if bstack111l1l1ll1_opy_:
            bstack111ll1llll_opy_ = {
                bstack11111ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ࿒"): event,
                bstack111ll1ll1l_opy_.bstack111lll1lll_opy_(): bstack111ll1ll1l_opy_.bstack111ll1l1l1_opy_(event)
            }
            self.bstack111l1l1l11_opy_.append(bstack111ll1llll_opy_)
        else:
            bstack1l1l1l1111_opy_.bstack11l11l1111_opy_(event, bstack111ll1ll1l_opy_)
class bstack111ll1l1ll_opy_:
    def __init__(self):
        self._111ll1111l_opy_ = []
    def bstack111l1ll111_opy_(self):
        self._111ll1111l_opy_.append([])
    def bstack111l1ll1ll_opy_(self):
        return self._111ll1111l_opy_.pop() if self._111ll1111l_opy_ else list()
    def push(self, message):
        self._111ll1111l_opy_[-1].append(message) if self._111ll1111l_opy_ else self._111ll1111l_opy_.append([message])
class bstack111l1l11ll_opy_:
    FAIL = bstack11111ll_opy_ (u"ࠬࡌࡁࡊࡎࠪ࿓")
    ERROR = bstack11111ll_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬ࿔")
    WARNING = bstack11111ll_opy_ (u"ࠧࡘࡃࡕࡒࠬ࿕")
    bstack111ll11111_opy_ = bstack11111ll_opy_ (u"ࠨࡋࡑࡊࡔ࠭࿖")
    DEBUG = bstack11111ll_opy_ (u"ࠩࡇࡉࡇ࡛ࡇࠨ࿗")
    TRACE = bstack11111ll_opy_ (u"ࠪࡘࡗࡇࡃࡆࠩ࿘")
    bstack111l1lllll_opy_ = [FAIL, ERROR]
def bstack111l11l1l1_opy_(bstack111l11l11l_opy_):
    if not bstack111l11l11l_opy_:
        return None
    if bstack111l11l11l_opy_.get(bstack11111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ࿙"), None):
        return getattr(bstack111l11l11l_opy_[bstack11111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿚")], bstack11111ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ࿛"), None)
    return bstack111l11l11l_opy_.get(bstack11111ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ࿜"), None)
def bstack111l1l1lll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11111ll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ࿝"), bstack11111ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ࿞")]:
        return
    if hook_type.lower() == bstack11111ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ࿟"):
        if current_test_uuid is None:
            return bstack11111ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨ࿠")
        else:
            return bstack11111ll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ࿡")
    elif hook_type.lower() == bstack11111ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ࿢"):
        if current_test_uuid is None:
            return bstack11111ll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ࿣")
        else:
            return bstack11111ll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ࿤")