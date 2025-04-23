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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.accessibility as bstack1ll1lll1l_opy_
from browserstack_sdk.bstack1lllll1ll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lllll11ll_opy_
class bstack1ll1l1l1l1_opy_:
    def __init__(self, args, logger, bstack1111lllll1_opy_, bstack111l111ll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111lllll1_opy_ = bstack1111lllll1_opy_
        self.bstack111l111ll1_opy_ = bstack111l111ll1_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11lll1l11l_opy_ = []
        self.bstack1111lll1ll_opy_ = None
        self.bstack1l11llll_opy_ = []
        self.bstack1111ll1lll_opy_ = self.bstack111l1lll1_opy_()
        self.bstack11l11l1ll_opy_ = -1
    def bstack111l1l1l_opy_(self, bstack1111llllll_opy_):
        self.parse_args()
        self.bstack1111llll11_opy_()
        self.bstack111l111l11_opy_(bstack1111llllll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack111l111lll_opy_():
        import importlib
        if getattr(importlib, bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡴࡤࡠ࡮ࡲࡥࡩ࡫ࡲࠨ࿦"), False):
            bstack111l11111l_opy_ = importlib.find_loader(bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭࿧"))
        else:
            bstack111l11111l_opy_ = importlib.util.find_spec(bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ࿨"))
    def bstack1111lll111_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11l11l1ll_opy_ = -1
        if self.bstack111l111ll1_opy_ and bstack1ll1l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭࿩") in self.bstack1111lllll1_opy_:
            self.bstack11l11l1ll_opy_ = int(self.bstack1111lllll1_opy_[bstack1ll1l11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ࿪")])
        try:
            bstack1111llll1l_opy_ = [bstack1ll1l11_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪ࿫"), bstack1ll1l11_opy_ (u"ࠩ࠰࠱ࡵࡲࡵࡨ࡫ࡱࡷࠬ࿬"), bstack1ll1l11_opy_ (u"ࠪ࠱ࡵ࠭࿭")]
            if self.bstack11l11l1ll_opy_ >= 0:
                bstack1111llll1l_opy_.extend([bstack1ll1l11_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ࿮"), bstack1ll1l11_opy_ (u"ࠬ࠳࡮ࠨ࿯")])
            for arg in bstack1111llll1l_opy_:
                self.bstack1111lll111_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1111llll11_opy_(self):
        bstack1111lll1ll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1111lll1ll_opy_ = bstack1111lll1ll_opy_
        return bstack1111lll1ll_opy_
    def bstack1l1ll1ll11_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack111l111lll_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1lllll11ll_opy_)
    def bstack111l111l11_opy_(self, bstack1111llllll_opy_):
        bstack11lll1111_opy_ = Config.bstack11111l1l1_opy_()
        if bstack1111llllll_opy_:
            self.bstack1111lll1ll_opy_.append(bstack1ll1l11_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ࿰"))
            self.bstack1111lll1ll_opy_.append(bstack1ll1l11_opy_ (u"ࠧࡕࡴࡸࡩࠬ࿱"))
        if bstack11lll1111_opy_.bstack1111lll11l_opy_():
            self.bstack1111lll1ll_opy_.append(bstack1ll1l11_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ࿲"))
            self.bstack1111lll1ll_opy_.append(bstack1ll1l11_opy_ (u"ࠩࡗࡶࡺ࡫ࠧ࿳"))
        self.bstack1111lll1ll_opy_.append(bstack1ll1l11_opy_ (u"ࠪ࠱ࡵ࠭࿴"))
        self.bstack1111lll1ll_opy_.append(bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠩ࿵"))
        self.bstack1111lll1ll_opy_.append(bstack1ll1l11_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧ࿶"))
        self.bstack1111lll1ll_opy_.append(bstack1ll1l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭࿷"))
        if self.bstack11l11l1ll_opy_ > 1:
            self.bstack1111lll1ll_opy_.append(bstack1ll1l11_opy_ (u"ࠧ࠮ࡰࠪ࿸"))
            self.bstack1111lll1ll_opy_.append(str(self.bstack11l11l1ll_opy_))
    def bstack1111ll1ll1_opy_(self):
        bstack1l11llll_opy_ = []
        for spec in self.bstack11lll1l11l_opy_:
            bstack11ll1l1ll1_opy_ = [spec]
            bstack11ll1l1ll1_opy_ += self.bstack1111lll1ll_opy_
            bstack1l11llll_opy_.append(bstack11ll1l1ll1_opy_)
        self.bstack1l11llll_opy_ = bstack1l11llll_opy_
        return bstack1l11llll_opy_
    def bstack111l1lll1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1111ll1lll_opy_ = True
            return True
        except Exception as e:
            self.bstack1111ll1lll_opy_ = False
        return self.bstack1111ll1lll_opy_
    def bstack1l1llllll_opy_(self, bstack111l1111ll_opy_, bstack111l1l1l_opy_):
        bstack111l1l1l_opy_[bstack1ll1l11_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ࿹")] = self.bstack1111lllll1_opy_
        multiprocessing.set_start_method(bstack1ll1l11_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨ࿺"))
        bstack1ll11ll1l1_opy_ = []
        manager = multiprocessing.Manager()
        bstack111l111111_opy_ = manager.list()
        if bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭࿻") in self.bstack1111lllll1_opy_:
            for index, platform in enumerate(self.bstack1111lllll1_opy_[bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ࿼")]):
                bstack1ll11ll1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack111l1111ll_opy_,
                                                            args=(self.bstack1111lll1ll_opy_, bstack111l1l1l_opy_, bstack111l111111_opy_)))
            bstack111l1111l1_opy_ = len(self.bstack1111lllll1_opy_[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࿽")])
        else:
            bstack1ll11ll1l1_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack111l1111ll_opy_,
                                                        args=(self.bstack1111lll1ll_opy_, bstack111l1l1l_opy_, bstack111l111111_opy_)))
            bstack111l1111l1_opy_ = 1
        i = 0
        for t in bstack1ll11ll1l1_opy_:
            os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭࿾")] = str(i)
            if bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ࿿") in self.bstack1111lllll1_opy_:
                os.environ[bstack1ll1l11_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩက")] = json.dumps(self.bstack1111lllll1_opy_[bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬခ")][i % bstack111l1111l1_opy_])
            i += 1
            t.start()
        for t in bstack1ll11ll1l1_opy_:
            t.join()
        return list(bstack111l111111_opy_)
    @staticmethod
    def bstack11ll1111l1_opy_(driver, bstack1111lll1l1_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧဂ"), None)
        if item and getattr(item, bstack1ll1l11_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪ࠭ဃ"), None) and not getattr(item, bstack1ll1l11_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࡡࡧࡳࡳ࡫ࠧင"), False):
            logger.info(
                bstack1ll1l11_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠧစ"))
            bstack111l111l1l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1ll1lll1l_opy_.bstack11111lll_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)