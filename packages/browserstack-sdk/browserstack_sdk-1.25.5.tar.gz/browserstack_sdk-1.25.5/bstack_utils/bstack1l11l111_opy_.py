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
import os
import json
from bstack_utils.bstack1ll1lllll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11lll1ll11l_opy_(object):
  bstack11l11lll11_opy_ = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"࠭ࡾࠨᘬ")), bstack1ll1l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᘭ"))
  bstack11lll1ll111_opy_ = os.path.join(bstack11l11lll11_opy_, bstack1ll1l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨᘮ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1l1ll1llll_opy_ = None
  bstack1l11l1ll_opy_ = None
  bstack11llll1l111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1ll1l11_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫᘯ")):
      cls.instance = super(bstack11lll1ll11l_opy_, cls).__new__(cls)
      cls.instance.bstack11lll1l1lll_opy_()
    return cls.instance
  def bstack11lll1l1lll_opy_(self):
    try:
      with open(self.bstack11lll1ll111_opy_, bstack1ll1l11_opy_ (u"ࠪࡶࠬᘰ")) as bstack11ll1ll1_opy_:
        bstack11lll1l1ll1_opy_ = bstack11ll1ll1_opy_.read()
        data = json.loads(bstack11lll1l1ll1_opy_)
        if bstack1ll1l11_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᘱ") in data:
          self.bstack11llll111l1_opy_(data[bstack1ll1l11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᘲ")])
        if bstack1ll1l11_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᘳ") in data:
          self.bstack1l1l11ll_opy_(data[bstack1ll1l11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᘴ")])
    except:
      pass
  def bstack1l1l11ll_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1ll1l11_opy_ (u"ࠨࡵࡦࡥࡳ࠭ᘵ"),bstack1ll1l11_opy_ (u"ࠩࠪᘶ"))
      self.bstack1l1ll1llll_opy_ = scripts.get(bstack1ll1l11_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧᘷ"),bstack1ll1l11_opy_ (u"ࠫࠬᘸ"))
      self.bstack1l11l1ll_opy_ = scripts.get(bstack1ll1l11_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩᘹ"),bstack1ll1l11_opy_ (u"࠭ࠧᘺ"))
      self.bstack11llll1l111_opy_ = scripts.get(bstack1ll1l11_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᘻ"),bstack1ll1l11_opy_ (u"ࠨࠩᘼ"))
  def bstack11llll111l1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11lll1ll111_opy_, bstack1ll1l11_opy_ (u"ࠩࡺࠫᘽ")) as file:
        json.dump({
          bstack1ll1l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࠧᘾ"): self.commands_to_wrap,
          bstack1ll1l11_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࡷࠧᘿ"): {
            bstack1ll1l11_opy_ (u"ࠧࡹࡣࡢࡰࠥᙀ"): self.perform_scan,
            bstack1ll1l11_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᙁ"): self.bstack1l1ll1llll_opy_,
            bstack1ll1l11_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦᙂ"): self.bstack1l11l1ll_opy_,
            bstack1ll1l11_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨᙃ"): self.bstack11llll1l111_opy_
          }
        }, file)
    except Exception as e:
      logger.error(bstack1ll1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠽ࠤࢀࢃࠢᙄ").format(e))
      pass
  def bstack1l1l11ll1l_opy_(self, bstack1l1ll11l11l_opy_):
    try:
      return any(command.get(bstack1ll1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨᙅ")) == bstack1l1ll11l11l_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack1l11l111_opy_ = bstack11lll1ll11l_opy_()