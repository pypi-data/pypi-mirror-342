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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll1l1l111_opy_, bstack11ll11llll1_opy_
import tempfile
import json
bstack11l111l1lll_opy_ = os.getenv(bstack11111ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡇࡠࡈࡌࡐࡊࠨᯛ"), None) or os.path.join(tempfile.gettempdir(), bstack11111ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠣᯜ"))
bstack11l11l111ll_opy_ = os.path.join(bstack11111ll_opy_ (u"ࠢ࡭ࡱࡪࠦᯝ"), bstack11111ll_opy_ (u"ࠨࡵࡧ࡯࠲ࡩ࡬ࡪ࠯ࡧࡩࡧࡻࡧ࠯࡮ࡲ࡫ࠬᯞ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11111ll_opy_ (u"ࠩࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬᯟ"),
      datefmt=bstack11111ll_opy_ (u"ࠪࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙࡚ࠪࠨᯠ"),
      stream=sys.stdout
    )
  return logger
def bstack1llll11l111_opy_():
  bstack11l11l1111l_opy_ = os.environ.get(bstack11111ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡈࡊࡈࡕࡈࠤᯡ"), bstack11111ll_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦᯢ"))
  return logging.DEBUG if bstack11l11l1111l_opy_.lower() == bstack11111ll_opy_ (u"ࠨࡴࡳࡷࡨࠦᯣ") else logging.INFO
def bstack1ll111lll1l_opy_():
  global bstack11l111l1lll_opy_
  if os.path.exists(bstack11l111l1lll_opy_):
    os.remove(bstack11l111l1lll_opy_)
  if os.path.exists(bstack11l11l111ll_opy_):
    os.remove(bstack11l11l111ll_opy_)
