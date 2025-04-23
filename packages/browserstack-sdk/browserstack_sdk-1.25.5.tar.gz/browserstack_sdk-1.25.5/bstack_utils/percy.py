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
from bstack_utils.helper import bstack1ll1l11l11_opy_, bstack11lllll1ll_opy_
from bstack_utils.measure import measure
class bstack111l111l_opy_:
  working_dir = os.getcwd()
  bstack1l11lllll_opy_ = False
  config = {}
  bstack11l11llll1l_opy_ = bstack1ll1l11_opy_ (u"ࠫࠬᱦ")
  binary_path = bstack1ll1l11_opy_ (u"ࠬ࠭ᱧ")
  bstack111ll1ll11l_opy_ = bstack1ll1l11_opy_ (u"࠭ࠧᱨ")
  bstack111ll1l1l_opy_ = False
  bstack11l1111l1ll_opy_ = None
  bstack11l111111ll_opy_ = {}
  bstack111ll11llll_opy_ = 300
  bstack111lll1l1ll_opy_ = False
  logger = None
  bstack111ll1l1111_opy_ = False
  bstack11l1l11ll1_opy_ = False
  percy_build_id = None
  bstack111ll1l11ll_opy_ = bstack1ll1l11_opy_ (u"ࠧࠨᱩ")
  bstack11l1111lll1_opy_ = {
    bstack1ll1l11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᱪ") : 1,
    bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪᱫ") : 2,
    bstack1ll1l11_opy_ (u"ࠪࡩࡩ࡭ࡥࠨᱬ") : 3,
    bstack1ll1l11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫᱭ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111llll111l_opy_(self):
    bstack11l11111lll_opy_ = bstack1ll1l11_opy_ (u"ࠬ࠭ᱮ")
    bstack111ll1ll1ll_opy_ = sys.platform
    bstack111llll1l1l_opy_ = bstack1ll1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᱯ")
    if re.match(bstack1ll1l11_opy_ (u"ࠢࡥࡣࡵࡻ࡮ࡴࡼ࡮ࡣࡦࠤࡴࡹࠢᱰ"), bstack111ll1ll1ll_opy_) != None:
      bstack11l11111lll_opy_ = bstack11ll1l11l1l_opy_ + bstack1ll1l11_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡱࡶࡼ࠳ࢀࡩࡱࠤᱱ")
      self.bstack111ll1l11ll_opy_ = bstack1ll1l11_opy_ (u"ࠩࡰࡥࡨ࠭ᱲ")
    elif re.match(bstack1ll1l11_opy_ (u"ࠥࡱࡸࡽࡩ࡯ࡾࡰࡷࡾࡹࡼ࡮࡫ࡱ࡫ࡼࢂࡣࡺࡩࡺ࡭ࡳࢂࡢࡤࡥࡺ࡭ࡳࢂࡷࡪࡰࡦࡩࢁ࡫࡭ࡤࡾࡺ࡭ࡳ࠹࠲ࠣᱳ"), bstack111ll1ll1ll_opy_) != None:
      bstack11l11111lll_opy_ = bstack11ll1l11l1l_opy_ + bstack1ll1l11_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡼ࡯࡮࠯ࡼ࡬ࡴࠧᱴ")
      bstack111llll1l1l_opy_ = bstack1ll1l11_opy_ (u"ࠧࡶࡥࡳࡥࡼ࠲ࡪࡾࡥࠣᱵ")
      self.bstack111ll1l11ll_opy_ = bstack1ll1l11_opy_ (u"࠭ࡷࡪࡰࠪᱶ")
    else:
      bstack11l11111lll_opy_ = bstack11ll1l11l1l_opy_ + bstack1ll1l11_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭࡭࡫ࡱࡹࡽ࠴ࡺࡪࡲࠥᱷ")
      self.bstack111ll1l11ll_opy_ = bstack1ll1l11_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧᱸ")
    return bstack11l11111lll_opy_, bstack111llll1l1l_opy_
  def bstack111ll1ll1l1_opy_(self):
    try:
      bstack111lll1ll11_opy_ = [os.path.join(expanduser(bstack1ll1l11_opy_ (u"ࠤࢁࠦᱹ")), bstack1ll1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᱺ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111lll1ll11_opy_:
        if(self.bstack111llllll11_opy_(path)):
          return path
      raise bstack1ll1l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣᱻ")
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠰ࠤࢀࢃࠢᱼ").format(e))
  def bstack111llllll11_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack11l1111ll11_opy_(self, bstack11l111111l1_opy_):
    return os.path.join(bstack11l111111l1_opy_, self.bstack11l11llll1l_opy_ + bstack1ll1l11_opy_ (u"ࠨ࠮ࡦࡶࡤ࡫ࠧᱽ"))
  def bstack111llll11ll_opy_(self, bstack11l111111l1_opy_, bstack111ll1l1lll_opy_):
    if not bstack111ll1l1lll_opy_: return
    try:
      bstack111lll11ll1_opy_ = self.bstack11l1111ll11_opy_(bstack11l111111l1_opy_)
      with open(bstack111lll11ll1_opy_, bstack1ll1l11_opy_ (u"ࠢࡸࠤ᱾")) as f:
        f.write(bstack111ll1l1lll_opy_)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡕࡤࡺࡪࡪࠠ࡯ࡧࡺࠤࡊ࡚ࡡࡨࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠧ᱿"))
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡡࡷࡧࠣࡸ࡭࡫ࠠࡦࡶࡤ࡫࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᲀ").format(e))
  def bstack11l11111ll1_opy_(self, bstack11l111111l1_opy_):
    try:
      bstack111lll11ll1_opy_ = self.bstack11l1111ll11_opy_(bstack11l111111l1_opy_)
      if os.path.exists(bstack111lll11ll1_opy_):
        with open(bstack111lll11ll1_opy_, bstack1ll1l11_opy_ (u"ࠥࡶࠧᲁ")) as f:
          bstack111ll1l1lll_opy_ = f.read().strip()
          return bstack111ll1l1lll_opy_ if bstack111ll1l1lll_opy_ else None
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡋࡔࡢࡩ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᲂ").format(e))
  def bstack111lllll1ll_opy_(self, bstack11l111111l1_opy_, bstack11l11111lll_opy_):
    bstack11l1111l1l1_opy_ = self.bstack11l11111ll1_opy_(bstack11l111111l1_opy_)
    if bstack11l1111l1l1_opy_:
      try:
        bstack11l11111111_opy_ = self.bstack11l1111ll1l_opy_(bstack11l1111l1l1_opy_, bstack11l11111lll_opy_)
        if not bstack11l11111111_opy_:
          self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮ࡹࠠࡶࡲࠣࡸࡴࠦࡤࡢࡶࡨࠤ࠭ࡋࡔࡢࡩࠣࡹࡳࡩࡨࡢࡰࡪࡩࡩ࠯ࠢᲃ"))
          return True
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡎࡦࡹࠣࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡹࡩࡷࡹࡩࡰࡰࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡻࡰࡥࡣࡷࡩࠧᲄ"))
        return False
      except Exception as e:
        self.logger.warn(bstack1ll1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧ࡭࡫ࡣ࡬ࠢࡩࡳࡷࠦࡢࡪࡰࡤࡶࡾࠦࡵࡱࡦࡤࡸࡪࡹࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡥ࡭ࡳࡧࡲࡺ࠼ࠣࡿࢂࠨᲅ").format(e))
    return False
  def bstack11l1111ll1l_opy_(self, bstack11l1111l1l1_opy_, bstack11l11111lll_opy_):
    try:
      headers = {
        bstack1ll1l11_opy_ (u"ࠣࡋࡩ࠱ࡓࡵ࡮ࡦ࠯ࡐࡥࡹࡩࡨࠣᲆ"): bstack11l1111l1l1_opy_
      }
      response = bstack11lllll1ll_opy_(bstack1ll1l11_opy_ (u"ࠩࡊࡉ࡙࠭ᲇ"), bstack11l11111lll_opy_, {}, {bstack1ll1l11_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶࠦᲈ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1ll1l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡷࡳࡨࡦࡺࡥࡴ࠼ࠣࡿࢂࠨᲉ").format(e))
  @measure(event_name=EVENTS.bstack11ll1lllll1_opy_, stage=STAGE.bstack1l11lll1l_opy_)
  def bstack11l11111l1l_opy_(self, bstack11l11111lll_opy_, bstack111llll1l1l_opy_):
    try:
      bstack111ll1ll111_opy_ = self.bstack111ll1ll1l1_opy_()
      bstack111lll11l11_opy_ = os.path.join(bstack111ll1ll111_opy_, bstack1ll1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡿ࡯ࡰࠨᲊ"))
      bstack111llll1111_opy_ = os.path.join(bstack111ll1ll111_opy_, bstack111llll1l1l_opy_)
      if self.bstack111lllll1ll_opy_(bstack111ll1ll111_opy_, bstack11l11111lll_opy_):
        if os.path.exists(bstack111llll1111_opy_):
          self.logger.info(bstack1ll1l11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣ᲋").format(bstack111llll1111_opy_))
          return bstack111llll1111_opy_
        if os.path.exists(bstack111lll11l11_opy_):
          self.logger.info(bstack1ll1l11_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡺࡪࡲࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡸࡲࡿ࡯ࡰࡱ࡫ࡱ࡫ࠧ᲌").format(bstack111lll11l11_opy_))
          return self.bstack111lll11lll_opy_(bstack111lll11l11_opy_, bstack111llll1l1l_opy_)
      self.logger.info(bstack1ll1l11_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯ࠣࡿࢂࠨ᲍").format(bstack11l11111lll_opy_))
      response = bstack11lllll1ll_opy_(bstack1ll1l11_opy_ (u"ࠩࡊࡉ࡙࠭᲎"), bstack11l11111lll_opy_, {}, {})
      if response.status_code == 200:
        bstack11l1111l111_opy_ = response.headers.get(bstack1ll1l11_opy_ (u"ࠥࡉ࡙ࡧࡧࠣ᲏"), bstack1ll1l11_opy_ (u"ࠦࠧᲐ"))
        if bstack11l1111l111_opy_:
          self.bstack111llll11ll_opy_(bstack111ll1ll111_opy_, bstack11l1111l111_opy_)
        with open(bstack111lll11l11_opy_, bstack1ll1l11_opy_ (u"ࠬࡽࡢࠨᲑ")) as file:
          file.write(response.content)
        self.logger.info(bstack1ll1l11_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡤࡲࡩࠦࡳࡢࡸࡨࡨࠥࡧࡴࠡࡽࢀࠦᲒ").format(bstack111lll11l11_opy_))
        return self.bstack111lll11lll_opy_(bstack111lll11l11_opy_, bstack111llll1l1l_opy_)
      else:
        raise(bstack1ll1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠡࡕࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪࡀࠠࡼࡿࠥᲓ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽ࠿ࠦࡻࡾࠤᲔ").format(e))
  def bstack111lllll1l1_opy_(self, bstack11l11111lll_opy_, bstack111llll1l1l_opy_):
    try:
      retry = 2
      bstack111llll1111_opy_ = None
      bstack111lll1ll1l_opy_ = False
      while retry > 0:
        bstack111llll1111_opy_ = self.bstack11l11111l1l_opy_(bstack11l11111lll_opy_, bstack111llll1l1l_opy_)
        bstack111lll1ll1l_opy_ = self.bstack11l1111l11l_opy_(bstack11l11111lll_opy_, bstack111llll1l1l_opy_, bstack111llll1111_opy_)
        if bstack111lll1ll1l_opy_:
          break
        retry -= 1
      return bstack111llll1111_opy_, bstack111lll1ll1l_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡲࡤࡸ࡭ࠨᲕ").format(e))
    return bstack111llll1111_opy_, False
  def bstack11l1111l11l_opy_(self, bstack11l11111lll_opy_, bstack111llll1l1l_opy_, bstack111llll1111_opy_, bstack111ll1llll1_opy_ = 0):
    if bstack111ll1llll1_opy_ > 1:
      return False
    if bstack111llll1111_opy_ == None or os.path.exists(bstack111llll1111_opy_) == False:
      self.logger.warn(bstack1ll1l11_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡷ࡫ࡴࡳࡻ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣᲖ"))
      return False
    bstack111lllllll1_opy_ = bstack1ll1l11_opy_ (u"ࠦࡣ࠴ࠪࡁࡲࡨࡶࡨࡿ࡜࠰ࡥ࡯࡭ࠥࡢࡤ࠯࡞ࡧ࠯࠳ࡢࡤࠬࠤᲗ")
    command = bstack1ll1l11_opy_ (u"ࠬࢁࡽࠡ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫᲘ").format(bstack111llll1111_opy_)
    bstack111lllll11l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111lllllll1_opy_, bstack111lllll11l_opy_) != None:
      return True
    else:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡣࡩࡧࡦ࡯ࠥ࡬ࡡࡪ࡮ࡨࡨࠧᲙ"))
      return False
  def bstack111lll11lll_opy_(self, bstack111lll11l11_opy_, bstack111llll1l1l_opy_):
    try:
      working_dir = os.path.dirname(bstack111lll11l11_opy_)
      shutil.unpack_archive(bstack111lll11l11_opy_, working_dir)
      bstack111llll1111_opy_ = os.path.join(working_dir, bstack111llll1l1l_opy_)
      os.chmod(bstack111llll1111_opy_, 0o755)
      return bstack111llll1111_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡹࡳࢀࡩࡱࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣᲚ"))
  def bstack111ll1lllll_opy_(self):
    try:
      bstack111llll1ll1_opy_ = self.config.get(bstack1ll1l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᲛ"))
      bstack111ll1lllll_opy_ = bstack111llll1ll1_opy_ or (bstack111llll1ll1_opy_ is None and self.bstack1l11lllll_opy_)
      if not bstack111ll1lllll_opy_ or self.config.get(bstack1ll1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᲜ"), None) not in bstack11ll11lllll_opy_:
        return False
      self.bstack111ll1l1l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᲝ").format(e))
  def bstack11l11111l11_opy_(self):
    try:
      bstack11l11111l11_opy_ = self.percy_capture_mode
      return bstack11l11111l11_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾࠦࡣࡢࡲࡷࡹࡷ࡫ࠠ࡮ࡱࡧࡩ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᲞ").format(e))
  def init(self, bstack1l11lllll_opy_, config, logger):
    self.bstack1l11lllll_opy_ = bstack1l11lllll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111ll1lllll_opy_():
      return
    self.bstack11l111111ll_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫᲟ"), {})
    self.percy_capture_mode = config.get(bstack1ll1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩᲠ"))
    try:
      bstack11l11111lll_opy_, bstack111llll1l1l_opy_ = self.bstack111llll111l_opy_()
      self.bstack11l11llll1l_opy_ = bstack111llll1l1l_opy_
      bstack111llll1111_opy_, bstack111lll1ll1l_opy_ = self.bstack111lllll1l1_opy_(bstack11l11111lll_opy_, bstack111llll1l1l_opy_)
      if bstack111lll1ll1l_opy_:
        self.binary_path = bstack111llll1111_opy_
        thread = Thread(target=self.bstack111ll1l1ll1_opy_)
        thread.start()
      else:
        self.bstack111ll1l1111_opy_ = True
        self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾ࠮࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡖࡥࡳࡥࡼࠦᲡ").format(bstack111llll1111_opy_))
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᲢ").format(e))
  def bstack111lll11111_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1ll1l11_opy_ (u"ࠩ࡯ࡳ࡬࠭Უ"), bstack1ll1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰࡯ࡳ࡬࠭Ფ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡕࡻࡳࡩ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࡴࠢࡤࡸࠥࢁࡽࠣᲥ").format(logfile))
      self.bstack111ll1ll11l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࠡࡲࡤࡸ࡭࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᲦ").format(e))
  @measure(event_name=EVENTS.bstack11ll1ll1ll1_opy_, stage=STAGE.bstack1l11lll1l_opy_)
  def bstack111ll1l1ll1_opy_(self):
    bstack111lll11l1l_opy_ = self.bstack111lll1llll_opy_()
    if bstack111lll11l1l_opy_ == None:
      self.bstack111ll1l1111_opy_ = True
      self.logger.error(bstack1ll1l11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠤᲧ"))
      return False
    command_args = [bstack1ll1l11_opy_ (u"ࠢࡢࡲࡳ࠾ࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠣᲨ") if self.bstack1l11lllll_opy_ else bstack1ll1l11_opy_ (u"ࠨࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠬᲩ")]
    bstack11l111lll11_opy_ = self.bstack111ll1lll11_opy_()
    if bstack11l111lll11_opy_ != None:
      command_args.append(bstack1ll1l11_opy_ (u"ࠤ࠰ࡧࠥࢁࡽࠣᲪ").format(bstack11l111lll11_opy_))
    env = os.environ.copy()
    env[bstack1ll1l11_opy_ (u"ࠥࡔࡊࡘࡃ࡚ࡡࡗࡓࡐࡋࡎࠣᲫ")] = bstack111lll11l1l_opy_
    env[bstack1ll1l11_opy_ (u"࡙ࠦࡎ࡟ࡃࡗࡌࡐࡉࡥࡕࡖࡋࡇࠦᲬ")] = os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᲭ"), bstack1ll1l11_opy_ (u"࠭ࠧᲮ"))
    bstack111lll1111l_opy_ = [self.binary_path]
    self.bstack111lll11111_opy_()
    self.bstack11l1111l1ll_opy_ = self.bstack111lll1l111_opy_(bstack111lll1111l_opy_ + command_args, env)
    self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡔࡶࡤࡶࡹ࡯࡮ࡨࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠣᲯ"))
    bstack111ll1llll1_opy_ = 0
    while self.bstack11l1111l1ll_opy_.poll() == None:
      bstack111lll1l11l_opy_ = self.bstack111ll1l11l1_opy_()
      if bstack111lll1l11l_opy_:
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠦᲰ"))
        self.bstack111lll1l1ll_opy_ = True
        return True
      bstack111ll1llll1_opy_ += 1
      self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡔࡨࡸࡷࡿࠠ࠮ࠢࡾࢁࠧᲱ").format(bstack111ll1llll1_opy_))
      time.sleep(2)
    self.logger.error(bstack1ll1l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡋࡧࡩ࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡿࢂࠦࡡࡵࡶࡨࡱࡵࡺࡳࠣᲲ").format(bstack111ll1llll1_opy_))
    self.bstack111ll1l1111_opy_ = True
    return False
  def bstack111ll1l11l1_opy_(self, bstack111ll1llll1_opy_ = 0):
    if bstack111ll1llll1_opy_ > 10:
      return False
    try:
      bstack111ll1l111l_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡗࡊࡘࡖࡆࡔࡢࡅࡉࡊࡒࡆࡕࡖࠫᲳ"), bstack1ll1l11_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴ࠻࠷࠶࠷࠽࠭Ჴ"))
      bstack111llll1lll_opy_ = bstack111ll1l111l_opy_ + bstack11ll1ll1l1l_opy_
      response = requests.get(bstack111llll1lll_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࠬᲵ"), {}).get(bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪᲶ"), None)
      return True
    except:
      self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢࡺ࡬࡮ࡲࡥࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢ࡮ࡷ࡬ࠥࡩࡨࡦࡥ࡮ࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨᲷ"))
      return False
  def bstack111lll1llll_opy_(self):
    bstack111lll1lll1_opy_ = bstack1ll1l11_opy_ (u"ࠩࡤࡴࡵ࠭Ჸ") if self.bstack1l11lllll_opy_ else bstack1ll1l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᲹ")
    bstack111lll1l1l1_opy_ = bstack1ll1l11_opy_ (u"ࠦࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠢᲺ") if self.config.get(bstack1ll1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ᲻")) is None else True
    bstack11l1l1l1111_opy_ = bstack1ll1l11_opy_ (u"ࠨࡡࡱ࡫࠲ࡥࡵࡶ࡟ࡱࡧࡵࡧࡾ࠵ࡧࡦࡶࡢࡴࡷࡵࡪࡦࡥࡷࡣࡹࡵ࡫ࡦࡰࡂࡲࡦࡳࡥ࠾ࡽࢀࠪࡹࡿࡰࡦ࠿ࡾࢁࠫࡶࡥࡳࡥࡼࡁࢀࢃࠢ᲼").format(self.config[bstack1ll1l11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᲽ")], bstack111lll1lll1_opy_, bstack111lll1l1l1_opy_)
    if self.percy_capture_mode:
      bstack11l1l1l1111_opy_ += bstack1ll1l11_opy_ (u"ࠣࠨࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫࠽ࡼࡿࠥᲾ").format(self.percy_capture_mode)
    uri = bstack1ll1l11l11_opy_(bstack11l1l1l1111_opy_)
    try:
      response = bstack11lllll1ll_opy_(bstack1ll1l11_opy_ (u"ࠩࡊࡉ࡙࠭Ჿ"), uri, {}, {bstack1ll1l11_opy_ (u"ࠪࡥࡺࡺࡨࠨ᳀"): (self.config[bstack1ll1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭᳁")], self.config[bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ᳂")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack111ll1l1l_opy_ = data.get(bstack1ll1l11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ᳃"))
        self.percy_capture_mode = data.get(bstack1ll1l11_opy_ (u"ࠧࡱࡧࡵࡧࡾࡥࡣࡢࡲࡷࡹࡷ࡫࡟࡮ࡱࡧࡩࠬ᳄"))
        os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭᳅")] = str(self.bstack111ll1l1l_opy_)
        os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭᳆")] = str(self.percy_capture_mode)
        if bstack111lll1l1l1_opy_ == bstack1ll1l11_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨ᳇") and str(self.bstack111ll1l1l_opy_).lower() == bstack1ll1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤ᳈"):
          self.bstack11l1l11ll1_opy_ = True
        if bstack1ll1l11_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦ᳉") in data:
          return data[bstack1ll1l11_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧ᳊")]
        else:
          raise bstack1ll1l11_opy_ (u"ࠧࡕࡱ࡮ࡩࡳࠦࡎࡰࡶࠣࡊࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠧ᳋").format(data)
      else:
        raise bstack1ll1l11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡴࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡸࡺࡡࡵࡷࡶࠤ࠲ࠦࡻࡾ࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡈ࡯ࡥࡻࠣ࠱ࠥࢁࡽࠣ᳌").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡳࡶࡴࡰࡥࡤࡶࠥ᳍").format(e))
  def bstack111ll1lll11_opy_(self):
    bstack111ll1l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠥࡴࡪࡸࡣࡺࡅࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳࠨ᳎"))
    try:
      if bstack1ll1l11_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᳏") not in self.bstack11l111111ll_opy_:
        self.bstack11l111111ll_opy_[bstack1ll1l11_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭᳐")] = 2
      with open(bstack111ll1l1l11_opy_, bstack1ll1l11_opy_ (u"࠭ࡷࠨ᳑")) as fp:
        json.dump(self.bstack11l111111ll_opy_, fp)
      return bstack111ll1l1l11_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡧࡷ࡫ࡡࡵࡧࠣࡴࡪࡸࡣࡺࠢࡦࡳࡳ࡬ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ᳒").format(e))
  def bstack111lll1l111_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111ll1l11ll_opy_ == bstack1ll1l11_opy_ (u"ࠨࡹ࡬ࡲࠬ᳓"):
        bstack111llll1l11_opy_ = [bstack1ll1l11_opy_ (u"ࠩࡦࡱࡩ࠴ࡥࡹࡧ᳔ࠪ"), bstack1ll1l11_opy_ (u"ࠪ࠳ࡨ᳕࠭")]
        cmd = bstack111llll1l11_opy_ + cmd
      cmd = bstack1ll1l11_opy_ (u"᳖ࠫࠥ࠭").join(cmd)
      self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡘࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻࡾࠤ᳗").format(cmd))
      with open(self.bstack111ll1ll11l_opy_, bstack1ll1l11_opy_ (u"ࠨࡡ᳘ࠣ")) as bstack111llllll1l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111llllll1l_opy_, text=True, stderr=bstack111llllll1l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111ll1l1111_opy_ = True
      self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠡࡹ࡬ࡸ࡭ࠦࡣ࡮ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ᳙").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111lll1l1ll_opy_:
        self.logger.info(bstack1ll1l11_opy_ (u"ࠣࡕࡷࡳࡵࡶࡩ࡯ࡩࠣࡔࡪࡸࡣࡺࠤ᳚"))
        cmd = [self.binary_path, bstack1ll1l11_opy_ (u"ࠤࡨࡼࡪࡩ࠺ࡴࡶࡲࡴࠧ᳛")]
        self.bstack111lll1l111_opy_(cmd)
        self.bstack111lll1l1ll_opy_ = False
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡱࡳࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡧࡴࡳ࡭ࡢࡰࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿ᳜ࠥ").format(cmd, e))
  def bstack1l1lll1111_opy_(self):
    if not self.bstack111ll1l1l_opy_:
      return
    try:
      bstack111ll1lll1l_opy_ = 0
      while not self.bstack111lll1l1ll_opy_ and bstack111ll1lll1l_opy_ < self.bstack111ll11llll_opy_:
        if self.bstack111ll1l1111_opy_:
          self.logger.info(bstack1ll1l11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡩࡥ࡮ࡲࡥࡥࠤ᳝"))
          return
        time.sleep(1)
        bstack111ll1lll1l_opy_ += 1
      os.environ[bstack1ll1l11_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡇࡋࡓࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐ᳞ࠫ")] = str(self.bstack111lllll111_opy_())
      self.logger.info(bstack1ll1l11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪ᳟ࠢ"))
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ᳠").format(e))
  def bstack111lllll111_opy_(self):
    if self.bstack1l11lllll_opy_:
      return
    try:
      bstack111llllllll_opy_ = [platform[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭᳡")].lower() for platform in self.config.get(bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷ᳢ࠬ"), [])]
      bstack111lll111ll_opy_ = sys.maxsize
      bstack111lll111l1_opy_ = bstack1ll1l11_opy_ (u"᳣ࠪࠫ")
      for browser in bstack111llllllll_opy_:
        if browser in self.bstack11l1111lll1_opy_:
          bstack111ll1l1l1l_opy_ = self.bstack11l1111lll1_opy_[browser]
        if bstack111ll1l1l1l_opy_ < bstack111lll111ll_opy_:
          bstack111lll111ll_opy_ = bstack111ll1l1l1l_opy_
          bstack111lll111l1_opy_ = browser
      return bstack111lll111l1_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡨࡥࡴࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁ᳤ࠧ").format(e))
  @classmethod
  def bstack11l1ll1lll_opy_(self):
    return os.getenv(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ᳥࡛ࠪ"), bstack1ll1l11_opy_ (u"࠭ࡆࡢ࡮ࡶࡩ᳦ࠬ")).lower()
  @classmethod
  def bstack111llll11_opy_(self):
    return os.getenv(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈ᳧ࠫ"), bstack1ll1l11_opy_ (u"ࠨ᳨ࠩ"))
  @classmethod
  def bstack111111l111_opy_(cls, value):
    cls.bstack11l1l11ll1_opy_ = value
  @classmethod
  def bstack111llll11l1_opy_(cls):
    return cls.bstack11l1l11ll1_opy_
  @classmethod
  def bstack1111l1l111_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack11l1111111l_opy_(cls):
    return cls.percy_build_id