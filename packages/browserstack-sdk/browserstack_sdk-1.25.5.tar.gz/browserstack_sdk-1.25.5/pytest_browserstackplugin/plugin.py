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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1ll11l1lll_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1ll1l1ll_opy_, bstack1111l1l11_opy_, update, bstack11l11111l_opy_,
                                       bstack111l11ll1_opy_, bstack11llll1111_opy_, bstack11lllll11_opy_, bstack1l1lll1l_opy_,
                                       bstack1l111111l_opy_, bstack11ll1l111l_opy_, bstack11l1llll1_opy_, bstack1l11l111l_opy_,
                                       bstack1ll1l11l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l1l1llll1_opy_)
from browserstack_sdk.bstack1l111llll1_opy_ import bstack1ll1l1l1l1_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1ll1lllll_opy_
from bstack_utils.capture import bstack11l111lll1_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l1llll1_opy_, bstack1l1llll11l_opy_, bstack11llllll11_opy_, \
    bstack1l1l1l111_opy_
from bstack_utils.helper import bstack11ll111l1_opy_, bstack11l1l111l1l_opy_, bstack111l1l1ll1_opy_, bstack1l1ll11lll_opy_, bstack1llll1l1l11_opy_, bstack1lllllll11_opy_, \
    bstack11l1l1ll1l1_opy_, \
    bstack11l1lll11l1_opy_, bstack1llll11ll_opy_, bstack11l1ll1111_opy_, bstack11ll11l1111_opy_, bstack1l1l1ll1l_opy_, Notset, \
    bstack1ll1ll1ll_opy_, bstack11l1lll1l11_opy_, bstack11l1l11ll1l_opy_, Result, bstack11l1ll1l111_opy_, bstack11ll1111l1l_opy_, bstack111l11lll1_opy_, \
    bstack1111l11l_opy_, bstack1l111lll_opy_, bstack11l1llllll_opy_, bstack11l1lll1111_opy_
from bstack_utils.bstack11l11l1lll1_opy_ import bstack11l11ll1111_opy_
from bstack_utils.messages import bstack1ll1l1111l_opy_, bstack1l11ll11l1_opy_, bstack1lll1ll11l_opy_, bstack1ll1l1l11l_opy_, bstack1lllll11ll_opy_, \
    bstack1ll111llll_opy_, bstack1l1l1l1lll_opy_, bstack1ll1ll11l1_opy_, bstack1l111l1ll_opy_, bstack11l11lll1_opy_, \
    bstack1l111l1111_opy_, bstack1111lll1l_opy_
from bstack_utils.proxy import bstack11l11ll11_opy_, bstack1llll1l11l_opy_
from bstack_utils.bstack1l1l1lll_opy_ import bstack111l1l1l11l_opy_, bstack111l1l11ll1_opy_, bstack111l1l1llll_opy_, bstack111l1l1ll11_opy_, \
    bstack111l1l1l1l1_opy_, bstack111l1l111ll_opy_, bstack111l1l11lll_opy_, bstack1l1lll1l1l_opy_, bstack111l1l1l111_opy_
from bstack_utils.bstack1l11lll1l1_opy_ import bstack1l1l1ll11_opy_
from bstack_utils.bstack11111l11_opy_ import bstack111lll111_opy_, bstack1l1l111l11_opy_, bstack111l11lll_opy_, \
    bstack11lll1l11_opy_, bstack11llllll1_opy_
