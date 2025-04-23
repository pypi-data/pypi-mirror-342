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
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1llll11l111_opy_ import bstack1ll111ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111lll1l_opy_ import bstack1l1lll1ll11_opy_, bstack1lll11l1ll1_opy_
class bstack1111111l1l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1ll1l11_opy_ (u"ࠢࡕࡧࡶࡸࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥፎ").format(self.name)
class bstack11111ll1l1_opy_(Enum):
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
        return bstack1ll1l11_opy_ (u"ࠣࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤፏ").format(self.name)
class bstack11111l111l_opy_(bstack1l1lll1ll11_opy_):
    bstack1l1lll11l1l_opy_: List[str]
    bstack1ll111ll111_opy_: Dict[str, str]
    state: bstack11111ll1l1_opy_
    bstack1l1ll111lll_opy_: datetime
    bstack1l1ll1111ll_opy_: datetime
    def __init__(
        self,
        context: bstack1lll11l1ll1_opy_,
        bstack1l1lll11l1l_opy_: List[str],
        bstack1ll111ll111_opy_: Dict[str, str],
        state=bstack11111ll1l1_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1l1lll11l1l_opy_ = bstack1l1lll11l1l_opy_
        self.bstack1ll111ll111_opy_ = bstack1ll111ll111_opy_
        self.state = state
        self.bstack1l1ll111lll_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1l1ll1111ll_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lllllll1l1_opy_(self, bstack1l1ll111l1l_opy_: bstack11111ll1l1_opy_):
        bstack1l1ll111l11_opy_ = bstack11111ll1l1_opy_(bstack1l1ll111l1l_opy_).name
        if not bstack1l1ll111l11_opy_:
            return False
        if bstack1l1ll111l1l_opy_ == self.state:
            return False
        self.state = bstack1l1ll111l1l_opy_
        self.bstack1l1ll1111ll_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1ll11l11111_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack111111llll_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1llll1l1lll_opy_: int = None
    bstack1llll1ll1ll_opy_: str = None
    bstack11l1ll1_opy_: str = None
    bstack111l1l111_opy_: str = None
    bstack1lllll11lll_opy_: str = None
    bstack1l1llll1lll_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack11111111ll_opy_ = bstack1ll1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧፐ")
    bstack1l1lll1llll_opy_ = bstack1ll1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡫ࡧࠦፑ")
    bstack1111l111ll_opy_ = bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠢፒ")
    bstack1l1lll1l1l1_opy_ = bstack1ll1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡠࡲࡤࡸ࡭ࠨፓ")
    bstack1ll111l1ll1_opy_ = bstack1ll1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡹࡧࡧࡴࠤፔ")
    bstack1lll111111l_opy_ = bstack1ll1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࠧፕ")
    bstack1llll11l1ll_opy_ = bstack1ll1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࡥࡡࡵࠤፖ")
    bstack1llll11llll_opy_ = bstack1ll1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦፗ")
    bstack1lllll1l1l1_opy_ = bstack1ll1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥፘ")
    bstack1l1lllll1ll_opy_ = bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳࡨࡧࡴࡪࡱࡱࠦፙ")
    bstack1llll1lllll_opy_ = bstack1ll1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠦፚ")
    bstack1lllllllll1_opy_ = bstack1ll1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ፛")
    bstack1l1lll111ll_opy_ = bstack1ll1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡩ࡯ࡥࡧࠥ፜")
    bstack11111lll1l_opy_ = bstack1ll1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠥ፝")
    bstack1111l11ll1_opy_ = bstack1ll1l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠥ፞")
    bstack1lll11l1111_opy_ = bstack1ll1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࠤ፟")
    bstack1ll111ll11l_opy_ = bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠣ፠")
    bstack1l1llll111l_opy_ = bstack1ll1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴ࡭ࡳࠣ፡")
    bstack1ll11l111l1_opy_ = bstack1ll1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡲ࡫ࡴࡢࠤ።")
    bstack1l1ll1l1l11_opy_ = bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡹࡣࡰࡲࡨࡷࠬ፣")
    bstack1ll1l1l11ll_opy_ = bstack1ll1l11_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤ፤")
    bstack1l1lll1111l_opy_ = bstack1ll1l11_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧ፥")
    bstack1ll11111ll1_opy_ = bstack1ll1l11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡨࡲࡩ࡫ࡤࡠࡣࡷࠦ፦")
    bstack1l1lll1l11l_opy_ = bstack1ll1l11_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡ࡬ࡨࠧ፧")
    bstack1l1lllllll1_opy_ = bstack1ll1l11_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡶࡪࡹࡵ࡭ࡶࠥ፨")
    bstack1l1llll11ll_opy_ = bstack1ll1l11_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡱࡵࡧࡴࠤ፩")
    bstack1ll11111111_opy_ = bstack1ll1l11_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠥ፪")
    bstack1l1ll1lll11_opy_ = bstack1ll1l11_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨ፫")
    bstack1ll11l11l11_opy_ = bstack1ll1l11_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦ፬")
    bstack1ll11l11ll1_opy_ = bstack1ll1l11_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦ፭")
    bstack1l1lll111l1_opy_ = bstack1ll1l11_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧ፮")
    bstack1llll1ll11l_opy_ = bstack1ll1l11_opy_ (u"࡚ࠧࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠢ፯")
    bstack1lllll11ll1_opy_ = bstack1ll1l11_opy_ (u"ࠨࡔࡆࡕࡗࡣࡑࡕࡇࠣ፰")
    bstack1lllllll111_opy_ = bstack1ll1l11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤ፱")
    bstack1lll111l111_opy_: Dict[str, bstack11111l111l_opy_] = dict()
    bstack1l1ll11ll11_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1lll11l1l_opy_: List[str]
    bstack1ll111ll111_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1lll11l1l_opy_: List[str],
        bstack1ll111ll111_opy_: Dict[str, str],
        bstack1llll11l111_opy_: bstack1ll111ll1ll_opy_
    ):
        self.bstack1l1lll11l1l_opy_ = bstack1l1lll11l1l_opy_
        self.bstack1ll111ll111_opy_ = bstack1ll111ll111_opy_
        self.bstack1llll11l111_opy_ = bstack1llll11l111_opy_
    def track_event(
        self,
        context: bstack1ll11l11111_opy_,
        test_framework_state: bstack11111ll1l1_opy_,
        test_hook_state: bstack1111111l1l_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡣࡵ࡫ࡸࡃࡻࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾࢁࠧ፲").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1ll111lllll_opy_(
        self,
        instance: bstack11111l111l_opy_,
        bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1ll11llllll_opy_ = TestFramework.bstack1ll11llll11_opy_(bstack111111111l_opy_)
        if not bstack1ll11llllll_opy_ in TestFramework.bstack1l1ll11ll11_opy_:
            return
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠤ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࢀࢃࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠥ፳").format(len(TestFramework.bstack1l1ll11ll11_opy_[bstack1ll11llllll_opy_])))
        for callback in TestFramework.bstack1l1ll11ll11_opy_[bstack1ll11llllll_opy_]:
            try:
                callback(self, instance, bstack111111111l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1ll1l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠥ፴").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1lll1llll11_opy_(self):
        return
    @abc.abstractmethod
    def bstack1llll111111_opy_(self, instance, bstack111111111l_opy_):
        return
    @abc.abstractmethod
    def bstack1llll1l1111_opy_(self, instance, bstack111111111l_opy_):
        return
    @staticmethod
    def bstack1ll11ll11l1_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1l1lll1ll11_opy_.create_context(target)
        instance = TestFramework.bstack1lll111l111_opy_.get(ctx.id, None)
        if instance and instance.bstack1l1ll1111l1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1llllllllll_opy_(reverse=True) -> List[bstack11111l111l_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1lll111l111_opy_.values(),
            ),
            key=lambda t: t.bstack1l1ll111lll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1111l1ll1l_opy_(ctx: bstack1lll11l1ll1_opy_, reverse=True) -> List[bstack11111l111l_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1lll111l111_opy_.values(),
            ),
            key=lambda t: t.bstack1l1ll111lll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llllll11l1_opy_(instance: bstack11111l111l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack11111l11l1_opy_(instance: bstack11111l111l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lllllll1l1_opy_(instance: bstack11111l111l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡫ࡦࡻࡀࡿࢂࠦࡶࡢ࡮ࡸࡩࡂࢁࡽࠣ፵").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l1llllllll_opy_(instance: bstack11111l111l_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡࡧࡱࡸࡷ࡯ࡥࡴ࠿ࡾࢁࠧ፶").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l1ll111ll1_opy_(instance: bstack11111ll1l1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡰ࡫ࡹ࠾ࡽࢀࠤࡻࡧ࡬ࡶࡧࡀࡿࢂࠨ፷").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1ll11ll11l1_opy_(target, strict)
        return TestFramework.bstack11111l11l1_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1ll11ll11l1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1ll11l1l1l1_opy_(instance: bstack11111l111l_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l1llll1ll1_opy_(instance: bstack11111l111l_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1ll11llll11_opy_(bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_]):
        return bstack1ll1l11_opy_ (u"ࠢ࠻ࠤ፸").join((bstack11111ll1l1_opy_(bstack111111111l_opy_[0]).name, bstack1111111l1l_opy_(bstack111111111l_opy_[1]).name))
    @staticmethod
    def bstack111111l1l1_opy_(bstack111111111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111111l1l_opy_], callback: Callable):
        bstack1ll11llllll_opy_ = TestFramework.bstack1ll11llll11_opy_(bstack111111111l_opy_)
        TestFramework.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡵࡨࡸࡤ࡮࡯ࡰ࡭ࡢࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡨࡰࡱ࡮ࡣࡷ࡫ࡧࡪࡵࡷࡶࡾࡥ࡫ࡦࡻࡀࡿࢂࠨ፹").format(bstack1ll11llllll_opy_))
        if not bstack1ll11llllll_opy_ in TestFramework.bstack1l1ll11ll11_opy_:
            TestFramework.bstack1l1ll11ll11_opy_[bstack1ll11llllll_opy_] = []
        TestFramework.bstack1l1ll11ll11_opy_[bstack1ll11llllll_opy_].append(callback)
    @staticmethod
    def bstack1llll11ll1l_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1ll1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡴࡪࡰࡶࠦ፺"):
            return klass.__qualname__
        return module + bstack1ll1l11_opy_ (u"ࠥ࠲ࠧ፻") + klass.__qualname__
    @staticmethod
    def bstack1llll1l111l_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}