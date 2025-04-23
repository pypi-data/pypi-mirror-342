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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l11l1l1ll_opy_, bstack1l1lllll1l_opy_
from bstack_utils.measure import measure
class bstack1l111l1l11_opy_:
  working_dir = os.getcwd()
  bstack11ll1l11_opy_ = False
  config = {}
  bstack11l1lllllll_opy_ = bstack11111ll_opy_ (u"࠭ࠧᱨ")
  binary_path = bstack11111ll_opy_ (u"ࠧࠨᱩ")
  bstack111llll11l1_opy_ = bstack11111ll_opy_ (u"ࠨࠩᱪ")
  bstack11llll11l1_opy_ = False
  bstack111llll1l1l_opy_ = None
  bstack111llllllll_opy_ = {}
  bstack111ll1l1l1l_opy_ = 300
  bstack111llllll11_opy_ = False
  logger = None
  bstack11l11111ll1_opy_ = False
  bstack1ll11lllll_opy_ = False
  percy_build_id = None
  bstack111ll1l1111_opy_ = bstack11111ll_opy_ (u"ࠩࠪᱫ")
  bstack11l1111lll1_opy_ = {
    bstack11111ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᱬ") : 1,
    bstack11111ll_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬᱭ") : 2,
    bstack11111ll_opy_ (u"ࠬ࡫ࡤࡨࡧࠪᱮ") : 3,
    bstack11111ll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ᱯ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111ll1lll11_opy_(self):
    bstack111llll11ll_opy_ = bstack11111ll_opy_ (u"ࠧࠨᱰ")
    bstack111lll11111_opy_ = sys.platform
    bstack111ll11llll_opy_ = bstack11111ll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᱱ")
    if re.match(bstack11111ll_opy_ (u"ࠤࡧࡥࡷࡽࡩ࡯ࡾࡰࡥࡨࠦ࡯ࡴࠤᱲ"), bstack111lll11111_opy_) != None:
      bstack111llll11ll_opy_ = bstack11ll1ll1l1l_opy_ + bstack11111ll_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡳࡸࡾ࠮ࡻ࡫ࡳࠦᱳ")
      self.bstack111ll1l1111_opy_ = bstack11111ll_opy_ (u"ࠫࡲࡧࡣࠨᱴ")
    elif re.match(bstack11111ll_opy_ (u"ࠧࡳࡳࡸ࡫ࡱࢀࡲࡹࡹࡴࡾࡰ࡭ࡳ࡭ࡷࡽࡥࡼ࡫ࡼ࡯࡮ࡽࡤࡦࡧࡼ࡯࡮ࡽࡹ࡬ࡲࡨ࡫ࡼࡦ࡯ࡦࢀࡼ࡯࡮࠴࠴ࠥᱵ"), bstack111lll11111_opy_) != None:
      bstack111llll11ll_opy_ = bstack11ll1ll1l1l_opy_ + bstack11111ll_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳ࡷࡪࡰ࠱ࡾ࡮ࡶࠢᱶ")
      bstack111ll11llll_opy_ = bstack11111ll_opy_ (u"ࠢࡱࡧࡵࡧࡾ࠴ࡥࡹࡧࠥᱷ")
      self.bstack111ll1l1111_opy_ = bstack11111ll_opy_ (u"ࠨࡹ࡬ࡲࠬᱸ")
    else:
      bstack111llll11ll_opy_ = bstack11ll1ll1l1l_opy_ + bstack11111ll_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯࡯࡭ࡳࡻࡸ࠯ࡼ࡬ࡴࠧᱹ")
      self.bstack111ll1l1111_opy_ = bstack11111ll_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩᱺ")
    return bstack111llll11ll_opy_, bstack111ll11llll_opy_
  def bstack111lll1ll11_opy_(self):
    try:
      bstack111ll1l1lll_opy_ = [os.path.join(expanduser(bstack11111ll_opy_ (u"ࠦࢃࠨᱻ")), bstack11111ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᱼ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111ll1l1lll_opy_:
        if(self.bstack11l1111ll1l_opy_(path)):
          return path
      raise bstack11111ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᱽ")
    except Exception as e:
      self.logger.error(bstack11111ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࠲ࠦࡻࡾࠤ᱾").format(e))
  def bstack11l1111ll1l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111ll1lll1l_opy_(self, bstack111lll1lll1_opy_):
    return os.path.join(bstack111lll1lll1_opy_, self.bstack11l1lllllll_opy_ + bstack11111ll_opy_ (u"ࠣ࠰ࡨࡸࡦ࡭ࠢ᱿"))
  def bstack11l11111l11_opy_(self, bstack111lll1lll1_opy_, bstack111ll1ll1ll_opy_):
    if not bstack111ll1ll1ll_opy_: return
    try:
      bstack111lll1llll_opy_ = self.bstack111ll1lll1l_opy_(bstack111lll1lll1_opy_)
      with open(bstack111lll1llll_opy_, bstack11111ll_opy_ (u"ࠤࡺࠦᲀ")) as f:
        f.write(bstack111ll1ll1ll_opy_)
        self.logger.debug(bstack11111ll_opy_ (u"ࠥࡗࡦࡼࡥࡥࠢࡱࡩࡼࠦࡅࡕࡣࡪࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠢᲁ"))
    except Exception as e:
      self.logger.error(bstack11111ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡣࡹࡩࠥࡺࡨࡦࠢࡨࡸࡦ࡭ࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᲂ").format(e))
  def bstack111llllll1l_opy_(self, bstack111lll1lll1_opy_):
    try:
      bstack111lll1llll_opy_ = self.bstack111ll1lll1l_opy_(bstack111lll1lll1_opy_)
      if os.path.exists(bstack111lll1llll_opy_):
        with open(bstack111lll1llll_opy_, bstack11111ll_opy_ (u"ࠧࡸࠢᲃ")) as f:
          bstack111ll1ll1ll_opy_ = f.read().strip()
          return bstack111ll1ll1ll_opy_ if bstack111ll1ll1ll_opy_ else None
    except Exception as e:
      self.logger.error(bstack11111ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡆࡖࡤ࡫࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᲄ").format(e))
  def bstack11l111111ll_opy_(self, bstack111lll1lll1_opy_, bstack111llll11ll_opy_):
    bstack111ll1l111l_opy_ = self.bstack111llllll1l_opy_(bstack111lll1lll1_opy_)
    if bstack111ll1l111l_opy_:
      try:
        bstack111lllll1ll_opy_ = self.bstack11l1111l11l_opy_(bstack111ll1l111l_opy_, bstack111llll11ll_opy_)
        if not bstack111lllll1ll_opy_:
          self.logger.debug(bstack11111ll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡩࡴࠢࡸࡴࠥࡺ࡯ࠡࡦࡤࡸࡪࠦࠨࡆࡖࡤ࡫ࠥࡻ࡮ࡤࡪࡤࡲ࡬࡫ࡤࠪࠤᲅ"))
          return True
        self.logger.debug(bstack11111ll_opy_ (u"ࠣࡐࡨࡻࠥࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡶࡲࡧࡥࡹ࡫ࠢᲆ"))
        return False
      except Exception as e:
        self.logger.warn(bstack11111ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡵࡲࠡࡤ࡬ࡲࡦࡸࡹࠡࡷࡳࡨࡦࡺࡥࡴ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣᲇ").format(e))
    return False
  def bstack11l1111l11l_opy_(self, bstack111ll1l111l_opy_, bstack111llll11ll_opy_):
    try:
      headers = {
        bstack11111ll_opy_ (u"ࠥࡍ࡫࠳ࡎࡰࡰࡨ࠱ࡒࡧࡴࡤࡪࠥᲈ"): bstack111ll1l111l_opy_
      }
      response = bstack1l1lllll1l_opy_(bstack11111ll_opy_ (u"ࠫࡌࡋࡔࠨᲉ"), bstack111llll11ll_opy_, {}, {bstack11111ll_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨᲊ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack11111ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡹࡵࡪࡡࡵࡧࡶ࠾ࠥࢁࡽࠣ᲋").format(e))
  @measure(event_name=EVENTS.bstack11ll1l111ll_opy_, stage=STAGE.bstack1l11111ll1_opy_)
  def bstack111ll1lllll_opy_(self, bstack111llll11ll_opy_, bstack111ll11llll_opy_):
    try:
      bstack111llll111l_opy_ = self.bstack111lll1ll11_opy_()
      bstack111ll1ll11l_opy_ = os.path.join(bstack111llll111l_opy_, bstack11111ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴ࡺࡪࡲࠪ᲌"))
      bstack11l1111l1ll_opy_ = os.path.join(bstack111llll111l_opy_, bstack111ll11llll_opy_)
      if self.bstack11l111111ll_opy_(bstack111llll111l_opy_, bstack111llll11ll_opy_):
        if os.path.exists(bstack11l1111l1ll_opy_):
          self.logger.info(bstack11111ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥ᲍").format(bstack11l1111l1ll_opy_))
          return bstack11l1111l1ll_opy_
        if os.path.exists(bstack111ll1ll11l_opy_):
          self.logger.info(bstack11111ll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡼ࡬ࡴࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡺࡴࡺࡪࡲࡳ࡭ࡳ࡭ࠢ᲎").format(bstack111ll1ll11l_opy_))
          return self.bstack111lll111l1_opy_(bstack111ll1ll11l_opy_, bstack111ll11llll_opy_)
      self.logger.info(bstack11111ll_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱࠥࢁࡽࠣ᲏").format(bstack111llll11ll_opy_))
      response = bstack1l1lllll1l_opy_(bstack11111ll_opy_ (u"ࠫࡌࡋࡔࠨᲐ"), bstack111llll11ll_opy_, {}, {})
      if response.status_code == 200:
        bstack111lllllll1_opy_ = response.headers.get(bstack11111ll_opy_ (u"ࠧࡋࡔࡢࡩࠥᲑ"), bstack11111ll_opy_ (u"ࠨࠢᲒ"))
        if bstack111lllllll1_opy_:
          self.bstack11l11111l11_opy_(bstack111llll111l_opy_, bstack111lllllll1_opy_)
        with open(bstack111ll1ll11l_opy_, bstack11111ll_opy_ (u"ࠧࡸࡤࠪᲓ")) as file:
          file.write(response.content)
        self.logger.info(bstack11111ll_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࢂࠨᲔ").format(bstack111ll1ll11l_opy_))
        return self.bstack111lll111l1_opy_(bstack111ll1ll11l_opy_, bstack111ll11llll_opy_)
      else:
        raise(bstack11111ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࢁࠧᲕ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11111ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦᲖ").format(e))
  def bstack11l11111lll_opy_(self, bstack111llll11ll_opy_, bstack111ll11llll_opy_):
    try:
      retry = 2
      bstack11l1111l1ll_opy_ = None
      bstack111lllll1l1_opy_ = False
      while retry > 0:
        bstack11l1111l1ll_opy_ = self.bstack111ll1lllll_opy_(bstack111llll11ll_opy_, bstack111ll11llll_opy_)
        bstack111lllll1l1_opy_ = self.bstack111lll1l111_opy_(bstack111llll11ll_opy_, bstack111ll11llll_opy_, bstack11l1111l1ll_opy_)
        if bstack111lllll1l1_opy_:
          break
        retry -= 1
      return bstack11l1111l1ll_opy_, bstack111lllll1l1_opy_
    except Exception as e:
      self.logger.error(bstack11111ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣᲗ").format(e))
    return bstack11l1111l1ll_opy_, False
  def bstack111lll1l111_opy_(self, bstack111llll11ll_opy_, bstack111ll11llll_opy_, bstack11l1111l1ll_opy_, bstack111lll1111l_opy_ = 0):
    if bstack111lll1111l_opy_ > 1:
      return False
    if bstack11l1111l1ll_opy_ == None or os.path.exists(bstack11l1111l1ll_opy_) == False:
      self.logger.warn(bstack11111ll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᲘ"))
      return False
    bstack111lllll11l_opy_ = bstack11111ll_opy_ (u"ࠨ࡞࠯ࠬࡃࡴࡪࡸࡣࡺ࡞࠲ࡧࡱ࡯ࠠ࡝ࡦ࠱ࡠࡩ࠱࠮࡝ࡦ࠮ࠦᲙ")
    command = bstack11111ll_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭Ლ").format(bstack11l1111l1ll_opy_)
    bstack11l11111111_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111lllll11l_opy_, bstack11l11111111_opy_) != None:
      return True
    else:
      self.logger.error(bstack11111ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢᲛ"))
      return False
  def bstack111lll111l1_opy_(self, bstack111ll1ll11l_opy_, bstack111ll11llll_opy_):
    try:
      working_dir = os.path.dirname(bstack111ll1ll11l_opy_)
      shutil.unpack_archive(bstack111ll1ll11l_opy_, working_dir)
      bstack11l1111l1ll_opy_ = os.path.join(working_dir, bstack111ll11llll_opy_)
      os.chmod(bstack11l1111l1ll_opy_, 0o755)
      return bstack11l1111l1ll_opy_
    except Exception as e:
      self.logger.error(bstack11111ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᲜ"))
  def bstack11l1111l1l1_opy_(self):
    try:
      bstack111ll1l1ll1_opy_ = self.config.get(bstack11111ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᲝ"))
      bstack11l1111l1l1_opy_ = bstack111ll1l1ll1_opy_ or (bstack111ll1l1ll1_opy_ is None and self.bstack11ll1l11_opy_)
      if not bstack11l1111l1l1_opy_ or self.config.get(bstack11111ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᲞ"), None) not in bstack11ll1l1llll_opy_:
        return False
      self.bstack11llll11l1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11111ll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᲟ").format(e))
  def bstack111lll1l11l_opy_(self):
    try:
      bstack111lll1l11l_opy_ = self.percy_capture_mode
      return bstack111lll1l11l_opy_
    except Exception as e:
      self.logger.error(bstack11111ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹࠡࡥࡤࡴࡹࡻࡲࡦࠢࡰࡳࡩ࡫ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᲠ").format(e))
  def init(self, bstack11ll1l11_opy_, config, logger):
    self.bstack11ll1l11_opy_ = bstack11ll1l11_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11l1111l1l1_opy_():
      return
    self.bstack111llllllll_opy_ = config.get(bstack11111ll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭Ს"), {})
    self.percy_capture_mode = config.get(bstack11111ll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᲢ"))
    try:
      bstack111llll11ll_opy_, bstack111ll11llll_opy_ = self.bstack111ll1lll11_opy_()
      self.bstack11l1lllllll_opy_ = bstack111ll11llll_opy_
      bstack11l1111l1ll_opy_, bstack111lllll1l1_opy_ = self.bstack11l11111lll_opy_(bstack111llll11ll_opy_, bstack111ll11llll_opy_)
      if bstack111lllll1l1_opy_:
        self.binary_path = bstack11l1111l1ll_opy_
        thread = Thread(target=self.bstack111lll11l1l_opy_)
        thread.start()
      else:
        self.bstack11l11111ll1_opy_ = True
        self.logger.error(bstack11111ll_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ࠰࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡑࡧࡵࡧࡾࠨᲣ").format(bstack11l1111l1ll_opy_))
    except Exception as e:
      self.logger.error(bstack11111ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᲤ").format(e))
  def bstack111llll1l11_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11111ll_opy_ (u"ࠫࡱࡵࡧࠨᲥ"), bstack11111ll_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡱࡵࡧࠨᲦ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11111ll_opy_ (u"ࠨࡐࡶࡵ࡫࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࡶࠤࡦࡺࠠࡼࡿࠥᲧ").format(logfile))
      self.bstack111llll11l1_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11111ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࠣࡴࡦࡺࡨ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᲨ").format(e))
  @measure(event_name=EVENTS.bstack11ll11lllll_opy_, stage=STAGE.bstack1l11111ll1_opy_)
  def bstack111lll11l1l_opy_(self):
    bstack111llll1lll_opy_ = self.bstack11l1111ll11_opy_()
    if bstack111llll1lll_opy_ == None:
      self.bstack11l11111ll1_opy_ = True
      self.logger.error(bstack11111ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠦᲩ"))
      return False
    command_args = [bstack11111ll_opy_ (u"ࠤࡤࡴࡵࡀࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠥᲪ") if self.bstack11ll1l11_opy_ else bstack11111ll_opy_ (u"ࠪࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠧᲫ")]
    bstack11l111ll1ll_opy_ = self.bstack111llll1111_opy_()
    if bstack11l111ll1ll_opy_ != None:
      command_args.append(bstack11111ll_opy_ (u"ࠦ࠲ࡩࠠࡼࡿࠥᲬ").format(bstack11l111ll1ll_opy_))
    env = os.environ.copy()
    env[bstack11111ll_opy_ (u"ࠧࡖࡅࡓࡅ࡜ࡣ࡙ࡕࡋࡆࡐࠥᲭ")] = bstack111llll1lll_opy_
    env[bstack11111ll_opy_ (u"ࠨࡔࡉࡡࡅ࡙ࡎࡒࡄࡠࡗࡘࡍࡉࠨᲮ")] = os.environ.get(bstack11111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᲯ"), bstack11111ll_opy_ (u"ࠨࠩᲰ"))
    bstack111lll11lll_opy_ = [self.binary_path]
    self.bstack111llll1l11_opy_()
    self.bstack111llll1l1l_opy_ = self.bstack111lllll111_opy_(bstack111lll11lll_opy_ + command_args, env)
    self.logger.debug(bstack11111ll_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥᲱ"))
    bstack111lll1111l_opy_ = 0
    while self.bstack111llll1l1l_opy_.poll() == None:
      bstack111lll1ll1l_opy_ = self.bstack111llll1ll1_opy_()
      if bstack111lll1ll1l_opy_:
        self.logger.debug(bstack11111ll_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨᲲ"))
        self.bstack111llllll11_opy_ = True
        return True
      bstack111lll1111l_opy_ += 1
      self.logger.debug(bstack11111ll_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢᲳ").format(bstack111lll1111l_opy_))
      time.sleep(2)
    self.logger.error(bstack11111ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵࠥᲴ").format(bstack111lll1111l_opy_))
    self.bstack11l11111ll1_opy_ = True
    return False
  def bstack111llll1ll1_opy_(self, bstack111lll1111l_opy_ = 0):
    if bstack111lll1111l_opy_ > 10:
      return False
    try:
      bstack11l1111111l_opy_ = os.environ.get(bstack11111ll_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ࠭Ჵ"), bstack11111ll_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨᲶ"))
      bstack111ll1ll1l1_opy_ = bstack11l1111111l_opy_ + bstack11lll1111l1_opy_
      response = requests.get(bstack111ll1ll1l1_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack11111ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧᲷ"), {}).get(bstack11111ll_opy_ (u"ࠩ࡬ࡨࠬᲸ"), None)
      return True
    except:
      self.logger.debug(bstack11111ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡳࡧࡧࠤࡼ࡮ࡩ࡭ࡧࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡰࡹ࡮ࠠࡤࡪࡨࡧࡰࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣᲹ"))
      return False
  def bstack11l1111ll11_opy_(self):
    bstack111ll1l1l11_opy_ = bstack11111ll_opy_ (u"ࠫࡦࡶࡰࠨᲺ") if self.bstack11ll1l11_opy_ else bstack11111ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ᲻")
    bstack11l11111l1l_opy_ = bstack11111ll_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤ᲼") if self.config.get(bstack11111ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭Ჽ")) is None else True
    bstack11l1l11l1ll_opy_ = bstack11111ll_opy_ (u"ࠣࡣࡳ࡭࠴ࡧࡰࡱࡡࡳࡩࡷࡩࡹ࠰ࡩࡨࡸࡤࡶࡲࡰ࡬ࡨࡧࡹࡥࡴࡰ࡭ࡨࡲࡄࡴࡡ࡮ࡧࡀࡿࢂࠬࡴࡺࡲࡨࡁࢀࢃࠦࡱࡧࡵࡧࡾࡃࡻࡾࠤᲾ").format(self.config[bstack11111ll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᲿ")], bstack111ll1l1l11_opy_, bstack11l11111l1l_opy_)
    if self.percy_capture_mode:
      bstack11l1l11l1ll_opy_ += bstack11111ll_opy_ (u"ࠥࠪࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦ࠿ࡾࢁࠧ᳀").format(self.percy_capture_mode)
    uri = bstack1l11l1l1ll_opy_(bstack11l1l11l1ll_opy_)
    try:
      response = bstack1l1lllll1l_opy_(bstack11111ll_opy_ (u"ࠫࡌࡋࡔࠨ᳁"), uri, {}, {bstack11111ll_opy_ (u"ࠬࡧࡵࡵࡪࠪ᳂"): (self.config[bstack11111ll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ᳃")], self.config[bstack11111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ᳄")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11llll11l1_opy_ = data.get(bstack11111ll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ᳅"))
        self.percy_capture_mode = data.get(bstack11111ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫ࠧ᳆"))
        os.environ[bstack11111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨ᳇")] = str(self.bstack11llll11l1_opy_)
        os.environ[bstack11111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨ᳈")] = str(self.percy_capture_mode)
        if bstack11l11111l1l_opy_ == bstack11111ll_opy_ (u"ࠧࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤࠣ᳉") and str(self.bstack11llll11l1_opy_).lower() == bstack11111ll_opy_ (u"ࠨࡴࡳࡷࡨࠦ᳊"):
          self.bstack1ll11lllll_opy_ = True
        if bstack11111ll_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨ᳋") in data:
          return data[bstack11111ll_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢ᳌")]
        else:
          raise bstack11111ll_opy_ (u"ࠩࡗࡳࡰ࡫࡮ࠡࡐࡲࡸࠥࡌ࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾࠩ᳍").format(data)
      else:
        raise bstack11111ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡶࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡳࡵࡣࡷࡹࡸࠦ࠭ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡃࡱࡧࡽࠥ࠳ࠠࡼࡿࠥ᳎").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11111ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡵࡸ࡯࡫ࡧࡦࡸࠧ᳏").format(e))
  def bstack111llll1111_opy_(self):
    bstack111ll1llll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11111ll_opy_ (u"ࠧࡶࡥࡳࡥࡼࡇࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠣ᳐"))
    try:
      if bstack11111ll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ᳑") not in self.bstack111llllllll_opy_:
        self.bstack111llllllll_opy_[bstack11111ll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᳒")] = 2
      with open(bstack111ll1llll1_opy_, bstack11111ll_opy_ (u"ࠨࡹࠪ᳓")) as fp:
        json.dump(self.bstack111llllllll_opy_, fp)
      return bstack111ll1llll1_opy_
    except Exception as e:
      self.logger.error(bstack11111ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡩࡲࡦࡣࡷࡩࠥࡶࡥࡳࡥࡼࠤࡨࡵ࡮ࡧ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ᳔").format(e))
  def bstack111lllll111_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111ll1l1111_opy_ == bstack11111ll_opy_ (u"ࠪࡻ࡮ࡴ᳕ࠧ"):
        bstack111lll1l1l1_opy_ = [bstack11111ll_opy_ (u"ࠫࡨࡳࡤ࠯ࡧࡻࡩ᳖ࠬ"), bstack11111ll_opy_ (u"ࠬ࠵ࡣࠨ᳗")]
        cmd = bstack111lll1l1l1_opy_ + cmd
      cmd = bstack11111ll_opy_ (u"࠭ࠠࠨ᳘").join(cmd)
      self.logger.debug(bstack11111ll_opy_ (u"ࠢࡓࡷࡱࡲ࡮ࡴࡧࠡࡽࢀ᳙ࠦ").format(cmd))
      with open(self.bstack111llll11l1_opy_, bstack11111ll_opy_ (u"ࠣࡣࠥ᳚")) as bstack11l111111l1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11l111111l1_opy_, text=True, stderr=bstack11l111111l1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11l11111ll1_opy_ = True
      self.logger.error(bstack11111ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠣࡻ࡮ࡺࡨࠡࡥࡰࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦ᳛").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111llllll11_opy_:
        self.logger.info(bstack11111ll_opy_ (u"ࠥࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡖࡥࡳࡥࡼ᳜ࠦ"))
        cmd = [self.binary_path, bstack11111ll_opy_ (u"ࠦࡪࡾࡥࡤ࠼ࡶࡸࡴࡶ᳝ࠢ")]
        self.bstack111lllll111_opy_(cmd)
        self.bstack111llllll11_opy_ = False
    except Exception as e:
      self.logger.error(bstack11111ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡳࡵࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁ᳞ࠧ").format(cmd, e))
  def bstack1llllllll_opy_(self):
    if not self.bstack11llll11l1_opy_:
      return
    try:
      bstack111ll1ll111_opy_ = 0
      while not self.bstack111llllll11_opy_ and bstack111ll1ll111_opy_ < self.bstack111ll1l1l1l_opy_:
        if self.bstack11l11111ll1_opy_:
          self.logger.info(bstack11111ll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧ᳟ࠦ"))
          return
        time.sleep(1)
        bstack111ll1ll111_opy_ += 1
      os.environ[bstack11111ll_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡂࡆࡕࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭᳠")] = str(self.bstack111ll1l11l1_opy_())
      self.logger.info(bstack11111ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠤ᳡"))
    except Exception as e:
      self.logger.error(bstack11111ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿ᳢ࠥ").format(e))
  def bstack111ll1l11l1_opy_(self):
    if self.bstack11ll1l11_opy_:
      return
    try:
      bstack111lll1l1ll_opy_ = [platform[bstack11111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ᳣")].lower() for platform in self.config.get(bstack11111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹ᳤ࠧ"), [])]
      bstack111lll11l11_opy_ = sys.maxsize
      bstack111ll1l11ll_opy_ = bstack11111ll_opy_ (u"᳥ࠬ࠭")
      for browser in bstack111lll1l1ll_opy_:
        if browser in self.bstack11l1111lll1_opy_:
          bstack111lll11ll1_opy_ = self.bstack11l1111lll1_opy_[browser]
        if bstack111lll11ll1_opy_ < bstack111lll11l11_opy_:
          bstack111lll11l11_opy_ = bstack111lll11ll1_opy_
          bstack111ll1l11ll_opy_ = browser
      return bstack111ll1l11ll_opy_
    except Exception as e:
      self.logger.error(bstack11111ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡣࡧࡶࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃ᳦ࠢ").format(e))
  @classmethod
  def bstack11llllllll_opy_(self):
    return os.getenv(bstack11111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝᳧ࠬ"), bstack11111ll_opy_ (u"ࠨࡈࡤࡰࡸ࡫᳨ࠧ")).lower()
  @classmethod
  def bstack1ll111l1ll_opy_(self):
    return os.getenv(bstack11111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ᳩ"), bstack11111ll_opy_ (u"ࠪࠫᳪ"))
  @classmethod
  def bstack1l1ll1l1l1l_opy_(cls, value):
    cls.bstack1ll11lllll_opy_ = value
  @classmethod
  def bstack111lll111ll_opy_(cls):
    return cls.bstack1ll11lllll_opy_
  @classmethod
  def bstack1l1ll1l1l11_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack11l1111l111_opy_(cls):
    return cls.percy_build_id