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
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1111l1ll11_opy_ import bstack1111l1l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll11l1ll_opy_ import bstack1lllllll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1llll_opy_ import bstack1lll1l1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1llllll_opy_ import bstack1lll1ll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll1l1_opy_ import bstack1lll1l1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1lll_opy_ import bstack1lllll1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lll11_opy_ import bstack1llll11llll_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import bstack1lllll1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llllll1_opy_ import bstack1llll11l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l1lll_opy_ import bstack1llll1l111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1l1ll1_opy_ import bstack1l1l1l1ll1_opy_, bstack11l1ll111_opy_, bstack11llll111l_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1lll1ll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1lllll11ll1_opy_ import bstack1ll1lllll11_opy_
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import bstack1111l1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1llll1ll1ll_opy_
from bstack_utils.helper import Notset, bstack1lllllll1ll_opy_, get_cli_dir, bstack1lll11l1l11_opy_, bstack1ll1ll1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1lll1lllll1_opy_ import bstack1lll11l1l1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1ll111_opy_ import bstack1l1111ll1l_opy_
from bstack_utils.helper import Notset, bstack1lllllll1ll_opy_, get_cli_dir, bstack1lll11l1l11_opy_, bstack1ll1ll1l_opy_, bstack1l1lllll1l_opy_, bstack1l11l1l1ll_opy_, bstack1ll11lll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll1l11ll_opy_, bstack1lll1l1l1l1_opy_, bstack1llllll1l11_opy_, bstack1ll1lllllll_opy_
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import bstack1111l1111l_opy_, bstack1111l11l1l_opy_, bstack11111l1ll1_opy_
from bstack_utils.constants import *
from bstack_utils import bstack11ll11llll_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1111lllll_opy_, bstack1lll11l1_opy_
logger = bstack11ll11llll_opy_.get_logger(__name__, bstack11ll11llll_opy_.bstack1llll11l111_opy_())
def bstack1llll11ll11_opy_(bs_config):
    bstack1lll1111ll1_opy_ = None
    bstack1lll11l11ll_opy_ = None
    try:
        bstack1lll11l11ll_opy_ = get_cli_dir()
        bstack1lll1111ll1_opy_ = bstack1lll11l1l11_opy_(bstack1lll11l11ll_opy_)
        bstack1llll111ll1_opy_ = bstack1lllllll1ll_opy_(bstack1lll1111ll1_opy_, bstack1lll11l11ll_opy_, bs_config)
        bstack1lll1111ll1_opy_ = bstack1llll111ll1_opy_ if bstack1llll111ll1_opy_ else bstack1lll1111ll1_opy_
        if not bstack1lll1111ll1_opy_:
            raise ValueError(bstack11111ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡘࡊࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡓࡅ࡙ࡎࠢဥ"))
    except Exception as ex:
        logger.debug(bstack11111ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡱࡧࡴࡦࡵࡷࠤࡧ࡯࡮ࡢࡴࡼࠤࢀࢃࠢဦ").format(ex))
        bstack1lll1111ll1_opy_ = os.environ.get(bstack11111ll_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠣဧ"))
        if bstack1lll1111ll1_opy_:
            logger.debug(bstack11111ll_opy_ (u"ࠨࡆࡢ࡮࡯࡭ࡳ࡭ࠠࡣࡣࡦ࡯ࠥࡺ࡯ࠡࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠤ࡫ࡸ࡯࡮ࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺ࠺ࠡࠤဨ") + str(bstack1lll1111ll1_opy_) + bstack11111ll_opy_ (u"ࠢࠣဩ"))
        else:
            logger.debug(bstack11111ll_opy_ (u"ࠣࡐࡲࠤࡻࡧ࡬ࡪࡦࠣࡗࡉࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡒࡄࡘࡍࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࡁࠠࡴࡧࡷࡹࡵࠦ࡭ࡢࡻࠣࡦࡪࠦࡩ࡯ࡥࡲࡱࡵࡲࡥࡵࡧ࠱ࠦဪ"))
    return bstack1lll1111ll1_opy_, bstack1lll11l11ll_opy_
bstack1lll1llll1l_opy_ = bstack11111ll_opy_ (u"ࠤ࠼࠽࠾࠿ࠢါ")
bstack1lll11l111l_opy_ = bstack11111ll_opy_ (u"ࠥࡶࡪࡧࡤࡺࠤာ")
bstack1lll111l1ll_opy_ = bstack11111ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣိ")
bstack1lllllll1l1_opy_ = bstack11111ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡒࡉࡔࡖࡈࡒࡤࡇࡄࡅࡔࠥီ")
bstack11ll1ll1_opy_ = bstack11111ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠤု")
bstack1llll1l1l11_opy_ = re.compile(bstack11111ll_opy_ (u"ࡲࠣࠪࡂ࡭࠮࠴ࠪࠩࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑࡼࡃࡕࠬ࠲࠯ࠨူ"))
bstack1llllll11l1_opy_ = bstack11111ll_opy_ (u"ࠣࡦࡨࡺࡪࡲ࡯ࡱ࡯ࡨࡲࡹࠨေ")
bstack1lllll11l11_opy_ = [
    bstack11l1ll111_opy_.bstack11111111l_opy_,
    bstack11l1ll111_opy_.CONNECT,
    bstack11l1ll111_opy_.bstack1l11ll11l_opy_,
]
class SDKCLI:
    _1lllll1ll11_opy_ = None
    process: Union[None, Any]
    bstack1llll11l11l_opy_: bool
    bstack1lll11llll1_opy_: bool
    bstack1lll1l111l1_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1lll1l11111_opy_: Union[None, grpc.Channel]
    bstack1lll1111l1l_opy_: str
    test_framework: TestFramework
    bstack1111l111l1_opy_: bstack1111l1l11l_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1llll1ll111_opy_: bstack1llll1l111l_opy_
    accessibility: bstack1lll1l1l11l_opy_
    bstack1l1l1ll111_opy_: bstack1l1111ll1l_opy_
    ai: bstack1lll1ll11ll_opy_
    bstack1llll1l11l1_opy_: bstack1lll1l1ll11_opy_
    bstack1lll1l11ll1_opy_: List[bstack1lllllll11l_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1lll11lll1l_opy_: Any
    bstack1llll1ll1l1_opy_: Dict[str, timedelta]
    bstack1lll1ll11l1_opy_: str
    bstack1111l1ll11_opy_: bstack1111l1l1ll_opy_
    def __new__(cls):
        if not cls._1lllll1ll11_opy_:
            cls._1lllll1ll11_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1lllll1ll11_opy_
    def __init__(self):
        self.process = None
        self.bstack1llll11l11l_opy_ = False
        self.bstack1lll1l11111_opy_ = None
        self.bstack1llll1l1111_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1lllllll1l1_opy_, None)
        self.bstack1lllll11l1l_opy_ = os.environ.get(bstack1lll111l1ll_opy_, bstack11111ll_opy_ (u"ࠤࠥဲ")) == bstack11111ll_opy_ (u"ࠥࠦဳ")
        self.bstack1lll11llll1_opy_ = False
        self.bstack1lll1l111l1_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1lll11lll1l_opy_ = None
        self.test_framework = None
        self.bstack1111l111l1_opy_ = None
        self.bstack1lll1111l1l_opy_=bstack11111ll_opy_ (u"ࠦࠧဴ")
        self.session_framework = None
        self.logger = bstack11ll11llll_opy_.get_logger(self.__class__.__name__, bstack11ll11llll_opy_.bstack1llll11l111_opy_())
        self.bstack1llll1ll1l1_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1111l1ll11_opy_ = bstack1111l1l1ll_opy_()
        self.bstack1llll1l1l1l_opy_ = None
        self.bstack1lll1ll1lll_opy_ = None
        self.bstack1llll1ll111_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1lll1l11ll1_opy_ = []
    def bstack1lllll1l1l_opy_(self):
        return os.environ.get(bstack11ll1ll1_opy_).lower().__eq__(bstack11111ll_opy_ (u"ࠧࡺࡲࡶࡧࠥဵ"))
    def is_enabled(self, config):
        if bstack11111ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪံ") in config and str(config[bstack11111ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨ့ࠫ")]).lower() != bstack11111ll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧး"):
            return False
        bstack1lll111lll1_opy_ = [bstack11111ll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤ္"), bstack11111ll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪ်ࠢ")]
        bstack1lll11l1111_opy_ = config.get(bstack11111ll_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢျ")) in bstack1lll111lll1_opy_ or os.environ.get(bstack11111ll_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ြ")) in bstack1lll111lll1_opy_
        os.environ[bstack11111ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤࡏࡓࡠࡔࡘࡒࡓࡏࡎࡈࠤွ")] = str(bstack1lll11l1111_opy_) # bstack1lll111l1l1_opy_ bstack1lllll11lll_opy_ VAR to bstack1lll111l11l_opy_ is binary running
        return bstack1lll11l1111_opy_
    def bstack11ll11l1_opy_(self):
        for event in bstack1lllll11l11_opy_:
            bstack1l1l1l1ll1_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1l1l1l1ll1_opy_.logger.debug(bstack11111ll_opy_ (u"ࠢࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂࠦ࠽࠿ࠢࡾࡥࡷ࡭ࡳࡾࠢࠥှ") + str(kwargs) + bstack11111ll_opy_ (u"ࠣࠤဿ"))
            )
        bstack1l1l1l1ll1_opy_.register(bstack11l1ll111_opy_.bstack11111111l_opy_, self.__1ll1lllll1l_opy_)
        bstack1l1l1l1ll1_opy_.register(bstack11l1ll111_opy_.CONNECT, self.__1lll1lll1l1_opy_)
        bstack1l1l1l1ll1_opy_.register(bstack11l1ll111_opy_.bstack1l11ll11l_opy_, self.__1lll11ll1ll_opy_)
        bstack1l1l1l1ll1_opy_.register(bstack11l1ll111_opy_.bstack1l1l1111l_opy_, self.__1lll1ll111l_opy_)
    def bstack1l11l1l1l1_opy_(self):
        return not self.bstack1lllll11l1l_opy_ and os.environ.get(bstack1lll111l1ll_opy_, bstack11111ll_opy_ (u"ࠤࠥ၀")) != bstack11111ll_opy_ (u"ࠥࠦ၁")
    def is_running(self):
        if self.bstack1lllll11l1l_opy_:
            return self.bstack1llll11l11l_opy_
        else:
            return bool(self.bstack1lll1l11111_opy_)
    def bstack1lll1l11lll_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1lll1l11ll1_opy_) and cli.is_running()
    def __1llll111l11_opy_(self, bstack1llll1l1ll1_opy_=10):
        if self.bstack1llll1l1111_opy_:
            return
        bstack11ll111l1l_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1lllllll1l1_opy_, self.cli_listen_addr)
        self.logger.debug(bstack11111ll_opy_ (u"ࠦࡠࠨ၂") + str(id(self)) + bstack11111ll_opy_ (u"ࠧࡣࠠࡤࡱࡱࡲࡪࡩࡴࡪࡰࡪࠦ၃"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack11111ll_opy_ (u"ࠨࡧࡳࡲࡦ࠲ࡪࡴࡡࡣ࡮ࡨࡣ࡭ࡺࡴࡱࡡࡳࡶࡴࡾࡹࠣ၄"), 0), (bstack11111ll_opy_ (u"ࠢࡨࡴࡳࡧ࠳࡫࡮ࡢࡤ࡯ࡩࡤ࡮ࡴࡵࡲࡶࡣࡵࡸ࡯ࡹࡻࠥ၅"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1llll1l1ll1_opy_)
        self.bstack1lll1l11111_opy_ = channel
        self.bstack1llll1l1111_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1lll1l11111_opy_)
        self.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡣࡰࡰࡱࡩࡨࡺࠢ၆"), datetime.now() - bstack11ll111l1l_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1lllllll1l1_opy_] = self.cli_listen_addr
        self.logger.debug(bstack11111ll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧ࠾ࠥ࡯ࡳࡠࡥ࡫࡭ࡱࡪ࡟ࡱࡴࡲࡧࡪࡹࡳ࠾ࠤ၇") + str(self.bstack1l11l1l1l1_opy_()) + bstack11111ll_opy_ (u"ࠥࠦ၈"))
    def __1lll11ll1ll_opy_(self, event_name):
        if self.bstack1l11l1l1l1_opy_():
            self.logger.debug(bstack11111ll_opy_ (u"ࠦࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡹࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡄࡎࡌࠦ၉"))
        self.__1lll1l11l11_opy_()
    def __1lll1ll111l_opy_(self, event_name, bstack1lll1lll111_opy_ = None, bstack1l11l111ll_opy_=1):
        if bstack1l11l111ll_opy_ == 1:
            self.logger.error(bstack11111ll_opy_ (u"࡙ࠧ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠧ၊"))
        bstack1lllll1l1l1_opy_ = Path(bstack1lllll1l111_opy_ (u"ࠨࡻࡴࡧ࡯ࡪ࠳ࡩ࡬ࡪࡡࡧ࡭ࡷࢃ࠯ࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࡴ࠰࡭ࡷࡴࡴࠢ။"))
        if self.bstack1lll11l11ll_opy_ and bstack1lllll1l1l1_opy_.exists():
            with open(bstack1lllll1l1l1_opy_, bstack11111ll_opy_ (u"ࠧࡳࠩ၌"), encoding=bstack11111ll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ၍")) as fp:
                data = json.load(fp)
                try:
                    bstack1l1lllll1l_opy_(bstack11111ll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ၎"), bstack1l11l1l1ll_opy_(bstack111ll11ll_opy_), data, {
                        bstack11111ll_opy_ (u"ࠪࡥࡺࡺࡨࠨ၏"): (self.config[bstack11111ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ၐ")], self.config[bstack11111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨၑ")])
                    })
                except Exception as e:
                    logger.debug(bstack1lll11l1_opy_.format(str(e)))
            bstack1lllll1l1l1_opy_.unlink()
        sys.exit(bstack1l11l111ll_opy_)
    @measure(event_name=EVENTS.bstack1llll1111l1_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def __1ll1lllll1l_opy_(self, event_name: str, data):
        from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll111l1l_opy_
        self.bstack1lll1111l1l_opy_, self.bstack1lll11l11ll_opy_ = bstack1llll11ll11_opy_(data.bs_config)
        os.environ[bstack11111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡝ࡒࡊࡖࡄࡆࡑࡋ࡟ࡅࡋࡕࠫၒ")] = self.bstack1lll11l11ll_opy_
        if not self.bstack1lll1111l1l_opy_ or not self.bstack1lll11l11ll_opy_:
            raise ValueError(bstack11111ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡶ࡫ࡩ࡙ࠥࡄࡌࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾࠨၓ"))
        if self.bstack1l11l1l1l1_opy_():
            self.__1lll1lll1l1_opy_(event_name, bstack11llll111l_opy_())
            return
        try:
            bstack1llll111l1l_opy_.end(EVENTS.bstack11lll1ll1l_opy_.value, EVENTS.bstack11lll1ll1l_opy_.value + bstack11111ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣၔ"), EVENTS.bstack11lll1ll1l_opy_.value + bstack11111ll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢၕ"), status=True, failure=None, test_name=None)
            logger.debug(bstack11111ll_opy_ (u"ࠥࡇࡴࡳࡰ࡭ࡧࡷࡩ࡙ࠥࡄࡌࠢࡖࡩࡹࡻࡰ࠯ࠤၖ"))
        except Exception as e:
            logger.debug(bstack11111ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࢁࡽࠣၗ").format(e))
        start = datetime.now()
        is_started = self.__1lllll111l1_opy_()
        self.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠧࡹࡰࡢࡹࡱࡣࡹ࡯࡭ࡦࠤၘ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1llll111l11_opy_()
            self.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧၙ"), datetime.now() - start)
            start = datetime.now()
            self.__1lll1l1ll1l_opy_(data)
            self.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧၚ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1llllll1ll1_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def __1lll1lll1l1_opy_(self, event_name: str, data: bstack11llll111l_opy_):
        if not self.bstack1l11l1l1l1_opy_():
            self.logger.debug(bstack11111ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡨࡵ࡮࡯ࡧࡦࡸ࠿ࠦ࡮ࡰࡶࠣࡥࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷࠧၛ"))
            return
        bin_session_id = os.environ.get(bstack1lll111l1ll_opy_)
        start = datetime.now()
        self.__1llll111l11_opy_()
        self.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࡢࡸ࡮ࡳࡥࠣၜ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack11111ll_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡩࡩࠦࡴࡰࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡈࡒࡉࠡࠤၝ") + str(bin_session_id) + bstack11111ll_opy_ (u"ࠦࠧၞ"))
        start = datetime.now()
        self.__1lllll1l1ll_opy_()
        self.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡺࡩ࡮ࡧࠥၟ"), datetime.now() - start)
    def __1lll1l111ll_opy_(self):
        if not self.bstack1llll1l1111_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack11111ll_opy_ (u"ࠨࡣࡢࡰࡱࡳࡹࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࠢࡰࡳࡩࡻ࡬ࡦࡵࠥၠ"))
            return
        bstack1lll1l11l1l_opy_ = {
            bstack11111ll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦၡ"): (bstack1lllll1ll1l_opy_, bstack1llll11l1l1_opy_, bstack1llll1ll1ll_opy_),
            bstack11111ll_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥၢ"): (bstack1lllll1l11l_opy_, bstack1llll11llll_opy_, bstack1ll1lllll11_opy_),
        }
        if not self.bstack1llll1l1l1l_opy_ and self.session_framework in bstack1lll1l11l1l_opy_:
            bstack1lll111ll1l_opy_, bstack1lllllll111_opy_, bstack1lll1l1lll1_opy_ = bstack1lll1l11l1l_opy_[self.session_framework]
            bstack1lll1llll11_opy_ = bstack1lllllll111_opy_()
            self.bstack1lll1ll1lll_opy_ = bstack1lll1llll11_opy_
            self.bstack1llll1l1l1l_opy_ = bstack1lll1l1lll1_opy_
            self.bstack1lll1l11ll1_opy_.append(bstack1lll1llll11_opy_)
            self.bstack1lll1l11ll1_opy_.append(bstack1lll111ll1l_opy_(self.bstack1lll1ll1lll_opy_))
        if not self.bstack1llll1ll111_opy_ and self.config_observability and self.config_observability.success: # bstack1llllll1l1l_opy_
            self.bstack1llll1ll111_opy_ = bstack1llll1l111l_opy_(self.bstack1llll1l1l1l_opy_, self.bstack1lll1ll1lll_opy_) # bstack1lll1111lll_opy_
            self.bstack1lll1l11ll1_opy_.append(self.bstack1llll1ll111_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1lll1l1l11l_opy_(self.bstack1llll1l1l1l_opy_, self.bstack1lll1ll1lll_opy_)
            self.bstack1lll1l11ll1_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack11111ll_opy_ (u"ࠤࡶࡩࡱ࡬ࡈࡦࡣ࡯ࠦၣ"), False) == True:
            self.ai = bstack1lll1ll11ll_opy_()
            self.bstack1lll1l11ll1_opy_.append(self.ai)
        if not self.percy and self.bstack1lll11lll1l_opy_ and self.bstack1lll11lll1l_opy_.success:
            self.percy = bstack1lll1l1ll11_opy_(self.bstack1lll11lll1l_opy_)
            self.bstack1lll1l11ll1_opy_.append(self.percy)
        for mod in self.bstack1lll1l11ll1_opy_:
            if not mod.bstack1llll11ll1l_opy_():
                mod.configure(self.bstack1llll1l1111_opy_, self.config, self.cli_bin_session_id, self.bstack1111l1ll11_opy_)
    def __1lll1ll1111_opy_(self):
        for mod in self.bstack1lll1l11ll1_opy_:
            if mod.bstack1llll11ll1l_opy_():
                mod.configure(self.bstack1llll1l1111_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1lll11lllll_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def __1lll1l1ll1l_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1lll11llll1_opy_:
            return
        self.__1lll1111111_opy_(data)
        bstack11ll111l1l_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack11111ll_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࠥၤ")
        req.sdk_language = bstack11111ll_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦၥ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1llll1l1l11_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack11111ll_opy_ (u"ࠧࡡࠢၦ") + str(id(self)) + bstack11111ll_opy_ (u"ࠨ࡝ࠡ࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡵࡷࡥࡷࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧၧ"))
            r = self.bstack1llll1l1111_opy_.StartBinSession(req)
            self.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡴࡢࡴࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤၨ"), datetime.now() - bstack11ll111l1l_opy_)
            os.environ[bstack1lll111l1ll_opy_] = r.bin_session_id
            self.__1lllll1111l_opy_(r)
            self.__1lll1l111ll_opy_()
            self.bstack1111l1ll11_opy_.start()
            self.bstack1lll11llll1_opy_ = True
            self.logger.debug(bstack11111ll_opy_ (u"ࠣ࡝ࠥၩ") + str(id(self)) + bstack11111ll_opy_ (u"ࠤࡠࠤࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠢၪ"))
        except grpc.bstack1llll1llll1_opy_ as bstack1lll11111ll_opy_:
            self.logger.error(bstack11111ll_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡷ࡭ࡲ࡫࡯ࡦࡷࡷ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧၫ") + str(bstack1lll11111ll_opy_) + bstack11111ll_opy_ (u"ࠦࠧၬ"))
            traceback.print_exc()
            raise bstack1lll11111ll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤၭ") + str(e) + bstack11111ll_opy_ (u"ࠨࠢၮ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1lll1ll1ll1_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def __1lllll1l1ll_opy_(self):
        if not self.bstack1l11l1l1l1_opy_() or not self.cli_bin_session_id or self.bstack1lll1l111l1_opy_:
            return
        bstack11ll111l1l_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack11111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧၯ"), bstack11111ll_opy_ (u"ࠨ࠲ࠪၰ")))
        try:
            self.logger.debug(bstack11111ll_opy_ (u"ࠤ࡞ࠦၱ") + str(id(self)) + bstack11111ll_opy_ (u"ࠥࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧၲ"))
            r = self.bstack1llll1l1111_opy_.ConnectBinSession(req)
            self.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡦࡳࡳࡴࡥࡤࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣၳ"), datetime.now() - bstack11ll111l1l_opy_)
            self.__1lllll1111l_opy_(r)
            self.__1lll1l111ll_opy_()
            self.bstack1111l1ll11_opy_.start()
            self.bstack1lll1l111l1_opy_ = True
            self.logger.debug(bstack11111ll_opy_ (u"ࠧࡡࠢၴ") + str(id(self)) + bstack11111ll_opy_ (u"ࠨ࡝ࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡨࡨࠧၵ"))
        except grpc.bstack1llll1llll1_opy_ as bstack1lll11111ll_opy_:
            self.logger.error(bstack11111ll_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡴࡪ࡯ࡨࡳࡪࡻࡴ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤၶ") + str(bstack1lll11111ll_opy_) + bstack11111ll_opy_ (u"ࠣࠤၷ"))
            traceback.print_exc()
            raise bstack1lll11111ll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨၸ") + str(e) + bstack11111ll_opy_ (u"ࠥࠦၹ"))
            traceback.print_exc()
            raise e
    def __1lllll1111l_opy_(self, r):
        self.bstack1llll111111_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack11111ll_opy_ (u"ࠦࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡵࡨࡶࡻ࡫ࡲࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥၺ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack11111ll_opy_ (u"ࠧ࡫࡭ࡱࡶࡼࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫ࡵࡵ࡯ࡦࠥၻ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack11111ll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡪࡸࡣࡺࠢ࡬ࡷࠥࡹࡥ࡯ࡶࠣࡳࡳࡲࡹࠡࡣࡶࠤࡵࡧࡲࡵࠢࡲࡪࠥࡺࡨࡦࠢࠥࡇࡴࡴ࡮ࡦࡥࡷࡆ࡮ࡴࡓࡦࡵࡶ࡭ࡴࡴࠬࠣࠢࡤࡲࡩࠦࡴࡩ࡫ࡶࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡩࡴࠢࡤࡰࡸࡵࠠࡶࡵࡨࡨࠥࡨࡹࠡࡕࡷࡥࡷࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡦࡴࡨࡪࡴࡸࡥ࠭ࠢࡑࡳࡳ࡫ࠠࡩࡣࡱࡨࡱ࡯࡮ࡨࠢ࡬ࡷࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣၼ")
        self.bstack1lll11lll1l_opy_ = getattr(r, bstack11111ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ၽ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack11111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬၾ")] = self.config_testhub.jwt
        os.environ[bstack11111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧၿ")] = self.config_testhub.build_hashed_id
    def bstack1lll1l1l1ll_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1llll11l11l_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1lll1ll1l1l_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1lll1ll1l1l_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1lll1l1l1ll_opy_(event_name=EVENTS.bstack1llllll111l_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def __1lllll111l1_opy_(self, bstack1llll1l1ll1_opy_=10):
        if self.bstack1llll11l11l_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠥࡷࡹࡧࡲࡵ࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠧႀ"))
            return True
        self.logger.debug(bstack11111ll_opy_ (u"ࠦࡸࡺࡡࡳࡶࠥႁ"))
        if os.getenv(bstack11111ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡇࡑ࡚ࠧႂ")) == bstack1llllll11l1_opy_:
            self.cli_bin_session_id = bstack1llllll11l1_opy_
            self.cli_listen_addr = bstack11111ll_opy_ (u"ࠨࡵ࡯࡫ࡻ࠾࠴ࡺ࡭ࡱ࠱ࡶࡨࡰ࠳ࡰ࡭ࡣࡷࡪࡴࡸ࡭࠮ࠧࡶ࠲ࡸࡵࡣ࡬ࠤႃ") % (self.cli_bin_session_id)
            self.bstack1llll11l11l_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1lll1111l1l_opy_, bstack11111ll_opy_ (u"ࠢࡴࡦ࡮ࠦႄ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1llll1lll1l_opy_ compat for text=True in bstack1llll11111l_opy_ python
            encoding=bstack11111ll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢႅ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1llll1lllll_opy_ = threading.Thread(target=self.__1lll1l1l111_opy_, args=(bstack1llll1l1ll1_opy_,))
        bstack1llll1lllll_opy_.start()
        bstack1llll1lllll_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack11111ll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡵࡳࡥࡼࡴ࠺ࠡࡴࡨࡸࡺࡸ࡮ࡤࡱࡧࡩࡂࢁࡳࡦ࡮ࡩ࠲ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡸࡥࡵࡷࡵࡲࡨࡵࡤࡦࡿࠣࡳࡺࡺ࠽ࡼࡵࡨࡰ࡫࠴ࡰࡳࡱࡦࡩࡸࡹ࠮ࡴࡶࡧࡳࡺࡺ࠮ࡳࡧࡤࡨ࠭࠯ࡽࠡࡧࡵࡶࡂࠨႆ") + str(self.process.stderr.read()) + bstack11111ll_opy_ (u"ࠥࠦႇ"))
        if not self.bstack1llll11l11l_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠦࡠࠨႈ") + str(id(self)) + bstack11111ll_opy_ (u"ࠧࡣࠠࡤ࡮ࡨࡥࡳࡻࡰࠣႉ"))
            self.__1lll1l11l11_opy_()
        self.logger.debug(bstack11111ll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡶࡲࡰࡥࡨࡷࡸࡥࡲࡦࡣࡧࡽ࠿ࠦࠢႊ") + str(self.bstack1llll11l11l_opy_) + bstack11111ll_opy_ (u"ࠢࠣႋ"))
        return self.bstack1llll11l11l_opy_
    def __1lll1l1l111_opy_(self, bstack1llll1ll11l_opy_=10):
        bstack1lll11l11l1_opy_ = time.time()
        while self.process and time.time() - bstack1lll11l11l1_opy_ < bstack1llll1ll11l_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack11111ll_opy_ (u"ࠣ࡫ࡧࡁࠧႌ") in line:
                    self.cli_bin_session_id = line.split(bstack11111ll_opy_ (u"ࠤ࡬ࡨࡂࠨႍ"))[-1:][0].strip()
                    self.logger.debug(bstack11111ll_opy_ (u"ࠥࡧࡱ࡯࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠻ࠤႎ") + str(self.cli_bin_session_id) + bstack11111ll_opy_ (u"ࠦࠧႏ"))
                    continue
                if bstack11111ll_opy_ (u"ࠧࡲࡩࡴࡶࡨࡲࡂࠨ႐") in line:
                    self.cli_listen_addr = line.split(bstack11111ll_opy_ (u"ࠨ࡬ࡪࡵࡷࡩࡳࡃࠢ႑"))[-1:][0].strip()
                    self.logger.debug(bstack11111ll_opy_ (u"ࠢࡤ࡮࡬ࡣࡱ࡯ࡳࡵࡧࡱࡣࡦࡪࡤࡳ࠼ࠥ႒") + str(self.cli_listen_addr) + bstack11111ll_opy_ (u"ࠣࠤ႓"))
                    continue
                if bstack11111ll_opy_ (u"ࠤࡳࡳࡷࡺ࠽ࠣ႔") in line:
                    port = line.split(bstack11111ll_opy_ (u"ࠥࡴࡴࡸࡴ࠾ࠤ႕"))[-1:][0].strip()
                    self.logger.debug(bstack11111ll_opy_ (u"ࠦࡵࡵࡲࡵ࠼ࠥ႖") + str(port) + bstack11111ll_opy_ (u"ࠧࠨ႗"))
                    continue
                if line.strip() == bstack1lll11l111l_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack11111ll_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡏࡏࡠࡕࡗࡖࡊࡇࡍࠣ႘"), bstack11111ll_opy_ (u"ࠢ࠲ࠤ႙")) == bstack11111ll_opy_ (u"ࠣ࠳ࠥႚ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1llll11l11l_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack11111ll_opy_ (u"ࠤࡨࡶࡷࡵࡲ࠻ࠢࠥႛ") + str(e) + bstack11111ll_opy_ (u"ࠥࠦႜ"))
        return False
    @measure(event_name=EVENTS.bstack1lll11l1ll1_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def __1lll1l11l11_opy_(self):
        if self.bstack1lll1l11111_opy_:
            self.bstack1111l1ll11_opy_.stop()
            start = datetime.now()
            if self.bstack1ll1llll1ll_opy_():
                self.cli_bin_session_id = None
                if self.bstack1lll1l111l1_opy_:
                    self.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠦࡸࡺ࡯ࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣႝ"), datetime.now() - start)
                else:
                    self.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠧࡹࡴࡰࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤ႞"), datetime.now() - start)
            self.__1lll1ll1111_opy_()
            start = datetime.now()
            self.bstack1lll1l11111_opy_.close()
            self.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠨࡤࡪࡵࡦࡳࡳࡴࡥࡤࡶࡢࡸ࡮ࡳࡥࠣ႟"), datetime.now() - start)
            self.bstack1lll1l11111_opy_ = None
        if self.process:
            self.logger.debug(bstack11111ll_opy_ (u"ࠢࡴࡶࡲࡴࠧႠ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠣ࡭࡬ࡰࡱࡥࡴࡪ࡯ࡨࠦႡ"), datetime.now() - start)
            self.process = None
            if self.bstack1lllll11l1l_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1l1llll1ll_opy_()
                self.logger.info(
                    bstack11111ll_opy_ (u"ࠤ࡙࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠧႢ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack11111ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩႣ")] = self.config_testhub.build_hashed_id
        self.bstack1llll11l11l_opy_ = False
    def __1lll1111111_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack11111ll_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨႤ")] = selenium.__version__
            data.frameworks.append(bstack11111ll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢႥ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack11111ll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥႦ")] = __version__
            data.frameworks.append(bstack11111ll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦႧ"))
        except:
            pass
    def bstack1lllll111ll_opy_(self, hub_url: str, platform_index: int, bstack11ll1l111l_opy_: Any):
        if self.bstack1111l111l1_opy_:
            self.logger.debug(bstack11111ll_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠢࡶࡩࡹࡻࡰࠡࡵࡨࡰࡪࡴࡩࡶ࡯࠽ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡹࡥࡵࠢࡸࡴࠧႨ"))
            return
        try:
            bstack11ll111l1l_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack11111ll_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦႩ")
            self.bstack1111l111l1_opy_ = bstack1ll1lllll11_opy_(
                cli.config.get(bstack11111ll_opy_ (u"ࠥ࡬ࡺࡨࡕࡳ࡮ࠥႪ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1lll111ll11_opy_={bstack11111ll_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡣࡴࡶࡴࡪࡱࡱࡷࡤ࡬ࡲࡰ࡯ࡢࡧࡦࡶࡳࠣႫ"): bstack11ll1l111l_opy_}
            )
            def bstack1lllll1lll1_opy_(self):
                return
            if self.config.get(bstack11111ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠢႬ"), True):
                Service.start = bstack1lllll1lll1_opy_
                Service.stop = bstack1lllll1lll1_opy_
            def get_accessibility_results(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results(driver, framework_name=framework)
            def get_accessibility_results_summary(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results_summary(driver, framework_name=framework)
            def perform_scan(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.perform_scan(driver, method=None, framework_name=framework)
            WebDriver.getAccessibilityResults = get_accessibility_results
            WebDriver.get_accessibility_results = get_accessibility_results
            WebDriver.getAccessibilityResultsSummary = get_accessibility_results_summary
            WebDriver.get_accessibility_results_summary = get_accessibility_results_summary
            WebDriver.upload_attachment = staticmethod(bstack1l1111ll1l_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1lll11l1l1l_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢႭ"), datetime.now() - bstack11ll111l1l_opy_)
        except Exception as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡶࡩࡱ࡫࡮ࡪࡷࡰ࠾ࠥࠨႮ") + str(e) + bstack11111ll_opy_ (u"ࠣࠤႯ"))
    def bstack1lllll11111_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack11l11l11l_opy_
            self.bstack1111l111l1_opy_ = bstack1llll1ll1ll_opy_(
                platform_index,
                framework_name=bstack11111ll_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨႰ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠼ࠣࠦႱ") + str(e) + bstack11111ll_opy_ (u"ࠦࠧႲ"))
            pass
    def bstack1lll11ll111_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack11111ll_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠦࡳࡦࡶࡸࡴࠥࡶࡹࡵࡧࡶࡸ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡴࡧࡷࠤࡺࡶࠢႳ"))
            return
        if bstack1ll1ll1l_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack11111ll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨႴ"): pytest.__version__ }, [bstack11111ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦႵ")], self.bstack1111l1ll11_opy_, self.bstack1llll1l1111_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1lll1ll1l11_opy_({ bstack11111ll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣႶ"): pytest.__version__ }, [bstack11111ll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤႷ")], self.bstack1111l1ll11_opy_, self.bstack1llll1l1111_opy_)
        except Exception as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶࡹࡵࡧࡶࡸ࠿ࠦࠢႸ") + str(e) + bstack11111ll_opy_ (u"ࠦࠧႹ"))
        self.bstack1llll1111ll_opy_()
    def bstack1llll1111ll_opy_(self):
        if not self.bstack1lllll1l1l_opy_():
            return
        bstack1l1ll1l11l_opy_ = None
        def bstack111l1l1l_opy_(config, startdir):
            return bstack11111ll_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿࠥႺ").format(bstack11111ll_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧႻ"))
        def bstack1lll1lll1_opy_():
            return
        def bstack1ll11lll1l_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack11111ll_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧႼ"):
                return bstack11111ll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢႽ")
            else:
                return bstack1l1ll1l11l_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1l1ll1l11l_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack111l1l1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1lll1lll1_opy_
            Config.getoption = bstack1ll11lll1l_opy_
        except Exception as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡵࡥ࡫ࠤࡵࡿࡴࡦࡵࡷࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡦࡰࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠼ࠣࠦႾ") + str(e) + bstack11111ll_opy_ (u"ࠥࠦႿ"))
    def bstack1lll1lll11l_opy_(self):
        bstack1llll111lll_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1llll111lll_opy_, dict):
            if cli.config_observability:
                bstack1llll111lll_opy_.update(
                    {bstack11111ll_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦჀ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack11111ll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹ࡟ࡵࡱࡢࡻࡷࡧࡰࠣჁ") in accessibility.get(bstack11111ll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢჂ"), {}):
                    bstack1lll111111l_opy_ = accessibility.get(bstack11111ll_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣჃ"))
                    bstack1lll111111l_opy_.update({ bstack11111ll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠤჄ"): bstack1lll111111l_opy_.pop(bstack11111ll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡣࡹࡵ࡟ࡸࡴࡤࡴࠧჅ")) })
                bstack1llll111lll_opy_.update({bstack11111ll_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥ჆"): accessibility })
        return bstack1llll111lll_opy_
    @measure(event_name=EVENTS.bstack1llll1lll11_opy_, stage=STAGE.bstack1l11111ll1_opy_)
    def bstack1ll1llll1ll_opy_(self, bstack1lll11ll11l_opy_: str = None, bstack1lll11l1lll_opy_: str = None, bstack1l11l111ll_opy_: int = None):
        if not self.cli_bin_session_id or not self.bstack1llll1l1111_opy_:
            return
        bstack11ll111l1l_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if bstack1l11l111ll_opy_:
            req.bstack1l11l111ll_opy_ = bstack1l11l111ll_opy_
        if bstack1lll11ll11l_opy_:
            req.bstack1lll11ll11l_opy_ = bstack1lll11ll11l_opy_
        if bstack1lll11l1lll_opy_:
            req.bstack1lll11l1lll_opy_ = bstack1lll11l1lll_opy_
        try:
            r = self.bstack1llll1l1111_opy_.StopBinSession(req)
            self.bstack1l1ll11ll_opy_(bstack11111ll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡸࡴࡶ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧჇ"), datetime.now() - bstack11ll111l1l_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1l1ll11ll_opy_(self, key: str, value: timedelta):
        tag = bstack11111ll_opy_ (u"ࠧࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷࠧ჈") if self.bstack1l11l1l1l1_opy_() else bstack11111ll_opy_ (u"ࠨ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷࠧ჉")
        self.bstack1llll1ll1l1_opy_[bstack11111ll_opy_ (u"ࠢ࠻ࠤ჊").join([tag + bstack11111ll_opy_ (u"ࠣ࠯ࠥ჋") + str(id(self)), key])] += value
    def bstack1l1llll1ll_opy_(self):
        if not os.getenv(bstack11111ll_opy_ (u"ࠤࡇࡉࡇ࡛ࡇࡠࡒࡈࡖࡋࠨ჌"), bstack11111ll_opy_ (u"ࠥ࠴ࠧჍ")) == bstack11111ll_opy_ (u"ࠦ࠶ࠨ჎"):
            return
        bstack1lll111llll_opy_ = dict()
        bstack11111llll1_opy_ = []
        if self.test_framework:
            bstack11111llll1_opy_.extend(list(self.test_framework.bstack11111llll1_opy_.values()))
        if self.bstack1111l111l1_opy_:
            bstack11111llll1_opy_.extend(list(self.bstack1111l111l1_opy_.bstack11111llll1_opy_.values()))
        for instance in bstack11111llll1_opy_:
            if not instance.platform_index in bstack1lll111llll_opy_:
                bstack1lll111llll_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1lll111llll_opy_[instance.platform_index]
            for k, v in instance.bstack1lll1111l11_opy_().items():
                report[k] += v
                report[k.split(bstack11111ll_opy_ (u"ࠧࡀࠢ჏"))[0]] += v
        bstack1lll1lll1ll_opy_ = sorted([(k, v) for k, v in self.bstack1llll1ll1l1_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1lll111l111_opy_ = 0
        for r in bstack1lll1lll1ll_opy_:
            bstack1lll1l1111l_opy_ = r[1].total_seconds()
            bstack1lll111l111_opy_ += bstack1lll1l1111l_opy_
            self.logger.debug(bstack11111ll_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡣ࡭࡫࠽ࡿࡷࡡ࠰࡞ࡿࡀࠦა") + str(bstack1lll1l1111l_opy_) + bstack11111ll_opy_ (u"ࠢࠣბ"))
        self.logger.debug(bstack11111ll_opy_ (u"ࠣ࠯࠰ࠦგ"))
        bstack1lll11111l1_opy_ = []
        for platform_index, report in bstack1lll111llll_opy_.items():
            bstack1lll11111l1_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1lll11111l1_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack11lll11l_opy_ = set()
        bstack1llllll1111_opy_ = 0
        for r in bstack1lll11111l1_opy_:
            bstack1lll1l1111l_opy_ = r[2].total_seconds()
            bstack1llllll1111_opy_ += bstack1lll1l1111l_opy_
            bstack11lll11l_opy_.add(r[0])
            self.logger.debug(bstack11111ll_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡷࡩࡸࡺ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠯ࡾࡶࡠ࠶࡝ࡾ࠼ࡾࡶࡠ࠷࡝ࡾ࠿ࠥდ") + str(bstack1lll1l1111l_opy_) + bstack11111ll_opy_ (u"ࠥࠦე"))
        if self.bstack1l11l1l1l1_opy_():
            self.logger.debug(bstack11111ll_opy_ (u"ࠦ࠲࠳ࠢვ"))
            self.logger.debug(bstack11111ll_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡩ࡬ࡪ࠼ࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠿ࡾࡸࡴࡺࡡ࡭ࡡࡦࡰ࡮ࢃࠠࡵࡧࡶࡸ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡳ࠮ࡽࡶࡸࡷ࠮ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠫࢀࡁࠧზ") + str(bstack1llllll1111_opy_) + bstack11111ll_opy_ (u"ࠨࠢთ"))
        else:
            self.logger.debug(bstack11111ll_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡤ࡮࡬࠾ࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵࡀࠦი") + str(bstack1lll111l111_opy_) + bstack11111ll_opy_ (u"ࠣࠤკ"))
        self.logger.debug(bstack11111ll_opy_ (u"ࠤ࠰࠱ࠧლ"))
    def bstack1llll111111_opy_(self, r):
        if r is not None and getattr(r, bstack11111ll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࠫმ"), None) and getattr(r.testhub, bstack11111ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫნ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack11111ll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦო")))
            for bstack1lll1l1llll_opy_, err in errors.items():
                if err[bstack11111ll_opy_ (u"࠭ࡴࡺࡲࡨࠫპ")] == bstack11111ll_opy_ (u"ࠧࡪࡰࡩࡳࠬჟ"):
                    self.logger.info(err[bstack11111ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩრ")])
                else:
                    self.logger.error(err[bstack11111ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪს")])
cli = SDKCLI()