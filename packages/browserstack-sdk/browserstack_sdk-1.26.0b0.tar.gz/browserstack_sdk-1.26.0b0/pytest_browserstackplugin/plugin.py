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
from browserstack_sdk.__init__ import (bstack1l1111lll1_opy_, bstack111l1llll_opy_, update, bstack11ll1l111l_opy_,
                                       bstack111l1l1l_opy_, bstack1lll1lll1_opy_, bstack1l1ll1l11_opy_, bstack1l1lll11l1_opy_,
                                       bstack11l1l111l1_opy_, bstack1111llll_opy_, bstack11ll1ll1l_opy_, bstack111111l1_opy_,
                                       bstack1ll1111111_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l1ll11l11_opy_)
from browserstack_sdk.bstack11l1lll1ll_opy_ import bstack11llll1l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack11ll11llll_opy_
from bstack_utils.capture import bstack11l111ll11_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack111l11l1l_opy_, bstack1l1lll1ll_opy_, bstack1111l1lll_opy_, \
    bstack111111ll_opy_
from bstack_utils.helper import bstack1l1llll11l_opy_, bstack11ll111ll1l_opy_, bstack111l1ll11l_opy_, bstack1l1ll1l111_opy_, bstack1l1lllll11l_opy_, bstack11lllll1l_opy_, \
    bstack11l1lll1l1l_opy_, \
    bstack11l1ll1llll_opy_, bstack1l1l1llll_opy_, bstack1l111l11l_opy_, bstack11l1lll11l1_opy_, bstack1ll1ll1l_opy_, Notset, \
    bstack111llllll_opy_, bstack11l1ll11l11_opy_, bstack11l1l1l111l_opy_, Result, bstack11ll111ll11_opy_, bstack11l1lll1111_opy_, bstack111ll1ll11_opy_, \
    bstack1ll111lll1_opy_, bstack11l1l111_opy_, bstack1l1111llll_opy_, bstack11l1lll111l_opy_
from bstack_utils.bstack11l11ll1ll1_opy_ import bstack11l11lll1l1_opy_
from bstack_utils.messages import bstack11llll1l1l_opy_, bstack1lll1111_opy_, bstack11l1111l1_opy_, bstack11l1l11111_opy_, bstack1111l1l1_opy_, \
    bstack1l1l1ll11_opy_, bstack11l1llll_opy_, bstack1llll111_opy_, bstack1l1111ll_opy_, bstack1l11ll11l1_opy_, \
    bstack1ll1llll11_opy_, bstack11lll1lll1_opy_
from bstack_utils.proxy import bstack11lll1l1ll_opy_, bstack1l111111_opy_
from bstack_utils.bstack1l1llllll_opy_ import bstack111l1l1l1l1_opy_, bstack111l1l111ll_opy_, bstack111l1l11l1l_opy_, bstack111l1l11ll1_opy_, \
    bstack111l1l11lll_opy_, bstack111l1l1llll_opy_, bstack111l1l1l11l_opy_, bstack11l1l11l_opy_, bstack111l1l1lll1_opy_
from bstack_utils.bstack1l11l1111_opy_ import bstack1lll111ll1_opy_
from bstack_utils.bstack11lll111ll_opy_ import bstack1l1l1ll1l_opy_, bstack1llll1ll_opy_, bstack111ll1ll_opy_, \
    bstack1l1l11l111_opy_, bstack1lllll11l_opy_
