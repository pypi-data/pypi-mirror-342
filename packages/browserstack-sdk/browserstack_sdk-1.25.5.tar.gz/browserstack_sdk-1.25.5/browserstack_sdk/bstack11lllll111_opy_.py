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
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11lll1l1ll_opy_():
  def __init__(self, args, logger, bstack1111lllll1_opy_, bstack111l111ll1_opy_, bstack1111ll1l1l_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111lllll1_opy_ = bstack1111lllll1_opy_
    self.bstack111l111ll1_opy_ = bstack111l111ll1_opy_
    self.bstack1111ll1l1l_opy_ = bstack1111ll1l1l_opy_
  def bstack1l1llllll_opy_(self, bstack111l1111ll_opy_, bstack111l1l1l_opy_, bstack1111ll1l11_opy_=False):
    bstack1ll11ll1l1_opy_ = []
    manager = multiprocessing.Manager()
    bstack111l111111_opy_ = manager.list()
    bstack11lll1111_opy_ = Config.bstack11111l1l1_opy_()
    if bstack1111ll1l11_opy_:
      for index, platform in enumerate(self.bstack1111lllll1_opy_[bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪဆ")]):
        if index == 0:
          bstack111l1l1l_opy_[bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫဇ")] = self.args
        bstack1ll11ll1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack111l1111ll_opy_,
                                                    args=(bstack111l1l1l_opy_, bstack111l111111_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111lllll1_opy_[bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬဈ")]):
        bstack1ll11ll1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack111l1111ll_opy_,
                                                    args=(bstack111l1l1l_opy_, bstack111l111111_opy_)))
    i = 0
    for t in bstack1ll11ll1l1_opy_:
      try:
        if bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫဉ")):
          os.environ[bstack1ll1l11_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬည")] = json.dumps(self.bstack1111lllll1_opy_[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨဋ")][i % self.bstack1111ll1l1l_opy_])
      except Exception as e:
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡨࡸࡦ࡯࡬ࡴ࠼ࠣࡿࢂࠨဌ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1ll11ll1l1_opy_:
      t.join()
    return list(bstack111l111111_opy_)