def bstack11l11lll11_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1111111ll_opy_(config, log_level):
  bstack11l111ll1l1_opy_ = log_level
  if bstack11111ll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᯤ") in config and config[bstack11111ll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᯥ")] in bstack11ll1l1l111_opy_:
    bstack11l111ll1l1_opy_ = bstack11ll1l1l111_opy_[config[bstack11111ll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯᯦ࠫ")]]
  if config.get(bstack11111ll_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬᯧ"), False):
    logging.getLogger().setLevel(bstack11l111ll1l1_opy_)
    return bstack11l111ll1l1_opy_
  global bstack11l111l1lll_opy_
  bstack11l11lll11_opy_()
  bstack11l11l11l11_opy_ = logging.Formatter(
    fmt=bstack11111ll_opy_ (u"ࠫࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧᯨ"),
    datefmt=bstack11111ll_opy_ (u"࡙ࠬࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࡜ࠪᯩ"),
  )
  bstack11l111llll1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11l111l1lll_opy_)
  file_handler.setFormatter(bstack11l11l11l11_opy_)
  bstack11l111llll1_opy_.setFormatter(bstack11l11l11l11_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack11l111llll1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11111ll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࡷ࡫࡭ࡰࡶࡨ࠲ࡷ࡫࡭ࡰࡶࡨࡣࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡵ࡮ࠨᯪ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack11l111llll1_opy_.setLevel(bstack11l111ll1l1_opy_)
  logging.getLogger().addHandler(bstack11l111llll1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11l111ll1l1_opy_
def bstack11l111l1ll1_opy_(config):
  try:
    bstack11l11l11lll_opy_ = set(bstack11ll11llll1_opy_)
    bstack11l111ll111_opy_ = bstack11111ll_opy_ (u"ࠧࠨᯫ")
    with open(bstack11111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫᯬ")) as bstack11l11l1l111_opy_:
      bstack11l11l11ll1_opy_ = bstack11l11l1l111_opy_.read()
      bstack11l111ll111_opy_ = re.sub(bstack11111ll_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠧ࠳࠰ࠤ࡝ࡰࠪᯭ"), bstack11111ll_opy_ (u"ࠪࠫᯮ"), bstack11l11l11ll1_opy_, flags=re.M)
      bstack11l111ll111_opy_ = re.sub(
        bstack11111ll_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄ࠮ࠧᯯ") + bstack11111ll_opy_ (u"ࠬࢂࠧᯰ").join(bstack11l11l11lll_opy_) + bstack11111ll_opy_ (u"࠭ࠩ࠯ࠬࠧࠫᯱ"),
        bstack11111ll_opy_ (u"ࡲࠨ࡞࠵࠾ࠥࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞᯲ࠩ"),
        bstack11l111ll111_opy_, flags=re.M | re.I
      )
    def bstack11l111l1l11_opy_(dic):
      bstack11l11l11111_opy_ = {}
      for key, value in dic.items():
        if key in bstack11l11l11lll_opy_:
          bstack11l11l11111_opy_[key] = bstack11111ll_opy_ (u"ࠨ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡ᯳ࠬ")
        else:
          if isinstance(value, dict):
            bstack11l11l11111_opy_[key] = bstack11l111l1l11_opy_(value)
          else:
            bstack11l11l11111_opy_[key] = value
      return bstack11l11l11111_opy_
    bstack11l11l11111_opy_ = bstack11l111l1l11_opy_(config)
    return {
      bstack11111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬ᯴"): bstack11l111ll111_opy_,
      bstack11111ll_opy_ (u"ࠪࡪ࡮ࡴࡡ࡭ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭᯵"): json.dumps(bstack11l11l11111_opy_)
    }
  except Exception as e:
    return {}
def bstack11l11l1l11l_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack11111ll_opy_ (u"ࠫࡱࡵࡧࠨ᯶"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l111ll1ll_opy_ = os.path.join(log_dir, bstack11111ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠭᯷"))
  if not os.path.exists(bstack11l111ll1ll_opy_):
    bstack11l111lll1l_opy_ = {
      bstack11111ll_opy_ (u"ࠨࡩ࡯࡫ࡳࡥࡹ࡮ࠢ᯸"): str(inipath),
      bstack11111ll_opy_ (u"ࠢࡳࡱࡲࡸࡵࡧࡴࡩࠤ᯹"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack11111ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧ᯺")), bstack11111ll_opy_ (u"ࠩࡺࠫ᯻")) as bstack11l111lllll_opy_:
      bstack11l111lllll_opy_.write(json.dumps(bstack11l111lll1l_opy_))
def bstack11l11l11l1l_opy_():
  try:
    bstack11l111ll1ll_opy_ = os.path.join(os.getcwd(), bstack11111ll_opy_ (u"ࠪࡰࡴ࡭ࠧ᯼"), bstack11111ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪ᯽"))
    if os.path.exists(bstack11l111ll1ll_opy_):
      with open(bstack11l111ll1ll_opy_, bstack11111ll_opy_ (u"ࠬࡸࠧ᯾")) as bstack11l111lllll_opy_:
        bstack11l111lll11_opy_ = json.load(bstack11l111lllll_opy_)
      return bstack11l111lll11_opy_.get(bstack11111ll_opy_ (u"࠭ࡩ࡯࡫ࡳࡥࡹ࡮ࠧ᯿"), bstack11111ll_opy_ (u"ࠧࠨᰀ")), bstack11l111lll11_opy_.get(bstack11111ll_opy_ (u"ࠨࡴࡲࡳࡹࡶࡡࡵࡪࠪᰁ"), bstack11111ll_opy_ (u"ࠩࠪᰂ"))
  except:
    pass
  return None, None
def bstack11l111ll11l_opy_():
  try:
    bstack11l111ll1ll_opy_ = os.path.join(os.getcwd(), bstack11111ll_opy_ (u"ࠪࡰࡴ࡭ࠧᰃ"), bstack11111ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪᰄ"))
    if os.path.exists(bstack11l111ll1ll_opy_):
      os.remove(bstack11l111ll1ll_opy_)
  except:
    pass
def bstack1llllll1l_opy_(config):
  from bstack_utils.helper import bstack11l1l1ll_opy_
  global bstack11l111l1lll_opy_
  try:
    if config.get(bstack11111ll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧᰅ"), False):
      return
    uuid = os.getenv(bstack11111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᰆ")) if os.getenv(bstack11111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᰇ")) else bstack11l1l1ll_opy_.get_property(bstack11111ll_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥᰈ"))
    if not uuid or uuid == bstack11111ll_opy_ (u"ࠩࡱࡹࡱࡲࠧᰉ"):
      return
    bstack11l11l111l1_opy_ = [bstack11111ll_opy_ (u"ࠪࡶࡪࡷࡵࡪࡴࡨࡱࡪࡴࡴࡴ࠰ࡷࡼࡹ࠭ᰊ"), bstack11111ll_opy_ (u"ࠫࡕ࡯ࡰࡧ࡫࡯ࡩࠬᰋ"), bstack11111ll_opy_ (u"ࠬࡶࡹࡱࡴࡲ࡮ࡪࡩࡴ࠯ࡶࡲࡱࡱ࠭ᰌ"), bstack11l111l1lll_opy_, bstack11l11l111ll_opy_]
    bstack11l11l1l1l1_opy_, root_path = bstack11l11l11l1l_opy_()
    if bstack11l11l1l1l1_opy_ != None:
      bstack11l11l111l1_opy_.append(bstack11l11l1l1l1_opy_)
    if root_path != None:
      bstack11l11l111l1_opy_.append(os.path.join(root_path, bstack11111ll_opy_ (u"࠭ࡣࡰࡰࡩࡸࡪࡹࡴ࠯ࡲࡼࠫᰍ")))
    bstack11l11lll11_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11111ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭࡭ࡱࡪࡷ࠲࠭ᰎ") + uuid + bstack11111ll_opy_ (u"ࠨ࠰ࡷࡥࡷ࠴ࡧࡻࠩᰏ"))
    with tarfile.open(output_file, bstack11111ll_opy_ (u"ࠤࡺ࠾࡬ࢀࠢᰐ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11l11l111l1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11l111l1ll1_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack11l111l1l1l_opy_ = data.encode()
        tarinfo.size = len(bstack11l111l1l1l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack11l111l1l1l_opy_))
    bstack11lllll11l_opy_ = MultipartEncoder(
      fields= {
        bstack11111ll_opy_ (u"ࠪࡨࡦࡺࡡࠨᰑ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11111ll_opy_ (u"ࠫࡷࡨࠧᰒ")), bstack11111ll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲ࡼ࠲࡭ࡺࡪࡲࠪᰓ")),
        bstack11111ll_opy_ (u"࠭ࡣ࡭࡫ࡨࡲࡹࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᰔ"): uuid
      }
    )
    response = requests.post(
      bstack11111ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡷࡳࡰࡴࡧࡤ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡨࡲࡩࡦࡰࡷ࠱ࡱࡵࡧࡴ࠱ࡸࡴࡱࡵࡡࡥࠤᰕ"),
      data=bstack11lllll11l_opy_,
      headers={bstack11111ll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᰖ"): bstack11lllll11l_opy_.content_type},
      auth=(config[bstack11111ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᰗ")], config[bstack11111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᰘ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11111ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡹࡵࡲ࡯ࡢࡦࠣࡰࡴ࡭ࡳ࠻ࠢࠪᰙ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11111ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵ࠽ࠫᰚ") + str(e))
  finally:
    try:
      bstack1ll111lll1l_opy_()
      bstack11l111ll11l_opy_()
    except:
      pass