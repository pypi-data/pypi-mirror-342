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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll1lll1l1_opy_, bstack11ll1l1ll1l_opy_
import tempfile
import json
bstack11l111l1l1l_opy_ = os.getenv(bstack1ll1l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡌࡥࡆࡊࡎࡈࠦᯙ"), None) or os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨࡪࡨࡵࡨ࠰࡯ࡳ࡬ࠨᯚ"))
bstack11l111l1l11_opy_ = os.path.join(bstack1ll1l11_opy_ (u"ࠧࡲ࡯ࡨࠤᯛ"), bstack1ll1l11_opy_ (u"࠭ࡳࡥ࡭࠰ࡧࡱ࡯࠭ࡥࡧࡥࡹ࡬࠴࡬ࡰࡩࠪᯜ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1ll1l11_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪᯝ"),
      datefmt=bstack1ll1l11_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭ᯞ"),
      stream=sys.stdout
    )
  return logger
def bstack1l1l1111l1l_opy_():
  bstack11l111lll1l_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡆࡈࡆ࡚ࡍࠢᯟ"), bstack1ll1l11_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤᯠ"))
  return logging.DEBUG if bstack11l111lll1l_opy_.lower() == bstack1ll1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤᯡ") else logging.INFO
def bstack1llll1l1111_opy_():
  global bstack11l111l1l1l_opy_
  if os.path.exists(bstack11l111l1l1l_opy_):
    os.remove(bstack11l111l1l1l_opy_)
  if os.path.exists(bstack11l111l1l11_opy_):
    os.remove(bstack11l111l1l11_opy_)
