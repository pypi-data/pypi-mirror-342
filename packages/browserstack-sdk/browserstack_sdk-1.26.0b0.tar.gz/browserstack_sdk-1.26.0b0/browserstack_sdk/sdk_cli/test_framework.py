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
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111l1ll11_opy_ import bstack1111l1l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1111l11ll1_opy_ import bstack11111l1l11_opy_, bstack111111l1ll_opy_
class bstack1llllll1l11_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11111ll_opy_ (u"ࠨࡔࡦࡵࡷࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᓪ").format(self.name)
class bstack1llll1l11ll_opy_(Enum):
    NONE = 0
    BEFORE_ALL = 1
    LOG = 2
    SETUP_FIXTURE = 3
    INIT_TEST = 4
    BEFORE_EACH = 5
    AFTER_EACH = 6
    TEST = 7
    STEP = 8
    LOG_REPORT = 9
    AFTER_ALL = 10
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack11111ll_opy_ (u"ࠢࡕࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣᓫ").format(self.name)
class bstack1lll1l1l1l1_opy_(bstack11111l1l11_opy_):
    bstack1ll1l111ll1_opy_: List[str]
    bstack1l111lllll1_opy_: Dict[str, str]
    state: bstack1llll1l11ll_opy_
    bstack1111l1l111_opy_: datetime
    bstack111111ll1l_opy_: datetime
    def __init__(
        self,
        context: bstack111111l1ll_opy_,
        bstack1ll1l111ll1_opy_: List[str],
        bstack1l111lllll1_opy_: Dict[str, str],
        state=bstack1llll1l11ll_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1l111ll1_opy_ = bstack1ll1l111ll1_opy_
        self.bstack1l111lllll1_opy_ = bstack1l111lllll1_opy_
        self.state = state
        self.bstack1111l1l111_opy_ = datetime.now(tz=timezone.utc)
        self.bstack111111ll1l_opy_ = datetime.now(tz=timezone.utc)
    def bstack11111l11ll_opy_(self, bstack11111111l1_opy_: bstack1llll1l11ll_opy_):
        bstack11111ll1l1_opy_ = bstack1llll1l11ll_opy_(bstack11111111l1_opy_).name
        if not bstack11111ll1l1_opy_:
            return False
        if bstack11111111l1_opy_ == self.state:
            return False
        self.state = bstack11111111l1_opy_
        self.bstack111111ll1l_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l11ll1111l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll1lllllll_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1ll1111l1l1_opy_: int = None
    bstack1ll111l1l1l_opy_: str = None
    bstack1l11ll_opy_: str = None
    bstack1l1111l11l_opy_: str = None
    bstack1ll111llll1_opy_: str = None
    bstack1l111llll11_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1ll1lll1_opy_ = bstack11111ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠦᓬ")
    bstack1l11ll11ll1_opy_ = bstack11111ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡪࡦࠥᓭ")
    bstack1ll1lll111l_opy_ = bstack11111ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡰࡤࡱࡪࠨᓮ")
    bstack1l11l111l11_opy_ = bstack11111ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫࡟ࡱࡣࡷ࡬ࠧᓯ")
    bstack1l11llll11l_opy_ = bstack11111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡸࡦ࡭ࡳࠣᓰ")
    bstack1l1l1lll1l1_opy_ = bstack11111ll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᓱ")
    bstack1l1llll11ll_opy_ = bstack11111ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࡤࡧࡴࠣᓲ")
    bstack1ll111l11ll_opy_ = bstack11111ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᓳ")
    bstack1ll111l111l_opy_ = bstack11111ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡦࡰࡧࡩࡩࡥࡡࡵࠤᓴ")
    bstack1l111l1ll11_opy_ = bstack11111ll_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᓵ")
    bstack1ll1ll1111l_opy_ = bstack11111ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠥᓶ")
    bstack1ll111l1lll_opy_ = bstack11111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᓷ")
    bstack1l11l111ll1_opy_ = bstack11111ll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡨࡵࡤࡦࠤᓸ")
    bstack1l1ll1ll111_opy_ = bstack11111ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠤᓹ")
    bstack1ll1ll111ll_opy_ = bstack11111ll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤᓺ")
    bstack1l1l1llll11_opy_ = bstack11111ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡣ࡬ࡰࡺࡸࡥࠣᓻ")
    bstack1l11l11lll1_opy_ = bstack11111ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠢᓼ")
    bstack1l11l1ll1l1_opy_ = bstack11111ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳ࡬ࡹࠢᓽ")
    bstack1l11l11l111_opy_ = bstack11111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡱࡪࡺࡡࠣᓾ")
    bstack1l111l11l1l_opy_ = bstack11111ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡸࡩ࡯ࡱࡧࡶࠫᓿ")
    bstack1l1l1111lll_opy_ = bstack11111ll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣᔀ")
    bstack1l11l111111_opy_ = bstack11111ll_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᔁ")
    bstack1l11l1llll1_opy_ = bstack11111ll_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᔂ")
    bstack1l11l1l1l1l_opy_ = bstack11111ll_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡫ࡧࠦᔃ")
    bstack1l11l1l1ll1_opy_ = bstack11111ll_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡵࡩࡸࡻ࡬ࡵࠤᔄ")
    bstack1l11ll1l11l_opy_ = bstack11111ll_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡰࡴ࡭ࡳࠣᔅ")
    bstack1l111lll1ll_opy_ = bstack11111ll_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠤᔆ")
    bstack1l11l1lll11_opy_ = bstack11111ll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᔇ")
    bstack1l11lll11l1_opy_ = bstack11111ll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᔈ")
    bstack1l11l1l111l_opy_ = bstack11111ll_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥᔉ")
    bstack1l11l1l1lll_opy_ = bstack11111ll_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦᔊ")
    bstack1ll11l1111l_opy_ = bstack11111ll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙ࠨᔋ")
    bstack1l1llllll1l_opy_ = bstack11111ll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡐࡔࡍࠢᔌ")
    bstack1ll111lllll_opy_ = bstack11111ll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᔍ")
    bstack11111llll1_opy_: Dict[str, bstack1lll1l1l1l1_opy_] = dict()
    bstack1l1111ll1ll_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1l111ll1_opy_: List[str]
    bstack1l111lllll1_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1l111ll1_opy_: List[str],
        bstack1l111lllll1_opy_: Dict[str, str],
        bstack1111l1ll11_opy_: bstack1111l1l1ll_opy_
    ):
        self.bstack1ll1l111ll1_opy_ = bstack1ll1l111ll1_opy_
        self.bstack1l111lllll1_opy_ = bstack1l111lllll1_opy_
        self.bstack1111l1ll11_opy_ = bstack1111l1ll11_opy_
    def track_event(
        self,
        context: bstack1l11ll1111l_opy_,
        test_framework_state: bstack1llll1l11ll_opy_,
        test_hook_state: bstack1llllll1l11_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11111ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡢࡴࡪࡷࡂࢁࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽࢀࠦᔎ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l11l11l1ll_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l11111l1_opy_ = TestFramework.bstack1l1l1111l11_opy_(bstack11111l111l_opy_)
        if not bstack1l1l11111l1_opy_ in TestFramework.bstack1l1111ll1ll_opy_:
            return
        self.logger.debug(bstack11111ll_opy_ (u"ࠣ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡿࢂࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠤᔏ").format(len(TestFramework.bstack1l1111ll1ll_opy_[bstack1l1l11111l1_opy_])))
        for callback in TestFramework.bstack1l1111ll1ll_opy_[bstack1l1l11111l1_opy_]:
            try:
                callback(self, instance, bstack11111l111l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11111ll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠤᔐ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1lll11l1l_opy_(self):
        return
    @abc.abstractmethod
    def bstack1ll1111l1ll_opy_(self, instance, bstack11111l111l_opy_):
        return
    @abc.abstractmethod
    def bstack1ll111lll1l_opy_(self, instance, bstack11111l111l_opy_):
        return
    @staticmethod
    def bstack1111l111ll_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack11111l1l11_opy_.create_context(target)
        instance = TestFramework.bstack11111llll1_opy_.get(ctx.id, None)
        if instance and instance.bstack1111l11111_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1llllllll_opy_(reverse=True) -> List[bstack1lll1l1l1l1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack11111llll1_opy_.values(),
            ),
            key=lambda t: t.bstack1111l1l111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack111111l1l1_opy_(ctx: bstack111111l1ll_opy_, reverse=True) -> List[bstack1lll1l1l1l1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack11111llll1_opy_.values(),
            ),
            key=lambda t: t.bstack1111l1l111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack111111l111_opy_(instance: bstack1lll1l1l1l1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack11111lll1l_opy_(instance: bstack1lll1l1l1l1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack11111l11ll_opy_(instance: bstack1lll1l1l1l1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11111ll_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡱࡥࡺ࠿ࡾࢁࠥࡼࡡ࡭ࡷࡨࡁࢀࢃࠢᔑ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11lll111l_opy_(instance: bstack1lll1l1l1l1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11111ll_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠࡦࡰࡷࡶ࡮࡫ࡳ࠾ࡽࢀࠦᔒ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l1111ll11l_opy_(instance: bstack1llll1l11ll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11111ll_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧᔓ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1111l111ll_opy_(target, strict)
        return TestFramework.bstack11111lll1l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1111l111ll_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l1l11ll_opy_(instance: bstack1lll1l1l1l1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l11ll1lll1_opy_(instance: bstack1lll1l1l1l1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l1l1111l11_opy_(bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_]):
        return bstack11111ll_opy_ (u"ࠨ࠺ࠣᔔ").join((bstack1llll1l11ll_opy_(bstack11111l111l_opy_[0]).name, bstack1llllll1l11_opy_(bstack11111l111l_opy_[1]).name))
    @staticmethod
    def bstack1ll1ll11l11_opy_(bstack11111l111l_opy_: Tuple[bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_], callback: Callable):
        bstack1l1l11111l1_opy_ = TestFramework.bstack1l1l1111l11_opy_(bstack11111l111l_opy_)
        TestFramework.logger.debug(bstack11111ll_opy_ (u"ࠢࡴࡧࡷࡣ࡭ࡵ࡯࡬ࡡࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥ࡮࡯ࡰ࡭ࡢࡶࡪ࡭ࡩࡴࡶࡵࡽࡤࡱࡥࡺ࠿ࡾࢁࠧᔕ").format(bstack1l1l11111l1_opy_))
        if not bstack1l1l11111l1_opy_ in TestFramework.bstack1l1111ll1ll_opy_:
            TestFramework.bstack1l1111ll1ll_opy_[bstack1l1l11111l1_opy_] = []
        TestFramework.bstack1l1111ll1ll_opy_[bstack1l1l11111l1_opy_].append(callback)
    @staticmethod
    def bstack1ll111ll1ll_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11111ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡺࡩ࡯ࡵࠥᔖ"):
            return klass.__qualname__
        return module + bstack11111ll_opy_ (u"ࠤ࠱ࠦᔗ") + klass.__qualname__
    @staticmethod
    def bstack1ll11l111l1_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}