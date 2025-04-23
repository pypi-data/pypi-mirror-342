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
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack11111lllll_opy_
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack11111l1lll_opy_,
    bstack111111ll1l_opy_,
    bstack1111l1lll1_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1lll1l11lll_opy_ import bstack1lll1l111l1_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1lll1ll11l_opy_
from bstack_utils.helper import bstack1llll1l1l11_opy_
import threading
import os
import urllib.parse
class bstack1lll1ll1l11_opy_(bstack11111lllll_opy_):
    def __init__(self, bstack1lll1ll1lll_opy_):
        super().__init__()
        bstack1lll1l111l1_opy_.bstack111111l1l1_opy_((bstack11111l1lll_opy_.bstack1lll11llll1_opy_, bstack111111ll1l_opy_.PRE), self.bstack1lll1ll111l_opy_)
        bstack1lll1l111l1_opy_.bstack111111l1l1_opy_((bstack11111l1lll_opy_.bstack1lll11llll1_opy_, bstack111111ll1l_opy_.PRE), self.bstack1lll1ll11l1_opy_)
        bstack1lll1l111l1_opy_.bstack111111l1l1_opy_((bstack11111l1lll_opy_.bstack1lll11ll1l1_opy_, bstack111111ll1l_opy_.PRE), self.bstack1lll11lllll_opy_)
        bstack1lll1l111l1_opy_.bstack111111l1l1_opy_((bstack11111l1lll_opy_.bstack1111l1l1l1_opy_, bstack111111ll1l_opy_.PRE), self.bstack1lll1l11l1l_opy_)
        bstack1lll1l111l1_opy_.bstack111111l1l1_opy_((bstack11111l1lll_opy_.bstack1lll11llll1_opy_, bstack111111ll1l_opy_.PRE), self.bstack1lll1ll1111_opy_)
        bstack1lll1l111l1_opy_.bstack111111l1l1_opy_((bstack11111l1lll_opy_.QUIT, bstack111111ll1l_opy_.PRE), self.on_close)
        self.bstack1lll1ll1lll_opy_ = bstack1lll1ll1lll_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1lll1ll111l_opy_(
        self,
        f: bstack1lll1l111l1_opy_,
        bstack1lll11ll1ll_opy_: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1l11_opy_ (u"ࠧࡲࡡࡶࡰࡦ࡬ࠧႥ"):
            return
        if not bstack1llll1l1l11_opy_():
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡲࡡࡶࡰࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥႦ"))
            return
        def wrapped(bstack1lll11ll1ll_opy_, launch, *args, **kwargs):
            response = self.bstack1lll11lll1l_opy_(f.platform_index, instance.ref(), json.dumps({bstack1ll1l11_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭Ⴇ"): True}).encode(bstack1ll1l11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢႨ")))
            if response is not None and response.capabilities:
                if not bstack1llll1l1l11_opy_():
                    browser = launch(bstack1lll11ll1ll_opy_)
                    return browser
                bstack1lll1l1l1l1_opy_ = json.loads(response.capabilities.decode(bstack1ll1l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣႩ")))
                if not bstack1lll1l1l1l1_opy_: # empty caps bstack1lll1l1lll1_opy_ bstack1lll1l1ll11_opy_ bstack1lll1l11l11_opy_ bstack1lll1l11111_opy_ or error in processing
                    return
                bstack1lll11lll11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1lll1l1l1l1_opy_))
                f.bstack1lllllll1l1_opy_(instance, bstack1lll1l111l1_opy_.bstack1lll1l1111l_opy_, bstack1lll11lll11_opy_)
                f.bstack1lllllll1l1_opy_(instance, bstack1lll1l111l1_opy_.bstack1lll1l1l1ll_opy_, bstack1lll1l1l1l1_opy_)
                browser = bstack1lll11ll1ll_opy_.connect(bstack1lll11lll11_opy_)
                return browser
        return wrapped
    def bstack1lll11lllll_opy_(
        self,
        f: bstack1lll1l111l1_opy_,
        Connection: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1l11_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧႪ"):
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥႫ"))
            return
        if not bstack1llll1l1l11_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1ll1l11_opy_ (u"ࠬࡶࡡࡳࡣࡰࡷࠬႬ"), {}).get(bstack1ll1l11_opy_ (u"࠭ࡢࡴࡒࡤࡶࡦࡳࡳࠨႭ")):
                    bstack1lll1l1ll1l_opy_ = args[0][bstack1ll1l11_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢႮ")][bstack1ll1l11_opy_ (u"ࠣࡤࡶࡔࡦࡸࡡ࡮ࡵࠥႯ")]
                    session_id = bstack1lll1l1ll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧႰ"))
                    f.bstack1lllllll1l1_opy_(instance, bstack1lll1l111l1_opy_.bstack1lll1l11ll1_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࠨႱ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1lll1ll1111_opy_(
        self,
        f: bstack1lll1l111l1_opy_,
        bstack1lll11ll1ll_opy_: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1l11_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧႲ"):
            return
        if not bstack1llll1l1l11_opy_():
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡨࡵ࡮࡯ࡧࡦࡸࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥႳ"))
            return
        def wrapped(bstack1lll11ll1ll_opy_, connect, *args, **kwargs):
            response = self.bstack1lll11lll1l_opy_(f.platform_index, instance.ref(), json.dumps({bstack1ll1l11_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬႴ"): True}).encode(bstack1ll1l11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨႵ")))
            if response is not None and response.capabilities:
                bstack1lll1l1l1l1_opy_ = json.loads(response.capabilities.decode(bstack1ll1l11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢႶ")))
                if not bstack1lll1l1l1l1_opy_:
                    return
                bstack1lll11lll11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1lll1l1l1l1_opy_))
                if bstack1lll1l1l1l1_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨႷ")):
                    browser = bstack1lll11ll1ll_opy_.bstack1lll1l111ll_opy_(bstack1lll11lll11_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1lll11lll11_opy_
                    return connect(bstack1lll11ll1ll_opy_, *args, **kwargs)
        return wrapped
    def bstack1lll1ll11l1_opy_(
        self,
        f: bstack1lll1l111l1_opy_,
        bstack1lll1l1llll_opy_: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1l11_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧႸ"):
            return
        if not bstack1llll1l1l11_opy_():
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡲࡪࡽ࡟ࡱࡣࡪࡩࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥႹ"))
            return
        def wrapped(bstack1lll1l1llll_opy_, bstack1lll1l1l111_opy_, *args, **kwargs):
            contexts = bstack1lll1l1llll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack1ll1l11_opy_ (u"ࠧࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠥႺ") in page.url:
                                    return page
                    else:
                        return bstack1lll1l1l111_opy_(bstack1lll1l1llll_opy_)
        return wrapped
    def bstack1lll11lll1l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡹࡨࡦࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦႻ") + str(req) + bstack1ll1l11_opy_ (u"ࠢࠣႼ"))
        try:
            r = self.bstack1llll111lll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦႽ") + str(r.success) + bstack1ll1l11_opy_ (u"ࠤࠥႾ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣႿ") + str(e) + bstack1ll1l11_opy_ (u"ࠦࠧჀ"))
            traceback.print_exc()
            raise e
    def bstack1lll1l11l1l_opy_(
        self,
        f: bstack1lll1l111l1_opy_,
        Connection: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1l11_opy_ (u"ࠧࡥࡳࡦࡰࡧࡣࡲ࡫ࡳࡴࡣࡪࡩࡤࡺ࡯ࡠࡵࡨࡶࡻ࡫ࡲࠣჁ"):
            return
        if not bstack1llll1l1l11_opy_():
            return
        def wrapped(Connection, bstack1lll1ll11ll_opy_, *args, **kwargs):
            return bstack1lll1ll11ll_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1lll1l111l1_opy_,
        bstack1lll11ll1ll_opy_: object,
        exec: Tuple[bstack1111l1lll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack11111l1lll_opy_, bstack111111ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1l11_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧჂ"):
            return
        if not bstack1llll1l1l11_opy_():
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦࡣ࡭ࡱࡶࡩࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥჃ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped