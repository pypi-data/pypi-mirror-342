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
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1111l11ll1_opy_ import bstack11111l1l11_opy_, bstack111111l1ll_opy_
import os
import threading
class bstack11111l1ll1_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11111ll_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦဒ").format(self.name)
class bstack1111l11l1l_opy_(Enum):
    NONE = 0
    bstack1111111l11_opy_ = 1
    bstack1lllllllll1_opy_ = 3
    bstack1llllllll1l_opy_ = 4
    bstack1111111ll1_opy_ = 5
    QUIT = 6
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack11111ll_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨဓ").format(self.name)
class bstack1111l1111l_opy_(bstack11111l1l11_opy_):
    framework_name: str
    framework_version: str
    state: bstack1111l11l1l_opy_
    previous_state: bstack1111l11l1l_opy_
    bstack1111l1l111_opy_: datetime
    bstack111111ll1l_opy_: datetime
    def __init__(
        self,
        context: bstack111111l1ll_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1111l11l1l_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1111l11l1l_opy_.NONE
        self.bstack1111l1l111_opy_ = datetime.now(tz=timezone.utc)
        self.bstack111111ll1l_opy_ = datetime.now(tz=timezone.utc)
    def bstack11111l11ll_opy_(self, bstack11111111l1_opy_: bstack1111l11l1l_opy_):
        bstack11111ll1l1_opy_ = bstack1111l11l1l_opy_(bstack11111111l1_opy_).name
        if not bstack11111ll1l1_opy_:
            return False
        if bstack11111111l1_opy_ == self.state:
            return False
        if self.state == bstack1111l11l1l_opy_.bstack1lllllllll1_opy_: # bstack1111111lll_opy_ bstack111111llll_opy_ for bstack11111111ll_opy_ in bstack11111ll111_opy_, it bstack111111111l_opy_ bstack111111l11l_opy_ bstack11111lll11_opy_ times bstack111111lll1_opy_ a new state
            return True
        if (
            bstack11111111l1_opy_ == bstack1111l11l1l_opy_.NONE
            or (self.state != bstack1111l11l1l_opy_.NONE and bstack11111111l1_opy_ == bstack1111l11l1l_opy_.bstack1111111l11_opy_)
            or (self.state < bstack1111l11l1l_opy_.bstack1111111l11_opy_ and bstack11111111l1_opy_ == bstack1111l11l1l_opy_.bstack1llllllll1l_opy_)
            or (self.state < bstack1111l11l1l_opy_.bstack1111111l11_opy_ and bstack11111111l1_opy_ == bstack1111l11l1l_opy_.QUIT)
        ):
            raise ValueError(bstack11111ll_opy_ (u"ࠢࡪࡰࡹࡥࡱ࡯ࡤࠡࡵࡷࡥࡹ࡫ࠠࡵࡴࡤࡲࡸ࡯ࡴࡪࡱࡱ࠾ࠥࠨန") + str(self.state) + bstack11111ll_opy_ (u"ࠣࠢࡀࡂࠥࠨပ") + str(bstack11111111l1_opy_))
        self.previous_state = self.state
        self.state = bstack11111111l1_opy_
        self.bstack111111ll1l_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1111l1l11l_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack11111llll1_opy_: Dict[str, bstack1111l1111l_opy_] = dict()
    framework_name: str
    framework_version: str
    classes: List[Type]
    def __init__(
        self,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
    ):
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.classes = classes
    @abc.abstractmethod
    def bstack11111l11l1_opy_(self, instance: bstack1111l1111l_opy_, method_name: str, bstack1111l11lll_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1llllllll11_opy_(
        self, method_name, previous_state: bstack1111l11l1l_opy_, *args, **kwargs
    ) -> bstack1111l11l1l_opy_:
        return
    @abc.abstractmethod
    def bstack111111ll11_opy_(
        self,
        target: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1111111111_opy_(self, bstack1llllllllll_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack1llllllllll_opy_:
                bstack1111l1l1l1_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1111l1l1l1_opy_):
                    self.logger.warning(bstack11111ll_opy_ (u"ࠤࡸࡲࡵࡧࡴࡤࡪࡨࡨࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࠢဖ") + str(method_name) + bstack11111ll_opy_ (u"ࠥࠦဗ"))
                    continue
                bstack11111l1lll_opy_ = self.bstack1llllllll11_opy_(
                    method_name, previous_state=bstack1111l11l1l_opy_.NONE
                )
                bstack1111l11l11_opy_ = self.bstack11111ll11l_opy_(
                    method_name,
                    (bstack11111l1lll_opy_ if bstack11111l1lll_opy_ else bstack1111l11l1l_opy_.NONE),
                    bstack1111l1l1l1_opy_,
                )
                if not callable(bstack1111l11l11_opy_):
                    self.logger.warning(bstack11111ll_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠤࡳࡵࡴࠡࡲࡤࡸࡨ࡮ࡥࡥ࠼ࠣࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࠬࢀࡹࡥ࡭ࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁ࠿ࠦࠢဘ") + str(self.framework_version) + bstack11111ll_opy_ (u"ࠧ࠯ࠢမ"))
                    continue
                setattr(clazz, method_name, bstack1111l11l11_opy_)
    def bstack11111ll11l_opy_(
        self,
        method_name: str,
        bstack11111l1lll_opy_: bstack1111l11l1l_opy_,
        bstack1111l1l1l1_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack11ll111l1l_opy_ = datetime.now()
            (bstack11111l1lll_opy_,) = wrapped.__vars__
            bstack11111l1lll_opy_ = (
                bstack11111l1lll_opy_
                if bstack11111l1lll_opy_ and bstack11111l1lll_opy_ != bstack1111l11l1l_opy_.NONE
                else self.bstack1llllllll11_opy_(method_name, previous_state=bstack11111l1lll_opy_, *args, **kwargs)
            )
            if bstack11111l1lll_opy_ == bstack1111l11l1l_opy_.bstack1111111l11_opy_:
                ctx = bstack11111l1l11_opy_.create_context(self.bstack11111lllll_opy_(target))
                if not self.bstack11111l1l1l_opy_() or ctx.id not in bstack1111l1l11l_opy_.bstack11111llll1_opy_:
                    bstack1111l1l11l_opy_.bstack11111llll1_opy_[ctx.id] = bstack1111l1111l_opy_(
                        ctx, self.framework_name, self.framework_version, bstack11111l1lll_opy_
                    )
                self.logger.debug(bstack11111ll_opy_ (u"ࠨࡷࡳࡣࡳࡴࡪࡪࠠ࡮ࡧࡷ࡬ࡴࡪࠠࡤࡴࡨࡥࡹ࡫ࡤ࠻ࠢࡾࡸࡦࡸࡧࡦࡶ࠱ࡣࡤࡩ࡬ࡢࡵࡶࡣࡤࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡨࡺࡸ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢယ") + str(bstack1111l1l11l_opy_.bstack11111llll1_opy_.keys()) + bstack11111ll_opy_ (u"ࠢࠣရ"))
            else:
                self.logger.debug(bstack11111ll_opy_ (u"ࠣࡹࡵࡥࡵࡶࡥࡥࠢࡰࡩࡹ࡮࡯ࡥࠢ࡬ࡲࡻࡵ࡫ࡦࡦ࠽ࠤࢀࡺࡡࡳࡩࡨࡸ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟ࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥလ") + str(bstack1111l1l11l_opy_.bstack11111llll1_opy_.keys()) + bstack11111ll_opy_ (u"ࠤࠥဝ"))
            instance = bstack1111l1l11l_opy_.bstack1111l111ll_opy_(self.bstack11111lllll_opy_(target))
            if bstack11111l1lll_opy_ == bstack1111l11l1l_opy_.NONE or not instance:
                ctx = bstack11111l1l11_opy_.create_context(self.bstack11111lllll_opy_(target))
                self.logger.warning(bstack11111ll_opy_ (u"ࠥࡻࡷࡧࡰࡱࡧࡧࠤࡲ࡫ࡴࡩࡱࡧࠤࡺࡴࡴࡳࡣࡦ࡯ࡪࡪ࠺ࠡࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡤࡶࡻࡁࢀࡩࡴࡹࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢသ") + str(bstack1111l1l11l_opy_.bstack11111llll1_opy_.keys()) + bstack11111ll_opy_ (u"ࠦࠧဟ"))
                return bstack1111l1l1l1_opy_(target, *args, **kwargs)
            bstack11111l1111_opy_ = self.bstack111111ll11_opy_(
                target,
                (instance, method_name),
                (bstack11111l1lll_opy_, bstack11111l1ll1_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack11111l11ll_opy_(bstack11111l1lll_opy_):
                self.logger.debug(bstack11111ll_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡩࡩࠦࡳࡵࡣࡷࡩ࠲ࡺࡲࡢࡰࡶ࡭ࡹ࡯࡯࡯࠼ࠣࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡰࡳࡧࡹ࡭ࡴࡻࡳࡠࡵࡷࡥࡹ࡫ࡽࠡ࠿ࡁࠤࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡴࡶࡤࡸࡪࢃࠠࠩࡽࡷࡽࡵ࡫ࠨࡵࡣࡵ࡫ࡪࡺࠩࡾ࠰ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡾࡥࡷ࡭ࡳࡾࠫࠣ࡟ࠧဠ") + str(instance.ref()) + bstack11111ll_opy_ (u"ࠨ࡝ࠣအ"))
            result = (
                bstack11111l1111_opy_(target, bstack1111l1l1l1_opy_, *args, **kwargs)
                if callable(bstack11111l1111_opy_)
                else bstack1111l1l1l1_opy_(target, *args, **kwargs)
            )
            bstack1111111l1l_opy_ = self.bstack111111ll11_opy_(
                target,
                (instance, method_name),
                (bstack11111l1lll_opy_, bstack11111l1ll1_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack11111l11l1_opy_(instance, method_name, datetime.now() - bstack11ll111l1l_opy_, *args, **kwargs)
            return bstack1111111l1l_opy_ if bstack1111111l1l_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack11111l1lll_opy_,)
        return wrapped
    @staticmethod
    def bstack1111l111ll_opy_(target: object, strict=True):
        ctx = bstack11111l1l11_opy_.create_context(target)
        instance = bstack1111l1l11l_opy_.bstack11111llll1_opy_.get(ctx.id, None)
        if instance and instance.bstack1111l11111_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack111111l1l1_opy_(
        ctx: bstack111111l1ll_opy_, state: bstack1111l11l1l_opy_, reverse=True
    ) -> List[bstack1111l1111l_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1111l1l11l_opy_.bstack11111llll1_opy_.values(),
            ),
            key=lambda t: t.bstack1111l1l111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack111111l111_opy_(instance: bstack1111l1111l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack11111lll1l_opy_(instance: bstack1111l1111l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack11111l11ll_opy_(instance: bstack1111l1111l_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1111l1l11l_opy_.logger.debug(bstack11111ll_opy_ (u"ࠢࡴࡧࡷࡣࡸࡺࡡࡵࡧ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢ࡮ࡩࡾࡃࡻ࡬ࡧࡼࢁࠥࡼࡡ࡭ࡷࡨࡁࠧဢ") + str(value) + bstack11111ll_opy_ (u"ࠣࠤဣ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1111l1l11l_opy_.bstack1111l111ll_opy_(target, strict)
        return bstack1111l1l11l_opy_.bstack11111lll1l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1111l1l11l_opy_.bstack1111l111ll_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack11111l1l1l_opy_(self):
        return self.framework_name == bstack11111ll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ဤ")
    def bstack11111lllll_opy_(self, target):
        return target if not self.bstack11111l1l1l_opy_() else self.bstack11111ll1ll_opy_()
    @staticmethod
    def bstack11111ll1ll_opy_():
        return str(os.getpid()) + str(threading.get_ident())