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
import abc
from browserstack_sdk.sdk_cli.bstack1llll11l111_opy_ import bstack1ll111ll1ll_opy_
class bstack11111lllll_opy_(abc.ABC):
    bin_session_id: str
    bstack1llll11l111_opy_: bstack1ll111ll1ll_opy_
    def __init__(self):
        self.bstack1llll111lll_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1llll11l111_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1l1l11ll1ll_opy_(self):
        return (self.bstack1llll111lll_opy_ != None and self.bin_session_id != None and self.bstack1llll11l111_opy_ != None)
    def configure(self, bstack1llll111lll_opy_, config, bin_session_id: str, bstack1llll11l111_opy_: bstack1ll111ll1ll_opy_):
        self.bstack1llll111lll_opy_ = bstack1llll111lll_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1llll11l111_opy_ = bstack1llll11l111_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࡩࠦ࡭ࡰࡦࡸࡰࡪࠦࡻࡴࡧ࡯ࡪ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟࠯ࡡࡢࡲࡦࡳࡥࡠࡡࢀ࠾ࠥࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡃࠢᔊ") + str(self.bin_session_id) + bstack1ll1l11_opy_ (u"ࠦࠧᔋ"))
    def bstack1lll1lll1ll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1ll1l11_opy_ (u"ࠧࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦࡣࡢࡰࡱࡳࡹࠦࡢࡦࠢࡑࡳࡳ࡫ࠢᔌ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False