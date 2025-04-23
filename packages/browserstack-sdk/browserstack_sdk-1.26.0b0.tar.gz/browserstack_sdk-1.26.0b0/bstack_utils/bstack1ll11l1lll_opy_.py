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
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack11ll11llll_opy_ import get_logger
logger = get_logger(__name__)
bstack111ll11111l_opy_: Dict[str, float] = {}
bstack111l1llll11_opy_: List = []
bstack111l1lll11l_opy_ = 5
bstack111ll11l1_opy_ = os.path.join(os.getcwd(), bstack11111ll_opy_ (u"ࠬࡲ࡯ࡨࠩᳬ"), bstack11111ll_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯᳭ࠩ"))
logging.getLogger(bstack11111ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠩᳮ")).setLevel(logging.WARNING)
lock = FileLock(bstack111ll11l1_opy_+bstack11111ll_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢᳯ"))
class bstack111ll111111_opy_:
    duration: float
    name: str
    startTime: float
    worker: int
    status: bool
    failure: str
    details: Optional[str]
    entryType: str
    platform: Optional[int]
    command: Optional[str]
    hookType: Optional[str]
    cli: Optional[bool]
    def __init__(self, duration: float, name: str, start_time: float, bstack111l1llll1l_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111l1llll1l_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack11111ll_opy_ (u"ࠤࡰࡩࡦࡹࡵࡳࡧࠥᳰ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1llll111l1l_opy_:
    global bstack111ll11111l_opy_
    @staticmethod
    def bstack1ll1l111lll_opy_(key: str):
        bstack1ll1ll1l1ll_opy_ = bstack1llll111l1l_opy_.bstack11lllll1l11_opy_(key)
        bstack1llll111l1l_opy_.mark(bstack1ll1ll1l1ll_opy_+bstack11111ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᳱ"))
        return bstack1ll1ll1l1ll_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111ll11111l_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack11111ll_opy_ (u"ࠦࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᳲ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1llll111l1l_opy_.mark(end)
            bstack1llll111l1l_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack11111ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷ࠿ࠦࡻࡾࠤᳳ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111ll11111l_opy_ or end not in bstack111ll11111l_opy_:
                logger.debug(bstack11111ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࠠ࡬ࡧࡼࠤࡼ࡯ࡴࡩࠢࡹࡥࡱࡻࡥࠡࡽࢀࠤࡴࡸࠠࡦࡰࡧࠤࡰ࡫ࡹࠡࡹ࡬ࡸ࡭ࠦࡶࡢ࡮ࡸࡩࠥࢁࡽࠣ᳴").format(start,end))
                return
            duration: float = bstack111ll11111l_opy_[end] - bstack111ll11111l_opy_[start]
            bstack111l1lll111_opy_ = os.environ.get(bstack11111ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡉࡔࡡࡕ࡙ࡓࡔࡉࡏࡉࠥᳵ"), bstack11111ll_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢᳶ")).lower() == bstack11111ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᳷")
            bstack111l1lll1l1_opy_: bstack111ll111111_opy_ = bstack111ll111111_opy_(duration, label, bstack111ll11111l_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack11111ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥ᳸"), 0), command, test_name, hook_type, bstack111l1lll111_opy_)
            del bstack111ll11111l_opy_[start]
            del bstack111ll11111l_opy_[end]
            bstack1llll111l1l_opy_.bstack111l1lllll1_opy_(bstack111l1lll1l1_opy_)
        except Exception as e:
            logger.debug(bstack11111ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡩࡦࡹࡵࡳ࡫ࡱ࡫ࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢ᳹").format(e))
    @staticmethod
    def bstack111l1lllll1_opy_(bstack111l1lll1l1_opy_):
        os.makedirs(os.path.dirname(bstack111ll11l1_opy_)) if not os.path.exists(os.path.dirname(bstack111ll11l1_opy_)) else None
        bstack1llll111l1l_opy_.bstack111l1lll1ll_opy_()
        try:
            with lock:
                with open(bstack111ll11l1_opy_, bstack11111ll_opy_ (u"ࠧࡸࠫࠣᳺ"), encoding=bstack11111ll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧ᳻")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack111l1lll1l1_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111l1llllll_opy_:
            logger.debug(bstack11111ll_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠡࡽࢀࠦ᳼").format(bstack111l1llllll_opy_))
            with lock:
                with open(bstack111ll11l1_opy_, bstack11111ll_opy_ (u"ࠣࡹࠥ᳽"), encoding=bstack11111ll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ᳾")) as file:
                    data = [bstack111l1lll1l1_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack11111ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡥࡵࡶࡥ࡯ࡦࠣࡿࢂࠨ᳿").format(str(e)))
        finally:
            if os.path.exists(bstack111ll11l1_opy_+bstack11111ll_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥᴀ")):
                os.remove(bstack111ll11l1_opy_+bstack11111ll_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦᴁ"))
    @staticmethod
    def bstack111l1lll1ll_opy_():
        attempt = 0
        while (attempt < bstack111l1lll11l_opy_):
            attempt += 1
            if os.path.exists(bstack111ll11l1_opy_+bstack11111ll_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧᴂ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11lllll1l11_opy_(label: str) -> str:
        try:
            return bstack11111ll_opy_ (u"ࠢࡼࡿ࠽ࡿࢂࠨᴃ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack11111ll_opy_ (u"ࠣࡇࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᴄ").format(e))