from bstack_utils.bstack111llll11l_opy_ import bstack111llll1ll_opy_
from bstack_utils.bstack11l11l11l1_opy_ import bstack11lll1l1_opy_
import bstack_utils.accessibility as bstack1l1111l1_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack1l1l1l1111_opy_
from bstack_utils.bstack1l11l1l11l_opy_ import bstack1l11l1l11l_opy_
from browserstack_sdk.__init__ import bstack1l11l111l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l1lll_opy_ import bstack1llll1l111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1l1ll1_opy_ import bstack1l1l1l1ll1_opy_, bstack11l1ll111_opy_, bstack11llll111l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l11ll1111l_opy_, bstack1llll1l11ll_opy_, bstack1llllll1l11_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1l1l1l1ll1_opy_ import bstack1l1l1l1ll1_opy_, bstack11l1ll111_opy_, bstack11llll111l_opy_
bstack1lll11lll_opy_ = None
bstack1l1ll1l1_opy_ = None
bstack1l111ll11_opy_ = None
bstack1l11l111l1_opy_ = None
bstack1l1l1lll_opy_ = None
bstack1l1l11l1l1_opy_ = None
bstack1lll1l1l_opy_ = None
bstack1l1l1l1l1_opy_ = None
bstack1ll111l1l_opy_ = None
bstack11l11l1lll_opy_ = None
bstack1l1ll1l11l_opy_ = None
bstack1ll11ll11_opy_ = None
bstack11lll11l11_opy_ = None
bstack111lll1l_opy_ = bstack11111ll_opy_ (u"ࠫࠬὅ")
CONFIG = {}
bstack1l11l11ll1_opy_ = False
bstack1l1lllll_opy_ = bstack11111ll_opy_ (u"ࠬ࠭὆")
bstack11l1l11lll_opy_ = bstack11111ll_opy_ (u"࠭ࠧ὇")
bstack111llll1_opy_ = False
bstack1l11ll1l_opy_ = []
bstack1l111lllll_opy_ = bstack111l11l1l_opy_
bstack11111ll111l_opy_ = bstack11111ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧὈ")
bstack1ll1l111l_opy_ = {}
bstack11ll11ll_opy_ = None
bstack1ll1l11l1l_opy_ = False
logger = bstack11ll11llll_opy_.get_logger(__name__, bstack1l111lllll_opy_)
store = {
    bstack11111ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬὉ"): []
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
_111l11l1ll_opy_ = {}
current_test_uuid = None
cli_context = bstack1l11ll1111l_opy_(
    test_framework_name=bstack1lll1lll1l_opy_[bstack11111ll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭Ὂ")] if bstack1ll1ll1l_opy_() else bstack1lll1lll1l_opy_[bstack11111ll_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࠪὋ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack111111lll_opy_(page, bstack1ll1l1111_opy_):
    try:
        page.evaluate(bstack11111ll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧὌ"),
                      bstack11111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩὍ") + json.dumps(
                          bstack1ll1l1111_opy_) + bstack11111ll_opy_ (u"ࠨࡽࡾࠤ὎"))
    except Exception as e:
        print(bstack11111ll_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧ὏"), e)
def bstack1lll1lllll_opy_(page, message, level):
    try:
        page.evaluate(bstack11111ll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤὐ"), bstack11111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧὑ") + json.dumps(
            message) + bstack11111ll_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭ὒ") + json.dumps(level) + bstack11111ll_opy_ (u"ࠫࢂࢃࠧὓ"))
    except Exception as e:
        print(bstack11111ll_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣὔ"), e)
def pytest_configure(config):
    global bstack1l1lllll_opy_
    global CONFIG
    bstack11l1l1ll_opy_ = Config.bstack11l1ll1ll1_opy_()
    config.args = bstack11lll1l1_opy_.bstack1111l1l11l1_opy_(config.args)
    bstack11l1l1ll_opy_.bstack1l11111l11_opy_(bstack1l1111llll_opy_(config.getoption(bstack11111ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪὕ"))))
    try:
        bstack11ll11llll_opy_.bstack11l11l1l11l_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1l1l1l1ll1_opy_.invoke(bstack11l1ll111_opy_.CONNECT, bstack11llll111l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧὖ"), bstack11111ll_opy_ (u"ࠨ࠲ࠪὗ")))
        config = json.loads(os.environ.get(bstack11111ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠣ὘"), bstack11111ll_opy_ (u"ࠥࡿࢂࠨὙ")))
        cli.bstack1lllll111ll_opy_(bstack1l111l11l_opy_(bstack1l1lllll_opy_, CONFIG), cli_context.platform_index, bstack11ll1l111l_opy_)
    if cli.bstack1lll1l11lll_opy_(bstack1llll1l111l_opy_):
        cli.bstack1lll11ll111_opy_()
        logger.debug(bstack11111ll_opy_ (u"ࠦࡈࡒࡉࠡ࡫ࡶࠤࡦࡩࡴࡪࡸࡨࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥ὚") + str(cli_context.platform_index) + bstack11111ll_opy_ (u"ࠧࠨὛ"))
        cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.BEFORE_ALL, bstack1llllll1l11_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack11111ll_opy_ (u"ࠨࡷࡩࡧࡱࠦ὜"), None)
    if cli.is_running() and when == bstack11111ll_opy_ (u"ࠢࡤࡣ࡯ࡰࠧὝ"):
        cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.LOG_REPORT, bstack1llllll1l11_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack11111ll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢ὞"):
            cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.BEFORE_EACH, bstack1llllll1l11_opy_.POST, item, call, outcome)
        elif when == bstack11111ll_opy_ (u"ࠤࡦࡥࡱࡲࠢὟ"):
            cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.LOG_REPORT, bstack1llllll1l11_opy_.POST, item, call, outcome)
        elif when == bstack11111ll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧὠ"):
            cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.AFTER_EACH, bstack1llllll1l11_opy_.POST, item, call, outcome)
        return # skip all existing bstack11111ll11ll_opy_
    bstack11111ll1l11_opy_ = item.config.getoption(bstack11111ll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ὡ"))
    plugins = item.config.getoption(bstack11111ll_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨὢ"))
    report = outcome.get_result()
    bstack1111l111l11_opy_(item, call, report)
    if bstack11111ll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦὣ") not in plugins or bstack1ll1ll1l_opy_():
        return
    summary = []
    driver = getattr(item, bstack11111ll_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣὤ"), None)
    page = getattr(item, bstack11111ll_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢὥ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack11111lll111_opy_(item, report, summary, bstack11111ll1l11_opy_)
    if (page is not None):
        bstack11111llllll_opy_(item, report, summary, bstack11111ll1l11_opy_)
def bstack11111lll111_opy_(item, report, summary, bstack11111ll1l11_opy_):
    if report.when == bstack11111ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨὦ") and report.skipped:
        bstack111l1l1lll1_opy_(report)
    if report.when in [bstack11111ll_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤὧ"), bstack11111ll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨὨ")]:
        return
    if not bstack1l1lllll11l_opy_():
        return
    try:
        if (str(bstack11111ll1l11_opy_).lower() != bstack11111ll_opy_ (u"ࠬࡺࡲࡶࡧࠪὩ") and not cli.is_running()):
            item._driver.execute_script(
                bstack11111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫὪ") + json.dumps(
                    report.nodeid) + bstack11111ll_opy_ (u"ࠧࡾࡿࠪὫ"))
        os.environ[bstack11111ll_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫὬ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11111ll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨ࠾ࠥࢁ࠰ࡾࠤὭ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11111ll_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧὮ")))
    bstack11llll111_opy_ = bstack11111ll_opy_ (u"ࠦࠧὯ")
    bstack111l1l1lll1_opy_(report)
    if not passed:
        try:
            bstack11llll111_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11111ll_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧὰ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11llll111_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11111ll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣά")))
        bstack11llll111_opy_ = bstack11111ll_opy_ (u"ࠢࠣὲ")
        if not passed:
            try:
                bstack11llll111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11111ll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣέ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11llll111_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ὴ")
                    + json.dumps(bstack11111ll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠤࠦή"))
                    + bstack11111ll_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢὶ")
                )
            else:
                item._driver.execute_script(
                    bstack11111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪί")
                    + json.dumps(str(bstack11llll111_opy_))
                    + bstack11111ll_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤὸ")
                )
        except Exception as e:
            summary.append(bstack11111ll_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡧ࡮࡯ࡱࡷࡥࡹ࡫࠺ࠡࡽ࠳ࢁࠧό").format(e))
def bstack1111l111ll1_opy_(test_name, error_message):
    try:
        bstack1111l111l1l_opy_ = []
        bstack1ll11l1111_opy_ = os.environ.get(bstack11111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨὺ"), bstack11111ll_opy_ (u"ࠩ࠳ࠫύ"))
        bstack1lllll11l1_opy_ = {bstack11111ll_opy_ (u"ࠪࡲࡦࡳࡥࠨὼ"): test_name, bstack11111ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪώ"): error_message, bstack11111ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ὾"): bstack1ll11l1111_opy_}
        bstack11111ll1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11111ll_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫ὿"))
        if os.path.exists(bstack11111ll1ll1_opy_):
            with open(bstack11111ll1ll1_opy_) as f:
                bstack1111l111l1l_opy_ = json.load(f)
        bstack1111l111l1l_opy_.append(bstack1lllll11l1_opy_)
        with open(bstack11111ll1ll1_opy_, bstack11111ll_opy_ (u"ࠧࡸࠩᾀ")) as f:
            json.dump(bstack1111l111l1l_opy_, f)
    except Exception as e:
        logger.debug(bstack11111ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡪࡸࡳࡪࡵࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡵࡿࡴࡦࡵࡷࠤࡪࡸࡲࡰࡴࡶ࠾ࠥ࠭ᾁ") + str(e))
def bstack11111llllll_opy_(item, report, summary, bstack11111ll1l11_opy_):
    if report.when in [bstack11111ll_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᾂ"), bstack11111ll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᾃ")]:
        return
    if (str(bstack11111ll1l11_opy_).lower() != bstack11111ll_opy_ (u"ࠫࡹࡸࡵࡦࠩᾄ")):
        bstack111111lll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11111ll_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᾅ")))
    bstack11llll111_opy_ = bstack11111ll_opy_ (u"ࠨࠢᾆ")
    bstack111l1l1lll1_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11llll111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11111ll_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢᾇ").format(e)
                )
        try:
            if passed:
                bstack1lllll11l_opy_(getattr(item, bstack11111ll_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧᾈ"), None), bstack11111ll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᾉ"))
            else:
                error_message = bstack11111ll_opy_ (u"ࠪࠫᾊ")
                if bstack11llll111_opy_:
                    bstack1lll1lllll_opy_(item._page, str(bstack11llll111_opy_), bstack11111ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥᾋ"))
                    bstack1lllll11l_opy_(getattr(item, bstack11111ll_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᾌ"), None), bstack11111ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᾍ"), str(bstack11llll111_opy_))
                    error_message = str(bstack11llll111_opy_)
                else:
                    bstack1lllll11l_opy_(getattr(item, bstack11111ll_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ᾎ"), None), bstack11111ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᾏ"))
                bstack1111l111ll1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11111ll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾ࠴ࢂࠨᾐ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack11111ll_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᾑ"), default=bstack11111ll_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥᾒ"), help=bstack11111ll_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦᾓ"))
    parser.addoption(bstack11111ll_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᾔ"), default=bstack11111ll_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨᾕ"), help=bstack11111ll_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢᾖ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11111ll_opy_ (u"ࠤ࠰࠱ࡩࡸࡩࡷࡧࡵࠦᾗ"), action=bstack11111ll_opy_ (u"ࠥࡷࡹࡵࡲࡦࠤᾘ"), default=bstack11111ll_opy_ (u"ࠦࡨ࡮ࡲࡰ࡯ࡨࠦᾙ"),
                         help=bstack11111ll_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶࠦᾚ"))
def bstack11l111l1l1_opy_(log):
    if not (log[bstack11111ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᾛ")] and log[bstack11111ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᾜ")].strip()):
        return
    active = bstack11l11111l1_opy_()
    log = {
        bstack11111ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᾝ"): log[bstack11111ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᾞ")],
        bstack11111ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᾟ"): bstack111l1ll11l_opy_().isoformat() + bstack11111ll_opy_ (u"ࠫ࡟࠭ᾠ"),
        bstack11111ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᾡ"): log[bstack11111ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᾢ")],
    }
    if active:
        if active[bstack11111ll_opy_ (u"ࠧࡵࡻࡳࡩࠬᾣ")] == bstack11111ll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᾤ"):
            log[bstack11111ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᾥ")] = active[bstack11111ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᾦ")]
        elif active[bstack11111ll_opy_ (u"ࠫࡹࡿࡰࡦࠩᾧ")] == bstack11111ll_opy_ (u"ࠬࡺࡥࡴࡶࠪᾨ"):
            log[bstack11111ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᾩ")] = active[bstack11111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᾪ")]
    bstack1l1l1l1111_opy_.bstack1llllll1l_opy_([log])
def bstack11l11111l1_opy_():
    if len(store[bstack11111ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᾫ")]) > 0 and store[bstack11111ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᾬ")][-1]:
        return {
            bstack11111ll_opy_ (u"ࠪࡸࡾࡶࡥࠨᾭ"): bstack11111ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᾮ"),
            bstack11111ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᾯ"): store[bstack11111ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᾰ")][-1]
        }
    if store.get(bstack11111ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᾱ"), None):
        return {
            bstack11111ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᾲ"): bstack11111ll_opy_ (u"ࠩࡷࡩࡸࡺࠧᾳ"),
            bstack11111ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᾴ"): store[bstack11111ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ᾵")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.INIT_TEST, bstack1llllll1l11_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.INIT_TEST, bstack1llllll1l11_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.TEST, bstack1llllll1l11_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._11111ll1l1l_opy_ = True
        bstack1ll1l1111l_opy_ = bstack1l1111l1_opy_.bstack11l11ll1l1_opy_(bstack11l1ll1llll_opy_(item.own_markers))
        if not cli.bstack1lll1l11lll_opy_(bstack1llll1l111l_opy_):
            item._a11y_test_case = bstack1ll1l1111l_opy_
            if bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᾶ"), None):
                driver = getattr(item, bstack11111ll_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᾷ"), None)
                item._a11y_started = bstack1l1111l1_opy_.bstack1l11l1l11_opy_(driver, bstack1ll1l1111l_opy_)
        if not bstack1l1l1l1111_opy_.on() or bstack11111ll111l_opy_ != bstack11111ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᾸ"):
            return
        global current_test_uuid #, bstack11l111l1ll_opy_
        bstack111l11l11l_opy_ = {
            bstack11111ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭Ᾱ"): uuid4().__str__(),
            bstack11111ll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭Ὰ"): bstack111l1ll11l_opy_().isoformat() + bstack11111ll_opy_ (u"ࠪ࡞ࠬΆ")
        }
        current_test_uuid = bstack111l11l11l_opy_[bstack11111ll_opy_ (u"ࠫࡺࡻࡩࡥࠩᾼ")]
        store[bstack11111ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ᾽")] = bstack111l11l11l_opy_[bstack11111ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫι")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l11l1ll_opy_[item.nodeid] = {**_111l11l1ll_opy_[item.nodeid], **bstack111l11l11l_opy_}
        bstack1111l11l11l_opy_(item, _111l11l1ll_opy_[item.nodeid], bstack11111ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ᾿"))
    except Exception as err:
        print(bstack11111ll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡥࡤࡰࡱࡀࠠࡼࡿࠪ῀"), str(err))
def pytest_runtest_setup(item):
    store[bstack11111ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭῁")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.BEFORE_EACH, bstack1llllll1l11_opy_.PRE, item, bstack11111ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩῂ"))
        return # skip all existing bstack11111ll11ll_opy_
    global bstack11111llll11_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l1lll11l1_opy_():
        atexit.register(bstack111111l11_opy_)
        if not bstack11111llll11_opy_:
            try:
                bstack11111ll11l1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1lll111l_opy_():
                    bstack11111ll11l1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack11111ll11l1_opy_:
                    signal.signal(s, bstack11111llll1l_opy_)
                bstack11111llll11_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11111ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡩ࡬ࡷࡹ࡫ࡲࠡࡵ࡬࡫ࡳࡧ࡬ࠡࡪࡤࡲࡩࡲࡥࡳࡵ࠽ࠤࠧῃ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111l1l1l1l1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11111ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬῄ")
    try:
        if not bstack1l1l1l1111_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l11l11l_opy_ = {
            bstack11111ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ῅"): uuid,
            bstack11111ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫῆ"): bstack111l1ll11l_opy_().isoformat() + bstack11111ll_opy_ (u"ࠨ࡜ࠪῇ"),
            bstack11111ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧῈ"): bstack11111ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨΈ"),
            bstack11111ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧῊ"): bstack11111ll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪΉ"),
            bstack11111ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩῌ"): bstack11111ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭῍")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11111ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ῎")] = item
        store[bstack11111ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭῏")] = [uuid]
        if not _111l11l1ll_opy_.get(item.nodeid, None):
            _111l11l1ll_opy_[item.nodeid] = {bstack11111ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩῐ"): [], bstack11111ll_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ῑ"): []}
        _111l11l1ll_opy_[item.nodeid][bstack11111ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫῒ")].append(bstack111l11l11l_opy_[bstack11111ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫΐ")])
        _111l11l1ll_opy_[item.nodeid + bstack11111ll_opy_ (u"ࠧ࠮ࡵࡨࡸࡺࡶࠧ῔")] = bstack111l11l11l_opy_
        bstack11111ll1111_opy_(item, bstack111l11l11l_opy_, bstack11111ll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ῕"))
    except Exception as err:
        print(bstack11111ll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬῖ"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.TEST, bstack1llllll1l11_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.AFTER_EACH, bstack1llllll1l11_opy_.PRE, item, bstack11111ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬῗ"))
        return # skip all existing bstack11111ll11ll_opy_
    try:
        global bstack1ll1l111l_opy_
        bstack1ll11l1111_opy_ = 0
        if bstack111llll1_opy_ is True:
            bstack1ll11l1111_opy_ = int(os.environ.get(bstack11111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫῘ")))
        if bstack1l111l1l11_opy_.bstack11llllllll_opy_() == bstack11111ll_opy_ (u"ࠧࡺࡲࡶࡧࠥῙ"):
            if bstack1l111l1l11_opy_.bstack1ll111l1ll_opy_() == bstack11111ll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣῚ"):
                bstack1111l111111_opy_ = bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪΊ"), None)
                bstack1111111l1_opy_ = bstack1111l111111_opy_ + bstack11111ll_opy_ (u"ࠣ࠯ࡷࡩࡸࡺࡣࡢࡵࡨࠦ῜")
                driver = getattr(item, bstack11111ll_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ῝"), None)
                bstack1l1ll1l1l1_opy_ = getattr(item, bstack11111ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ῞"), None)
                bstack11111111_opy_ = getattr(item, bstack11111ll_opy_ (u"ࠫࡺࡻࡩࡥࠩ῟"), None)
                PercySDK.screenshot(driver, bstack1111111l1_opy_, bstack1l1ll1l1l1_opy_=bstack1l1ll1l1l1_opy_, bstack11111111_opy_=bstack11111111_opy_, bstack1ll111ll11_opy_=bstack1ll11l1111_opy_)
        if not cli.bstack1lll1l11lll_opy_(bstack1llll1l111l_opy_):
            if getattr(item, bstack11111ll_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺࡡࡳࡶࡨࡨࠬῠ"), False):
                bstack11llll1l_opy_.bstack1ll1ll1l1l_opy_(getattr(item, bstack11111ll_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧῡ"), None), bstack1ll1l111l_opy_, logger, item)
        if not bstack1l1l1l1111_opy_.on():
            return
        bstack111l11l11l_opy_ = {
            bstack11111ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬῢ"): uuid4().__str__(),
            bstack11111ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬΰ"): bstack111l1ll11l_opy_().isoformat() + bstack11111ll_opy_ (u"ࠩ࡝ࠫῤ"),
            bstack11111ll_opy_ (u"ࠪࡸࡾࡶࡥࠨῥ"): bstack11111ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩῦ"),
            bstack11111ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨῧ"): bstack11111ll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪῨ"),
            bstack11111ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪῩ"): bstack11111ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪῪ")
        }
        _111l11l1ll_opy_[item.nodeid + bstack11111ll_opy_ (u"ࠩ࠰ࡸࡪࡧࡲࡥࡱࡺࡲࠬΎ")] = bstack111l11l11l_opy_
        bstack11111ll1111_opy_(item, bstack111l11l11l_opy_, bstack11111ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫῬ"))
    except Exception as err:
        print(bstack11111ll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡀࠠࡼࡿࠪ῭"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack111l1l11ll1_opy_(fixturedef.argname):
        store[bstack11111ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫ΅")] = request.node
    elif bstack111l1l11lll_opy_(fixturedef.argname):
        store[bstack11111ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫ`")] = request.node
    if not bstack1l1l1l1111_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.SETUP_FIXTURE, bstack1llllll1l11_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.SETUP_FIXTURE, bstack1llllll1l11_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack11111ll11ll_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.SETUP_FIXTURE, bstack1llllll1l11_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.SETUP_FIXTURE, bstack1llllll1l11_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack11111ll11ll_opy_
    try:
        fixture = {
            bstack11111ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ῰"): fixturedef.argname,
            bstack11111ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ῱"): bstack11l1lll1l1l_opy_(outcome),
            bstack11111ll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫῲ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11111ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧῳ")]
        if not _111l11l1ll_opy_.get(current_test_item.nodeid, None):
            _111l11l1ll_opy_[current_test_item.nodeid] = {bstack11111ll_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ῴ"): []}
        _111l11l1ll_opy_[current_test_item.nodeid][bstack11111ll_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ῵")].append(fixture)
    except Exception as err:
        logger.debug(bstack11111ll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩῶ"), str(err))
if bstack1ll1ll1l_opy_() and bstack1l1l1l1111_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.STEP, bstack1llllll1l11_opy_.PRE, request, step)
            return
        try:
            _111l11l1ll_opy_[request.node.nodeid][bstack11111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪῷ")].bstack1l11lll1_opy_(id(step))
        except Exception as err:
            print(bstack11111ll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭Ὸ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.STEP, bstack1llllll1l11_opy_.POST, request, step, exception)
            return
        try:
            _111l11l1ll_opy_[request.node.nodeid][bstack11111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬΌ")].bstack11l111ll1l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11111ll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧῺ"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.STEP, bstack1llllll1l11_opy_.POST, request, step)
            return
        try:
            bstack111llll11l_opy_: bstack111llll1ll_opy_ = _111l11l1ll_opy_[request.node.nodeid][bstack11111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧΏ")]
            bstack111llll11l_opy_.bstack11l111ll1l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11111ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩῼ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11111ll111l_opy_
        try:
            if not bstack1l1l1l1111_opy_.on() or bstack11111ll111l_opy_ != bstack11111ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪ´"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.TEST, bstack1llllll1l11_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭῾"), None)
            if not _111l11l1ll_opy_.get(request.node.nodeid, None):
                _111l11l1ll_opy_[request.node.nodeid] = {}
            bstack111llll11l_opy_ = bstack111llll1ll_opy_.bstack111l111111l_opy_(
                scenario, feature, request.node,
                name=bstack111l1l1llll_opy_(request.node, scenario),
                started_at=bstack11lllll1l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11111ll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ῿"),
                tags=bstack111l1l1l11l_opy_(feature, scenario),
                bstack11l1111111_opy_=bstack1l1l1l1111_opy_.bstack111llllll1_opy_(driver) if driver and driver.session_id else {}
            )
            _111l11l1ll_opy_[request.node.nodeid][bstack11111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ ")] = bstack111llll11l_opy_
            bstack1111l11ll1l_opy_(bstack111llll11l_opy_.uuid)
            bstack1l1l1l1111_opy_.bstack11l11l1111_opy_(bstack11111ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ "), bstack111llll11l_opy_)
        except Exception as err:
            print(bstack11111ll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ "), str(err))
def bstack1111l11l1l1_opy_(bstack11l1111lll_opy_):
    if bstack11l1111lll_opy_ in store[bstack11111ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ ")]:
        store[bstack11111ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ ")].remove(bstack11l1111lll_opy_)
def bstack1111l11ll1l_opy_(test_uuid):
    store[bstack11111ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ ")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1l1l1l1111_opy_.bstack1111ll1111l_opy_
def bstack1111l111l11_opy_(item, call, report):
    logger.debug(bstack11111ll_opy_ (u"ࠨࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡸࡺࡡࡳࡶࠪ "))
    global bstack11111ll111l_opy_
    bstack11lll11111_opy_ = bstack11lllll1l_opy_()
    if hasattr(report, bstack11111ll_opy_ (u"ࠩࡶࡸࡴࡶࠧ ")):
        bstack11lll11111_opy_ = bstack11ll111ll11_opy_(report.stop)
    elif hasattr(report, bstack11111ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࠩ ")):
        bstack11lll11111_opy_ = bstack11ll111ll11_opy_(report.start)
    try:
        if getattr(report, bstack11111ll_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ "), bstack11111ll_opy_ (u"ࠬ࠭ ")) == bstack11111ll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ​"):
            logger.debug(bstack11111ll_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡴࡦࠢ࠰ࠤࢀࢃࠬࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࠲ࠦࡻࡾࠩ‌").format(getattr(report, bstack11111ll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭‍"), bstack11111ll_opy_ (u"ࠩࠪ‎")).__str__(), bstack11111ll111l_opy_))
            if bstack11111ll111l_opy_ == bstack11111ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ‏"):
                _111l11l1ll_opy_[item.nodeid][bstack11111ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ‐")] = bstack11lll11111_opy_
                bstack1111l11l11l_opy_(item, _111l11l1ll_opy_[item.nodeid], bstack11111ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ‑"), report, call)
                store[bstack11111ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ‒")] = None
            elif bstack11111ll111l_opy_ == bstack11111ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦ–"):
                bstack111llll11l_opy_ = _111l11l1ll_opy_[item.nodeid][bstack11111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ—")]
                bstack111llll11l_opy_.set(hooks=_111l11l1ll_opy_[item.nodeid].get(bstack11111ll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ―"), []))
                exception, bstack11l1111l11_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11l1111l11_opy_ = [call.excinfo.exconly(), getattr(report, bstack11111ll_opy_ (u"ࠪࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠩ‖"), bstack11111ll_opy_ (u"ࠫࠬ‗"))]
                bstack111llll11l_opy_.stop(time=bstack11lll11111_opy_, result=Result(result=getattr(report, bstack11111ll_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭‘"), bstack11111ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭’")), exception=exception, bstack11l1111l11_opy_=bstack11l1111l11_opy_))
                bstack1l1l1l1111_opy_.bstack11l11l1111_opy_(bstack11111ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ‚"), _111l11l1ll_opy_[item.nodeid][bstack11111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ‛")])
        elif getattr(report, bstack11111ll_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ“"), bstack11111ll_opy_ (u"ࠪࠫ”")) in [bstack11111ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ„"), bstack11111ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ‟")]:
            logger.debug(bstack11111ll_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡺࡥࠡ࠯ࠣࡿࢂ࠲ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࠱ࠥࢁࡽࠨ†").format(getattr(report, bstack11111ll_opy_ (u"ࠧࡸࡪࡨࡲࠬ‡"), bstack11111ll_opy_ (u"ࠨࠩ•")).__str__(), bstack11111ll111l_opy_))
            bstack11l111l111_opy_ = item.nodeid + bstack11111ll_opy_ (u"ࠩ࠰ࠫ‣") + getattr(report, bstack11111ll_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ․"), bstack11111ll_opy_ (u"ࠫࠬ‥"))
            if getattr(report, bstack11111ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭…"), False):
                hook_type = bstack11111ll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ‧") if getattr(report, bstack11111ll_opy_ (u"ࠧࡸࡪࡨࡲࠬ "), bstack11111ll_opy_ (u"ࠨࠩ ")) == bstack11111ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ‪") else bstack11111ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ‫")
                _111l11l1ll_opy_[bstack11l111l111_opy_] = {
                    bstack11111ll_opy_ (u"ࠫࡺࡻࡩࡥࠩ‬"): uuid4().__str__(),
                    bstack11111ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ‭"): bstack11lll11111_opy_,
                    bstack11111ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ‮"): hook_type
                }
            _111l11l1ll_opy_[bstack11l111l111_opy_][bstack11111ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ ")] = bstack11lll11111_opy_
            bstack1111l11l1l1_opy_(_111l11l1ll_opy_[bstack11l111l111_opy_][bstack11111ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭‰")])
            bstack11111ll1111_opy_(item, _111l11l1ll_opy_[bstack11l111l111_opy_], bstack11111ll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ‱"), report, call)
            if getattr(report, bstack11111ll_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ′"), bstack11111ll_opy_ (u"ࠫࠬ″")) == bstack11111ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ‴"):
                if getattr(report, bstack11111ll_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ‵"), bstack11111ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ‶")) == bstack11111ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ‷"):
                    bstack111l11l11l_opy_ = {
                        bstack11111ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ‸"): uuid4().__str__(),
                        bstack11111ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ‹"): bstack11lllll1l_opy_(),
                        bstack11111ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ›"): bstack11lllll1l_opy_()
                    }
                    _111l11l1ll_opy_[item.nodeid] = {**_111l11l1ll_opy_[item.nodeid], **bstack111l11l11l_opy_}
                    bstack1111l11l11l_opy_(item, _111l11l1ll_opy_[item.nodeid], bstack11111ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭※"))
                    bstack1111l11l11l_opy_(item, _111l11l1ll_opy_[item.nodeid], bstack11111ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ‼"), report, call)
    except Exception as err:
        print(bstack11111ll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡾࢁࠬ‽"), str(err))
def bstack11111lll1ll_opy_(test, bstack111l11l11l_opy_, result=None, call=None, bstack11l11lll1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111llll11l_opy_ = {
        bstack11111ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭‾"): bstack111l11l11l_opy_[bstack11111ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ‿")],
        bstack11111ll_opy_ (u"ࠪࡸࡾࡶࡥࠨ⁀"): bstack11111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ⁁"),
        bstack11111ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⁂"): test.name,
        bstack11111ll_opy_ (u"࠭ࡢࡰࡦࡼࠫ⁃"): {
            bstack11111ll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ⁄"): bstack11111ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ⁅"),
            bstack11111ll_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ⁆"): inspect.getsource(test.obj)
        },
        bstack11111ll_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⁇"): test.name,
        bstack11111ll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪ⁈"): test.name,
        bstack11111ll_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ⁉"): bstack11lll1l1_opy_.bstack111l1l111l_opy_(test),
        bstack11111ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ⁊"): file_path,
        bstack11111ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ⁋"): file_path,
        bstack11111ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⁌"): bstack11111ll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⁍"),
        bstack11111ll_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ⁎"): file_path,
        bstack11111ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⁏"): bstack111l11l11l_opy_[bstack11111ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⁐")],
        bstack11111ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⁑"): bstack11111ll_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧ⁒"),
        bstack11111ll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫ⁓"): {
            bstack11111ll_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭⁔"): test.nodeid
        },
        bstack11111ll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ⁕"): bstack11l1ll1llll_opy_(test.own_markers)
    }
    if bstack11l11lll1_opy_ in [bstack11111ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ⁖"), bstack11111ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⁗")]:
        bstack111llll11l_opy_[bstack11111ll_opy_ (u"࠭࡭ࡦࡶࡤࠫ⁘")] = {
            bstack11111ll_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⁙"): bstack111l11l11l_opy_.get(bstack11111ll_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ⁚"), [])
        }
    if bstack11l11lll1_opy_ == bstack11111ll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ⁛"):
        bstack111llll11l_opy_[bstack11111ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⁜")] = bstack11111ll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⁝")
        bstack111llll11l_opy_[bstack11111ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⁞")] = bstack111l11l11l_opy_[bstack11111ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ ")]
        bstack111llll11l_opy_[bstack11111ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⁠")] = bstack111l11l11l_opy_[bstack11111ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⁡")]
    if result:
        bstack111llll11l_opy_[bstack11111ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⁢")] = result.outcome
        bstack111llll11l_opy_[bstack11111ll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ⁣")] = result.duration * 1000
        bstack111llll11l_opy_[bstack11111ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⁤")] = bstack111l11l11l_opy_[bstack11111ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⁥")]
        if result.failed:
            bstack111llll11l_opy_[bstack11111ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⁦")] = bstack1l1l1l1111_opy_.bstack1111ll1l11_opy_(call.excinfo.typename)
            bstack111llll11l_opy_[bstack11111ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⁧")] = bstack1l1l1l1111_opy_.bstack1111llll111_opy_(call.excinfo, result)
        bstack111llll11l_opy_[bstack11111ll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⁨")] = bstack111l11l11l_opy_[bstack11111ll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⁩")]
    if outcome:
        bstack111llll11l_opy_[bstack11111ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⁪")] = bstack11l1lll1l1l_opy_(outcome)
        bstack111llll11l_opy_[bstack11111ll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ⁫")] = 0
        bstack111llll11l_opy_[bstack11111ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⁬")] = bstack111l11l11l_opy_[bstack11111ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⁭")]
        if bstack111llll11l_opy_[bstack11111ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⁮")] == bstack11111ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⁯"):
            bstack111llll11l_opy_[bstack11111ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⁰")] = bstack11111ll_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫⁱ")  # bstack11111l1llll_opy_
            bstack111llll11l_opy_[bstack11111ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⁲")] = [{bstack11111ll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ⁳"): [bstack11111ll_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪ⁴")]}]
        bstack111llll11l_opy_[bstack11111ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⁵")] = bstack111l11l11l_opy_[bstack11111ll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⁶")]
    return bstack111llll11l_opy_
def bstack11111lllll1_opy_(test, bstack111l1l11l1_opy_, bstack11l11lll1_opy_, result, call, outcome, bstack1111l1111ll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l1l11l1_opy_[bstack11111ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⁷")]
    hook_name = bstack111l1l11l1_opy_[bstack11111ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭⁸")]
    hook_data = {
        bstack11111ll_opy_ (u"ࠫࡺࡻࡩࡥࠩ⁹"): bstack111l1l11l1_opy_[bstack11111ll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⁺")],
        bstack11111ll_opy_ (u"࠭ࡴࡺࡲࡨࠫ⁻"): bstack11111ll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⁼"),
        bstack11111ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭⁽"): bstack11111ll_opy_ (u"ࠩࡾࢁࠬ⁾").format(bstack111l1l111ll_opy_(hook_name)),
        bstack11111ll_opy_ (u"ࠪࡦࡴࡪࡹࠨⁿ"): {
            bstack11111ll_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ₀"): bstack11111ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ₁"),
            bstack11111ll_opy_ (u"࠭ࡣࡰࡦࡨࠫ₂"): None
        },
        bstack11111ll_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭₃"): test.name,
        bstack11111ll_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ₄"): bstack11lll1l1_opy_.bstack111l1l111l_opy_(test, hook_name),
        bstack11111ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ₅"): file_path,
        bstack11111ll_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬ₆"): file_path,
        bstack11111ll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ₇"): bstack11111ll_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭₈"),
        bstack11111ll_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫ₉"): file_path,
        bstack11111ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ₊"): bstack111l1l11l1_opy_[bstack11111ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ₋")],
        bstack11111ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ₌"): bstack11111ll_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬ₍") if bstack11111ll111l_opy_ == bstack11111ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ₎") else bstack11111ll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ₏"),
        bstack11111ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩₐ"): hook_type
    }
    bstack1111lllllll_opy_ = bstack111l11l1l1_opy_(_111l11l1ll_opy_.get(test.nodeid, None))
    if bstack1111lllllll_opy_:
        hook_data[bstack11111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬₑ")] = bstack1111lllllll_opy_
    if result:
        hook_data[bstack11111ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨₒ")] = result.outcome
        hook_data[bstack11111ll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪₓ")] = result.duration * 1000
        hook_data[bstack11111ll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨₔ")] = bstack111l1l11l1_opy_[bstack11111ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩₕ")]
        if result.failed:
            hook_data[bstack11111ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫₖ")] = bstack1l1l1l1111_opy_.bstack1111ll1l11_opy_(call.excinfo.typename)
            hook_data[bstack11111ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧₗ")] = bstack1l1l1l1111_opy_.bstack1111llll111_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11111ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧₘ")] = bstack11l1lll1l1l_opy_(outcome)
        hook_data[bstack11111ll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩₙ")] = 100
        hook_data[bstack11111ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧₚ")] = bstack111l1l11l1_opy_[bstack11111ll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨₛ")]
        if hook_data[bstack11111ll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫₜ")] == bstack11111ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ₝"):
            hook_data[bstack11111ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ₞")] = bstack11111ll_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨ₟")  # bstack11111l1llll_opy_
            hook_data[bstack11111ll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ₠")] = [{bstack11111ll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ₡"): [bstack11111ll_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧ₢")]}]
    if bstack1111l1111ll_opy_:
        hook_data[bstack11111ll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ₣")] = bstack1111l1111ll_opy_.result
        hook_data[bstack11111ll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭₤")] = bstack11l1ll11l11_opy_(bstack111l1l11l1_opy_[bstack11111ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ₥")], bstack111l1l11l1_opy_[bstack11111ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ₦")])
        hook_data[bstack11111ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭₧")] = bstack111l1l11l1_opy_[bstack11111ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ₨")]
        if hook_data[bstack11111ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ₩")] == bstack11111ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ₪"):
            hook_data[bstack11111ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ₫")] = bstack1l1l1l1111_opy_.bstack1111ll1l11_opy_(bstack1111l1111ll_opy_.exception_type)
            hook_data[bstack11111ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ€")] = [{bstack11111ll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ₭"): bstack11l1l1l111l_opy_(bstack1111l1111ll_opy_.exception)}]
    return hook_data
def bstack1111l11l11l_opy_(test, bstack111l11l11l_opy_, bstack11l11lll1_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack11111ll_opy_ (u"ࠨࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡧࡹࡩࡳࡺ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡸࡪࡹࡴࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠠ࠮ࠢࡾࢁࠬ₮").format(bstack11l11lll1_opy_))
    bstack111llll11l_opy_ = bstack11111lll1ll_opy_(test, bstack111l11l11l_opy_, result, call, bstack11l11lll1_opy_, outcome)
    driver = getattr(test, bstack11111ll_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ₯"), None)
    if bstack11l11lll1_opy_ == bstack11111ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ₰") and driver:
        bstack111llll11l_opy_[bstack11111ll_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪ₱")] = bstack1l1l1l1111_opy_.bstack111llllll1_opy_(driver)
    if bstack11l11lll1_opy_ == bstack11111ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭₲"):
        bstack11l11lll1_opy_ = bstack11111ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ₳")
    bstack111ll1llll_opy_ = {
        bstack11111ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ₴"): bstack11l11lll1_opy_,
        bstack11111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ₵"): bstack111llll11l_opy_
    }
    bstack1l1l1l1111_opy_.bstack1111l11l_opy_(bstack111ll1llll_opy_)
    if bstack11l11lll1_opy_ == bstack11111ll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ₶"):
        threading.current_thread().bstackTestMeta = {bstack11111ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ₷"): bstack11111ll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ₸")}
    elif bstack11l11lll1_opy_ == bstack11111ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ₹"):
        threading.current_thread().bstackTestMeta = {bstack11111ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭₺"): getattr(result, bstack11111ll_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨ₻"), bstack11111ll_opy_ (u"ࠨࠩ₼"))}
def bstack11111ll1111_opy_(test, bstack111l11l11l_opy_, bstack11l11lll1_opy_, result=None, call=None, outcome=None, bstack1111l1111ll_opy_=None):
    logger.debug(bstack11111ll_opy_ (u"ࠩࡶࡩࡳࡪ࡟ࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡨࡺࡪࡴࡴ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤ࡭ࡵ࡯࡬ࠢࡧࡥࡹࡧࠬࠡࡧࡹࡩࡳࡺࡔࡺࡲࡨࠤ࠲ࠦࡻࡾࠩ₽").format(bstack11l11lll1_opy_))
    hook_data = bstack11111lllll1_opy_(test, bstack111l11l11l_opy_, bstack11l11lll1_opy_, result, call, outcome, bstack1111l1111ll_opy_)
    bstack111ll1llll_opy_ = {
        bstack11111ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ₾"): bstack11l11lll1_opy_,
        bstack11111ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭₿"): hook_data
    }
    bstack1l1l1l1111_opy_.bstack1111l11l_opy_(bstack111ll1llll_opy_)
def bstack111l11l1l1_opy_(bstack111l11l11l_opy_):
    if not bstack111l11l11l_opy_:
        return None
    if bstack111l11l11l_opy_.get(bstack11111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⃀"), None):
        return getattr(bstack111l11l11l_opy_[bstack11111ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⃁")], bstack11111ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⃂"), None)
    return bstack111l11l11l_opy_.get(bstack11111ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⃃"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.LOG, bstack1llllll1l11_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_.LOG, bstack1llllll1l11_opy_.POST, request, caplog)
        return # skip all existing bstack11111ll11ll_opy_
    try:
        if not bstack1l1l1l1111_opy_.on():
            return
        places = [bstack11111ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⃄"), bstack11111ll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⃅"), bstack11111ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⃆")]
        logs = []
        for bstack11111lll11l_opy_ in places:
            records = caplog.get_records(bstack11111lll11l_opy_)
            bstack1111l11l1ll_opy_ = bstack11111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⃇") if bstack11111lll11l_opy_ == bstack11111ll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⃈") else bstack11111ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⃉")
            bstack1111l1111l1_opy_ = request.node.nodeid + (bstack11111ll_opy_ (u"ࠨࠩ⃊") if bstack11111lll11l_opy_ == bstack11111ll_opy_ (u"ࠩࡦࡥࡱࡲࠧ⃋") else bstack11111ll_opy_ (u"ࠪ࠱ࠬ⃌") + bstack11111lll11l_opy_)
            test_uuid = bstack111l11l1l1_opy_(_111l11l1ll_opy_.get(bstack1111l1111l1_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11l1lll1111_opy_(record.message):
                    continue
                logs.append({
                    bstack11111ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⃍"): bstack11ll111ll1l_opy_(record.created).isoformat() + bstack11111ll_opy_ (u"ࠬࡠࠧ⃎"),
                    bstack11111ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⃏"): record.levelname,
                    bstack11111ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⃐"): record.message,
                    bstack1111l11l1ll_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1l1l1l1111_opy_.bstack1llllll1l_opy_(logs)
    except Exception as err:
        print(bstack11111ll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡦࡳࡳࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ⃑"), str(err))
def bstack1l1lll1111_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1ll1l11l1l_opy_
    bstack1l11ll11_opy_ = bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ⃒࠭"), None) and bstack1l1llll11l_opy_(
            threading.current_thread(), bstack11111ll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮⃓ࠩ"), None)
    bstack11lll1llll_opy_ = getattr(driver, bstack11111ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ⃔"), None) != None and getattr(driver, bstack11111ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ⃕"), None) == True
    if sequence == bstack11111ll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭⃖") and driver != None:
      if not bstack1ll1l11l1l_opy_ and bstack1l1lllll11l_opy_() and bstack11111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⃗") in CONFIG and CONFIG[bstack11111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⃘")] == True and bstack1l11l1l11l_opy_.bstack1lll1ll1l_opy_(driver_command) and (bstack11lll1llll_opy_ or bstack1l11ll11_opy_) and not bstack1l1ll11l11_opy_(args):
        try:
          bstack1ll1l11l1l_opy_ = True
          logger.debug(bstack11111ll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀ⃙ࠫ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11111ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨ⃚").format(str(err)))
        bstack1ll1l11l1l_opy_ = False
    if sequence == bstack11111ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ⃛"):
        if driver_command == bstack11111ll_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ⃜"):
            bstack1l1l1l1111_opy_.bstack1l111l1ll1_opy_({
                bstack11111ll_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ⃝"): response[bstack11111ll_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭⃞")],
                bstack11111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⃟"): store[bstack11111ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⃠")]
            })
def bstack111111l11_opy_():
    global bstack1l11ll1l_opy_
    bstack11ll11llll_opy_.bstack11l11lll11_opy_()
    logging.shutdown()
    bstack1l1l1l1111_opy_.bstack111l1lll11_opy_()
    for driver in bstack1l11ll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11111llll1l_opy_(*args):
    global bstack1l11ll1l_opy_
    bstack1l1l1l1111_opy_.bstack111l1lll11_opy_()
    for driver in bstack1l11ll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11llll1l11_opy_, stage=STAGE.bstack1l11111ll1_opy_, bstack1l1l1l11_opy_=bstack11ll11ll_opy_)
def bstack1l11l1ll1l_opy_(self, *args, **kwargs):
    bstack111lll11_opy_ = bstack1lll11lll_opy_(self, *args, **kwargs)
    bstack1l1l1111_opy_ = getattr(threading.current_thread(), bstack11111ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ⃡"), None)
    if bstack1l1l1111_opy_ and bstack1l1l1111_opy_.get(bstack11111ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⃢"), bstack11111ll_opy_ (u"ࠬ࠭⃣")) == bstack11111ll_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⃤"):
        bstack1l1l1l1111_opy_.bstack1lll11l111_opy_(self)
    return bstack111lll11_opy_
@measure(event_name=EVENTS.bstack11lll1ll1l_opy_, stage=STAGE.bstack11ll1ll111_opy_, bstack1l1l1l11_opy_=bstack11ll11ll_opy_)
def bstack1ll1l1lll1_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11l1l1ll_opy_ = Config.bstack11l1ll1ll1_opy_()
    if bstack11l1l1ll_opy_.get_property(bstack11111ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧ⃥ࠫ")):
        return
    bstack11l1l1ll_opy_.bstack1ll11111l_opy_(bstack11111ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨ⃦ࠬ"), True)
    global bstack111lll1l_opy_
    global bstack1ll11lll_opy_
    bstack111lll1l_opy_ = framework_name
    logger.info(bstack11lll1lll1_opy_.format(bstack111lll1l_opy_.split(bstack11111ll_opy_ (u"ࠩ࠰ࠫ⃧"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1lllll11l_opy_():
            Service.start = bstack1l1ll1l11_opy_
            Service.stop = bstack1l1lll11l1_opy_
            webdriver.Remote.get = bstack1l11llllll_opy_
            webdriver.Remote.__init__ = bstack111l1ll1l_opy_
            if not isinstance(os.getenv(bstack11111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏ⃨ࠫ")), str):
                return
            WebDriver.close = bstack11l1l111l1_opy_
            WebDriver.quit = bstack1llll11l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1l1l1l1111_opy_.on():
            webdriver.Remote.__init__ = bstack1l11l1ll1l_opy_
        bstack1ll11lll_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack11111ll_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩ⃩")):
        bstack1ll11lll_opy_ = eval(os.environ.get(bstack11111ll_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆ⃪ࠪ")))
    if not bstack1ll11lll_opy_:
        bstack11ll1ll1l_opy_(bstack11111ll_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤ⃫ࠣ"), bstack1ll1llll11_opy_)
    if bstack1111llll1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._1ll1l111_opy_ = bstack1llll1llll_opy_
        except Exception as e:
            logger.error(bstack1l1l1ll11_opy_.format(str(e)))
    if bstack11111ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ⃬ࠧ") in str(framework_name).lower():
        if not bstack1l1lllll11l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack111l1l1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1lll1lll1_opy_
            Config.getoption = bstack1ll11lll1l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11ll1l11ll_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l11l1lll1_opy_, stage=STAGE.bstack1l11111ll1_opy_, bstack1l1l1l11_opy_=bstack11ll11ll_opy_)
def bstack1llll11l_opy_(self):
    global bstack111lll1l_opy_
    global bstack11l1l1ll11_opy_
    global bstack1l1ll1l1_opy_
    try:
        if bstack11111ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⃭") in bstack111lll1l_opy_ and self.session_id != None and bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ⃮࠭"), bstack11111ll_opy_ (u"⃯ࠪࠫ")) != bstack11111ll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⃰"):
            bstack1lll1l1lll_opy_ = bstack11111ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⃱") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11111ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⃲")
            bstack11l1l111_opy_(logger, True)
            if self != None:
                bstack1l1l11l111_opy_(self, bstack1lll1l1lll_opy_, bstack11111ll_opy_ (u"ࠧ࠭ࠢࠪ⃳").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1lll1l11lll_opy_(bstack1llll1l111l_opy_):
            item = store.get(bstack11111ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⃴"), None)
            if item is not None and bstack1l1llll11l_opy_(threading.current_thread(), bstack11111ll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⃵"), None):
                bstack11llll1l_opy_.bstack1ll1ll1l1l_opy_(self, bstack1ll1l111l_opy_, logger, item)
        threading.current_thread().testStatus = bstack11111ll_opy_ (u"ࠪࠫ⃶")
    except Exception as e:
        logger.debug(bstack11111ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ⃷") + str(e))
    bstack1l1ll1l1_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11l1l1l11_opy_, stage=STAGE.bstack1l11111ll1_opy_, bstack1l1l1l11_opy_=bstack11ll11ll_opy_)
def bstack111l1ll1l_opy_(self, command_executor,
             desired_capabilities=None, bstack1lll1111l_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11l1l1ll11_opy_
    global bstack11ll11ll_opy_
    global bstack111llll1_opy_
    global bstack111lll1l_opy_
    global bstack1lll11lll_opy_
    global bstack1l11ll1l_opy_
    global bstack1l1lllll_opy_
    global bstack11l1l11lll_opy_
    global bstack1ll1l111l_opy_
    CONFIG[bstack11111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ⃸")] = str(bstack111lll1l_opy_) + str(__version__)
    command_executor = bstack1l111l11l_opy_(bstack1l1lllll_opy_, CONFIG)
    logger.debug(bstack11l1l11111_opy_.format(command_executor))
    proxy = bstack1ll1111111_opy_(CONFIG, proxy)
    bstack1ll11l1111_opy_ = 0
    try:
        if bstack111llll1_opy_ is True:
            bstack1ll11l1111_opy_ = int(os.environ.get(bstack11111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⃹")))
    except:
        bstack1ll11l1111_opy_ = 0
    bstack11ll111l11_opy_ = bstack1l1111lll1_opy_(CONFIG, bstack1ll11l1111_opy_)
    logger.debug(bstack1llll111_opy_.format(str(bstack11ll111l11_opy_)))
    bstack1ll1l111l_opy_ = CONFIG.get(bstack11111ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⃺"))[bstack1ll11l1111_opy_]
    if bstack11111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ⃻") in CONFIG and CONFIG[bstack11111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭⃼")]:
        bstack111ll1ll_opy_(bstack11ll111l11_opy_, bstack11l1l11lll_opy_)
    if bstack1l1111l1_opy_.bstack11l11lllll_opy_(CONFIG, bstack1ll11l1111_opy_) and bstack1l1111l1_opy_.bstack1lll11111l_opy_(bstack11ll111l11_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1lll1l11lll_opy_(bstack1llll1l111l_opy_):
            bstack1l1111l1_opy_.set_capabilities(bstack11ll111l11_opy_, CONFIG)
    if desired_capabilities:
        bstack111ll1lll_opy_ = bstack111l1llll_opy_(desired_capabilities)
        bstack111ll1lll_opy_[bstack11111ll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ⃽")] = bstack111llllll_opy_(CONFIG)
        bstack11ll1llll1_opy_ = bstack1l1111lll1_opy_(bstack111ll1lll_opy_)
        if bstack11ll1llll1_opy_:
            bstack11ll111l11_opy_ = update(bstack11ll1llll1_opy_, bstack11ll111l11_opy_)
        desired_capabilities = None
    if options:
        bstack1111llll_opy_(options, bstack11ll111l11_opy_)
    if not options:
        options = bstack11ll1l111l_opy_(bstack11ll111l11_opy_)
    if proxy and bstack1l1l1llll_opy_() >= version.parse(bstack11111ll_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫ⃾")):
        options.proxy(proxy)
    if options and bstack1l1l1llll_opy_() >= version.parse(bstack11111ll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ⃿")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l1l1llll_opy_() < version.parse(bstack11111ll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ℀")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11ll111l11_opy_)
    logger.info(bstack11l1111l1_opy_)
    bstack1ll11l1lll_opy_.end(EVENTS.bstack11lll1ll1l_opy_.value, EVENTS.bstack11lll1ll1l_opy_.value + bstack11111ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ℁"),
                               EVENTS.bstack11lll1ll1l_opy_.value + bstack11111ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨℂ"), True, None)
    if bstack1l1l1llll_opy_() >= version.parse(bstack11111ll_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ℃")):
        bstack1lll11lll_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1l1llll_opy_() >= version.parse(bstack11111ll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ℄")):
        bstack1lll11lll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack1lll1111l_opy_=bstack1lll1111l_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1l1llll_opy_() >= version.parse(bstack11111ll_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫ℅")):
        bstack1lll11lll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1lll1111l_opy_=bstack1lll1111l_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1lll11lll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1lll1111l_opy_=bstack1lll1111l_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack11ll1111_opy_ = bstack11111ll_opy_ (u"ࠬ࠭℆")
        if bstack1l1l1llll_opy_() >= version.parse(bstack11111ll_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧℇ")):
            bstack11ll1111_opy_ = self.caps.get(bstack11111ll_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ℈"))
        else:
            bstack11ll1111_opy_ = self.capabilities.get(bstack11111ll_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ℉"))
        if bstack11ll1111_opy_:
            bstack1ll111lll1_opy_(bstack11ll1111_opy_)
            if bstack1l1l1llll_opy_() <= version.parse(bstack11111ll_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩℊ")):
                self.command_executor._url = bstack11111ll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦℋ") + bstack1l1lllll_opy_ + bstack11111ll_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣℌ")
            else:
                self.command_executor._url = bstack11111ll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢℍ") + bstack11ll1111_opy_ + bstack11111ll_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢℎ")
            logger.debug(bstack1lll1111_opy_.format(bstack11ll1111_opy_))
        else:
            logger.debug(bstack11llll1l1l_opy_.format(bstack11111ll_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣℏ")))
    except Exception as e:
        logger.debug(bstack11llll1l1l_opy_.format(e))
    bstack11l1l1ll11_opy_ = self.session_id
    if bstack11111ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨℐ") in bstack111lll1l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11111ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ℑ"), None)
        if item:
            bstack1111l11l111_opy_ = getattr(item, bstack11111ll_opy_ (u"ࠪࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨℒ"), False)
            if not getattr(item, bstack11111ll_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬℓ"), None) and bstack1111l11l111_opy_:
                setattr(store[bstack11111ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ℔")], bstack11111ll_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧℕ"), self)
        bstack1l1l1111_opy_ = getattr(threading.current_thread(), bstack11111ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ№"), None)
        if bstack1l1l1111_opy_ and bstack1l1l1111_opy_.get(bstack11111ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ℗"), bstack11111ll_opy_ (u"ࠩࠪ℘")) == bstack11111ll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫℙ"):
            bstack1l1l1l1111_opy_.bstack1lll11l111_opy_(self)
    bstack1l11ll1l_opy_.append(self)
    if bstack11111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧℚ") in CONFIG and bstack11111ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪℛ") in CONFIG[bstack11111ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩℜ")][bstack1ll11l1111_opy_]:
        bstack11ll11ll_opy_ = CONFIG[bstack11111ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪℝ")][bstack1ll11l1111_opy_][bstack11111ll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭℞")]
    logger.debug(bstack1l11ll11l1_opy_.format(bstack11l1l1ll11_opy_))
@measure(event_name=EVENTS.bstack1l111ll1_opy_, stage=STAGE.bstack1l11111ll1_opy_, bstack1l1l1l11_opy_=bstack11ll11ll_opy_)
def bstack1l11llllll_opy_(self, url):
    global bstack1ll111l1l_opy_
    global CONFIG
    try:
        bstack1llll1ll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1111ll_opy_.format(str(err)))
    try:
        bstack1ll111l1l_opy_(self, url)
    except Exception as e:
        try:
            bstack1l1l1111ll_opy_ = str(e)
            if any(err_msg in bstack1l1l1111ll_opy_ for err_msg in bstack1111l1lll_opy_):
                bstack1llll1ll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1111ll_opy_.format(str(err)))
        raise e
def bstack1l1ll1111_opy_(item, when):
    global bstack1ll11ll11_opy_
    try:
        bstack1ll11ll11_opy_(item, when)
    except Exception as e:
        pass
def bstack11ll1l11ll_opy_(item, call, rep):
    global bstack11lll11l11_opy_
    global bstack1l11ll1l_opy_
    name = bstack11111ll_opy_ (u"ࠩࠪ℟")
    try:
        if rep.when == bstack11111ll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ℠"):
            bstack11l1l1ll11_opy_ = threading.current_thread().bstackSessionId
            bstack11111ll1l11_opy_ = item.config.getoption(bstack11111ll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭℡"))
            try:
                if (str(bstack11111ll1l11_opy_).lower() != bstack11111ll_opy_ (u"ࠬࡺࡲࡶࡧࠪ™")):
                    name = str(rep.nodeid)
                    bstack1111ll1l1_opy_ = bstack1l1l1ll1l_opy_(bstack11111ll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ℣"), name, bstack11111ll_opy_ (u"ࠧࠨℤ"), bstack11111ll_opy_ (u"ࠨࠩ℥"), bstack11111ll_opy_ (u"ࠩࠪΩ"), bstack11111ll_opy_ (u"ࠪࠫ℧"))
                    os.environ[bstack11111ll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧℨ")] = name
                    for driver in bstack1l11ll1l_opy_:
                        if bstack11l1l1ll11_opy_ == driver.session_id:
                            driver.execute_script(bstack1111ll1l1_opy_)
            except Exception as e:
                logger.debug(bstack11111ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ℩").format(str(e)))
            try:
                bstack11l1l11l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11111ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧK"):
                    status = bstack11111ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧÅ") if rep.outcome.lower() == bstack11111ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨℬ") else bstack11111ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩℭ")
                    reason = bstack11111ll_opy_ (u"ࠪࠫ℮")
                    if status == bstack11111ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫℯ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11111ll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪℰ") if status == bstack11111ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ℱ") else bstack11111ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭Ⅎ")
                    data = name + bstack11111ll_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪℳ") if status == bstack11111ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩℴ") else name + bstack11111ll_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭ℵ") + reason
                    bstack1ll1111lll_opy_ = bstack1l1l1ll1l_opy_(bstack11111ll_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ℶ"), bstack11111ll_opy_ (u"ࠬ࠭ℷ"), bstack11111ll_opy_ (u"࠭ࠧℸ"), bstack11111ll_opy_ (u"ࠧࠨℹ"), level, data)
                    for driver in bstack1l11ll1l_opy_:
                        if bstack11l1l1ll11_opy_ == driver.session_id:
                            driver.execute_script(bstack1ll1111lll_opy_)
            except Exception as e:
                logger.debug(bstack11111ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ℺").format(str(e)))
    except Exception as e:
        logger.debug(bstack11111ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭℻").format(str(e)))
    bstack11lll11l11_opy_(item, call, rep)
notset = Notset()
def bstack1ll11lll1l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l1ll1l11l_opy_
    if str(name).lower() == bstack11111ll_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪℼ"):
        return bstack11111ll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥℽ")
    else:
        return bstack1l1ll1l11l_opy_(self, name, default, skip)
def bstack1llll1llll_opy_(self):
    global CONFIG
    global bstack1lll1l1l_opy_
    try:
        proxy = bstack11lll1l1ll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11111ll_opy_ (u"ࠬ࠴ࡰࡢࡥࠪℾ")):
                proxies = bstack1l111111_opy_(proxy, bstack1l111l11l_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l1l1l11l_opy_ = proxies.popitem()
                    if bstack11111ll_opy_ (u"ࠨ࠺࠰࠱ࠥℿ") in bstack1l1l1l11l_opy_:
                        return bstack1l1l1l11l_opy_
                    else:
                        return bstack11111ll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ⅀") + bstack1l1l1l11l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11111ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡵࡸ࡯ࡹࡻࠣࡹࡷࡲࠠ࠻ࠢࡾࢁࠧ⅁").format(str(e)))
    return bstack1lll1l1l_opy_(self)
def bstack1111llll1_opy_():
    return (bstack11111ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ⅂") in CONFIG or bstack11111ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ⅃") in CONFIG) and bstack1l1ll1l111_opy_() and bstack1l1l1llll_opy_() >= version.parse(
        bstack1l1lll1ll_opy_)
def bstack111ll11l_opy_(self,
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
    global bstack11ll11ll_opy_
    global bstack111llll1_opy_
    global bstack111lll1l_opy_
    CONFIG[bstack11111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭⅄")] = str(bstack111lll1l_opy_) + str(__version__)
    bstack1ll11l1111_opy_ = 0
    try:
        if bstack111llll1_opy_ is True:
            bstack1ll11l1111_opy_ = int(os.environ.get(bstack11111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬⅅ")))
    except:
        bstack1ll11l1111_opy_ = 0
    CONFIG[bstack11111ll_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧⅆ")] = True
    bstack11ll111l11_opy_ = bstack1l1111lll1_opy_(CONFIG, bstack1ll11l1111_opy_)
    logger.debug(bstack1llll111_opy_.format(str(bstack11ll111l11_opy_)))
    if CONFIG.get(bstack11111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫⅇ")):
        bstack111ll1ll_opy_(bstack11ll111l11_opy_, bstack11l1l11lll_opy_)
    if bstack11111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫⅈ") in CONFIG and bstack11111ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧⅉ") in CONFIG[bstack11111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⅊")][bstack1ll11l1111_opy_]:
        bstack11ll11ll_opy_ = CONFIG[bstack11111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⅋")][bstack1ll11l1111_opy_][bstack11111ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⅌")]
    import urllib
    import json
    if bstack11111ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⅍") in CONFIG and str(CONFIG[bstack11111ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫⅎ")]).lower() != bstack11111ll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ⅏"):
        bstack1ll11l1l1_opy_ = bstack1l11l111l_opy_()
        bstack11ll11111_opy_ = bstack1ll11l1l1_opy_ + urllib.parse.quote(json.dumps(bstack11ll111l11_opy_))
    else:
        bstack11ll11111_opy_ = bstack11111ll_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ⅐") + urllib.parse.quote(json.dumps(bstack11ll111l11_opy_))
    browser = self.connect(bstack11ll11111_opy_)
    return browser
def bstack111llll11_opy_():
    global bstack1ll11lll_opy_
    global bstack111lll1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11l11l11l_opy_
        if not bstack1l1lllll11l_opy_():
            global bstack11l1l1l11l_opy_
            if not bstack11l1l1l11l_opy_:
                from bstack_utils.helper import bstack1llll1lll1_opy_, bstack1lll111111_opy_
                bstack11l1l1l11l_opy_ = bstack1llll1lll1_opy_()
                bstack1lll111111_opy_(bstack111lll1l_opy_)
            BrowserType.connect = bstack11l11l11l_opy_
            return
        BrowserType.launch = bstack111ll11l_opy_
        bstack1ll11lll_opy_ = True
    except Exception as e:
        pass
def bstack1111l11111l_opy_():
    global CONFIG
    global bstack1l11l11ll1_opy_
    global bstack1l1lllll_opy_
    global bstack11l1l11lll_opy_
    global bstack111llll1_opy_
    global bstack1l111lllll_opy_
    CONFIG = json.loads(os.environ.get(bstack11111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ⅑")))
    bstack1l11l11ll1_opy_ = eval(os.environ.get(bstack11111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ⅒")))
    bstack1l1lllll_opy_ = os.environ.get(bstack11111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬ⅓"))
    bstack111111l1_opy_(CONFIG, bstack1l11l11ll1_opy_)
    bstack1l111lllll_opy_ = bstack11ll11llll_opy_.bstack1111111ll_opy_(CONFIG, bstack1l111lllll_opy_)
    if cli.bstack1l11l1l1l1_opy_():
        bstack1l1l1l1ll1_opy_.invoke(bstack11l1ll111_opy_.CONNECT, bstack11llll111l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⅔"), bstack11111ll_opy_ (u"ࠧ࠱ࠩ⅕")))
        cli.bstack1lllll11111_opy_(cli_context.platform_index)
        cli.bstack1lllll111ll_opy_(bstack1l111l11l_opy_(bstack1l1lllll_opy_, CONFIG), cli_context.platform_index, bstack11ll1l111l_opy_)
        cli.bstack1lll11ll111_opy_()
        logger.debug(bstack11111ll_opy_ (u"ࠣࡅࡏࡍࠥ࡯ࡳࠡࡣࡦࡸ࡮ࡼࡥࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢ⅖") + str(cli_context.platform_index) + bstack11111ll_opy_ (u"ࠤࠥ⅗"))
        return # skip all existing bstack11111ll11ll_opy_
    global bstack1lll11lll_opy_
    global bstack1l1ll1l1_opy_
    global bstack1l111ll11_opy_
    global bstack1l11l111l1_opy_
    global bstack1l1l1lll_opy_
    global bstack1l1l11l1l1_opy_
    global bstack1l1l1l1l1_opy_
    global bstack1ll111l1l_opy_
    global bstack1lll1l1l_opy_
    global bstack1l1ll1l11l_opy_
    global bstack1ll11ll11_opy_
    global bstack11lll11l11_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1lll11lll_opy_ = webdriver.Remote.__init__
        bstack1l1ll1l1_opy_ = WebDriver.quit
        bstack1l1l1l1l1_opy_ = WebDriver.close
        bstack1ll111l1l_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11111ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭⅘") in CONFIG or bstack11111ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ⅙") in CONFIG) and bstack1l1ll1l111_opy_():
        if bstack1l1l1llll_opy_() < version.parse(bstack1l1lll1ll_opy_):
            logger.error(bstack11l1llll_opy_.format(bstack1l1l1llll_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1lll1l1l_opy_ = RemoteConnection._1ll1l111_opy_
            except Exception as e:
                logger.error(bstack1l1l1ll11_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l1ll1l11l_opy_ = Config.getoption
        from _pytest import runner
        bstack1ll11ll11_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1111l1l1_opy_)
    try:
        from pytest_bdd import reporting
        bstack11lll11l11_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11111ll_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭⅚"))
    bstack11l1l11lll_opy_ = CONFIG.get(bstack11111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ⅛"), {}).get(bstack11111ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⅜"))
    bstack111llll1_opy_ = True
    bstack1ll1l1lll1_opy_(bstack111111ll_opy_)
if (bstack11l1lll11l1_opy_()):
    bstack1111l11111l_opy_()
@bstack111ll1ll11_opy_(class_method=False)
def bstack1111l11ll11_opy_(hook_name, event, bstack1l111ll1l1l_opy_=None):
    if hook_name not in [bstack11111ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⅝"), bstack11111ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⅞"), bstack11111ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ⅟"), bstack11111ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭Ⅰ"), bstack11111ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪⅡ"), bstack11111ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧⅢ"), bstack11111ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭Ⅳ"), bstack11111ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪⅤ")]:
        return
    node = store[bstack11111ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭Ⅵ")]
    if hook_name in [bstack11111ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩⅦ"), bstack11111ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭Ⅷ")]:
        node = store[bstack11111ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫⅨ")]
    elif hook_name in [bstack11111ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫⅩ"), bstack11111ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨⅪ")]:
        node = store[bstack11111ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭Ⅻ")]
    hook_type = bstack111l1l11l1l_opy_(hook_name)
    if event == bstack11111ll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩⅬ"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_[hook_type], bstack1llllll1l11_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l1l11l1_opy_ = {
            bstack11111ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨⅭ"): uuid,
            bstack11111ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨⅮ"): bstack11lllll1l_opy_(),
            bstack11111ll_opy_ (u"ࠬࡺࡹࡱࡧࠪⅯ"): bstack11111ll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫⅰ"),
            bstack11111ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪⅱ"): hook_type,
            bstack11111ll_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫⅲ"): hook_name
        }
        store[bstack11111ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ⅳ")].append(uuid)
        bstack11111lll1l1_opy_ = node.nodeid
        if hook_type == bstack11111ll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨⅴ"):
            if not _111l11l1ll_opy_.get(bstack11111lll1l1_opy_, None):
                _111l11l1ll_opy_[bstack11111lll1l1_opy_] = {bstack11111ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪⅵ"): []}
            _111l11l1ll_opy_[bstack11111lll1l1_opy_][bstack11111ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫⅶ")].append(bstack111l1l11l1_opy_[bstack11111ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫⅷ")])
        _111l11l1ll_opy_[bstack11111lll1l1_opy_ + bstack11111ll_opy_ (u"ࠧ࠮ࠩⅸ") + hook_name] = bstack111l1l11l1_opy_
        bstack11111ll1111_opy_(node, bstack111l1l11l1_opy_, bstack11111ll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩⅹ"))
    elif event == bstack11111ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨⅺ"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1l11ll_opy_[hook_type], bstack1llllll1l11_opy_.POST, node, None, bstack1l111ll1l1l_opy_)
            return
        bstack11l111l111_opy_ = node.nodeid + bstack11111ll_opy_ (u"ࠪ࠱ࠬⅻ") + hook_name
        _111l11l1ll_opy_[bstack11l111l111_opy_][bstack11111ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩⅼ")] = bstack11lllll1l_opy_()
        bstack1111l11l1l1_opy_(_111l11l1ll_opy_[bstack11l111l111_opy_][bstack11111ll_opy_ (u"ࠬࡻࡵࡪࡦࠪⅽ")])
        bstack11111ll1111_opy_(node, _111l11l1ll_opy_[bstack11l111l111_opy_], bstack11111ll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨⅾ"), bstack1111l1111ll_opy_=bstack1l111ll1l1l_opy_)
def bstack11111ll1lll_opy_():
    global bstack11111ll111l_opy_
    if bstack1ll1ll1l_opy_():
        bstack11111ll111l_opy_ = bstack11111ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫⅿ")
    else:
        bstack11111ll111l_opy_ = bstack11111ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨↀ")
@bstack1l1l1l1111_opy_.bstack1111ll1111l_opy_
def bstack1111l111lll_opy_():
    bstack11111ll1lll_opy_()
    if cli.is_running():
        try:
            bstack11l11lll1l1_opy_(bstack1111l11ll11_opy_)
        except Exception as e:
            logger.debug(bstack11111ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࡹࠠࡱࡣࡷࡧ࡭ࡀࠠࡼࡿࠥↁ").format(e))
        return
    if bstack1l1ll1l111_opy_():
        bstack11l1l1ll_opy_ = Config.bstack11l1ll1ll1_opy_()
        bstack11111ll_opy_ (u"ࠪࠫࠬࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡋࡵࡲࠡࡲࡳࡴࠥࡃࠠ࠲࠮ࠣࡱࡴࡪ࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡩࡨࡸࡸࠦࡵࡴࡧࡧࠤ࡫ࡵࡲࠡࡣ࠴࠵ࡾࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠮ࡹࡵࡥࡵࡶࡩ࡯ࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥࡶࡰࡱࠢࡁࠤ࠶࠲ࠠ࡮ࡱࡧࡣࡪࡾࡥࡤࡷࡷࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡳࡷࡱࠤࡧ࡫ࡣࡢࡷࡶࡩࠥ࡯ࡴࠡ࡫ࡶࠤࡵࡧࡴࡤࡪࡨࡨࠥ࡯࡮ࠡࡣࠣࡨ࡮࡬ࡦࡦࡴࡨࡲࡹࠦࡰࡳࡱࡦࡩࡸࡹࠠࡪࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫ࡹࡸࠦࡷࡦࠢࡱࡩࡪࡪࠠࡵࡱࠣࡹࡸ࡫ࠠࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࡒࡤࡸࡨ࡮ࠨࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡫ࡥࡳࡪ࡬ࡦࡴࠬࠤ࡫ࡵࡲࠡࡲࡳࡴࠥࡄࠠ࠲ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠫࠬ࠭ↂ")
        if bstack11l1l1ll_opy_.get_property(bstack11111ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨↃ")):
            if CONFIG.get(bstack11111ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬↄ")) is not None and int(CONFIG[bstack11111ll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ↅ")]) > 1:
                bstack1lll111ll1_opy_(bstack1l1lll1111_opy_)
            return
        bstack1lll111ll1_opy_(bstack1l1lll1111_opy_)
    try:
        bstack11l11lll1l1_opy_(bstack1111l11ll11_opy_)
    except Exception as e:
        logger.debug(bstack11111ll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡷࠥࡶࡡࡵࡥ࡫࠾ࠥࢁࡽࠣↆ").format(e))
bstack1111l111lll_opy_()