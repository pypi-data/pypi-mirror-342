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
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll11l1ll_opy_ import bstack1lllllll11l_opy_
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import (
    bstack1111l11l1l_opy_,
    bstack11111l1ll1_opy_,
    bstack1111l1111l_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1llll1ll1ll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11l1111l1_opy_
from bstack_utils.helper import bstack1l1lllll11l_opy_
import threading
import os
import urllib.parse
class bstack1lllll1ll1l_opy_(bstack1lllllll11l_opy_):
    def __init__(self, bstack1lll1ll1lll_opy_):
        super().__init__()
        bstack1llll1ll1ll_opy_.bstack1ll1ll11l11_opy_((bstack1111l11l1l_opy_.bstack1111111l11_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1l1ll1111l1_opy_)
        bstack1llll1ll1ll_opy_.bstack1ll1ll11l11_opy_((bstack1111l11l1l_opy_.bstack1111111l11_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1l1ll11lll1_opy_)
        bstack1llll1ll1ll_opy_.bstack1ll1ll11l11_opy_((bstack1111l11l1l_opy_.bstack1lllllllll1_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1l1ll1l1111_opy_)
        bstack1llll1ll1ll_opy_.bstack1ll1ll11l11_opy_((bstack1111l11l1l_opy_.bstack1llllllll1l_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1l1ll11111l_opy_)
        bstack1llll1ll1ll_opy_.bstack1ll1ll11l11_opy_((bstack1111l11l1l_opy_.bstack1111111l11_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1l1ll111lll_opy_)
        bstack1llll1ll1ll_opy_.bstack1ll1ll11l11_opy_((bstack1111l11l1l_opy_.QUIT, bstack11111l1ll1_opy_.PRE), self.on_close)
        self.bstack1lll1ll1lll_opy_ = bstack1lll1ll1lll_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll1111l1_opy_(
        self,
        f: bstack1llll1ll1ll_opy_,
        bstack1l1l1llllll_opy_: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11111ll_opy_ (u"ࠦࡱࡧࡵ࡯ࡥ࡫ࠦቁ"):
            return
        if not bstack1l1lllll11l_opy_():
            self.logger.debug(bstack11111ll_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡱࡧࡵ࡯ࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤቂ"))
            return
        def wrapped(bstack1l1l1llllll_opy_, launch, *args, **kwargs):
            response = self.bstack1l1ll1111ll_opy_(f.platform_index, instance.ref(), json.dumps({bstack11111ll_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬቃ"): True}).encode(bstack11111ll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨቄ")))
            if response is not None and response.capabilities:
                if not bstack1l1lllll11l_opy_():
                    browser = launch(bstack1l1l1llllll_opy_)
                    return browser
                bstack1l1ll111111_opy_ = json.loads(response.capabilities.decode(bstack11111ll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢቅ")))
                if not bstack1l1ll111111_opy_: # empty caps bstack1l1ll11ll1l_opy_ bstack1l1ll11ll11_opy_ bstack1l1ll111l11_opy_ bstack1llllll1l1l_opy_ or error in processing
                    return
                bstack1l1ll11llll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1ll111111_opy_))
                f.bstack11111l11ll_opy_(instance, bstack1llll1ll1ll_opy_.bstack1l1ll11l1ll_opy_, bstack1l1ll11llll_opy_)
                f.bstack11111l11ll_opy_(instance, bstack1llll1ll1ll_opy_.bstack1l1ll111l1l_opy_, bstack1l1ll111111_opy_)
                browser = bstack1l1l1llllll_opy_.connect(bstack1l1ll11llll_opy_)
                return browser
        return wrapped
    def bstack1l1ll1l1111_opy_(
        self,
        f: bstack1llll1ll1ll_opy_,
        Connection: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11111ll_opy_ (u"ࠤࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠦቆ"):
            self.logger.debug(bstack11111ll_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤቇ"))
            return
        if not bstack1l1lllll11l_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack11111ll_opy_ (u"ࠫࡵࡧࡲࡢ࡯ࡶࠫቈ"), {}).get(bstack11111ll_opy_ (u"ࠬࡨࡳࡑࡣࡵࡥࡲࡹࠧ቉")):
                    bstack1l1ll11l11l_opy_ = args[0][bstack11111ll_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨቊ")][bstack11111ll_opy_ (u"ࠢࡣࡵࡓࡥࡷࡧ࡭ࡴࠤቋ")]
                    session_id = bstack1l1ll11l11l_opy_.get(bstack11111ll_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠦቌ"))
                    f.bstack11111l11ll_opy_(instance, bstack1llll1ll1ll_opy_.bstack1l1ll11l111_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack11111ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࠧቍ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1ll111lll_opy_(
        self,
        f: bstack1llll1ll1ll_opy_,
        bstack1l1l1llllll_opy_: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11111ll_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦ቎"):
            return
        if not bstack1l1lllll11l_opy_():
            self.logger.debug(bstack11111ll_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡧࡴࡴ࡮ࡦࡥࡷࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤ቏"))
            return
        def wrapped(bstack1l1l1llllll_opy_, connect, *args, **kwargs):
            response = self.bstack1l1ll1111ll_opy_(f.platform_index, instance.ref(), json.dumps({bstack11111ll_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫቐ"): True}).encode(bstack11111ll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧቑ")))
            if response is not None and response.capabilities:
                bstack1l1ll111111_opy_ = json.loads(response.capabilities.decode(bstack11111ll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨቒ")))
                if not bstack1l1ll111111_opy_:
                    return
                bstack1l1ll11llll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1ll111111_opy_))
                if bstack1l1ll111111_opy_.get(bstack11111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧቓ")):
                    browser = bstack1l1l1llllll_opy_.bstack1l1ll1l111l_opy_(bstack1l1ll11llll_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1ll11llll_opy_
                    return connect(bstack1l1l1llllll_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1ll11lll1_opy_(
        self,
        f: bstack1llll1ll1ll_opy_,
        bstack1ll11l1llll_opy_: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11111ll_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦቔ"):
            return
        if not bstack1l1lllll11l_opy_():
            self.logger.debug(bstack11111ll_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡱࡩࡼࡥࡰࡢࡩࡨࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤቕ"))
            return
        def wrapped(bstack1ll11l1llll_opy_, bstack1l1ll11l1l1_opy_, *args, **kwargs):
            contexts = bstack1ll11l1llll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack11111ll_opy_ (u"ࠦࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠤቖ") in page.url:
                                    return page
                    else:
                        return bstack1l1ll11l1l1_opy_(bstack1ll11l1llll_opy_)
        return wrapped
    def bstack1l1ll1111ll_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack11111ll_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࠥ቗") + str(req) + bstack11111ll_opy_ (u"ࠨࠢቘ"))
        try:
            r = self.bstack1llll1l1111_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11111ll_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥ቙") + str(r.success) + bstack11111ll_opy_ (u"ࠣࠤቚ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11111ll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢቛ") + str(e) + bstack11111ll_opy_ (u"ࠥࠦቜ"))
            traceback.print_exc()
            raise e
    def bstack1l1ll11111l_opy_(
        self,
        f: bstack1llll1ll1ll_opy_,
        Connection: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11111ll_opy_ (u"ࠦࡤࡹࡥ࡯ࡦࡢࡱࡪࡹࡳࡢࡩࡨࡣࡹࡵ࡟ࡴࡧࡵࡺࡪࡸࠢቝ"):
            return
        if not bstack1l1lllll11l_opy_():
            return
        def wrapped(Connection, bstack1l1ll111ll1_opy_, *args, **kwargs):
            return bstack1l1ll111ll1_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1llll1ll1ll_opy_,
        bstack1l1l1llllll_opy_: object,
        exec: Tuple[bstack1111l1111l_opy_, str],
        bstack11111l111l_opy_: Tuple[bstack1111l11l1l_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11111ll_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦ቞"):
            return
        if not bstack1l1lllll11l_opy_():
            self.logger.debug(bstack11111ll_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡩ࡬ࡰࡵࡨࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤ቟"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped