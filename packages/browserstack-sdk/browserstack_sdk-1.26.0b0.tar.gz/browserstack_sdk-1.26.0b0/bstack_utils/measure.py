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
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack11ll11llll_opy_ import get_logger
from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll111l1l_opy_
bstack1ll11l1lll_opy_ = bstack1llll111l1l_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1l1l1l11_opy_: Optional[str] = None):
    bstack11111ll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡄࡦࡥࡲࡶࡦࡺ࡯ࡳࠢࡷࡳࠥࡲ࡯ࡨࠢࡷ࡬ࡪࠦࡳࡵࡣࡵࡸࠥࡺࡩ࡮ࡧࠣࡳ࡫ࠦࡡࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࡥࡱࡵ࡮ࡨࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࠦ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡࡵࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠨࠢࠣᰛ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1ll1l1ll_opy_: str = bstack1ll11l1lll_opy_.bstack11lllll1l11_opy_(label)
            start_mark: str = label + bstack11111ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᰜ")
            end_mark: str = label + bstack11111ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᰝ")
            result = None
            try:
                if stage.value == STAGE.bstack11ll1ll111_opy_.value:
                    bstack1ll11l1lll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1ll11l1lll_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1l1l1l11_opy_)
                elif stage.value == STAGE.bstack1l11111ll1_opy_.value:
                    start_mark: str = bstack1ll1ll1l1ll_opy_ + bstack11111ll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᰞ")
                    end_mark: str = bstack1ll1ll1l1ll_opy_ + bstack11111ll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᰟ")
                    bstack1ll11l1lll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1ll11l1lll_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1l1l1l11_opy_)
            except Exception as e:
                bstack1ll11l1lll_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1l1l1l11_opy_)
            return result
        return wrapper
    return decorator