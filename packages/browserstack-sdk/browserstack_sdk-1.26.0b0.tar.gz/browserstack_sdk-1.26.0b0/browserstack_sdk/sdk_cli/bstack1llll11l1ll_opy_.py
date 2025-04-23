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
import abc
from browserstack_sdk.sdk_cli.bstack1111l1ll11_opy_ import bstack1111l1l1ll_opy_
class bstack1lllllll11l_opy_(abc.ABC):
    bin_session_id: str
    bstack1111l1ll11_opy_: bstack1111l1l1ll_opy_
    def __init__(self):
        self.bstack1llll1l1111_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111l1ll11_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1llll11ll1l_opy_(self):
        return (self.bstack1llll1l1111_opy_ != None and self.bin_session_id != None and self.bstack1111l1ll11_opy_ != None)
    def configure(self, bstack1llll1l1111_opy_, config, bin_session_id: str, bstack1111l1ll11_opy_: bstack1111l1l1ll_opy_):
        self.bstack1llll1l1111_opy_ = bstack1llll1l1111_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111l1ll11_opy_ = bstack1111l1ll11_opy_
        if self.bin_session_id:
            self.logger.debug(bstack11111ll_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࡧࠤࡲࡵࡤࡶ࡮ࡨࠤࢀࡹࡥ࡭ࡨ࠱ࡣࡤࡩ࡬ࡢࡵࡶࡣࡤ࠴࡟ࡠࡰࡤࡱࡪࡥ࡟ࡾ࠼ࠣࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡁࠧᆝ") + str(self.bin_session_id) + bstack11111ll_opy_ (u"ࠤࠥᆞ"))
    def bstack1ll1l1l1lll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11111ll_opy_ (u"ࠥࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠤࡨࡧ࡮࡯ࡱࡷࠤࡧ࡫ࠠࡏࡱࡱࡩࠧᆟ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False