from bstack_utils.bstack111llll111_opy_ import bstack11l11l1111_opy_
from bstack_utils.bstack11l1111l1l_opy_ import bstack1lll111111_opy_
import bstack_utils.accessibility as bstack1ll1lll1l_opy_
from bstack_utils.bstack11l111l1ll_opy_ import bstack1ll1l11l1l_opy_
from bstack_utils.bstack1l11l111_opy_ import bstack1l11l111_opy_
from browserstack_sdk.__init__ import bstack1l1111lll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l1ll1_opy_ import bstack1llllll11ll_opy_
from browserstack_sdk.sdk_cli.bstack11ll11111l_opy_ import bstack11ll11111l_opy_, bstack11lll1l1l1_opy_, bstack1l1ll1l1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1ll11l11111_opy_, bstack11111ll1l1_opy_, bstack1111111l1l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11ll11111l_opy_ import bstack11ll11111l_opy_, bstack11lll1l1l1_opy_, bstack1l1ll1l1ll_opy_
bstack111llll1l_opy_ = None
bstack1l1lll11ll_opy_ = None
bstack1111ll1ll_opy_ = None
bstack1lllllll1_opy_ = None
bstack1ll1l1l1ll_opy_ = None
bstack1l111lll1l_opy_ = None
bstack1l111l1l1l_opy_ = None
bstack11l111lll_opy_ = None
bstack1ll1l11l1_opy_ = None
bstack11l11ll1_opy_ = None
bstack11ll11l1_opy_ = None
bstack1l11ll111_opy_ = None
bstack1l11l1l1l_opy_ = None
bstack1l111111ll_opy_ = bstack1ll1l11_opy_ (u"ࠩࠪὃ")
CONFIG = {}
bstack11l1llll1l_opy_ = False
bstack1l11ll1lll_opy_ = bstack1ll1l11_opy_ (u"ࠪࠫὄ")
bstack11l1111ll_opy_ = bstack1ll1l11_opy_ (u"ࠫࠬὅ")
bstack1l1l11l1l1_opy_ = False
bstack1lll11111_opy_ = []
bstack111l1lll_opy_ = bstack1l1llll1_opy_
bstack1111l111ll1_opy_ = bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ὆")
bstack11ll11ll11_opy_ = {}
bstack11l111111_opy_ = None
bstack1l1ll111l_opy_ = False
logger = bstack1ll1lllll_opy_.get_logger(__name__, bstack111l1lll_opy_)
store = {
    bstack1ll1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ὇"): []
}
bstack11111llll11_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111lll1ll1_opy_ = {}
current_test_uuid = None
cli_context = bstack1ll11l11111_opy_(
    test_framework_name=bstack11l1111l_opy_[bstack1ll1l11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࠭ࡃࡆࡇࠫὈ")] if bstack1l1l1ll1l_opy_() else bstack11l1111l_opy_[bstack1ll1l11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࠨὉ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1lllll1l11_opy_(page, bstack1llll11ll1_opy_):
    try:
        page.evaluate(bstack1ll1l11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥὊ"),
                      bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧὋ") + json.dumps(
                          bstack1llll11ll1_opy_) + bstack1ll1l11_opy_ (u"ࠦࢂࢃࠢὌ"))
    except Exception as e:
        print(bstack1ll1l11_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥὍ"), e)
def bstack11l11111_opy_(page, message, level):
    try:
        page.evaluate(bstack1ll1l11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ὎"), bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ὏") + json.dumps(
            message) + bstack1ll1l11_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫὐ") + json.dumps(level) + bstack1ll1l11_opy_ (u"ࠩࢀࢁࠬὑ"))
    except Exception as e:
        print(bstack1ll1l11_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࠨὒ"), e)
def pytest_configure(config):
    global bstack1l11ll1lll_opy_
    global CONFIG
    bstack11lll1111_opy_ = Config.bstack11111l1l1_opy_()
    config.args = bstack1lll111111_opy_.bstack1111l1l111l_opy_(config.args)
    bstack11lll1111_opy_.bstack1llll111l1_opy_(bstack11l1llllll_opy_(config.getoption(bstack1ll1l11_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨὓ"))))
    try:
        bstack1ll1lllll_opy_.bstack11l111ll111_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack11ll11111l_opy_.invoke(bstack11lll1l1l1_opy_.CONNECT, bstack1l1ll1l1ll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬὔ"), bstack1ll1l11_opy_ (u"࠭࠰ࠨὕ")))
        config = json.loads(os.environ.get(bstack1ll1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࠨὖ"), bstack1ll1l11_opy_ (u"ࠣࡽࢀࠦὗ")))
        cli.bstack1l11lll1lll_opy_(bstack11l1ll1111_opy_(bstack1l11ll1lll_opy_, CONFIG), cli_context.platform_index, bstack11l11111l_opy_)
    if cli.bstack1l11l1llll1_opy_(bstack1llllll11ll_opy_):
        cli.bstack1l1l111l11l_opy_()
        logger.debug(bstack1ll1l11_opy_ (u"ࠤࡆࡐࡎࠦࡩࡴࠢࡤࡧࡹ࡯ࡶࡦࠢࡩࡳࡷࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࠣ὘") + str(cli_context.platform_index) + bstack1ll1l11_opy_ (u"ࠥࠦὙ"))
        cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.BEFORE_ALL, bstack1111111l1l_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1ll1l11_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤ὚"), None)
    if cli.is_running() and when == bstack1ll1l11_opy_ (u"ࠧࡩࡡ࡭࡮ࠥὛ"):
        cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.LOG_REPORT, bstack1111111l1l_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack1ll1l11_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧ὜"):
            cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.BEFORE_EACH, bstack1111111l1l_opy_.POST, item, call, outcome)
        elif when == bstack1ll1l11_opy_ (u"ࠢࡤࡣ࡯ࡰࠧὝ"):
            cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.LOG_REPORT, bstack1111111l1l_opy_.POST, item, call, outcome)
        elif when == bstack1ll1l11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥ὞"):
            cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.AFTER_EACH, bstack1111111l1l_opy_.POST, item, call, outcome)
        return # skip all existing bstack11111llll1l_opy_
    bstack1111l11l11l_opy_ = item.config.getoption(bstack1ll1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫὟ"))
    plugins = item.config.getoption(bstack1ll1l11_opy_ (u"ࠥࡴࡱࡻࡧࡪࡰࡶࠦὠ"))
    report = outcome.get_result()
    bstack1111l111l1l_opy_(item, call, report)
    if bstack1ll1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠤὡ") not in plugins or bstack1l1l1ll1l_opy_():
        return
    summary = []
    driver = getattr(item, bstack1ll1l11_opy_ (u"ࠧࡥࡤࡳ࡫ࡹࡩࡷࠨὢ"), None)
    page = getattr(item, bstack1ll1l11_opy_ (u"ࠨ࡟ࡱࡣࡪࡩࠧὣ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1111l1111l1_opy_(item, report, summary, bstack1111l11l11l_opy_)
    if (page is not None):
        bstack11111ll11ll_opy_(item, report, summary, bstack1111l11l11l_opy_)
def bstack1111l1111l1_opy_(item, report, summary, bstack1111l11l11l_opy_):
    if report.when == bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ὤ") and report.skipped:
        bstack111l1l1l111_opy_(report)
    if report.when in [bstack1ll1l11_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢὥ"), bstack1ll1l11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦὦ")]:
        return
    if not bstack1llll1l1l11_opy_():
        return
    try:
        if (str(bstack1111l11l11l_opy_).lower() != bstack1ll1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨὧ") and not cli.is_running()):
            item._driver.execute_script(
                bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩὨ") + json.dumps(
                    report.nodeid) + bstack1ll1l11_opy_ (u"ࠬࢃࡽࠨὩ"))
        os.environ[bstack1ll1l11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩὪ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1ll1l11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦ࠼ࠣࡿ࠵ࢃࠢὫ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1l11_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥὬ")))
    bstack11l1l1l111_opy_ = bstack1ll1l11_opy_ (u"ࠤࠥὭ")
    bstack111l1l1l111_opy_(report)
    if not passed:
        try:
            bstack11l1l1l111_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1ll1l11_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥὮ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11l1l1l111_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1ll1l11_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨὯ")))
        bstack11l1l1l111_opy_ = bstack1ll1l11_opy_ (u"ࠧࠨὰ")
        if not passed:
            try:
                bstack11l1l1l111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll1l11_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨά").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11l1l1l111_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫὲ")
                    + json.dumps(bstack1ll1l11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠢࠤέ"))
                    + bstack1ll1l11_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧὴ")
                )
            else:
                item._driver.execute_script(
                    bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨή")
                    + json.dumps(str(bstack11l1l1l111_opy_))
                    + bstack1ll1l11_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢὶ")
                )
        except Exception as e:
            summary.append(bstack1ll1l11_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡥࡳࡴ࡯ࡵࡣࡷࡩ࠿ࠦࡻ࠱ࡿࠥί").format(e))
def bstack11111llllll_opy_(test_name, error_message):
    try:
        bstack11111lllll1_opy_ = []
        bstack1lll1l1l_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ὸ"), bstack1ll1l11_opy_ (u"ࠧ࠱ࠩό"))
        bstack11ll1llll_opy_ = {bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ὺ"): test_name, bstack1ll1l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨύ"): error_message, bstack1ll1l11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩὼ"): bstack1lll1l1l_opy_}
        bstack1111l11l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩώ"))
        if os.path.exists(bstack1111l11l1l1_opy_):
            with open(bstack1111l11l1l1_opy_) as f:
                bstack11111lllll1_opy_ = json.load(f)
        bstack11111lllll1_opy_.append(bstack11ll1llll_opy_)
        with open(bstack1111l11l1l1_opy_, bstack1ll1l11_opy_ (u"ࠬࡽࠧ὾")) as f:
            json.dump(bstack11111lllll1_opy_, f)
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡨࡶࡸ࡯ࡳࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡳࡽࡹ࡫ࡳࡵࠢࡨࡶࡷࡵࡲࡴ࠼ࠣࠫ὿") + str(e))
def bstack11111ll11ll_opy_(item, report, summary, bstack1111l11l11l_opy_):
    if report.when in [bstack1ll1l11_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᾀ"), bstack1ll1l11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᾁ")]:
        return
    if (str(bstack1111l11l11l_opy_).lower() != bstack1ll1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᾂ")):
        bstack1lllll1l11_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1l11_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᾃ")))
    bstack11l1l1l111_opy_ = bstack1ll1l11_opy_ (u"ࠦࠧᾄ")
    bstack111l1l1l111_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11l1l1l111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll1l11_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᾅ").format(e)
                )
        try:
            if passed:
                bstack11llllll1_opy_(getattr(item, bstack1ll1l11_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᾆ"), None), bstack1ll1l11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᾇ"))
            else:
                error_message = bstack1ll1l11_opy_ (u"ࠨࠩᾈ")
                if bstack11l1l1l111_opy_:
                    bstack11l11111_opy_(item._page, str(bstack11l1l1l111_opy_), bstack1ll1l11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣᾉ"))
                    bstack11llllll1_opy_(getattr(item, bstack1ll1l11_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩᾊ"), None), bstack1ll1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᾋ"), str(bstack11l1l1l111_opy_))
                    error_message = str(bstack11l1l1l111_opy_)
                else:
                    bstack11llllll1_opy_(getattr(item, bstack1ll1l11_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᾌ"), None), bstack1ll1l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᾍ"))
                bstack11111llllll_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1ll1l11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼ࠲ࢀࠦᾎ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1ll1l11_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᾏ"), default=bstack1ll1l11_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣᾐ"), help=bstack1ll1l11_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤᾑ"))
    parser.addoption(bstack1ll1l11_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᾒ"), default=bstack1ll1l11_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦᾓ"), help=bstack1ll1l11_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧᾔ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1ll1l11_opy_ (u"ࠢ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠤᾕ"), action=bstack1ll1l11_opy_ (u"ࠣࡵࡷࡳࡷ࡫ࠢᾖ"), default=bstack1ll1l11_opy_ (u"ࠤࡦ࡬ࡷࡵ࡭ࡦࠤᾗ"),
                         help=bstack1ll1l11_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴࠤᾘ"))
def bstack11l1111ll1_opy_(log):
    if not (log[bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᾙ")] and log[bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᾚ")].strip()):
        return
    active = bstack11l11l111l_opy_()
    log = {
        bstack1ll1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᾛ"): log[bstack1ll1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᾜ")],
        bstack1ll1l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᾝ"): bstack111l1l1ll1_opy_().isoformat() + bstack1ll1l11_opy_ (u"ࠩ࡝ࠫᾞ"),
        bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᾟ"): log[bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᾠ")],
    }
    if active:
        if active[bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪᾡ")] == bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᾢ"):
            log[bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᾣ")] = active[bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᾤ")]
        elif active[bstack1ll1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᾥ")] == bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࠨᾦ"):
            log[bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᾧ")] = active[bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᾨ")]
    bstack1ll1l11l1l_opy_.bstack1l1l11l1l_opy_([log])
def bstack11l11l111l_opy_():
    if len(store[bstack1ll1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᾩ")]) > 0 and store[bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᾪ")][-1]:
        return {
            bstack1ll1l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᾫ"): bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᾬ"),
            bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᾭ"): store[bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᾮ")][-1]
        }
    if store.get(bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᾯ"), None):
        return {
            bstack1ll1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫᾰ"): bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࠬᾱ"),
            bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᾲ"): store[bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᾳ")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.INIT_TEST, bstack1111111l1l_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.INIT_TEST, bstack1111111l1l_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.TEST, bstack1111111l1l_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._11111ll1l1l_opy_ = True
        bstack1l1111ll_opy_ = bstack1ll1lll1l_opy_.bstack11ll1ll1l1_opy_(bstack11l1lll11l1_opy_(item.own_markers))
        if not cli.bstack1l11l1llll1_opy_(bstack1llllll11ll_opy_):
            item._a11y_test_case = bstack1l1111ll_opy_
            if bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᾴ"), None):
                driver = getattr(item, bstack1ll1l11_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ᾵"), None)
                item._a11y_started = bstack1ll1lll1l_opy_.bstack1lllll111l_opy_(driver, bstack1l1111ll_opy_)
        if not bstack1ll1l11l1l_opy_.on() or bstack1111l111ll1_opy_ != bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᾶ"):
            return
        global current_test_uuid #, bstack111llllll1_opy_
        bstack111ll111l1_opy_ = {
            bstack1ll1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᾷ"): uuid4().__str__(),
            bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᾸ"): bstack111l1l1ll1_opy_().isoformat() + bstack1ll1l11_opy_ (u"ࠨ࡜ࠪᾹ")
        }
        current_test_uuid = bstack111ll111l1_opy_[bstack1ll1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᾺ")]
        store[bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧΆ")] = bstack111ll111l1_opy_[bstack1ll1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩᾼ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111lll1ll1_opy_[item.nodeid] = {**_111lll1ll1_opy_[item.nodeid], **bstack111ll111l1_opy_}
        bstack1111l111lll_opy_(item, _111lll1ll1_opy_[item.nodeid], bstack1ll1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭᾽"))
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡣࡢ࡮࡯࠾ࠥࢁࡽࠨι"), str(err))
def pytest_runtest_setup(item):
    store[bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ᾿")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.BEFORE_EACH, bstack1111111l1l_opy_.PRE, item, bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ῀"))
        return # skip all existing bstack11111llll1l_opy_
    global bstack11111llll11_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11ll11l1111_opy_():
        atexit.register(bstack1l111lll11_opy_)
        if not bstack11111llll11_opy_:
            try:
                bstack11111ll111l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1lll1111_opy_():
                    bstack11111ll111l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack11111ll111l_opy_:
                    signal.signal(s, bstack11111lll1l1_opy_)
                bstack11111llll11_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1ll1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡧࡪࡵࡷࡩࡷࠦࡳࡪࡩࡱࡥࡱࠦࡨࡢࡰࡧࡰࡪࡸࡳ࠻ࠢࠥ῁") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111l1l1l11l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1ll1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪῂ")
    try:
        if not bstack1ll1l11l1l_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111ll111l1_opy_ = {
            bstack1ll1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩῃ"): uuid,
            bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩῄ"): bstack111l1l1ll1_opy_().isoformat() + bstack1ll1l11_opy_ (u"࡚࠭ࠨ῅"),
            bstack1ll1l11_opy_ (u"ࠧࡵࡻࡳࡩࠬῆ"): bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰ࠭ῇ"),
            bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬῈ"): bstack1ll1l11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨΈ"),
            bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧῊ"): bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫΉ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1ll1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪῌ")] = item
        store[bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ῍")] = [uuid]
        if not _111lll1ll1_opy_.get(item.nodeid, None):
            _111lll1ll1_opy_[item.nodeid] = {bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ῎"): [], bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ῏"): []}
        _111lll1ll1_opy_[item.nodeid][bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩῐ")].append(bstack111ll111l1_opy_[bstack1ll1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩῑ")])
        _111lll1ll1_opy_[item.nodeid + bstack1ll1l11_opy_ (u"ࠬ࠳ࡳࡦࡶࡸࡴࠬῒ")] = bstack111ll111l1_opy_
        bstack11111ll1111_opy_(item, bstack111ll111l1_opy_, bstack1ll1l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧΐ"))
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪ῔"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.TEST, bstack1111111l1l_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.AFTER_EACH, bstack1111111l1l_opy_.PRE, item, bstack1ll1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ῕"))
        return # skip all existing bstack11111llll1l_opy_
    try:
        global bstack11ll11ll11_opy_
        bstack1lll1l1l_opy_ = 0
        if bstack1l1l11l1l1_opy_ is True:
            bstack1lll1l1l_opy_ = int(os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩῖ")))
        if bstack111l111l_opy_.bstack11l1ll1lll_opy_() == bstack1ll1l11_opy_ (u"ࠥࡸࡷࡻࡥࠣῗ"):
            if bstack111l111l_opy_.bstack111llll11_opy_() == bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨῘ"):
                bstack11111ll11l1_opy_ = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨῙ"), None)
                bstack1ll1l111_opy_ = bstack11111ll11l1_opy_ + bstack1ll1l11_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤῚ")
                driver = getattr(item, bstack1ll1l11_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨΊ"), None)
                bstack1l1111ll1l_opy_ = getattr(item, bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭῜"), None)
                bstack1lllll1111_opy_ = getattr(item, bstack1ll1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ῝"), None)
                PercySDK.screenshot(driver, bstack1ll1l111_opy_, bstack1l1111ll1l_opy_=bstack1l1111ll1l_opy_, bstack1lllll1111_opy_=bstack1lllll1111_opy_, bstack1ll11lll_opy_=bstack1lll1l1l_opy_)
        if not cli.bstack1l11l1llll1_opy_(bstack1llllll11ll_opy_):
            if getattr(item, bstack1ll1l11_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡶࡸࡦࡸࡴࡦࡦࠪ῞"), False):
                bstack1ll1l1l1l1_opy_.bstack11ll1111l1_opy_(getattr(item, bstack1ll1l11_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ῟"), None), bstack11ll11ll11_opy_, logger, item)
        if not bstack1ll1l11l1l_opy_.on():
            return
        bstack111ll111l1_opy_ = {
            bstack1ll1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪῠ"): uuid4().__str__(),
            bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪῡ"): bstack111l1l1ll1_opy_().isoformat() + bstack1ll1l11_opy_ (u"࡛ࠧࠩῢ"),
            bstack1ll1l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ΰ"): bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧῤ"),
            bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ῥ"): bstack1ll1l11_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨῦ"),
            bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨῧ"): bstack1ll1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨῨ")
        }
        _111lll1ll1_opy_[item.nodeid + bstack1ll1l11_opy_ (u"ࠧ࠮ࡶࡨࡥࡷࡪ࡯ࡸࡰࠪῩ")] = bstack111ll111l1_opy_
        bstack11111ll1111_opy_(item, bstack111ll111l1_opy_, bstack1ll1l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩῪ"))
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱ࠾ࠥࢁࡽࠨΎ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack111l1l1ll11_opy_(fixturedef.argname):
        store[bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩῬ")] = request.node
    elif bstack111l1l1l1l1_opy_(fixturedef.argname):
        store[bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩ῭")] = request.node
    if not bstack1ll1l11l1l_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.SETUP_FIXTURE, bstack1111111l1l_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.SETUP_FIXTURE, bstack1111111l1l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack11111llll1l_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.SETUP_FIXTURE, bstack1111111l1l_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.SETUP_FIXTURE, bstack1111111l1l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack11111llll1l_opy_
    try:
        fixture = {
            bstack1ll1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ΅"): fixturedef.argname,
            bstack1ll1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭`"): bstack11l1l1ll1l1_opy_(outcome),
            bstack1ll1l11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ῰"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ῱")]
        if not _111lll1ll1_opy_.get(current_test_item.nodeid, None):
            _111lll1ll1_opy_[current_test_item.nodeid] = {bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫῲ"): []}
        _111lll1ll1_opy_[current_test_item.nodeid][bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬῳ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1ll1l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧῴ"), str(err))
if bstack1l1l1ll1l_opy_() and bstack1ll1l11l1l_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.STEP, bstack1111111l1l_opy_.PRE, request, step)
            return
        try:
            _111lll1ll1_opy_[request.node.nodeid][bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ῵")].bstack1l111ll1l_opy_(id(step))
        except Exception as err:
            print(bstack1ll1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶ࠺ࠡࡽࢀࠫῶ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.STEP, bstack1111111l1l_opy_.POST, request, step, exception)
            return
        try:
            _111lll1ll1_opy_[request.node.nodeid][bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪῷ")].bstack111lllllll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1ll1l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬῸ"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.STEP, bstack1111111l1l_opy_.POST, request, step)
            return
        try:
            bstack111llll111_opy_: bstack11l11l1111_opy_ = _111lll1ll1_opy_[request.node.nodeid][bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬΌ")]
            bstack111llll111_opy_.bstack111lllllll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1ll1l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧῺ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1111l111ll1_opy_
        try:
            if not bstack1ll1l11l1l_opy_.on() or bstack1111l111ll1_opy_ != bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨΏ"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.TEST, bstack1111111l1l_opy_.PRE, request, feature, scenario)
                return
            driver = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫῼ"), None)
            if not _111lll1ll1_opy_.get(request.node.nodeid, None):
                _111lll1ll1_opy_[request.node.nodeid] = {}
            bstack111llll111_opy_ = bstack11l11l1111_opy_.bstack111l1111l1l_opy_(
                scenario, feature, request.node,
                name=bstack111l1l111ll_opy_(request.node, scenario),
                started_at=bstack1lllllll11_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1ll1l11_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ´"),
                tags=bstack111l1l11lll_opy_(feature, scenario),
                bstack11l1111lll_opy_=bstack1ll1l11l1l_opy_.bstack11l111ll11_opy_(driver) if driver and driver.session_id else {}
            )
            _111lll1ll1_opy_[request.node.nodeid][bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ῾")] = bstack111llll111_opy_
            bstack11111ll1lll_opy_(bstack111llll111_opy_.uuid)
            bstack1ll1l11l1l_opy_.bstack111lllll1l_opy_(bstack1ll1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ῿"), bstack111llll111_opy_)
        except Exception as err:
            print(bstack1ll1l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫ "), str(err))
def bstack1111l111111_opy_(bstack11l1111111_opy_):
    if bstack11l1111111_opy_ in store[bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ ")]:
        store[bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ ")].remove(bstack11l1111111_opy_)
def bstack11111ll1lll_opy_(test_uuid):
    store[bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ ")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1ll1l11l1l_opy_.bstack1111lll1ll1_opy_
def bstack1111l111l1l_opy_(item, call, report):
    logger.debug(bstack1ll1l11_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡸࡴࠨ "))
    global bstack1111l111ll1_opy_
    bstack11111l1ll_opy_ = bstack1lllllll11_opy_()
    if hasattr(report, bstack1ll1l11_opy_ (u"ࠧࡴࡶࡲࡴࠬ ")):
        bstack11111l1ll_opy_ = bstack11l1ll1l111_opy_(report.stop)
    elif hasattr(report, bstack1ll1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࠧ ")):
        bstack11111l1ll_opy_ = bstack11l1ll1l111_opy_(report.start)
    try:
        if getattr(report, bstack1ll1l11_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ "), bstack1ll1l11_opy_ (u"ࠪࠫ ")) == bstack1ll1l11_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ "):
            logger.debug(bstack1ll1l11_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡹ࡫ࠠ࠮ࠢࡾࢁ࠱ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࠰ࠤࢀࢃࠧ ").format(getattr(report, bstack1ll1l11_opy_ (u"࠭ࡷࡩࡧࡱࠫ​"), bstack1ll1l11_opy_ (u"ࠧࠨ‌")).__str__(), bstack1111l111ll1_opy_))
            if bstack1111l111ll1_opy_ == bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ‍"):
                _111lll1ll1_opy_[item.nodeid][bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ‎")] = bstack11111l1ll_opy_
                bstack1111l111lll_opy_(item, _111lll1ll1_opy_[item.nodeid], bstack1ll1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ‏"), report, call)
                store[bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ‐")] = None
            elif bstack1111l111ll1_opy_ == bstack1ll1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤ‑"):
                bstack111llll111_opy_ = _111lll1ll1_opy_[item.nodeid][bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ‒")]
                bstack111llll111_opy_.set(hooks=_111lll1ll1_opy_[item.nodeid].get(bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭–"), []))
                exception, bstack111llll1l1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111llll1l1_opy_ = [call.excinfo.exconly(), getattr(report, bstack1ll1l11_opy_ (u"ࠨ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠧ—"), bstack1ll1l11_opy_ (u"ࠩࠪ―"))]
                bstack111llll111_opy_.stop(time=bstack11111l1ll_opy_, result=Result(result=getattr(report, bstack1ll1l11_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ‖"), bstack1ll1l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ‗")), exception=exception, bstack111llll1l1_opy_=bstack111llll1l1_opy_))
                bstack1ll1l11l1l_opy_.bstack111lllll1l_opy_(bstack1ll1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ‘"), _111lll1ll1_opy_[item.nodeid][bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ’")])
        elif getattr(report, bstack1ll1l11_opy_ (u"ࠧࡸࡪࡨࡲࠬ‚"), bstack1ll1l11_opy_ (u"ࠨࠩ‛")) in [bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ“"), bstack1ll1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ”")]:
            logger.debug(bstack1ll1l11_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡸࡪࠦ࠭ࠡࡽࢀ࠰ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࠯ࠣࡿࢂ࠭„").format(getattr(report, bstack1ll1l11_opy_ (u"ࠬࡽࡨࡦࡰࠪ‟"), bstack1ll1l11_opy_ (u"࠭ࠧ†")).__str__(), bstack1111l111ll1_opy_))
            bstack111llll1ll_opy_ = item.nodeid + bstack1ll1l11_opy_ (u"ࠧ࠮ࠩ‡") + getattr(report, bstack1ll1l11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭•"), bstack1ll1l11_opy_ (u"ࠩࠪ‣"))
            if getattr(report, bstack1ll1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ․"), False):
                hook_type = bstack1ll1l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ‥") if getattr(report, bstack1ll1l11_opy_ (u"ࠬࡽࡨࡦࡰࠪ…"), bstack1ll1l11_opy_ (u"࠭ࠧ‧")) == bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ ") else bstack1ll1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ ")
                _111lll1ll1_opy_[bstack111llll1ll_opy_] = {
                    bstack1ll1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ‪"): uuid4().__str__(),
                    bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ‫"): bstack11111l1ll_opy_,
                    bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ‬"): hook_type
                }
            _111lll1ll1_opy_[bstack111llll1ll_opy_][bstack1ll1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ‭")] = bstack11111l1ll_opy_
            bstack1111l111111_opy_(_111lll1ll1_opy_[bstack111llll1ll_opy_][bstack1ll1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ‮")])
            bstack11111ll1111_opy_(item, _111lll1ll1_opy_[bstack111llll1ll_opy_], bstack1ll1l11_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ "), report, call)
            if getattr(report, bstack1ll1l11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭‰"), bstack1ll1l11_opy_ (u"ࠩࠪ‱")) == bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ′"):
                if getattr(report, bstack1ll1l11_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ″"), bstack1ll1l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ‴")) == bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭‵"):
                    bstack111ll111l1_opy_ = {
                        bstack1ll1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ‶"): uuid4().__str__(),
                        bstack1ll1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ‷"): bstack1lllllll11_opy_(),
                        bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ‸"): bstack1lllllll11_opy_()
                    }
                    _111lll1ll1_opy_[item.nodeid] = {**_111lll1ll1_opy_[item.nodeid], **bstack111ll111l1_opy_}
                    bstack1111l111lll_opy_(item, _111lll1ll1_opy_[item.nodeid], bstack1ll1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ‹"))
                    bstack1111l111lll_opy_(item, _111lll1ll1_opy_[item.nodeid], bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭›"), report, call)
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡼࡿࠪ※"), str(err))
def bstack1111l11ll1l_opy_(test, bstack111ll111l1_opy_, result=None, call=None, bstack1l11l1ll1l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111llll111_opy_ = {
        bstack1ll1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ‼"): bstack111ll111l1_opy_[bstack1ll1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ‽")],
        bstack1ll1l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭‾"): bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺࠧ‿"),
        bstack1ll1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ⁀"): test.name,
        bstack1ll1l11_opy_ (u"ࠫࡧࡵࡤࡺࠩ⁁"): {
            bstack1ll1l11_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ⁂"): bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭⁃"),
            bstack1ll1l11_opy_ (u"ࠧࡤࡱࡧࡩࠬ⁄"): inspect.getsource(test.obj)
        },
        bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⁅"): test.name,
        bstack1ll1l11_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨ⁆"): test.name,
        bstack1ll1l11_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ⁇"): bstack1lll111111_opy_.bstack111ll11ll1_opy_(test),
        bstack1ll1l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ⁈"): file_path,
        bstack1ll1l11_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧ⁉"): file_path,
        bstack1ll1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⁊"): bstack1ll1l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⁋"),
        bstack1ll1l11_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭⁌"): file_path,
        bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⁍"): bstack111ll111l1_opy_[bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⁎")],
        bstack1ll1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ⁏"): bstack1ll1l11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ⁐"),
        bstack1ll1l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩ⁑"): {
            bstack1ll1l11_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫ⁒"): test.nodeid
        },
        bstack1ll1l11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭⁓"): bstack11l1lll11l1_opy_(test.own_markers)
    }
    if bstack1l11l1ll1l_opy_ in [bstack1ll1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ⁔"), bstack1ll1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⁕")]:
        bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡴࡢࠩ⁖")] = {
            bstack1ll1l11_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ⁗"): bstack111ll111l1_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ⁘"), [])
        }
    if bstack1l11l1ll1l_opy_ == bstack1ll1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ⁙"):
        bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⁚")] = bstack1ll1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⁛")
        bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⁜")] = bstack111ll111l1_opy_[bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⁝")]
        bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⁞")] = bstack111ll111l1_opy_[bstack1ll1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ ")]
    if result:
        bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⁠")] = result.outcome
        bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⁡")] = result.duration * 1000
        bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⁢")] = bstack111ll111l1_opy_[bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⁣")]
        if result.failed:
            bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⁤")] = bstack1ll1l11l1l_opy_.bstack1111ll1111_opy_(call.excinfo.typename)
            bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⁥")] = bstack1ll1l11l1l_opy_.bstack1111ll1ll11_opy_(call.excinfo, result)
        bstack111llll111_opy_[bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⁦")] = bstack111ll111l1_opy_[bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⁧")]
    if outcome:
        bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⁨")] = bstack11l1l1ll1l1_opy_(outcome)
        bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⁩")] = 0
        bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⁪")] = bstack111ll111l1_opy_[bstack1ll1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⁫")]
        if bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⁬")] == bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⁭"):
            bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭⁮")] = bstack1ll1l11_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩ⁯")  # bstack11111lll111_opy_
            bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ⁰")] = [{bstack1ll1l11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ⁱ"): [bstack1ll1l11_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨ⁲")]}]
        bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⁳")] = bstack111ll111l1_opy_[bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⁴")]
    return bstack111llll111_opy_
def bstack1111l111l11_opy_(test, bstack111ll11lll_opy_, bstack1l11l1ll1l_opy_, result, call, outcome, bstack11111l1llll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111ll11lll_opy_[bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⁵")]
    hook_name = bstack111ll11lll_opy_[bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ⁶")]
    hook_data = {
        bstack1ll1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⁷"): bstack111ll11lll_opy_[bstack1ll1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⁸")],
        bstack1ll1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩ⁹"): bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⁺"),
        bstack1ll1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⁻"): bstack1ll1l11_opy_ (u"ࠧࡼࡿࠪ⁼").format(bstack111l1l11ll1_opy_(hook_name)),
        bstack1ll1l11_opy_ (u"ࠨࡤࡲࡨࡾ࠭⁽"): {
            bstack1ll1l11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧ⁾"): bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪⁿ"),
            bstack1ll1l11_opy_ (u"ࠫࡨࡵࡤࡦࠩ₀"): None
        },
        bstack1ll1l11_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫ₁"): test.name,
        bstack1ll1l11_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭₂"): bstack1lll111111_opy_.bstack111ll11ll1_opy_(test, hook_name),
        bstack1ll1l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ₃"): file_path,
        bstack1ll1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪ₄"): file_path,
        bstack1ll1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ₅"): bstack1ll1l11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ₆"),
        bstack1ll1l11_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩ₇"): file_path,
        bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ₈"): bstack111ll11lll_opy_[bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ₉")],
        bstack1ll1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ₊"): bstack1ll1l11_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ₋") if bstack1111l111ll1_opy_ == bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭₌") else bstack1ll1l11_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ₍"),
        bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ₎"): hook_type
    }
    bstack1111llll11l_opy_ = bstack111l1lllll_opy_(_111lll1ll1_opy_.get(test.nodeid, None))
    if bstack1111llll11l_opy_:
        hook_data[bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪ₏")] = bstack1111llll11l_opy_
    if result:
        hook_data[bstack1ll1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ₐ")] = result.outcome
        hook_data[bstack1ll1l11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨₑ")] = result.duration * 1000
        hook_data[bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ₒ")] = bstack111ll11lll_opy_[bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧₓ")]
        if result.failed:
            hook_data[bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩₔ")] = bstack1ll1l11l1l_opy_.bstack1111ll1111_opy_(call.excinfo.typename)
            hook_data[bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬₕ")] = bstack1ll1l11l1l_opy_.bstack1111ll1ll11_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1ll1l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬₖ")] = bstack11l1l1ll1l1_opy_(outcome)
        hook_data[bstack1ll1l11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧₗ")] = 100
        hook_data[bstack1ll1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬₘ")] = bstack111ll11lll_opy_[bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ₙ")]
        if hook_data[bstack1ll1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩₚ")] == bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪₛ"):
            hook_data[bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪₜ")] = bstack1ll1l11_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭₝")  # bstack11111lll111_opy_
            hook_data[bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ₞")] = [{bstack1ll1l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ₟"): [bstack1ll1l11_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬ₠")]}]
    if bstack11111l1llll_opy_:
        hook_data[bstack1ll1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ₡")] = bstack11111l1llll_opy_.result
        hook_data[bstack1ll1l11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ₢")] = bstack11l1lll1l11_opy_(bstack111ll11lll_opy_[bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ₣")], bstack111ll11lll_opy_[bstack1ll1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ₤")])
        hook_data[bstack1ll1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ₥")] = bstack111ll11lll_opy_[bstack1ll1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ₦")]
        if hook_data[bstack1ll1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ₧")] == bstack1ll1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ₨"):
            hook_data[bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ₩")] = bstack1ll1l11l1l_opy_.bstack1111ll1111_opy_(bstack11111l1llll_opy_.exception_type)
            hook_data[bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ₪")] = [{bstack1ll1l11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ₫"): bstack11l1l11ll1l_opy_(bstack11111l1llll_opy_.exception)}]
    return hook_data
def bstack1111l111lll_opy_(test, bstack111ll111l1_opy_, bstack1l11l1ll1l_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1ll1l11_opy_ (u"࠭ࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡥࡷࡧࡱࡸ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡶࡨࡷࡹࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠥ࠳ࠠࡼࡿࠪ€").format(bstack1l11l1ll1l_opy_))
    bstack111llll111_opy_ = bstack1111l11ll1l_opy_(test, bstack111ll111l1_opy_, result, call, bstack1l11l1ll1l_opy_, outcome)
    driver = getattr(test, bstack1ll1l11_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ₭"), None)
    if bstack1l11l1ll1l_opy_ == bstack1ll1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ₮") and driver:
        bstack111llll111_opy_[bstack1ll1l11_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ₯")] = bstack1ll1l11l1l_opy_.bstack11l111ll11_opy_(driver)
    if bstack1l11l1ll1l_opy_ == bstack1ll1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ₰"):
        bstack1l11l1ll1l_opy_ = bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭₱")
    bstack111ll1l1l1_opy_ = {
        bstack1ll1l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ₲"): bstack1l11l1ll1l_opy_,
        bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ₳"): bstack111llll111_opy_
    }
    bstack1ll1l11l1l_opy_.bstack11l1lll111_opy_(bstack111ll1l1l1_opy_)
    if bstack1l11l1ll1l_opy_ == bstack1ll1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ₴"):
        threading.current_thread().bstackTestMeta = {bstack1ll1l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ₵"): bstack1ll1l11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ₶")}
    elif bstack1l11l1ll1l_opy_ == bstack1ll1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ₷"):
        threading.current_thread().bstackTestMeta = {bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ₸"): getattr(result, bstack1ll1l11_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭₹"), bstack1ll1l11_opy_ (u"࠭ࠧ₺"))}
def bstack11111ll1111_opy_(test, bstack111ll111l1_opy_, bstack1l11l1ll1l_opy_, result=None, call=None, outcome=None, bstack11111l1llll_opy_=None):
    logger.debug(bstack1ll1l11_opy_ (u"ࠧࡴࡧࡱࡨࡤ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡦࡸࡨࡲࡹࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢ࡫ࡳࡴࡱࠠࡥࡣࡷࡥ࠱ࠦࡥࡷࡧࡱࡸ࡙ࡿࡰࡦࠢ࠰ࠤࢀࢃࠧ₻").format(bstack1l11l1ll1l_opy_))
    hook_data = bstack1111l111l11_opy_(test, bstack111ll111l1_opy_, bstack1l11l1ll1l_opy_, result, call, outcome, bstack11111l1llll_opy_)
    bstack111ll1l1l1_opy_ = {
        bstack1ll1l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ₼"): bstack1l11l1ll1l_opy_,
        bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫ₽"): hook_data
    }
    bstack1ll1l11l1l_opy_.bstack11l1lll111_opy_(bstack111ll1l1l1_opy_)
def bstack111l1lllll_opy_(bstack111ll111l1_opy_):
    if not bstack111ll111l1_opy_:
        return None
    if bstack111ll111l1_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭₾"), None):
        return getattr(bstack111ll111l1_opy_[bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ₿")], bstack1ll1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ⃀"), None)
    return bstack111ll111l1_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⃁"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.LOG, bstack1111111l1l_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_.LOG, bstack1111111l1l_opy_.POST, request, caplog)
        return # skip all existing bstack11111llll1l_opy_
    try:
        if not bstack1ll1l11l1l_opy_.on():
            return
        places = [bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⃂"), bstack1ll1l11_opy_ (u"ࠨࡥࡤࡰࡱ࠭⃃"), bstack1ll1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ⃄")]
        logs = []
        for bstack11111lll1ll_opy_ in places:
            records = caplog.get_records(bstack11111lll1ll_opy_)
            bstack1111l11l111_opy_ = bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⃅") if bstack11111lll1ll_opy_ == bstack1ll1l11_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ⃆") else bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⃇")
            bstack11111ll1ll1_opy_ = request.node.nodeid + (bstack1ll1l11_opy_ (u"࠭ࠧ⃈") if bstack11111lll1ll_opy_ == bstack1ll1l11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ⃉") else bstack1ll1l11_opy_ (u"ࠨ࠯ࠪ⃊") + bstack11111lll1ll_opy_)
            test_uuid = bstack111l1lllll_opy_(_111lll1ll1_opy_.get(bstack11111ll1ll1_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11ll1111l1l_opy_(record.message):
                    continue
                logs.append({
                    bstack1ll1l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⃋"): bstack11l1l111l1l_opy_(record.created).isoformat() + bstack1ll1l11_opy_ (u"ࠪ࡞ࠬ⃌"),
                    bstack1ll1l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⃍"): record.levelname,
                    bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⃎"): record.message,
                    bstack1111l11l111_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1ll1l11l1l_opy_.bstack1l1l11l1l_opy_(logs)
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡤࡱࡱࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡀࠠࡼࡿࠪ⃏"), str(err))
def bstack1ll1l11lll_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1ll111l_opy_
    bstack1lll1lllll_opy_ = bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ⃐"), None) and bstack11ll111l1_opy_(
            threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⃑"), None)
    bstack1l1l1l1l1l_opy_ = getattr(driver, bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯⃒ࠩ"), None) != None and getattr(driver, bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰ⃓ࠪ"), None) == True
    if sequence == bstack1ll1l11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ⃔") and driver != None:
      if not bstack1l1ll111l_opy_ and bstack1llll1l1l11_opy_() and bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⃕") in CONFIG and CONFIG[bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⃖")] == True and bstack1l11l111_opy_.bstack1l1l11ll1l_opy_(driver_command) and (bstack1l1l1l1l1l_opy_ or bstack1lll1lllll_opy_) and not bstack1l1l1llll1_opy_(args):
        try:
          bstack1l1ll111l_opy_ = True
          logger.debug(bstack1ll1l11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡻࡾࠩ⃗").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1ll1l11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡹࡣࡢࡰࠣࡿࢂ⃘࠭").format(str(err)))
        bstack1l1ll111l_opy_ = False
    if sequence == bstack1ll1l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ⃙"):
        if driver_command == bstack1ll1l11_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺ⃚ࠧ"):
            bstack1ll1l11l1l_opy_.bstack1ll1llll11_opy_({
                bstack1ll1l11_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ⃛"): response[bstack1ll1l11_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ⃜")],
                bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⃝"): store[bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⃞")]
            })
def bstack1l111lll11_opy_():
    global bstack1lll11111_opy_
    bstack1ll1lllll_opy_.bstack1l11l1ll1_opy_()
    logging.shutdown()
    bstack1ll1l11l1l_opy_.bstack111l1llll1_opy_()
    for driver in bstack1lll11111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11111lll1l1_opy_(*args):
    global bstack1lll11111_opy_
    bstack1ll1l11l1l_opy_.bstack111l1llll1_opy_()
    for driver in bstack1lll11111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11ll1ll11l_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack11ll111l_opy_(self, *args, **kwargs):
    bstack11l1l1ll1l_opy_ = bstack111llll1l_opy_(self, *args, **kwargs)
    bstack111l1l1l1_opy_ = getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩ⃟"), None)
    if bstack111l1l1l1_opy_ and bstack111l1l1l1_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⃠"), bstack1ll1l11_opy_ (u"ࠪࠫ⃡")) == bstack1ll1l11_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⃢"):
        bstack1ll1l11l1l_opy_.bstack1ll11ll11_opy_(self)
    return bstack11l1l1ll1l_opy_
@measure(event_name=EVENTS.bstack11ll1l1l_opy_, stage=STAGE.bstack1l11l1l1ll_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1ll1lll1l1_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11lll1111_opy_ = Config.bstack11111l1l1_opy_()
    if bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ⃣")):
        return
    bstack11lll1111_opy_.bstack1lll11lll1_opy_(bstack1ll1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ⃤"), True)
    global bstack1l111111ll_opy_
    global bstack1l1ll1lll_opy_
    bstack1l111111ll_opy_ = framework_name
    logger.info(bstack1111lll1l_opy_.format(bstack1l111111ll_opy_.split(bstack1ll1l11_opy_ (u"ࠧ࠮⃥ࠩ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1llll1l1l11_opy_():
            Service.start = bstack11lllll11_opy_
            Service.stop = bstack1l1lll1l_opy_
            webdriver.Remote.get = bstack1l1l1llll_opy_
            webdriver.Remote.__init__ = bstack1111l11l1_opy_
            if not isinstance(os.getenv(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍ⃦ࠩ")), str):
                return
            WebDriver.close = bstack1l111111l_opy_
            WebDriver.quit = bstack1ll11111_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1ll1l11l1l_opy_.on():
            webdriver.Remote.__init__ = bstack11ll111l_opy_
        bstack1l1ll1lll_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ⃧")):
        bstack1l1ll1lll_opy_ = eval(os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨ⃨")))
    if not bstack1l1ll1lll_opy_:
        bstack11l1llll1_opy_(bstack1ll1l11_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨ⃩"), bstack1l111l1111_opy_)
    if bstack11l1lll11l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._11l11lllll_opy_ = bstack1l1l1l1ll1_opy_
        except Exception as e:
            logger.error(bstack1ll111llll_opy_.format(str(e)))
    if bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ⃪ࠬ") in str(framework_name).lower():
        if not bstack1llll1l1l11_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack111l11ll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11llll1111_opy_
            Config.getoption = bstack1l1l1l1l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l1ll11ll_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1l11l111_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1ll11111_opy_(self):
    global bstack1l111111ll_opy_
    global bstack1lllllll1l_opy_
    global bstack1l1lll11ll_opy_
    try:
        if bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ⃫࠭") in bstack1l111111ll_opy_ and self.session_id != None and bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶ⃬ࠫ"), bstack1ll1l11_opy_ (u"ࠨ⃭ࠩ")) != bstack1ll1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦ⃮ࠪ"):
            bstack11lll111ll_opy_ = bstack1ll1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦ⃯ࠪ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⃰")
            bstack1l111lll_opy_(logger, True)
            if self != None:
                bstack11lll1l11_opy_(self, bstack11lll111ll_opy_, bstack1ll1l11_opy_ (u"ࠬ࠲ࠠࠨ⃱").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1l11l1llll1_opy_(bstack1llllll11ll_opy_):
            item = store.get(bstack1ll1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⃲"), None)
            if item is not None and bstack11ll111l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭⃳"), None):
                bstack1ll1l1l1l1_opy_.bstack11ll1111l1_opy_(self, bstack11ll11ll11_opy_, logger, item)
        threading.current_thread().testStatus = bstack1ll1l11_opy_ (u"ࠨࠩ⃴")
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥ⃵") + str(e))
    bstack1l1lll11ll_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1ll1111ll_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1111l11l1_opy_(self, command_executor,
             desired_capabilities=None, bstack11llll1ll1_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1lllllll1l_opy_
    global bstack11l111111_opy_
    global bstack1l1l11l1l1_opy_
    global bstack1l111111ll_opy_
    global bstack111llll1l_opy_
    global bstack1lll11111_opy_
    global bstack1l11ll1lll_opy_
    global bstack11l1111ll_opy_
    global bstack11ll11ll11_opy_
    CONFIG[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ⃶")] = str(bstack1l111111ll_opy_) + str(__version__)
    command_executor = bstack11l1ll1111_opy_(bstack1l11ll1lll_opy_, CONFIG)
    logger.debug(bstack1ll1l1l11l_opy_.format(command_executor))
    proxy = bstack1ll1l11l_opy_(CONFIG, proxy)
    bstack1lll1l1l_opy_ = 0
    try:
        if bstack1l1l11l1l1_opy_ is True:
            bstack1lll1l1l_opy_ = int(os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⃷")))
    except:
        bstack1lll1l1l_opy_ = 0
    bstack11ll1111ll_opy_ = bstack1ll1l1ll_opy_(CONFIG, bstack1lll1l1l_opy_)
    logger.debug(bstack1ll1ll11l1_opy_.format(str(bstack11ll1111ll_opy_)))
    bstack11ll11ll11_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⃸"))[bstack1lll1l1l_opy_]
    if bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⃹") in CONFIG and CONFIG[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⃺")]:
        bstack111l11lll_opy_(bstack11ll1111ll_opy_, bstack11l1111ll_opy_)
    if bstack1ll1lll1l_opy_.bstack1l1lllll1_opy_(CONFIG, bstack1lll1l1l_opy_) and bstack1ll1lll1l_opy_.bstack1l111ll111_opy_(bstack11ll1111ll_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1l11l1llll1_opy_(bstack1llllll11ll_opy_):
            bstack1ll1lll1l_opy_.set_capabilities(bstack11ll1111ll_opy_, CONFIG)
    if desired_capabilities:
        bstack1ll1l1l1_opy_ = bstack1111l1l11_opy_(desired_capabilities)
        bstack1ll1l1l1_opy_[bstack1ll1l11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ⃻")] = bstack1ll1ll1ll_opy_(CONFIG)
        bstack111ll111l_opy_ = bstack1ll1l1ll_opy_(bstack1ll1l1l1_opy_)
        if bstack111ll111l_opy_:
            bstack11ll1111ll_opy_ = update(bstack111ll111l_opy_, bstack11ll1111ll_opy_)
        desired_capabilities = None
    if options:
        bstack11ll1l111l_opy_(options, bstack11ll1111ll_opy_)
    if not options:
        options = bstack11l11111l_opy_(bstack11ll1111ll_opy_)
    if proxy and bstack1llll11ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ⃼")):
        options.proxy(proxy)
    if options and bstack1llll11ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ⃽")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1llll11ll_opy_() < version.parse(bstack1ll1l11_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ⃾")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11ll1111ll_opy_)
    logger.info(bstack1lll1ll11l_opy_)
    bstack1ll11l1lll_opy_.end(EVENTS.bstack11ll1l1l_opy_.value, EVENTS.bstack11ll1l1l_opy_.value + bstack1ll1l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ⃿"),
                               EVENTS.bstack11ll1l1l_opy_.value + bstack1ll1l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ℀"), True, None)
    if bstack1llll11ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ℁")):
        bstack111llll1l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1llll11ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧℂ")):
        bstack111llll1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack11llll1ll1_opy_=bstack11llll1ll1_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1llll11ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ℃")):
        bstack111llll1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11llll1ll1_opy_=bstack11llll1ll1_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack111llll1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11llll1ll1_opy_=bstack11llll1ll1_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1l11l11ll1_opy_ = bstack1ll1l11_opy_ (u"ࠪࠫ℄")
        if bstack1llll11ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ℅")):
            bstack1l11l11ll1_opy_ = self.caps.get(bstack1ll1l11_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ℆"))
        else:
            bstack1l11l11ll1_opy_ = self.capabilities.get(bstack1ll1l11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨℇ"))
        if bstack1l11l11ll1_opy_:
            bstack1111l11l_opy_(bstack1l11l11ll1_opy_)
            if bstack1llll11ll_opy_() <= version.parse(bstack1ll1l11_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ℈")):
                self.command_executor._url = bstack1ll1l11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ℉") + bstack1l11ll1lll_opy_ + bstack1ll1l11_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨℊ")
            else:
                self.command_executor._url = bstack1ll1l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧℋ") + bstack1l11l11ll1_opy_ + bstack1ll1l11_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧℌ")
            logger.debug(bstack1l11ll11l1_opy_.format(bstack1l11l11ll1_opy_))
        else:
            logger.debug(bstack1ll1l1111l_opy_.format(bstack1ll1l11_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨℍ")))
    except Exception as e:
        logger.debug(bstack1ll1l1111l_opy_.format(e))
    bstack1lllllll1l_opy_ = self.session_id
    if bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ℎ") in bstack1l111111ll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫℏ"), None)
        if item:
            bstack11111lll11l_opy_ = getattr(item, bstack1ll1l11_opy_ (u"ࠨࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࡤࡹࡴࡢࡴࡷࡩࡩ࠭ℐ"), False)
            if not getattr(item, bstack1ll1l11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪℑ"), None) and bstack11111lll11l_opy_:
                setattr(store[bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧℒ")], bstack1ll1l11_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬℓ"), self)
        bstack111l1l1l1_opy_ = getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭℔"), None)
        if bstack111l1l1l1_opy_ and bstack111l1l1l1_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ℕ"), bstack1ll1l11_opy_ (u"ࠧࠨ№")) == bstack1ll1l11_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ℗"):
            bstack1ll1l11l1l_opy_.bstack1ll11ll11_opy_(self)
    bstack1lll11111_opy_.append(self)
    if bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ℘") in CONFIG and bstack1ll1l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨℙ") in CONFIG[bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧℚ")][bstack1lll1l1l_opy_]:
        bstack11l111111_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨℛ")][bstack1lll1l1l_opy_][bstack1ll1l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫℜ")]
    logger.debug(bstack11l11lll1_opy_.format(bstack1lllllll1l_opy_))
@measure(event_name=EVENTS.bstack11ll1l11l1_opy_, stage=STAGE.bstack1l11lll1l_opy_, bstack1l1ll111l1_opy_=bstack11l111111_opy_)
def bstack1l1l1llll_opy_(self, url):
    global bstack1ll1l11l1_opy_
    global CONFIG
    try:
        bstack1l1l111l11_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l111l1ll_opy_.format(str(err)))
    try:
        bstack1ll1l11l1_opy_(self, url)
    except Exception as e:
        try:
            bstack1l1lll1ll1_opy_ = str(e)
            if any(err_msg in bstack1l1lll1ll1_opy_ for err_msg in bstack11llllll11_opy_):
                bstack1l1l111l11_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l111l1ll_opy_.format(str(err)))
        raise e
def bstack1lll1l11l1_opy_(item, when):
    global bstack1l11ll111_opy_
    try:
        bstack1l11ll111_opy_(item, when)
    except Exception as e:
        pass
def bstack1l1ll11ll_opy_(item, call, rep):
    global bstack1l11l1l1l_opy_
    global bstack1lll11111_opy_
    name = bstack1ll1l11_opy_ (u"ࠧࠨℝ")
    try:
        if rep.when == bstack1ll1l11_opy_ (u"ࠨࡥࡤࡰࡱ࠭℞"):
            bstack1lllllll1l_opy_ = threading.current_thread().bstackSessionId
            bstack1111l11l11l_opy_ = item.config.getoption(bstack1ll1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ℟"))
            try:
                if (str(bstack1111l11l11l_opy_).lower() != bstack1ll1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨ℠")):
                    name = str(rep.nodeid)
                    bstack111ll1lll_opy_ = bstack111lll111_opy_(bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ℡"), name, bstack1ll1l11_opy_ (u"ࠬ࠭™"), bstack1ll1l11_opy_ (u"࠭ࠧ℣"), bstack1ll1l11_opy_ (u"ࠧࠨℤ"), bstack1ll1l11_opy_ (u"ࠨࠩ℥"))
                    os.environ[bstack1ll1l11_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬΩ")] = name
                    for driver in bstack1lll11111_opy_:
                        if bstack1lllllll1l_opy_ == driver.session_id:
                            driver.execute_script(bstack111ll1lll_opy_)
            except Exception as e:
                logger.debug(bstack1ll1l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ℧").format(str(e)))
            try:
                bstack1l1lll1l1l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1ll1l11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬℨ"):
                    status = bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ℩") if rep.outcome.lower() == bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭K") else bstack1ll1l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧÅ")
                    reason = bstack1ll1l11_opy_ (u"ࠨࠩℬ")
                    if status == bstack1ll1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩℭ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1ll1l11_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨ℮") if status == bstack1ll1l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫℯ") else bstack1ll1l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫℰ")
                    data = name + bstack1ll1l11_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨℱ") if status == bstack1ll1l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧℲ") else name + bstack1ll1l11_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫℳ") + reason
                    bstack1ll1l1l11_opy_ = bstack111lll111_opy_(bstack1ll1l11_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫℴ"), bstack1ll1l11_opy_ (u"ࠪࠫℵ"), bstack1ll1l11_opy_ (u"ࠫࠬℶ"), bstack1ll1l11_opy_ (u"ࠬ࠭ℷ"), level, data)
                    for driver in bstack1lll11111_opy_:
                        if bstack1lllllll1l_opy_ == driver.session_id:
                            driver.execute_script(bstack1ll1l1l11_opy_)
            except Exception as e:
                logger.debug(bstack1ll1l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪℸ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫℹ").format(str(e)))
    bstack1l11l1l1l_opy_(item, call, rep)
notset = Notset()
def bstack1l1l1l1l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11ll11l1_opy_
    if str(name).lower() == bstack1ll1l11_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨ℺"):
        return bstack1ll1l11_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣ℻")
    else:
        return bstack11ll11l1_opy_(self, name, default, skip)
def bstack1l1l1l1ll1_opy_(self):
    global CONFIG
    global bstack1l111l1l1l_opy_
    try:
        proxy = bstack11l11ll11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1ll1l11_opy_ (u"ࠪ࠲ࡵࡧࡣࠨℼ")):
                proxies = bstack1llll1l11l_opy_(proxy, bstack11l1ll1111_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll11ll111_opy_ = proxies.popitem()
                    if bstack1ll1l11_opy_ (u"ࠦ࠿࠵࠯ࠣℽ") in bstack1ll11ll111_opy_:
                        return bstack1ll11ll111_opy_
                    else:
                        return bstack1ll1l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨℾ") + bstack1ll11ll111_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1ll1l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥℿ").format(str(e)))
    return bstack1l111l1l1l_opy_(self)
def bstack11l1lll11l_opy_():
    return (bstack1ll1l11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⅀") in CONFIG or bstack1ll1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ⅁") in CONFIG) and bstack1l1ll11lll_opy_() and bstack1llll11ll_opy_() >= version.parse(
        bstack1l1llll11l_opy_)
def bstack1l1l1ll111_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack11l111111_opy_
    global bstack1l1l11l1l1_opy_
    global bstack1l111111ll_opy_
    CONFIG[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ⅂")] = str(bstack1l111111ll_opy_) + str(__version__)
    bstack1lll1l1l_opy_ = 0
    try:
        if bstack1l1l11l1l1_opy_ is True:
            bstack1lll1l1l_opy_ = int(os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⅃")))
    except:
        bstack1lll1l1l_opy_ = 0
    CONFIG[bstack1ll1l11_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ⅄")] = True
    bstack11ll1111ll_opy_ = bstack1ll1l1ll_opy_(CONFIG, bstack1lll1l1l_opy_)
    logger.debug(bstack1ll1ll11l1_opy_.format(str(bstack11ll1111ll_opy_)))
    if CONFIG.get(bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩⅅ")):
        bstack111l11lll_opy_(bstack11ll1111ll_opy_, bstack11l1111ll_opy_)
    if bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩⅆ") in CONFIG and bstack1ll1l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬⅇ") in CONFIG[bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫⅈ")][bstack1lll1l1l_opy_]:
        bstack11l111111_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬⅉ")][bstack1lll1l1l_opy_][bstack1ll1l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⅊")]
    import urllib
    import json
    if bstack1ll1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⅋") in CONFIG and str(CONFIG[bstack1ll1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⅌")]).lower() != bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ⅍"):
        bstack1l1111l111_opy_ = bstack1l1111lll1_opy_()
        bstack111111ll1_opy_ = bstack1l1111l111_opy_ + urllib.parse.quote(json.dumps(bstack11ll1111ll_opy_))
    else:
        bstack111111ll1_opy_ = bstack1ll1l11_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩⅎ") + urllib.parse.quote(json.dumps(bstack11ll1111ll_opy_))
    browser = self.connect(bstack111111ll1_opy_)
    return browser
def bstack111llll1_opy_():
    global bstack1l1ll1lll_opy_
    global bstack1l111111ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1l1l11_opy_
        if not bstack1llll1l1l11_opy_():
            global bstack1l111llll_opy_
            if not bstack1l111llll_opy_:
                from bstack_utils.helper import bstack11l11llll_opy_, bstack1lll11l11l_opy_
                bstack1l111llll_opy_ = bstack11l11llll_opy_()
                bstack1lll11l11l_opy_(bstack1l111111ll_opy_)
            BrowserType.connect = bstack1l1l1l11_opy_
            return
        BrowserType.launch = bstack1l1l1ll111_opy_
        bstack1l1ll1lll_opy_ = True
    except Exception as e:
        pass
def bstack11111ll1l11_opy_():
    global CONFIG
    global bstack11l1llll1l_opy_
    global bstack1l11ll1lll_opy_
    global bstack11l1111ll_opy_
    global bstack1l1l11l1l1_opy_
    global bstack111l1lll_opy_
    CONFIG = json.loads(os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧ⅏")))
    bstack11l1llll1l_opy_ = eval(os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ⅐")))
    bstack1l11ll1lll_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪ⅑"))
    bstack1l11l111l_opy_(CONFIG, bstack11l1llll1l_opy_)
    bstack111l1lll_opy_ = bstack1ll1lllll_opy_.bstack1ll11111ll_opy_(CONFIG, bstack111l1lll_opy_)
    if cli.bstack11ll111ll_opy_():
        bstack11ll11111l_opy_.invoke(bstack11lll1l1l1_opy_.CONNECT, bstack1l1ll1l1ll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⅒"), bstack1ll1l11_opy_ (u"ࠬ࠶ࠧ⅓")))
        cli.bstack1l1l11l1lll_opy_(cli_context.platform_index)
        cli.bstack1l11lll1lll_opy_(bstack11l1ll1111_opy_(bstack1l11ll1lll_opy_, CONFIG), cli_context.platform_index, bstack11l11111l_opy_)
        cli.bstack1l1l111l11l_opy_()
        logger.debug(bstack1ll1l11_opy_ (u"ࠨࡃࡍࡋࠣ࡭ࡸࠦࡡࡤࡶ࡬ࡺࡪࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧ⅔") + str(cli_context.platform_index) + bstack1ll1l11_opy_ (u"ࠢࠣ⅕"))
        return # skip all existing bstack11111llll1l_opy_
    global bstack111llll1l_opy_
    global bstack1l1lll11ll_opy_
    global bstack1111ll1ll_opy_
    global bstack1lllllll1_opy_
    global bstack1ll1l1l1ll_opy_
    global bstack1l111lll1l_opy_
    global bstack11l111lll_opy_
    global bstack1ll1l11l1_opy_
    global bstack1l111l1l1l_opy_
    global bstack11ll11l1_opy_
    global bstack1l11ll111_opy_
    global bstack1l11l1l1l_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack111llll1l_opy_ = webdriver.Remote.__init__
        bstack1l1lll11ll_opy_ = WebDriver.quit
        bstack11l111lll_opy_ = WebDriver.close
        bstack1ll1l11l1_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1ll1l11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ⅖") in CONFIG or bstack1ll1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭⅗") in CONFIG) and bstack1l1ll11lll_opy_():
        if bstack1llll11ll_opy_() < version.parse(bstack1l1llll11l_opy_):
            logger.error(bstack1l1l1l1lll_opy_.format(bstack1llll11ll_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1l111l1l1l_opy_ = RemoteConnection._11l11lllll_opy_
            except Exception as e:
                logger.error(bstack1ll111llll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11ll11l1_opy_ = Config.getoption
        from _pytest import runner
        bstack1l11ll111_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1lllll11ll_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l11l1l1l_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫ⅘"))
    bstack11l1111ll_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ⅙"), {}).get(bstack1ll1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⅚"))
    bstack1l1l11l1l1_opy_ = True
    bstack1ll1lll1l1_opy_(bstack1l1l1l111_opy_)
if (bstack11ll11l1111_opy_()):
    bstack11111ll1l11_opy_()
@bstack111l11lll1_opy_(class_method=False)
def bstack1111l1111ll_opy_(hook_name, event, bstack1ll111llll1_opy_=None):
    if hook_name not in [bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⅛"), bstack1ll1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ⅜"), bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⅝"), bstack1ll1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ⅞"), bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ⅟"), bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬⅠ"), bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫⅡ"), bstack1ll1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨⅢ")]:
        return
    node = store[bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫⅣ")]
    if hook_name in [bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧⅤ"), bstack1ll1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫⅥ")]:
        node = store[bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩⅦ")]
    elif hook_name in [bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩⅧ"), bstack1ll1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭Ⅸ")]:
        node = store[bstack1ll1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫⅩ")]
    hook_type = bstack111l1l1llll_opy_(hook_name)
    if event == bstack1ll1l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧⅪ"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_[hook_type], bstack1111111l1l_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111ll11lll_opy_ = {
            bstack1ll1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭Ⅻ"): uuid,
            bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭Ⅼ"): bstack1lllllll11_opy_(),
            bstack1ll1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨⅭ"): bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩⅮ"),
            bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨⅯ"): hook_type,
            bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩⅰ"): hook_name
        }
        store[bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫⅱ")].append(uuid)
        bstack1111l11l1ll_opy_ = node.nodeid
        if hook_type == bstack1ll1l11_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ⅲ"):
            if not _111lll1ll1_opy_.get(bstack1111l11l1ll_opy_, None):
                _111lll1ll1_opy_[bstack1111l11l1ll_opy_] = {bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨⅳ"): []}
            _111lll1ll1_opy_[bstack1111l11l1ll_opy_][bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩⅴ")].append(bstack111ll11lll_opy_[bstack1ll1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩⅵ")])
        _111lll1ll1_opy_[bstack1111l11l1ll_opy_ + bstack1ll1l11_opy_ (u"ࠬ࠳ࠧⅶ") + hook_name] = bstack111ll11lll_opy_
        bstack11111ll1111_opy_(node, bstack111ll11lll_opy_, bstack1ll1l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧⅷ"))
    elif event == bstack1ll1l11_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ⅸ"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack11111ll1l1_opy_[hook_type], bstack1111111l1l_opy_.POST, node, None, bstack1ll111llll1_opy_)
            return
        bstack111llll1ll_opy_ = node.nodeid + bstack1ll1l11_opy_ (u"ࠨ࠯ࠪⅹ") + hook_name
        _111lll1ll1_opy_[bstack111llll1ll_opy_][bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧⅺ")] = bstack1lllllll11_opy_()
        bstack1111l111111_opy_(_111lll1ll1_opy_[bstack111llll1ll_opy_][bstack1ll1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨⅻ")])
        bstack11111ll1111_opy_(node, _111lll1ll1_opy_[bstack111llll1ll_opy_], bstack1ll1l11_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ⅼ"), bstack11111l1llll_opy_=bstack1ll111llll1_opy_)
def bstack1111l11ll11_opy_():
    global bstack1111l111ll1_opy_
    if bstack1l1l1ll1l_opy_():
        bstack1111l111ll1_opy_ = bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩⅽ")
    else:
        bstack1111l111ll1_opy_ = bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ⅾ")
@bstack1ll1l11l1l_opy_.bstack1111lll1ll1_opy_
def bstack1111l11111l_opy_():
    bstack1111l11ll11_opy_()
    if cli.is_running():
        try:
            bstack11l11ll1111_opy_(bstack1111l1111ll_opy_)
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡷࠥࡶࡡࡵࡥ࡫࠾ࠥࢁࡽࠣⅿ").format(e))
        return
    if bstack1l1ll11lll_opy_():
        bstack11lll1111_opy_ = Config.bstack11111l1l1_opy_()
        bstack1ll1l11_opy_ (u"ࠨࠩࠪࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡉࡳࡷࠦࡰࡱࡲࠣࡁࠥ࠷ࠬࠡ࡯ࡲࡨࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡧࡦࡶࡶࠤࡺࡹࡥࡥࠢࡩࡳࡷࠦࡡ࠲࠳ࡼࠤࡨࡵ࡭࡮ࡣࡱࡨࡸ࠳ࡷࡳࡣࡳࡴ࡮ࡴࡧࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡴࡵࡶࠠ࠿ࠢ࠴࠰ࠥࡳ࡯ࡥࡡࡨࡼࡪࡩࡵࡵࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡥࡩࡨࡧࡵࡴࡧࠣ࡭ࡹࠦࡩࡴࠢࡳࡥࡹࡩࡨࡦࡦࠣ࡭ࡳࠦࡡࠡࡦ࡬ࡪ࡫࡫ࡲࡦࡰࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࠥ࡯ࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩࡷࡶࠤࡼ࡫ࠠ࡯ࡧࡨࡨࠥࡺ࡯ࠡࡷࡶࡩ࡙ࠥࡥ࡭ࡧࡱ࡭ࡺࡳࡐࡢࡶࡦ࡬࠭ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡩࡣࡱࡨࡱ࡫ࡲࠪࠢࡩࡳࡷࠦࡰࡱࡲࠣࡂࠥ࠷ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠩࠪࠫↀ")
        if bstack11lll1111_opy_.get_property(bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭ↁ")):
            if CONFIG.get(bstack1ll1l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪↂ")) is not None and int(CONFIG[bstack1ll1l11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫↃ")]) > 1:
                bstack1l1l1ll11_opy_(bstack1ll1l11lll_opy_)
            return
        bstack1l1l1ll11_opy_(bstack1ll1l11lll_opy_)
    try:
        bstack11l11ll1111_opy_(bstack1111l1111ll_opy_)
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡵࠣࡴࡦࡺࡣࡩ࠼ࠣࡿࢂࠨↄ").format(e))
bstack1111l11111l_opy_()