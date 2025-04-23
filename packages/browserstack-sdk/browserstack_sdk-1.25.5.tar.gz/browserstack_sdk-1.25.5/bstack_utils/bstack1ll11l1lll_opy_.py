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
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1ll1lllll_opy_ import get_logger
logger = get_logger(__name__)
bstack111l1lll1ll_opy_: Dict[str, float] = {}
bstack111l1lll11l_opy_: List = []
bstack111l1lll111_opy_ = 5
bstack1l111l111_opy_ = os.path.join(os.getcwd(), bstack1ll1l11_opy_ (u"ࠪࡰࡴ࡭ࠧᳪ"), bstack1ll1l11_opy_ (u"ࠫࡰ࡫ࡹ࠮࡯ࡨࡸࡷ࡯ࡣࡴ࠰࡭ࡷࡴࡴࠧᳫ"))
logging.getLogger(bstack1ll1l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠧᳬ")).setLevel(logging.WARNING)
lock = FileLock(bstack1l111l111_opy_+bstack1ll1l11_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯᳭ࠧ"))
class bstack111l1llll1l_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack111ll11111l_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111ll11111l_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1ll1l11_opy_ (u"ࠢ࡮ࡧࡤࡷࡺࡸࡥࠣᳮ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack111111lll1_opy_:
    global bstack111l1lll1ll_opy_
    @staticmethod
    def bstack11111l1111_opy_(key: str):
        bstack11111l11ll_opy_ = bstack111111lll1_opy_.bstack11llllll111_opy_(key)
        bstack111111lll1_opy_.mark(bstack11111l11ll_opy_+bstack1ll1l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᳯ"))
        return bstack11111l11ll_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111l1lll1ll_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᳰ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack111111lll1_opy_.mark(end)
            bstack111111lll1_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢᳱ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111l1lll1ll_opy_ or end not in bstack111l1lll1ll_opy_:
                logger.debug(bstack1ll1l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥࡱࡥࡺࠢࡺ࡭ࡹ࡮ࠠࡷࡣ࡯ࡹࡪࠦࡻࡾࠢࡲࡶࠥ࡫࡮ࡥࠢ࡮ࡩࡾࠦࡷࡪࡶ࡫ࠤࡻࡧ࡬ࡶࡧࠣࡿࢂࠨᳲ").format(start,end))
                return
            duration: float = bstack111l1lll1ll_opy_[end] - bstack111l1lll1ll_opy_[start]
            bstack111l1lll1l1_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣࡎ࡙࡟ࡓࡗࡑࡒࡎࡔࡇࠣᳳ"), bstack1ll1l11_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧ᳴")).lower() == bstack1ll1l11_opy_ (u"ࠢࡵࡴࡸࡩࠧᳵ")
            bstack111ll111111_opy_: bstack111l1llll1l_opy_ = bstack111l1llll1l_opy_(duration, label, bstack111l1lll1ll_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1ll1l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᳶ"), 0), command, test_name, hook_type, bstack111l1lll1l1_opy_)
            del bstack111l1lll1ll_opy_[start]
            del bstack111l1lll1ll_opy_[end]
            bstack111111lll1_opy_.bstack111l1lllll1_opy_(bstack111ll111111_opy_)
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡧࡤࡷࡺࡸࡩ࡯ࡩࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳ࠻ࠢࡾࢁࠧ᳷").format(e))
    @staticmethod
    def bstack111l1lllll1_opy_(bstack111ll111111_opy_):
        os.makedirs(os.path.dirname(bstack1l111l111_opy_)) if not os.path.exists(os.path.dirname(bstack1l111l111_opy_)) else None
        bstack111111lll1_opy_.bstack111l1llllll_opy_()
        try:
            with lock:
                with open(bstack1l111l111_opy_, bstack1ll1l11_opy_ (u"ࠥࡶ࠰ࠨ᳸"), encoding=bstack1ll1l11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ᳹")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack111ll111111_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111l1llll11_opy_:
            logger.debug(bstack1ll1l11_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠦࡻࡾࠤᳺ").format(bstack111l1llll11_opy_))
            with lock:
                with open(bstack1l111l111_opy_, bstack1ll1l11_opy_ (u"ࠨࡷࠣ᳻"), encoding=bstack1ll1l11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ᳼")) as file:
                    data = [bstack111ll111111_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡣࡳࡴࡪࡴࡤࠡࡽࢀࠦ᳽").format(str(e)))
        finally:
            if os.path.exists(bstack1l111l111_opy_+bstack1ll1l11_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣ᳾")):
                os.remove(bstack1l111l111_opy_+bstack1ll1l11_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤ᳿"))
    @staticmethod
    def bstack111l1llllll_opy_():
        attempt = 0
        while (attempt < bstack111l1lll111_opy_):
            attempt += 1
            if os.path.exists(bstack1l111l111_opy_+bstack1ll1l11_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥᴀ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11llllll111_opy_(label: str) -> str:
        try:
            return bstack1ll1l11_opy_ (u"ࠧࢁࡽ࠻ࡽࢀࠦᴁ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠨࡅࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᴂ").format(e))