def bstack1l11l1ll1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1ll11111ll_opy_(config, log_level):
  bstack11l11l11l11_opy_ = log_level
  if bstack1ll1l11_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᯢ") in config and config[bstack1ll1l11_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᯣ")] in bstack11ll1lll1l1_opy_:
    bstack11l11l11l11_opy_ = bstack11ll1lll1l1_opy_[config[bstack1ll1l11_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᯤ")]]
  if config.get(bstack1ll1l11_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᯥ"), False):
    logging.getLogger().setLevel(bstack11l11l11l11_opy_)
    return bstack11l11l11l11_opy_
  global bstack11l111l1l1l_opy_
  bstack1l11l1ll1_opy_()
  bstack11l111lllll_opy_ = logging.Formatter(
    fmt=bstack1ll1l11_opy_ (u"ࠩࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷ᯦ࠬ"),
    datefmt=bstack1ll1l11_opy_ (u"ࠪࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙࡚ࠪࠨᯧ"),
  )
  bstack11l11l1l1l1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11l111l1l1l_opy_)
  file_handler.setFormatter(bstack11l111lllll_opy_)
  bstack11l11l1l1l1_opy_.setFormatter(bstack11l111lllll_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack11l11l1l1l1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1ll1l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡵࡩࡲࡵࡴࡦ࠰ࡵࡩࡲࡵࡴࡦࡡࡦࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࠭ᯨ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack11l11l1l1l1_opy_.setLevel(bstack11l11l11l11_opy_)
  logging.getLogger().addHandler(bstack11l11l1l1l1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11l11l11l11_opy_
def bstack11l11l1l11l_opy_(config):
  try:
    bstack11l11l11l1l_opy_ = set(bstack11ll1l1ll1l_opy_)
    bstack11l111l1lll_opy_ = bstack1ll1l11_opy_ (u"ࠬ࠭ᯩ")
    with open(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩᯪ")) as bstack11l11l111l1_opy_:
      bstack11l11l11111_opy_ = bstack11l11l111l1_opy_.read()
      bstack11l111l1lll_opy_ = re.sub(bstack1ll1l11_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠥ࠱࠮ࠩࡢ࡮ࠨᯫ"), bstack1ll1l11_opy_ (u"ࠨࠩᯬ"), bstack11l11l11111_opy_, flags=re.M)
      bstack11l111l1lll_opy_ = re.sub(
        bstack1ll1l11_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠬࠬᯭ") + bstack1ll1l11_opy_ (u"ࠪࢀࠬᯮ").join(bstack11l11l11l1l_opy_) + bstack1ll1l11_opy_ (u"ࠫ࠮࠴ࠪࠥࠩᯯ"),
        bstack1ll1l11_opy_ (u"ࡷ࠭࡜࠳࠼ࠣ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧᯰ"),
        bstack11l111l1lll_opy_, flags=re.M | re.I
      )
    def bstack11l11l11lll_opy_(dic):
      bstack11l111ll11l_opy_ = {}
      for key, value in dic.items():
        if key in bstack11l11l11l1l_opy_:
          bstack11l111ll11l_opy_[key] = bstack1ll1l11_opy_ (u"࡛࠭ࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪᯱ")
        else:
          if isinstance(value, dict):
            bstack11l111ll11l_opy_[key] = bstack11l11l11lll_opy_(value)
          else:
            bstack11l111ll11l_opy_[key] = value
      return bstack11l111ll11l_opy_
    bstack11l111ll11l_opy_ = bstack11l11l11lll_opy_(config)
    return {
      bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮᯲ࠪ"): bstack11l111l1lll_opy_,
      bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡲࡦࡲࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱ᯳ࠫ"): json.dumps(bstack11l111ll11l_opy_)
    }
  except Exception as e:
    return {}
def bstack11l111ll111_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1ll1l11_opy_ (u"ࠩ࡯ࡳ࡬࠭᯴"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l111lll11_opy_ = os.path.join(log_dir, bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶࠫ᯵"))
  if not os.path.exists(bstack11l111lll11_opy_):
    bstack11l11l1111l_opy_ = {
      bstack1ll1l11_opy_ (u"ࠦ࡮ࡴࡩࡱࡣࡷ࡬ࠧ᯶"): str(inipath),
      bstack1ll1l11_opy_ (u"ࠧࡸ࡯ࡰࡶࡳࡥࡹ࡮ࠢ᯷"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬ᯸")), bstack1ll1l11_opy_ (u"ࠧࡸࠩ᯹")) as bstack11l11l1l111_opy_:
      bstack11l11l1l111_opy_.write(json.dumps(bstack11l11l1111l_opy_))
def bstack11l111llll1_opy_():
  try:
    bstack11l111lll11_opy_ = os.path.join(os.getcwd(), bstack1ll1l11_opy_ (u"ࠨ࡮ࡲ࡫ࠬ᯺"), bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨ᯻"))
    if os.path.exists(bstack11l111lll11_opy_):
      with open(bstack11l111lll11_opy_, bstack1ll1l11_opy_ (u"ࠪࡶࠬ᯼")) as bstack11l11l1l111_opy_:
        bstack11l11l11ll1_opy_ = json.load(bstack11l11l1l111_opy_)
      return bstack11l11l11ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡩࡱࡣࡷ࡬ࠬ᯽"), bstack1ll1l11_opy_ (u"ࠬ࠭᯾")), bstack11l11l11ll1_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡲࡰࡱࡷࡴࡦࡺࡨࠨ᯿"), bstack1ll1l11_opy_ (u"ࠧࠨᰀ"))
  except:
    pass
  return None, None
def bstack11l111l1ll1_opy_():
  try:
    bstack11l111lll11_opy_ = os.path.join(os.getcwd(), bstack1ll1l11_opy_ (u"ࠨ࡮ࡲ࡫ࠬᰁ"), bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨᰂ"))
    if os.path.exists(bstack11l111lll11_opy_):
      os.remove(bstack11l111lll11_opy_)
  except:
    pass
def bstack1l1l11l1l_opy_(config):
  from bstack_utils.helper import bstack11lll1111_opy_
  global bstack11l111l1l1l_opy_
  try:
    if config.get(bstack1ll1l11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬᰃ"), False):
      return
    uuid = os.getenv(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᰄ")) if os.getenv(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᰅ")) else bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣᰆ"))
    if not uuid or uuid == bstack1ll1l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᰇ"):
      return
    bstack11l111ll1l1_opy_ = [bstack1ll1l11_opy_ (u"ࠨࡴࡨࡵࡺ࡯ࡲࡦ࡯ࡨࡲࡹࡹ࠮ࡵࡺࡷࠫᰈ"), bstack1ll1l11_opy_ (u"ࠩࡓ࡭ࡵ࡬ࡩ࡭ࡧࠪᰉ"), bstack1ll1l11_opy_ (u"ࠪࡴࡾࡶࡲࡰ࡬ࡨࡧࡹ࠴ࡴࡰ࡯࡯ࠫᰊ"), bstack11l111l1l1l_opy_, bstack11l111l1l11_opy_]
    bstack11l11l111ll_opy_, root_path = bstack11l111llll1_opy_()
    if bstack11l11l111ll_opy_ != None:
      bstack11l111ll1l1_opy_.append(bstack11l11l111ll_opy_)
    if root_path != None:
      bstack11l111ll1l1_opy_.append(os.path.join(root_path, bstack1ll1l11_opy_ (u"ࠫࡨࡵ࡮ࡧࡶࡨࡷࡹ࠴ࡰࡺࠩᰋ")))
    bstack1l11l1ll1_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡲ࡯ࡨࡵ࠰ࠫᰌ") + uuid + bstack1ll1l11_opy_ (u"࠭࠮ࡵࡣࡵ࠲࡬ࢀࠧᰍ"))
    with tarfile.open(output_file, bstack1ll1l11_opy_ (u"ࠢࡸ࠼ࡪࡾࠧᰎ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11l111ll1l1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11l11l1l11l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack11l111ll1ll_opy_ = data.encode()
        tarinfo.size = len(bstack11l111ll1ll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack11l111ll1ll_opy_))
    bstack111l1111_opy_ = MultipartEncoder(
      fields= {
        bstack1ll1l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᰏ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1ll1l11_opy_ (u"ࠩࡵࡦࠬᰐ")), bstack1ll1l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰ࡺ࠰࡫ࡿ࡯ࡰࠨᰑ")),
        bstack1ll1l11_opy_ (u"ࠫࡨࡲࡩࡦࡰࡷࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᰒ"): uuid
      }
    )
    response = requests.post(
      bstack1ll1l11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡵࡱ࡮ࡲࡥࡩ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡦࡰ࡮࡫࡮ࡵ࠯࡯ࡳ࡬ࡹ࠯ࡶࡲ࡯ࡳࡦࡪࠢᰓ"),
      data=bstack111l1111_opy_,
      headers={bstack1ll1l11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬᰔ"): bstack111l1111_opy_.content_type},
      auth=(config[bstack1ll1l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᰕ")], config[bstack1ll1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᰖ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1ll1l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡷࡳࡰࡴࡧࡤࠡ࡮ࡲ࡫ࡸࡀࠠࠨᰗ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1ll1l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡰࡴ࡭ࡳ࠻ࠩᰘ") + str(e))
  finally:
    try:
      bstack1llll1l1111_opy_()
      bstack11l111l1ll1_opy_()
    except:
      pass