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
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1ll111lll1l_opy_ import bstack1l1lll1ll11_opy_, bstack1lll11l1ll1_opy_
import os
import threading
class bstack111111ll1l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1ll1l11_opy_ (u"ࠣࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᎀ").format(self.name)
class bstack11111l1lll_opy_(Enum):
    NONE = 0
    bstack1lll11llll1_opy_ = 1
    bstack1lll11ll1l1_opy_ = 3
    bstack1111l1l1l1_opy_ = 4
    bstack1l1l1ll11l1_opy_ = 5
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
        return bstack1ll1l11_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᎁ").format(self.name)
class bstack1111l1lll1_opy_(bstack1l1lll1ll11_opy_):
    framework_name: str
    framework_version: str
    state: bstack11111l1lll_opy_
    previous_state: bstack11111l1lll_opy_
    bstack1l1ll111lll_opy_: datetime
    bstack1l1ll1111ll_opy_: datetime
    def __init__(
        self,
        context: bstack1lll11l1ll1_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack11111l1lll_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack11111l1lll_opy_.NONE
        self.bstack1l1ll111lll_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1l1ll1111ll_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lllllll1l1_opy_(self, bstack1l1ll111l1l_opy_: bstack11111l1lll_opy_):
        bstack1l1ll111l11_opy_ = bstack11111l1lll_opy_(bstack1l1ll111l1l_opy_).name
        if not bstack1l1ll111l11_opy_:
            return False
        if bstack1l1ll111l1l_opy_ == self.state:
            return False
        if self.state == bstack11111l1lll_opy_.bstack1lll11ll1l1_opy_: # bstack1l1l1l1l1ll_opy_ bstack1l1l1ll1l11_opy_ for bstack1l1l1ll1lll_opy_ in bstack1l1l1l1ll1l_opy_, it bstack1l1l1lll1l1_opy_ bstack1l1l1l1l1l1_opy_ bstack1l1l1l1ll11_opy_ times bstack1l1l1ll1ll1_opy_ a new state
            return True
        if (
            bstack1l1ll111l1l_opy_ == bstack11111l1lll_opy_.NONE
            or (self.state != bstack11111l1lll_opy_.NONE and bstack1l1ll111l1l_opy_ == bstack11111l1lll_opy_.bstack1lll11llll1_opy_)
            or (self.state < bstack11111l1lll_opy_.bstack1lll11llll1_opy_ and bstack1l1ll111l1l_opy_ == bstack11111l1lll_opy_.bstack1111l1l1l1_opy_)
            or (self.state < bstack11111l1lll_opy_.bstack1lll11llll1_opy_ and bstack1l1ll111l1l_opy_ == bstack11111l1lll_opy_.QUIT)
        ):
            raise ValueError(bstack1ll1l11_opy_ (u"ࠥ࡭ࡳࡼࡡ࡭࡫ࡧࠤࡸࡺࡡࡵࡧࠣࡸࡷࡧ࡮ࡴ࡫ࡷ࡭ࡴࡴ࠺ࠡࠤᎂ") + str(self.state) + bstack1ll1l11_opy_ (u"ࠦࠥࡃ࠾ࠡࠤᎃ") + str(bstack1l1ll111l1l_opy_))
        self.previous_state = self.state
        self.state = bstack1l1ll111l1l_opy_
        self.bstack1l1ll1111ll_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1ll1l1l1111_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1lll111l111_opy_: Dict[str, bstack1111l1lll1_opy_] = dict()
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
    def bstack1ll11lll11l_opy_(self, instance: bstack1111l1lll1_opy_, method_name: str, bstack1ll11lllll1_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1ll1l11l1l1_opy_(
        self, method_name, previous_state: bstack11111l1lll_opy_, *args, **kwargs
    ) -> bstack11111l1lll_opy_:
        return
    @abc.abstractmethod
    def bstack1ll11llll1l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1ll1l11l11l_opy_(self, bstack1l1l1ll111l_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack1l1l1ll111l_opy_:
                bstack1l1l1l1l11l_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1l1l1l1l11l_opy_):
                    self.logger.warning(bstack1ll1l11_opy_ (u"ࠧࡻ࡮ࡱࡣࡷࡧ࡭࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࠥᎄ") + str(method_name) + bstack1ll1l11_opy_ (u"ࠨࠢᎅ"))
                    continue
                bstack1ll1l111l11_opy_ = self.bstack1ll1l11l1l1_opy_(
                    method_name, previous_state=bstack11111l1lll_opy_.NONE
                )
                bstack1l1l1lll11l_opy_ = self.bstack1l1l1ll1111_opy_(
                    method_name,
                    (bstack1ll1l111l11_opy_ if bstack1ll1l111l11_opy_ else bstack11111l1lll_opy_.NONE),
                    bstack1l1l1l1l11l_opy_,
                )
                if not callable(bstack1l1l1lll11l_opy_):
                    self.logger.warning(bstack1ll1l11_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠠ࡯ࡱࡷࠤࡵࡧࡴࡤࡪࡨࡨ࠿ࠦࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࠨࡼࡵࡨࡰ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽ࠻ࠢࠥᎆ") + str(self.framework_version) + bstack1ll1l11_opy_ (u"ࠣࠫࠥᎇ"))
                    continue
                setattr(clazz, method_name, bstack1l1l1lll11l_opy_)
    def bstack1l1l1ll1111_opy_(
        self,
        method_name: str,
        bstack1ll1l111l11_opy_: bstack11111l1lll_opy_,
        bstack1l1l1l1l11l_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack1l1l1lllll_opy_ = datetime.now()
            (bstack1ll1l111l11_opy_,) = wrapped.__vars__
            bstack1ll1l111l11_opy_ = (
                bstack1ll1l111l11_opy_
                if bstack1ll1l111l11_opy_ and bstack1ll1l111l11_opy_ != bstack11111l1lll_opy_.NONE
                else self.bstack1ll1l11l1l1_opy_(method_name, previous_state=bstack1ll1l111l11_opy_, *args, **kwargs)
            )
            if bstack1ll1l111l11_opy_ == bstack11111l1lll_opy_.bstack1lll11llll1_opy_:
                ctx = bstack1l1lll1ll11_opy_.create_context(self.bstack1l1l1l1llll_opy_(target))
                if not self.bstack1l1l1ll1l1l_opy_() or ctx.id not in bstack1ll1l1l1111_opy_.bstack1lll111l111_opy_:
                    bstack1ll1l1l1111_opy_.bstack1lll111l111_opy_[ctx.id] = bstack1111l1lll1_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1ll1l111l11_opy_
                    )
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡺࡶࡦࡶࡰࡦࡦࠣࡱࡪࡺࡨࡰࡦࠣࡧࡷ࡫ࡡࡵࡧࡧ࠾ࠥࢁࡴࡢࡴࡪࡩࡹ࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡤࡶࡻࡁࢀࡩࡴࡹ࠰࡬ࡨࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥᎈ") + str(bstack1ll1l1l1111_opy_.bstack1lll111l111_opy_.keys()) + bstack1ll1l11_opy_ (u"ࠥࠦᎉ"))
            else:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡼࡸࡡࡱࡲࡨࡨࠥࡳࡥࡵࡪࡲࡨࠥ࡯࡮ࡷࡱ࡮ࡩࡩࡀࠠࡼࡶࡤࡶ࡬࡫ࡴ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᎊ") + str(bstack1ll1l1l1111_opy_.bstack1lll111l111_opy_.keys()) + bstack1ll1l11_opy_ (u"ࠧࠨᎋ"))
            instance = bstack1ll1l1l1111_opy_.bstack1ll11ll11l1_opy_(self.bstack1l1l1l1llll_opy_(target))
            if bstack1ll1l111l11_opy_ == bstack11111l1lll_opy_.NONE or not instance:
                ctx = bstack1l1lll1ll11_opy_.create_context(self.bstack1l1l1l1llll_opy_(target))
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠨࡷࡳࡣࡳࡴࡪࡪࠠ࡮ࡧࡷ࡬ࡴࡪࠠࡶࡰࡷࡶࡦࡩ࡫ࡦࡦ࠽ࠤࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡧࡹࡾ࠽ࡼࡥࡷࡼࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥᎌ") + str(bstack1ll1l1l1111_opy_.bstack1lll111l111_opy_.keys()) + bstack1ll1l11_opy_ (u"ࠢࠣᎍ"))
                return bstack1l1l1l1l11l_opy_(target, *args, **kwargs)
            bstack1l1l1l1lll1_opy_ = self.bstack1ll11llll1l_opy_(
                target,
                (instance, method_name),
                (bstack1ll1l111l11_opy_, bstack111111ll1l_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1lllllll1l1_opy_(bstack1ll1l111l11_opy_):
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡥࡥࠢࡶࡸࡦࡺࡥ࠮ࡶࡵࡥࡳࡹࡩࡵ࡫ࡲࡲ࠿ࠦࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡳࡶࡪࡼࡩࡰࡷࡶࡣࡸࡺࡡࡵࡧࢀࠤࡂࡄࠠࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡷࡹࡧࡴࡦࡿࠣࠬࢀࡺࡹࡱࡧࠫࡸࡦࡸࡧࡦࡶࠬࢁ࠳ࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥࢁࡡࡳࡩࡶࢁ࠮࡛ࠦࠣᎎ") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠤࡠࠦᎏ"))
            result = (
                bstack1l1l1l1lll1_opy_(target, bstack1l1l1l1l11l_opy_, *args, **kwargs)
                if callable(bstack1l1l1l1lll1_opy_)
                else bstack1l1l1l1l11l_opy_(target, *args, **kwargs)
            )
            bstack1l1l1lll111_opy_ = self.bstack1ll11llll1l_opy_(
                target,
                (instance, method_name),
                (bstack1ll1l111l11_opy_, bstack111111ll1l_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1ll11lll11l_opy_(instance, method_name, datetime.now() - bstack1l1l1lllll_opy_, *args, **kwargs)
            return bstack1l1l1lll111_opy_ if bstack1l1l1lll111_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1ll1l111l11_opy_,)
        return wrapped
    @staticmethod
    def bstack1ll11ll11l1_opy_(target: object, strict=True):
        ctx = bstack1l1lll1ll11_opy_.create_context(target)
        instance = bstack1ll1l1l1111_opy_.bstack1lll111l111_opy_.get(ctx.id, None)
        if instance and instance.bstack1l1ll1111l1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1111l1ll1l_opy_(
        ctx: bstack1lll11l1ll1_opy_, state: bstack11111l1lll_opy_, reverse=True
    ) -> List[bstack1111l1lll1_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1ll1l1l1111_opy_.bstack1lll111l111_opy_.values(),
            ),
            key=lambda t: t.bstack1l1ll111lll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llllll11l1_opy_(instance: bstack1111l1lll1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack11111l11l1_opy_(instance: bstack1111l1lll1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lllllll1l1_opy_(instance: bstack1111l1lll1_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1ll1l1l1111_opy_.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥࡱࡥࡺ࠿ࡾ࡯ࡪࡿࡽࠡࡸࡤࡰࡺ࡫࠽ࠣ᎐") + str(value) + bstack1ll1l11_opy_ (u"ࠦࠧ᎑"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1ll1l1l1111_opy_.bstack1ll11ll11l1_opy_(target, strict)
        return bstack1ll1l1l1111_opy_.bstack11111l11l1_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1ll1l1l1111_opy_.bstack1ll11ll11l1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1l1l1ll1l1l_opy_(self):
        return self.framework_name == bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩ᎒")
    def bstack1l1l1l1llll_opy_(self, target):
        return target if not self.bstack1l1l1ll1l1l_opy_() else self.bstack1l1l1ll11ll_opy_()
    @staticmethod
    def bstack1l1l1ll11ll_opy_():
        return str(os.getpid()) + str(threading.get_ident())