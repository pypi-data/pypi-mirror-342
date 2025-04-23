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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.accessibility as bstack1l1111l1_opy_
from browserstack_sdk.bstack1ll1ll11ll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1111l1l1_opy_
class bstack11llll1l_opy_:
    def __init__(self, args, logger, bstack1111lll1l1_opy_, bstack111l1111ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111lll1l1_opy_ = bstack1111lll1l1_opy_
        self.bstack111l1111ll_opy_ = bstack111l1111ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l1llll1l_opy_ = []
        self.bstack111l111l1l_opy_ = None
        self.bstack1l1111111_opy_ = []
        self.bstack111l111111_opy_ = self.bstack1111ll1l_opy_()
        self.bstack1l1l11ll1_opy_ = -1
    def bstack11ll111ll1_opy_(self, bstack1111ll1lll_opy_):
        self.parse_args()
        self.bstack1111lll11l_opy_()
        self.bstack1111llll1l_opy_(bstack1111ll1lll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack111l111ll1_opy_():
        import importlib
        if getattr(importlib, bstack11111ll_opy_ (u"ࠩࡩ࡭ࡳࡪ࡟࡭ࡱࡤࡨࡪࡸࠧ࿥"), False):
            bstack111l11111l_opy_ = importlib.find_loader(bstack11111ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬ࿦"))
        else:
            bstack111l11111l_opy_ = importlib.util.find_spec(bstack11111ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭࿧"))
    def bstack111l11l111_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l1l11ll1_opy_ = -1
        if self.bstack111l1111ll_opy_ and bstack11111ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ࿨") in self.bstack1111lll1l1_opy_:
            self.bstack1l1l11ll1_opy_ = int(self.bstack1111lll1l1_opy_[bstack11111ll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭࿩")])
        try:
            bstack1111lll1ll_opy_ = [bstack11111ll_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩ࿪"), bstack11111ll_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫ࿫"), bstack11111ll_opy_ (u"ࠩ࠰ࡴࠬ࿬")]
            if self.bstack1l1l11ll1_opy_ >= 0:
                bstack1111lll1ll_opy_.extend([bstack11111ll_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ࿭"), bstack11111ll_opy_ (u"ࠫ࠲ࡴࠧ࿮")])
            for arg in bstack1111lll1ll_opy_:
                self.bstack111l11l111_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1111lll11l_opy_(self):
        bstack111l111l1l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack111l111l1l_opy_ = bstack111l111l1l_opy_
        return bstack111l111l1l_opy_
    def bstack1l11111111_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack111l111ll1_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1111l1l1_opy_)
    def bstack1111llll1l_opy_(self, bstack1111ll1lll_opy_):
        bstack11l1l1ll_opy_ = Config.bstack11l1ll1ll1_opy_()
        if bstack1111ll1lll_opy_:
            self.bstack111l111l1l_opy_.append(bstack11111ll_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ࿯"))
            self.bstack111l111l1l_opy_.append(bstack11111ll_opy_ (u"࠭ࡔࡳࡷࡨࠫ࿰"))
        if bstack11l1l1ll_opy_.bstack1111lllll1_opy_():
            self.bstack111l111l1l_opy_.append(bstack11111ll_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭࿱"))
            self.bstack111l111l1l_opy_.append(bstack11111ll_opy_ (u"ࠨࡖࡵࡹࡪ࠭࿲"))
        self.bstack111l111l1l_opy_.append(bstack11111ll_opy_ (u"ࠩ࠰ࡴࠬ࿳"))
        self.bstack111l111l1l_opy_.append(bstack11111ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨ࿴"))
        self.bstack111l111l1l_opy_.append(bstack11111ll_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭࿵"))
        self.bstack111l111l1l_opy_.append(bstack11111ll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ࿶"))
        if self.bstack1l1l11ll1_opy_ > 1:
            self.bstack111l111l1l_opy_.append(bstack11111ll_opy_ (u"࠭࠭࡯ࠩ࿷"))
            self.bstack111l111l1l_opy_.append(str(self.bstack1l1l11ll1_opy_))
    def bstack111l111l11_opy_(self):
        bstack1l1111111_opy_ = []
        for spec in self.bstack1l1llll1l_opy_:
            bstack1l111ll1ll_opy_ = [spec]
            bstack1l111ll1ll_opy_ += self.bstack111l111l1l_opy_
            bstack1l1111111_opy_.append(bstack1l111ll1ll_opy_)
        self.bstack1l1111111_opy_ = bstack1l1111111_opy_
        return bstack1l1111111_opy_
    def bstack1111ll1l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack111l111111_opy_ = True
            return True
        except Exception as e:
            self.bstack111l111111_opy_ = False
        return self.bstack111l111111_opy_
    def bstack1llll1ll1_opy_(self, bstack1111llllll_opy_, bstack11ll111ll1_opy_):
        bstack11ll111ll1_opy_[bstack11111ll_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ࿸")] = self.bstack1111lll1l1_opy_
        multiprocessing.set_start_method(bstack11111ll_opy_ (u"ࠨࡵࡳࡥࡼࡴࠧ࿹"))
        bstack1ll111l1l1_opy_ = []
        manager = multiprocessing.Manager()
        bstack111l1111l1_opy_ = manager.list()
        if bstack11111ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ࿺") in self.bstack1111lll1l1_opy_:
            for index, platform in enumerate(self.bstack1111lll1l1_opy_[bstack11111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭࿻")]):
                bstack1ll111l1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1111llllll_opy_,
                                                            args=(self.bstack111l111l1l_opy_, bstack11ll111ll1_opy_, bstack111l1111l1_opy_)))
            bstack1111lll111_opy_ = len(self.bstack1111lll1l1_opy_[bstack11111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ࿼")])
        else:
            bstack1ll111l1l1_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1111llllll_opy_,
                                                        args=(self.bstack111l111l1l_opy_, bstack11ll111ll1_opy_, bstack111l1111l1_opy_)))
            bstack1111lll111_opy_ = 1
        i = 0
        for t in bstack1ll111l1l1_opy_:
            os.environ[bstack11111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ࿽")] = str(i)
            if bstack11111ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ࿾") in self.bstack1111lll1l1_opy_:
                os.environ[bstack11111ll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ࿿")] = json.dumps(self.bstack1111lll1l1_opy_[bstack11111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫက")][i % bstack1111lll111_opy_])
            i += 1
            t.start()
        for t in bstack1ll111l1l1_opy_:
            t.join()
        return list(bstack111l1111l1_opy_)
    @staticmethod
    def bstack1ll1ll1l1l_opy_(driver, bstack111l111lll_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11111ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ခ"), None)
        if item and getattr(item, bstack11111ll_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࠬဂ"), None) and not getattr(item, bstack11111ll_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࡠࡦࡲࡲࡪ࠭ဃ"), False):
            logger.info(
                bstack11111ll_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠦင"))
            bstack1111llll11_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l1111l1_opy_.bstack11ll11l1l_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)