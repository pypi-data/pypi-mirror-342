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
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1ll1lllll_opy_ import get_logger
from bstack_utils.bstack1ll11l1lll_opy_ import bstack111111lll1_opy_
bstack1ll11l1lll_opy_ = bstack111111lll1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1l1ll111l1_opy_: Optional[str] = None):
    bstack1ll1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡉ࡫ࡣࡰࡴࡤࡸࡴࡸࠠࡵࡱࠣࡰࡴ࡭ࠠࡵࡪࡨࠤࡸࡺࡡࡳࡶࠣࡸ࡮ࡳࡥࠡࡱࡩࠤࡦࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠎࠥࠦࠠࠡࡣ࡯ࡳࡳ࡭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࠤࡳࡧ࡭ࡦࠢࡤࡲࡩࠦࡳࡵࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࠦࠧࠨᰙ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack11111l11ll_opy_: str = bstack1ll11l1lll_opy_.bstack11llllll111_opy_(label)
            start_mark: str = label + bstack1ll1l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᰚ")
            end_mark: str = label + bstack1ll1l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᰛ")
            result = None
            try:
                if stage.value == STAGE.bstack1l11l1l1ll_opy_.value:
                    bstack1ll11l1lll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1ll11l1lll_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1l1ll111l1_opy_)
                elif stage.value == STAGE.bstack1l11lll1l_opy_.value:
                    start_mark: str = bstack11111l11ll_opy_ + bstack1ll1l11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᰜ")
                    end_mark: str = bstack11111l11ll_opy_ + bstack1ll1l11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᰝ")
                    bstack1ll11l1lll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1ll11l1lll_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1l1ll111l1_opy_)
            except Exception as e:
                bstack1ll11l1lll_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1l1ll111l1_opy_)
            return result
        return wrapper
    return decorator