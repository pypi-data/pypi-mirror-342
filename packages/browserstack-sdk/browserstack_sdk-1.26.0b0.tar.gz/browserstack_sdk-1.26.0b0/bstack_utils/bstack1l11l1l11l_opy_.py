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
import os
import json
from bstack_utils.bstack11ll11llll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11lll1ll11l_opy_(object):
  bstack11111l1l_opy_ = os.path.join(os.path.expanduser(bstack11111ll_opy_ (u"࠭ࡾࠨᘬ")), bstack11111ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᘭ"))
  bstack11lll1l1lll_opy_ = os.path.join(bstack11111l1l_opy_, bstack11111ll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨᘮ"))
  commands_to_wrap = None
  perform_scan = None
  bstack111lllll1_opy_ = None
  bstack1ll1ll1lll_opy_ = None
  bstack11llll1111l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11111ll_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫᘯ")):
      cls.instance = super(bstack11lll1ll11l_opy_, cls).__new__(cls)
      cls.instance.bstack11lll1ll111_opy_()
    return cls.instance
  def bstack11lll1ll111_opy_(self):
    try:
      with open(self.bstack11lll1l1lll_opy_, bstack11111ll_opy_ (u"ࠪࡶࠬᘰ")) as bstack11l1lll1_opy_:
        bstack11lll1ll1l1_opy_ = bstack11l1lll1_opy_.read()
        data = json.loads(bstack11lll1ll1l1_opy_)
        if bstack11111ll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᘱ") in data:
          self.bstack11lll1llll1_opy_(data[bstack11111ll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᘲ")])
        if bstack11111ll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᘳ") in data:
          self.bstack1l1111111l_opy_(data[bstack11111ll_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᘴ")])
    except:
      pass
  def bstack1l1111111l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11111ll_opy_ (u"ࠨࡵࡦࡥࡳ࠭ᘵ"),bstack11111ll_opy_ (u"ࠩࠪᘶ"))
      self.bstack111lllll1_opy_ = scripts.get(bstack11111ll_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧᘷ"),bstack11111ll_opy_ (u"ࠫࠬᘸ"))
      self.bstack1ll1ll1lll_opy_ = scripts.get(bstack11111ll_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩᘹ"),bstack11111ll_opy_ (u"࠭ࠧᘺ"))
      self.bstack11llll1111l_opy_ = scripts.get(bstack11111ll_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᘻ"),bstack11111ll_opy_ (u"ࠨࠩᘼ"))
  def bstack11lll1llll1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11lll1l1lll_opy_, bstack11111ll_opy_ (u"ࠩࡺࠫᘽ")) as file:
        json.dump({
          bstack11111ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࠧᘾ"): self.commands_to_wrap,
          bstack11111ll_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࡷࠧᘿ"): {
            bstack11111ll_opy_ (u"ࠧࡹࡣࡢࡰࠥᙀ"): self.perform_scan,
            bstack11111ll_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᙁ"): self.bstack111lllll1_opy_,
            bstack11111ll_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦᙂ"): self.bstack1ll1ll1lll_opy_,
            bstack11111ll_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨᙃ"): self.bstack11llll1111l_opy_
          }
        }, file)
    except Exception as e:
      logger.error(bstack11111ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠽ࠤࢀࢃࠢᙄ").format(e))
      pass
  def bstack1lll1ll1l_opy_(self, bstack1ll1ll1ll11_opy_):
    try:
      return any(command.get(bstack11111ll_opy_ (u"ࠪࡲࡦࡳࡥࠨᙅ")) == bstack1ll1ll1ll11_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack1l11l1l11l_opy_ = bstack11lll1ll11l_opy_()