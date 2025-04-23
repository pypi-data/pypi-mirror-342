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
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll11l111_opy_ import bstack1ll111ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack11111lllll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1ll1l_opy_ import bstack1l11ll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1l11lllll1l_opy_ import bstack1l11lll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1111l1111l_opy_ import bstack111111ll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll111l1_opy_ import bstack1ll1ll1ll11_opy_
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import bstack1111l11lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l11l_opy_ import bstack1lll1ll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll111ll11_opy_ import bstack1lll11ll11l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l1ll1_opy_ import bstack1llllll11ll_opy_
from browserstack_sdk.sdk_cli.bstack11ll11111l_opy_ import bstack11ll11111l_opy_, bstack11lll1l1l1_opy_, bstack1l1ll1l1ll_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1l1ll1l1ll1_opy_ import bstack1l1ll1ll11l_opy_
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import bstack1111111ll1_opy_
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import bstack1ll1l1l1111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11lll_opy_ import bstack1lll1l111l1_opy_
from bstack_utils.helper import Notset, bstack1l11ll11ll1_opy_, get_cli_dir, bstack1l11l1ll1ll_opy_, bstack1l1l1ll1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1ll1111111l_opy_ import bstack1ll1111l1ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1111l1l1_opy_ import bstack11l1ll11l_opy_
from bstack_utils.helper import Notset, bstack1l11ll11ll1_opy_, get_cli_dir, bstack1l11l1ll1ll_opy_, bstack1l1l1ll1l_opy_, bstack11lllll1ll_opy_, bstack1ll1l11l11_opy_, bstack11l11lll1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack11111ll1l1_opy_, bstack11111l111l_opy_, bstack1111111l1l_opy_, bstack111111llll_opy_
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import bstack1111l1lll1_opy_, bstack11111l1lll_opy_, bstack111111ll1l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1ll1lllll_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack111l11l1_opy_, bstack11l1l11l_opy_
logger = bstack1ll1lllll_opy_.get_logger(__name__, bstack1ll1lllll_opy_.bstack1l1l1111l1l_opy_())
def bstack1l11lllllll_opy_(bs_config):
    bstack1l11ll11l11_opy_ = None
    bstack1l1l1l11l1l_opy_ = None
    try:
        bstack1l1l1l11l1l_opy_ = get_cli_dir()
        bstack1l11ll11l11_opy_ = bstack1l11l1ll1ll_opy_(bstack1l1l1l11l1l_opy_)
        bstack1l1l1111l11_opy_ = bstack1l11ll11ll1_opy_(bstack1l11ll11l11_opy_, bstack1l1l1l11l1l_opy_, bs_config)
        bstack1l11ll11l11_opy_ = bstack1l1l1111l11_opy_ if bstack1l1l1111l11_opy_ else bstack1l11ll11l11_opy_
        if not bstack1l11ll11l11_opy_:
            raise ValueError(bstack1ll1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠥ᎓"))
    except Exception as ex:
        logger.debug(bstack1ll1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡸ࡭࡫ࠠ࡭ࡣࡷࡩࡸࡺࠠࡣ࡫ࡱࡥࡷࡿࠠࡼࡿࠥ᎔").format(ex))
        bstack1l11ll11l11_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠦ᎕"))
        if bstack1l11ll11l11_opy_:
            logger.debug(bstack1ll1l11_opy_ (u"ࠤࡉࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠡࡶࡲࠤࡘࡊࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡓࡅ࡙ࡎࠠࡧࡴࡲࡱࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠽ࠤࠧ᎖") + str(bstack1l11ll11l11_opy_) + bstack1ll1l11_opy_ (u"ࠥࠦ᎗"))
        else:
            logger.debug(bstack1ll1l11_opy_ (u"ࠦࡓࡵࠠࡷࡣ࡯࡭ࡩࠦࡓࡅࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡕࡇࡔࡉࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵ࠽ࠣࡷࡪࡺࡵࡱࠢࡰࡥࡾࠦࡢࡦࠢ࡬ࡲࡨࡵ࡭ࡱ࡮ࡨࡸࡪ࠴ࠢ᎘"))
    return bstack1l11ll11l11_opy_, bstack1l1l1l11l1l_opy_
bstack1l11ll1ll11_opy_ = bstack1ll1l11_opy_ (u"ࠧ࠿࠹࠺࠻ࠥ᎙")
bstack1l11l1l1l11_opy_ = bstack1ll1l11_opy_ (u"ࠨࡲࡦࡣࡧࡽࠧ᎚")
bstack1l1l111l111_opy_ = bstack1ll1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦ᎛")
bstack1l11ll1ll1l_opy_ = bstack1ll1l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡎࡌࡗ࡙ࡋࡎࡠࡃࡇࡈࡗࠨ᎜")
bstack1lll111ll1_opy_ = bstack1ll1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠧ᎝")
bstack1l11llll1ll_opy_ = re.compile(bstack1ll1l11_opy_ (u"ࡵࠦ࠭ࡅࡩࠪ࠰࠭ࠬࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡿࡆࡘ࠯࠮ࠫࠤ᎞"))
bstack1l11l11lll1_opy_ = bstack1ll1l11_opy_ (u"ࠦࡩ࡫ࡶࡦ࡮ࡲࡴࡲ࡫࡮ࡵࠤ᎟")
bstack1l11ll1l11l_opy_ = [
    bstack11lll1l1l1_opy_.bstack11111l11l_opy_,
    bstack11lll1l1l1_opy_.CONNECT,
    bstack11lll1l1l1_opy_.bstack1lll11l1_opy_,
]
class SDKCLI:
    _1l11l11l1ll_opy_ = None
    process: Union[None, Any]
    bstack1l11l1l1111_opy_: bool
    bstack1l11l11llll_opy_: bool
    bstack1l1l11111ll_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1l1l11ll11l_opy_: Union[None, grpc.Channel]
    bstack1l1l1l11111_opy_: str
    test_framework: TestFramework
    bstack111111l1ll_opy_: bstack1ll1l1l1111_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1l11ll11l1l_opy_: bstack1llllll11ll_opy_
    accessibility: bstack1l11ll111l1_opy_
    bstack1l1111l1l1_opy_: bstack11l1ll11l_opy_
    ai: bstack1l11lll1l11_opy_
    bstack1l1l111l1ll_opy_: bstack111111ll11_opy_
    bstack1l11ll1111l_opy_: List[bstack11111lllll_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1l11lllll11_opy_: Any
    bstack1l11llll11l_opy_: Dict[str, timedelta]
    bstack1l11lll1111_opy_: str
    bstack1llll11l111_opy_: bstack1ll111ll1ll_opy_
    def __new__(cls):
        if not cls._1l11l11l1ll_opy_:
            cls._1l11l11l1ll_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1l11l11l1ll_opy_
    def __init__(self):
        self.process = None
        self.bstack1l11l1l1111_opy_ = False
        self.bstack1l1l11ll11l_opy_ = None
        self.bstack1llll111lll_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1l11ll1ll1l_opy_, None)
        self.bstack1l11l1ll1l1_opy_ = os.environ.get(bstack1l1l111l111_opy_, bstack1ll1l11_opy_ (u"ࠧࠨᎠ")) == bstack1ll1l11_opy_ (u"ࠨࠢᎡ")
        self.bstack1l11l11llll_opy_ = False
        self.bstack1l1l11111ll_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1l11lllll11_opy_ = None
        self.test_framework = None
        self.bstack111111l1ll_opy_ = None
        self.bstack1l1l1l11111_opy_=bstack1ll1l11_opy_ (u"ࠢࠣᎢ")
        self.session_framework = None
        self.logger = bstack1ll1lllll_opy_.get_logger(self.__class__.__name__, bstack1ll1lllll_opy_.bstack1l1l1111l1l_opy_())
        self.bstack1l11llll11l_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1llll11l111_opy_ = bstack1ll111ll1ll_opy_()
        self.bstack1llll11lll1_opy_ = None
        self.bstack1lll1ll1lll_opy_ = None
        self.bstack1l11ll11l1l_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1l11ll1111l_opy_ = []
    def bstack1l1l1lll1_opy_(self):
        return os.environ.get(bstack1lll111ll1_opy_).lower().__eq__(bstack1ll1l11_opy_ (u"ࠣࡶࡵࡹࡪࠨᎣ"))
    def is_enabled(self, config):
        if bstack1ll1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭Ꭴ") in config and str(config[bstack1ll1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᎥ")]).lower() != bstack1ll1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᎦ"):
            return False
        bstack1l1l11l111l_opy_ = [bstack1ll1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᎧ"), bstack1ll1l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᎨ")]
        bstack1l1l111ll1l_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥᎩ")) in bstack1l1l11l111l_opy_ or os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩᎪ")) in bstack1l1l11l111l_opy_
        os.environ[bstack1ll1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧᎫ")] = str(bstack1l1l111ll1l_opy_) # bstack1l1l11lll1l_opy_ bstack1l1l111l1l1_opy_ VAR to bstack1l11l11ll11_opy_ is binary running
        return bstack1l1l111ll1l_opy_
    def bstack11l11ll1ll_opy_(self):
        for event in bstack1l11ll1l11l_opy_:
            bstack11ll11111l_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack11ll11111l_opy_.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠢࡀࡂࠥࢁࡡࡳࡩࡶࢁࠥࠨᎬ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠦࠧᎭ"))
            )
        bstack11ll11111l_opy_.register(bstack11lll1l1l1_opy_.bstack11111l11l_opy_, self.__1l11ll11111_opy_)
        bstack11ll11111l_opy_.register(bstack11lll1l1l1_opy_.CONNECT, self.__1l1l11l1ll1_opy_)
        bstack11ll11111l_opy_.register(bstack11lll1l1l1_opy_.bstack1lll11l1_opy_, self.__1l1l11l11l1_opy_)
        bstack11ll11111l_opy_.register(bstack11lll1l1l1_opy_.bstack1111l111l_opy_, self.__1l1l1l11l11_opy_)
    def bstack11ll111ll_opy_(self):
        return not self.bstack1l11l1ll1l1_opy_ and os.environ.get(bstack1l1l111l111_opy_, bstack1ll1l11_opy_ (u"ࠧࠨᎮ")) != bstack1ll1l11_opy_ (u"ࠨࠢᎯ")
    def is_running(self):
        if self.bstack1l11l1ll1l1_opy_:
            return self.bstack1l11l1l1111_opy_
        else:
            return bool(self.bstack1l1l11ll11l_opy_)
    def bstack1l11l1llll1_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1l11ll1111l_opy_) and cli.is_running()
    def __1l11l1l111l_opy_(self, bstack1l1l1l111ll_opy_=10):
        if self.bstack1llll111lll_opy_:
            return
        bstack1l1l1lllll_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1l11ll1ll1l_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠢ࡜ࠤᎰ") + str(id(self)) + bstack1ll1l11_opy_ (u"ࠣ࡟ࠣࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡳ࡭ࠢᎱ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1ll1l11_opy_ (u"ࠤࡪࡶࡵࡩ࠮ࡦࡰࡤࡦࡱ࡫࡟ࡩࡶࡷࡴࡤࡶࡲࡰࡺࡼࠦᎲ"), 0), (bstack1ll1l11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠯ࡧࡱࡥࡧࡲࡥࡠࡪࡷࡸࡵࡹ࡟ࡱࡴࡲࡼࡾࠨᎳ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1l1l1l111ll_opy_)
        self.bstack1l1l11ll11l_opy_ = channel
        self.bstack1llll111lll_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1l1l11ll11l_opy_)
        self.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡦࡳࡳࡴࡥࡤࡶࠥᎴ"), datetime.now() - bstack1l1l1lllll_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1l11ll1ll1l_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪ࠺ࠡ࡫ࡶࡣࡨ࡮ࡩ࡭ࡦࡢࡴࡷࡵࡣࡦࡵࡶࡁࠧᎵ") + str(self.bstack11ll111ll_opy_()) + bstack1ll1l11_opy_ (u"ࠨࠢᎶ"))
    def __1l1l11l11l1_opy_(self, event_name):
        if self.bstack11ll111ll_opy_():
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡵࡷࡳࡵࡶࡩ࡯ࡩࠣࡇࡑࡏࠢᎷ"))
        self.__1l1l11ll111_opy_()
    def __1l1l1l11l11_opy_(self, event_name, bstack1l11ll1lll1_opy_ = None, bstack1ll1lll1_opy_=1):
        if bstack1ll1lll1_opy_ == 1:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠣᎸ"))
        bstack1l11l11l1l1_opy_ = Path(bstack1lll1111ll1_opy_ (u"ࠤࡾࡷࡪࡲࡦ࠯ࡥ࡯࡭ࡤࡪࡩࡳࡿ࠲ࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࡷ࠳ࡰࡳࡰࡰࠥᎹ"))
        if self.bstack1l1l1l11l1l_opy_ and bstack1l11l11l1l1_opy_.exists():
            with open(bstack1l11l11l1l1_opy_, bstack1ll1l11_opy_ (u"ࠪࡶࠬᎺ"), encoding=bstack1ll1l11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᎻ")) as fp:
                data = json.load(fp)
                try:
                    bstack11lllll1ll_opy_(bstack1ll1l11_opy_ (u"ࠬࡖࡏࡔࡖࠪᎼ"), bstack1ll1l11l11_opy_(bstack11l1l1111l_opy_), data, {
                        bstack1ll1l11_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᎽ"): (self.config[bstack1ll1l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᎾ")], self.config[bstack1ll1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᎿ")])
                    })
                except Exception as e:
                    logger.debug(bstack11l1l11l_opy_.format(str(e)))
            bstack1l11l11l1l1_opy_.unlink()
        sys.exit(bstack1ll1lll1_opy_)
    @measure(event_name=EVENTS.bstack1l1l1111ll1_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def __1l11ll11111_opy_(self, event_name: str, data):
        from bstack_utils.bstack1ll11l1lll_opy_ import bstack111111lll1_opy_
        self.bstack1l1l1l11111_opy_, self.bstack1l1l1l11l1l_opy_ = bstack1l11lllllll_opy_(data.bs_config)
        os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠ࡙ࡕࡍ࡙ࡇࡂࡍࡇࡢࡈࡎࡘࠧᏀ")] = self.bstack1l1l1l11l1l_opy_
        if not self.bstack1l1l1l11111_opy_ or not self.bstack1l1l1l11l1l_opy_:
            raise ValueError(bstack1ll1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺࠤᏁ"))
        if self.bstack11ll111ll_opy_():
            self.__1l1l11l1ll1_opy_(event_name, bstack1l1ll1l1ll_opy_())
            return
        try:
            bstack111111lll1_opy_.end(EVENTS.bstack11ll1l1l_opy_.value, EVENTS.bstack11ll1l1l_opy_.value + bstack1ll1l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᏂ"), EVENTS.bstack11ll1l1l_opy_.value + bstack1ll1l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᏃ"), status=True, failure=None, test_name=None)
            logger.debug(bstack1ll1l11_opy_ (u"ࠨࡃࡰ࡯ࡳࡰࡪࡺࡥࠡࡕࡇࡏ࡙ࠥࡥࡵࡷࡳ࠲ࠧᏄ"))
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡽࢀࠦᏅ").format(e))
        start = datetime.now()
        is_started = self.__1l1l111llll_opy_()
        self.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠣࡵࡳࡥࡼࡴ࡟ࡵ࡫ࡰࡩࠧᏆ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1l11l1l111l_opy_()
            self.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࡢࡸ࡮ࡳࡥࠣᏇ"), datetime.now() - start)
            start = datetime.now()
            self.__1l11ll11lll_opy_(data)
            self.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣᏈ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1l1l1111lll_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def __1l1l11l1ll1_opy_(self, event_name: str, data: bstack1l1ll1l1ll_opy_):
        if not self.bstack11ll111ll_opy_():
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱࡱࡲࡪࡩࡴ࠻ࠢࡱࡳࡹࠦࡡࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳࠣᏉ"))
            return
        bin_session_id = os.environ.get(bstack1l1l111l111_opy_)
        start = datetime.now()
        self.__1l11l1l111l_opy_()
        self.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦᏊ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠢࡷࡳࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡄࡎࡌࠤࠧᏋ") + str(bin_session_id) + bstack1ll1l11_opy_ (u"ࠢࠣᏌ"))
        start = datetime.now()
        self.__1l11lll11ll_opy_()
        self.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨᏍ"), datetime.now() - start)
    def __1l11lll111l_opy_(self):
        if not self.bstack1llll111lll_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡦࡥࡳࡴ࡯ࡵࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࠥࡳ࡯ࡥࡷ࡯ࡩࡸࠨᏎ"))
            return
        bstack1l11l1l1lll_opy_ = {
            bstack1ll1l11_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᏏ"): (bstack1lll1ll1l11_opy_, bstack1lll11ll11l_opy_, bstack1lll1l111l1_opy_),
            bstack1ll1l11_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᏐ"): (bstack1ll1ll1ll11_opy_, bstack1111l11lll_opy_, bstack1111111ll1_opy_),
        }
        if not self.bstack1llll11lll1_opy_ and self.session_framework in bstack1l11l1l1lll_opy_:
            bstack1l11l11ll1l_opy_, bstack1l11l1l1l1l_opy_, bstack1l1l1l111l1_opy_ = bstack1l11l1l1lll_opy_[self.session_framework]
            bstack1l11ll111ll_opy_ = bstack1l11l1l1l1l_opy_()
            self.bstack1lll1ll1lll_opy_ = bstack1l11ll111ll_opy_
            self.bstack1llll11lll1_opy_ = bstack1l1l1l111l1_opy_
            self.bstack1l11ll1111l_opy_.append(bstack1l11ll111ll_opy_)
            self.bstack1l11ll1111l_opy_.append(bstack1l11l11ll1l_opy_(self.bstack1lll1ll1lll_opy_))
        if not self.bstack1l11ll11l1l_opy_ and self.config_observability and self.config_observability.success: # bstack1lll1l11111_opy_
            self.bstack1l11ll11l1l_opy_ = bstack1llllll11ll_opy_(self.bstack1llll11lll1_opy_, self.bstack1lll1ll1lll_opy_) # bstack1l1l11l1111_opy_
            self.bstack1l11ll1111l_opy_.append(self.bstack1l11ll11l1l_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1l11ll111l1_opy_(self.bstack1llll11lll1_opy_, self.bstack1lll1ll1lll_opy_)
            self.bstack1l11ll1111l_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1ll1l11_opy_ (u"ࠧࡹࡥ࡭ࡨࡋࡩࡦࡲࠢᏑ"), False) == True:
            self.ai = bstack1l11lll1l11_opy_()
            self.bstack1l11ll1111l_opy_.append(self.ai)
        if not self.percy and self.bstack1l11lllll11_opy_ and self.bstack1l11lllll11_opy_.success:
            self.percy = bstack111111ll11_opy_(self.bstack1l11lllll11_opy_)
            self.bstack1l11ll1111l_opy_.append(self.percy)
        for mod in self.bstack1l11ll1111l_opy_:
            if not mod.bstack1l1l11ll1ll_opy_():
                mod.configure(self.bstack1llll111lll_opy_, self.config, self.cli_bin_session_id, self.bstack1llll11l111_opy_)
    def __1l1l11lllll_opy_(self):
        for mod in self.bstack1l11ll1111l_opy_:
            if mod.bstack1l1l11ll1ll_opy_():
                mod.configure(self.bstack1llll111lll_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1l1l11l1l11_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def __1l11ll11lll_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1l11l11llll_opy_:
            return
        self.__1l1l11111l1_opy_(data)
        bstack1l1l1lllll_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1ll1l11_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨᏒ")
        req.sdk_language = bstack1ll1l11_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢᏓ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1l11llll1ll_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠣ࡝ࠥᏔ") + str(id(self)) + bstack1ll1l11_opy_ (u"ࠤࡠࠤࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡸࡺࡡࡳࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᏕ"))
            r = self.bstack1llll111lll_opy_.StartBinSession(req)
            self.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡷࡥࡷࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᏖ"), datetime.now() - bstack1l1l1lllll_opy_)
            os.environ[bstack1l1l111l111_opy_] = r.bin_session_id
            self.__1l11l1l11l1_opy_(r)
            self.__1l11lll111l_opy_()
            self.bstack1llll11l111_opy_.start()
            self.bstack1l11l11llll_opy_ = True
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡠࠨᏗ") + str(id(self)) + bstack1ll1l11_opy_ (u"ࠧࡣࠠ࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦࠥᏘ"))
        except grpc.bstack1l1l1l1111l_opy_ as bstack1l11lll1l1l_opy_:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡺࡩ࡮ࡧࡲࡩࡺࡺ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᏙ") + str(bstack1l11lll1l1l_opy_) + bstack1ll1l11_opy_ (u"ࠢࠣᏚ"))
            traceback.print_exc()
            raise bstack1l11lll1l1l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᏛ") + str(e) + bstack1ll1l11_opy_ (u"ࠤࠥᏜ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11l1lll1l_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def __1l11lll11ll_opy_(self):
        if not self.bstack11ll111ll_opy_() or not self.cli_bin_session_id or self.bstack1l1l11111ll_opy_:
            return
        bstack1l1l1lllll_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᏝ"), bstack1ll1l11_opy_ (u"ࠫ࠵࠭Ꮮ")))
        try:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡡࠢᏟ") + str(id(self)) + bstack1ll1l11_opy_ (u"ࠨ࡝ࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᏠ"))
            r = self.bstack1llll111lll_opy_.ConnectBinSession(req)
            self.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡩ࡯࡯ࡰࡨࡧࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦᏡ"), datetime.now() - bstack1l1l1lllll_opy_)
            self.__1l11l1l11l1_opy_(r)
            self.__1l11lll111l_opy_()
            self.bstack1llll11l111_opy_.start()
            self.bstack1l1l11111ll_opy_ = True
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠣ࡝ࠥᏢ") + str(id(self)) + bstack1ll1l11_opy_ (u"ࠤࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠣᏣ"))
        except grpc.bstack1l1l1l1111l_opy_ as bstack1l11lll1l1l_opy_:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡷ࡭ࡲ࡫࡯ࡦࡷࡷ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᏤ") + str(bstack1l11lll1l1l_opy_) + bstack1ll1l11_opy_ (u"ࠦࠧᏥ"))
            traceback.print_exc()
            raise bstack1l11lll1l1l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᏦ") + str(e) + bstack1ll1l11_opy_ (u"ࠨࠢᏧ"))
            traceback.print_exc()
            raise e
    def __1l11l1l11l1_opy_(self, r):
        self.bstack1l11lll1ll1_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1ll1l11_opy_ (u"ࠢࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡸ࡫ࡲࡷࡧࡵࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨᏨ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1ll1l11_opy_ (u"ࠣࡧࡰࡴࡹࡿࠠࡤࡱࡱࡪ࡮࡭ࠠࡧࡱࡸࡲࡩࠨᏩ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1ll1l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡦࡴࡦࡽࠥ࡯ࡳࠡࡵࡨࡲࡹࠦ࡯࡯࡮ࡼࠤࡦࡹࠠࡱࡣࡵࡸࠥࡵࡦࠡࡶ࡫ࡩࠥࠨࡃࡰࡰࡱࡩࡨࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰ࠯ࠦࠥࡧ࡮ࡥࠢࡷ࡬࡮ࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢ࡬ࡷࠥࡧ࡬ࡴࡱࠣࡹࡸ࡫ࡤࠡࡤࡼࠤࡘࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫ࡩࡷ࡫ࡦࡰࡴࡨ࠰ࠥࡔ࡯࡯ࡧࠣ࡬ࡦࡴࡤ࡭࡫ࡱ࡫ࠥ࡯ࡳࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᏪ")
        self.bstack1l11lllll11_opy_ = getattr(r, bstack1ll1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᏫ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᏬ")] = self.config_testhub.jwt
        os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᏭ")] = self.config_testhub.build_hashed_id
    def bstack1l1l1l1l111_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1l11l1l1111_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1l1l11l1l1l_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1l1l11l1l1l_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1l1l1l1l111_opy_(event_name=EVENTS.bstack1l11llll111_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def __1l1l111llll_opy_(self, bstack1l1l1l111ll_opy_=10):
        if self.bstack1l11l1l1111_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡳࡵࡣࡵࡸ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠣᏮ"))
            return True
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡴࡶࡤࡶࡹࠨᏯ"))
        if os.getenv(bstack1ll1l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡊࡔࡖࠣᏰ")) == bstack1l11l11lll1_opy_:
            self.cli_bin_session_id = bstack1l11l11lll1_opy_
            self.cli_listen_addr = bstack1ll1l11_opy_ (u"ࠤࡸࡲ࡮ࡾ࠺࠰ࡶࡰࡴ࠴ࡹࡤ࡬࠯ࡳࡰࡦࡺࡦࡰࡴࡰ࠱ࠪࡹ࠮ࡴࡱࡦ࡯ࠧᏱ") % (self.cli_bin_session_id)
            self.bstack1l11l1l1111_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1l1l1l11111_opy_, bstack1ll1l11_opy_ (u"ࠥࡷࡩࡱࠢᏲ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1l1l1l11ll1_opy_ compat for text=True in bstack1l11l1l11ll_opy_ python
            encoding=bstack1ll1l11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᏳ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1l11lll11l1_opy_ = threading.Thread(target=self.__1l1l111lll1_opy_, args=(bstack1l1l1l111ll_opy_,))
        bstack1l11lll11l1_opy_.start()
        bstack1l11lll11l1_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡸࡶࡡࡸࡰ࠽ࠤࡷ࡫ࡴࡶࡴࡱࡧࡴࡪࡥ࠾ࡽࡶࡩࡱ࡬࠮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡴࡨࡸࡺࡸ࡮ࡤࡱࡧࡩࢂࠦ࡯ࡶࡶࡀࡿࡸ࡫࡬ࡧ࠰ࡳࡶࡴࡩࡥࡴࡵ࠱ࡷࡹࡪ࡯ࡶࡶ࠱ࡶࡪࡧࡤࠩࠫࢀࠤࡪࡸࡲ࠾ࠤᏴ") + str(self.process.stderr.read()) + bstack1ll1l11_opy_ (u"ࠨࠢᏵ"))
        if not self.bstack1l11l1l1111_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠢ࡜ࠤ᏶") + str(id(self)) + bstack1ll1l11_opy_ (u"ࠣ࡟ࠣࡧࡱ࡫ࡡ࡯ࡷࡳࠦ᏷"))
            self.__1l1l11ll111_opy_()
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡲࡵࡳࡨ࡫ࡳࡴࡡࡵࡩࡦࡪࡹ࠻ࠢࠥᏸ") + str(self.bstack1l11l1l1111_opy_) + bstack1ll1l11_opy_ (u"ࠥࠦᏹ"))
        return self.bstack1l11l1l1111_opy_
    def __1l1l111lll1_opy_(self, bstack1l11l1ll111_opy_=10):
        bstack1l11l1l1ll1_opy_ = time.time()
        while self.process and time.time() - bstack1l11l1l1ll1_opy_ < bstack1l11l1ll111_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1ll1l11_opy_ (u"ࠦ࡮ࡪ࠽ࠣᏺ") in line:
                    self.cli_bin_session_id = line.split(bstack1ll1l11_opy_ (u"ࠧ࡯ࡤ࠾ࠤᏻ"))[-1:][0].strip()
                    self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡣ࡭࡫ࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧ࠾ࠧᏼ") + str(self.cli_bin_session_id) + bstack1ll1l11_opy_ (u"ࠢࠣᏽ"))
                    continue
                if bstack1ll1l11_opy_ (u"ࠣ࡮࡬ࡷࡹ࡫࡮࠾ࠤ᏾") in line:
                    self.cli_listen_addr = line.split(bstack1ll1l11_opy_ (u"ࠤ࡯࡭ࡸࡺࡥ࡯࠿ࠥ᏿"))[-1:][0].strip()
                    self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡧࡱ࡯࡟࡭࡫ࡶࡸࡪࡴ࡟ࡢࡦࡧࡶ࠿ࠨ᐀") + str(self.cli_listen_addr) + bstack1ll1l11_opy_ (u"ࠦࠧᐁ"))
                    continue
                if bstack1ll1l11_opy_ (u"ࠧࡶ࡯ࡳࡶࡀࠦᐂ") in line:
                    port = line.split(bstack1ll1l11_opy_ (u"ࠨࡰࡰࡴࡷࡁࠧᐃ"))[-1:][0].strip()
                    self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡱࡱࡵࡸ࠿ࠨᐄ") + str(port) + bstack1ll1l11_opy_ (u"ࠣࠤᐅ"))
                    continue
                if line.strip() == bstack1l11l1l1l11_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1ll1l11_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡋࡒࡣࡘ࡚ࡒࡆࡃࡐࠦᐆ"), bstack1ll1l11_opy_ (u"ࠥ࠵ࠧᐇ")) == bstack1ll1l11_opy_ (u"ࠦ࠶ࠨᐈ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1l11l1l1111_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵ࠾ࠥࠨᐉ") + str(e) + bstack1ll1l11_opy_ (u"ࠨࠢᐊ"))
        return False
    @measure(event_name=EVENTS.bstack1l11l1lll11_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def __1l1l11ll111_opy_(self):
        if self.bstack1l1l11ll11l_opy_:
            self.bstack1llll11l111_opy_.stop()
            start = datetime.now()
            if self.bstack1l11ll1l1ll_opy_():
                self.cli_bin_session_id = None
                if self.bstack1l1l11111ll_opy_:
                    self.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠢࡴࡶࡲࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦᐋ"), datetime.now() - start)
                else:
                    self.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠣࡵࡷࡳࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧᐌ"), datetime.now() - start)
            self.__1l1l11lllll_opy_()
            start = datetime.now()
            self.bstack1l1l11ll11l_opy_.close()
            self.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠤࡧ࡭ࡸࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦᐍ"), datetime.now() - start)
            self.bstack1l1l11ll11l_opy_ = None
        if self.process:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡷࡹࡵࡰࠣᐎ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠦࡰ࡯࡬࡭ࡡࡷ࡭ࡲ࡫ࠢᐏ"), datetime.now() - start)
            self.process = None
            if self.bstack1l11l1ll1l1_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1111l1l1_opy_()
                self.logger.info(
                    bstack1ll1l11_opy_ (u"ࠧ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠣᐐ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᐑ")] = self.config_testhub.build_hashed_id
        self.bstack1l11l1l1111_opy_ = False
    def __1l1l11111l1_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack1ll1l11_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᐒ")] = selenium.__version__
            data.frameworks.append(bstack1ll1l11_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᐓ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack1ll1l11_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᐔ")] = __version__
            data.frameworks.append(bstack1ll1l11_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᐕ"))
        except:
            pass
    def bstack1l11lll1lll_opy_(self, hub_url: str, platform_index: int, bstack11l11111l_opy_: Any):
        if self.bstack111111l1ll_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡵࡨࡸࠥࡻࡰࠣᐖ"))
            return
        try:
            bstack1l1l1lllll_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1ll1l11_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᐗ")
            self.bstack111111l1ll_opy_ = bstack1111111ll1_opy_(
                hub_url,
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1ll1l1ll111_opy_={bstack1ll1l11_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥᐘ"): bstack11l11111l_opy_}
            )
            def bstack1l1l1l11lll_opy_(self):
                return
            if self.config.get(bstack1ll1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠤᐙ"), True):
                Service.start = bstack1l1l1l11lll_opy_
                Service.stop = bstack1l1l1l11lll_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack11l1ll11l_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1ll1111l1ll_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᐚ"), datetime.now() - bstack1l1l1lllll_opy_)
        except Exception as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࠣᐛ") + str(e) + bstack1ll1l11_opy_ (u"ࠥࠦᐜ"))
    def bstack1l1l11l1lll_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1l1l1l11_opy_
            self.bstack111111l1ll_opy_ = bstack1lll1l111l1_opy_(
                platform_index,
                framework_name=bstack1ll1l11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᐝ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠾ࠥࠨᐞ") + str(e) + bstack1ll1l11_opy_ (u"ࠨࠢᐟ"))
            pass
    def bstack1l1l111l11l_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠡࡵࡨࡸࡺࡶࠠࡱࡻࡷࡩࡸࡺ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡶࡩࡹࠦࡵࡱࠤᐠ"))
            return
        if bstack1l1l1ll1l_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1ll1l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᐡ"): pytest.__version__ }, [bstack1ll1l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᐢ")], self.bstack1llll11l111_opy_, self.bstack1llll111lll_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1l1ll1ll11l_opy_({ bstack1ll1l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᐣ"): pytest.__version__ }, [bstack1ll1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᐤ")], self.bstack1llll11l111_opy_, self.bstack1llll111lll_opy_)
        except Exception as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡻࡷࡩࡸࡺ࠺ࠡࠤᐥ") + str(e) + bstack1ll1l11_opy_ (u"ࠨࠢᐦ"))
        self.bstack1l11llllll1_opy_()
    def bstack1l11llllll1_opy_(self):
        if not self.bstack1l1l1lll1_opy_():
            return
        bstack11ll11l1_opy_ = None
        def bstack111l11ll1_opy_(config, startdir):
            return bstack1ll1l11_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧᐧ").format(bstack1ll1l11_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢᐨ"))
        def bstack11llll1111_opy_():
            return
        def bstack1l1l1l1l_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1ll1l11_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩᐩ"):
                return bstack1ll1l11_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤᐪ")
            else:
                return bstack11ll11l1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack11ll11l1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack111l11ll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11llll1111_opy_
            Config.getoption = bstack1l1l1l1l_opy_
        except Exception as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡷࡧ࡭ࠦࡰࡺࡶࡨࡷࡹࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡨࡲࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠾ࠥࠨᐫ") + str(e) + bstack1ll1l11_opy_ (u"ࠧࠨᐬ"))
    def bstack1l1l1111111_opy_(self):
        bstack1l11ll1l1l1_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1l11ll1l1l1_opy_, dict):
            if cli.config_observability:
                bstack1l11ll1l1l1_opy_.update(
                    {bstack1ll1l11_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨᐭ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1ll1l11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࡡࡷࡳࡤࡽࡲࡢࡲࠥᐮ") in accessibility.get(bstack1ll1l11_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᐯ"), {}):
                    bstack1l11l1lllll_opy_ = accessibility.get(bstack1ll1l11_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᐰ"))
                    bstack1l11l1lllll_opy_.update({ bstack1ll1l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠦᐱ"): bstack1l11l1lllll_opy_.pop(bstack1ll1l11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸࡥࡴࡰࡡࡺࡶࡦࡶࠢᐲ")) })
                bstack1l11ll1l1l1_opy_.update({bstack1ll1l11_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧᐳ"): accessibility })
        return bstack1l11ll1l1l1_opy_
    @measure(event_name=EVENTS.bstack1l1l11lll11_opy_, stage=STAGE.bstack1l11lll1l_opy_)
    def bstack1l11ll1l1ll_opy_(self, bstack1l1l11llll1_opy_: str = None, bstack1l11l1ll11l_opy_: str = None, bstack1ll1lll1_opy_: int = None):
        if not self.cli_bin_session_id or not self.bstack1llll111lll_opy_:
            return
        bstack1l1l1lllll_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if bstack1ll1lll1_opy_:
            req.bstack1ll1lll1_opy_ = bstack1ll1lll1_opy_
        if bstack1l1l11llll1_opy_:
            req.bstack1l1l11llll1_opy_ = bstack1l1l11llll1_opy_
        if bstack1l11l1ll11l_opy_:
            req.bstack1l11l1ll11l_opy_ = bstack1l11l1ll11l_opy_
        try:
            r = self.bstack1llll111lll_opy_.StopBinSession(req)
            self.bstack11llll111l_opy_(bstack1ll1l11_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸࡺ࡯ࡱࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᐴ"), datetime.now() - bstack1l1l1lllll_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack11llll111l_opy_(self, key: str, value: timedelta):
        tag = bstack1ll1l11_opy_ (u"ࠢࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹࠢᐵ") if self.bstack11ll111ll_opy_() else bstack1ll1l11_opy_ (u"ࠣ࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹࠢᐶ")
        self.bstack1l11llll11l_opy_[bstack1ll1l11_opy_ (u"ࠤ࠽ࠦᐷ").join([tag + bstack1ll1l11_opy_ (u"ࠥ࠱ࠧᐸ") + str(id(self)), key])] += value
    def bstack1111l1l1_opy_(self):
        if not os.getenv(bstack1ll1l11_opy_ (u"ࠦࡉࡋࡂࡖࡉࡢࡔࡊࡘࡆࠣᐹ"), bstack1ll1l11_opy_ (u"ࠧ࠶ࠢᐺ")) == bstack1ll1l11_opy_ (u"ࠨ࠱ࠣᐻ"):
            return
        bstack1l11ll1llll_opy_ = dict()
        bstack1lll111l111_opy_ = []
        if self.test_framework:
            bstack1lll111l111_opy_.extend(list(self.test_framework.bstack1lll111l111_opy_.values()))
        if self.bstack111111l1ll_opy_:
            bstack1lll111l111_opy_.extend(list(self.bstack111111l1ll_opy_.bstack1lll111l111_opy_.values()))
        for instance in bstack1lll111l111_opy_:
            if not instance.platform_index in bstack1l11ll1llll_opy_:
                bstack1l11ll1llll_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1l11ll1llll_opy_[instance.platform_index]
            for k, v in instance.bstack1l1ll11111l_opy_().items():
                report[k] += v
                report[k.split(bstack1ll1l11_opy_ (u"ࠢ࠻ࠤᐼ"))[0]] += v
        bstack1l1l11l11ll_opy_ = sorted([(k, v) for k, v in self.bstack1l11llll11l_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1l1l11ll1l1_opy_ = 0
        for r in bstack1l1l11l11ll_opy_:
            bstack1l11ll1l111_opy_ = r[1].total_seconds()
            bstack1l1l11ll1l1_opy_ += bstack1l11ll1l111_opy_
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡥ࡯࡭࠿ࢁࡲ࡜࠲ࡠࢁࡂࠨᐽ") + str(bstack1l11ll1l111_opy_) + bstack1ll1l11_opy_ (u"ࠤࠥᐾ"))
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠥ࠱࠲ࠨᐿ"))
        bstack1l11llll1l1_opy_ = []
        for platform_index, report in bstack1l11ll1llll_opy_.items():
            bstack1l11llll1l1_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1l11llll1l1_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack11llll11_opy_ = set()
        bstack1l1l111111l_opy_ = 0
        for r in bstack1l11llll1l1_opy_:
            bstack1l11ll1l111_opy_ = r[2].total_seconds()
            bstack1l1l111111l_opy_ += bstack1l11ll1l111_opy_
            bstack11llll11_opy_.add(r[0])
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡹ࡫ࡳࡵ࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࠱ࢀࡸ࡛࠱࡟ࢀ࠾ࢀࡸ࡛࠲࡟ࢀࡁࠧᑀ") + str(bstack1l11ll1l111_opy_) + bstack1ll1l11_opy_ (u"ࠧࠨᑁ"))
        if self.bstack11ll111ll_opy_():
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠨ࠭࠮ࠤᑂ"))
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡤ࡮࡬࠾ࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶࡁࢀࡺ࡯ࡵࡣ࡯ࡣࡨࡲࡩࡾࠢࡷࡩࡸࡺ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵ࠰ࡿࡸࡺࡲࠩࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ࠭ࢂࡃࠢᑃ") + str(bstack1l1l111111l_opy_) + bstack1ll1l11_opy_ (u"ࠣࠤᑄ"))
        else:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷࡂࠨᑅ") + str(bstack1l1l11ll1l1_opy_) + bstack1ll1l11_opy_ (u"ࠥࠦᑆ"))
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠦ࠲࠳ࠢᑇ"))
    def bstack1l11lll1ll1_opy_(self, r):
        if r is not None and getattr(r, bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧ࠭ᑈ"), None) and getattr(r.testhub, bstack1ll1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ᑉ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1ll1l11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᑊ")))
            for bstack1l1l111ll11_opy_, err in errors.items():
                if err[bstack1ll1l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᑋ")] == bstack1ll1l11_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᑌ"):
                    self.logger.info(err[bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᑍ")])
                else:
                    self.logger.error(err[bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᑎ")])
cli = SDKCLI()