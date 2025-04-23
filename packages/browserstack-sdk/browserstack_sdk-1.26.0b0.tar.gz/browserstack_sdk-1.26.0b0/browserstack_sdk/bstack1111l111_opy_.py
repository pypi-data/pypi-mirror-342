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
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1ll1l1ll_opy_():
  def __init__(self, args, logger, bstack1111lll1l1_opy_, bstack111l1111ll_opy_, bstack1111ll1ll1_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111lll1l1_opy_ = bstack1111lll1l1_opy_
    self.bstack111l1111ll_opy_ = bstack111l1111ll_opy_
    self.bstack1111ll1ll1_opy_ = bstack1111ll1ll1_opy_
  def bstack1llll1ll1_opy_(self, bstack1111llllll_opy_, bstack11ll111ll1_opy_, bstack1111ll1l1l_opy_=False):
    bstack1ll111l1l1_opy_ = []
    manager = multiprocessing.Manager()
    bstack111l1111l1_opy_ = manager.list()
    bstack11l1l1ll_opy_ = Config.bstack11l1ll1ll1_opy_()
    if bstack1111ll1l1l_opy_:
      for index, platform in enumerate(self.bstack1111lll1l1_opy_[bstack11111ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩစ")]):
        if index == 0:
          bstack11ll111ll1_opy_[bstack11111ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪဆ")] = self.args
        bstack1ll111l1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111llllll_opy_,
                                                    args=(bstack11ll111ll1_opy_, bstack111l1111l1_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111lll1l1_opy_[bstack11111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫဇ")]):
        bstack1ll111l1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111llllll_opy_,
                                                    args=(bstack11ll111ll1_opy_, bstack111l1111l1_opy_)))
    i = 0
    for t in bstack1ll111l1l1_opy_:
      try:
        if bstack11l1l1ll_opy_.get_property(bstack11111ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪဈ")):
          os.environ[bstack11111ll_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫဉ")] = json.dumps(self.bstack1111lll1l1_opy_[bstack11111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧည")][i % self.bstack1111ll1ll1_opy_])
      except Exception as e:
        self.logger.debug(bstack11111ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡾࢁࠧဋ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1ll111l1l1_opy_:
      t.join()
    return list(bstack111l1111l1_opy_)