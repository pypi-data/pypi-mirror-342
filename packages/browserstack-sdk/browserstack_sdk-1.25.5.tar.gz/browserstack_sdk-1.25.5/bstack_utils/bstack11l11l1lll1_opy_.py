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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11ll11l111l_opy_
from browserstack_sdk.bstack1l111llll1_opy_ import bstack1ll1l1l1l1_opy_
def _11l11lll1l1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l11ll1111_opy_:
    def __init__(self, handler):
        self._11l11l1llll_opy_ = {}
        self._11l11ll1l1l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1ll1l1l1l1_opy_.version()
        if bstack11ll11l111l_opy_(pytest_version, bstack1ll1l11_opy_ (u"ࠤ࠻࠲࠶࠴࠱ࠣᮮ")) >= 0:
            self._11l11l1llll_opy_[bstack1ll1l11_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᮯ")] = Module._register_setup_function_fixture
            self._11l11l1llll_opy_[bstack1ll1l11_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᮰")] = Module._register_setup_module_fixture
            self._11l11l1llll_opy_[bstack1ll1l11_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᮱")] = Class._register_setup_class_fixture
            self._11l11l1llll_opy_[bstack1ll1l11_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᮲")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11l11ll111l_opy_(bstack1ll1l11_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ᮳"))
            Module._register_setup_module_fixture = self.bstack11l11ll111l_opy_(bstack1ll1l11_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᮴"))
            Class._register_setup_class_fixture = self.bstack11l11ll111l_opy_(bstack1ll1l11_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᮵"))
            Class._register_setup_method_fixture = self.bstack11l11ll111l_opy_(bstack1ll1l11_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᮶"))
        else:
            self._11l11l1llll_opy_[bstack1ll1l11_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᮷")] = Module._inject_setup_function_fixture
            self._11l11l1llll_opy_[bstack1ll1l11_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᮸")] = Module._inject_setup_module_fixture
            self._11l11l1llll_opy_[bstack1ll1l11_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᮹")] = Class._inject_setup_class_fixture
            self._11l11l1llll_opy_[bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᮺ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11l11ll111l_opy_(bstack1ll1l11_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᮻ"))
            Module._inject_setup_module_fixture = self.bstack11l11ll111l_opy_(bstack1ll1l11_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᮼ"))
            Class._inject_setup_class_fixture = self.bstack11l11ll111l_opy_(bstack1ll1l11_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᮽ"))
            Class._inject_setup_method_fixture = self.bstack11l11ll111l_opy_(bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᮾ"))
    def bstack11l11ll11l1_opy_(self, bstack11l11l1l1ll_opy_, hook_type):
        bstack11l11ll1lll_opy_ = id(bstack11l11l1l1ll_opy_.__class__)
        if (bstack11l11ll1lll_opy_, hook_type) in self._11l11ll1l1l_opy_:
            return
        meth = getattr(bstack11l11l1l1ll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l11ll1l1l_opy_[(bstack11l11ll1lll_opy_, hook_type)] = meth
            setattr(bstack11l11l1l1ll_opy_, hook_type, self.bstack11l11lll111_opy_(hook_type, bstack11l11ll1lll_opy_))
    def bstack11l11ll1l11_opy_(self, instance, bstack11l11ll1ll1_opy_):
        if bstack11l11ll1ll1_opy_ == bstack1ll1l11_opy_ (u"ࠧ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᮿ"):
            self.bstack11l11ll11l1_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢᯀ"))
            self.bstack11l11ll11l1_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦᯁ"))
        if bstack11l11ll1ll1_opy_ == bstack1ll1l11_opy_ (u"ࠣ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᯂ"):
            self.bstack11l11ll11l1_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠣᯃ"))
            self.bstack11l11ll11l1_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠧᯄ"))
        if bstack11l11ll1ll1_opy_ == bstack1ll1l11_opy_ (u"ࠦࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠦᯅ"):
            self.bstack11l11ll11l1_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠥᯆ"))
            self.bstack11l11ll11l1_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠢᯇ"))
        if bstack11l11ll1ll1_opy_ == bstack1ll1l11_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᯈ"):
            self.bstack11l11ll11l1_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠢᯉ"))
            self.bstack11l11ll11l1_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠦᯊ"))
    @staticmethod
    def bstack11l11lll11l_opy_(hook_type, func, args):
        if hook_type in [bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᯋ"), bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᯌ")]:
            _11l11lll1l1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l11lll111_opy_(self, hook_type, bstack11l11ll1lll_opy_):
        def bstack11l11l1ll11_opy_(arg=None):
            self.handler(hook_type, bstack1ll1l11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬᯍ"))
            result = None
            try:
                bstack1l1l1l1l11l_opy_ = self._11l11ll1l1l_opy_[(bstack11l11ll1lll_opy_, hook_type)]
                self.bstack11l11lll11l_opy_(hook_type, bstack1l1l1l1l11l_opy_, (arg,))
                result = Result(result=bstack1ll1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᯎ"))
            except Exception as e:
                result = Result(result=bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᯏ"), exception=e)
                self.handler(hook_type, bstack1ll1l11_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᯐ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll1l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᯑ"), result)
        def bstack11l11l1ll1l_opy_(this, arg=None):
            self.handler(hook_type, bstack1ll1l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᯒ"))
            result = None
            exception = None
            try:
                self.bstack11l11lll11l_opy_(hook_type, self._11l11ll1l1l_opy_[hook_type], (this, arg))
                result = Result(result=bstack1ll1l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᯓ"))
            except Exception as e:
                result = Result(result=bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᯔ"), exception=e)
                self.handler(hook_type, bstack1ll1l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᯕ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll1l11_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᯖ"), result)
        if hook_type in [bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᯗ"), bstack1ll1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᯘ")]:
            return bstack11l11l1ll1l_opy_
        return bstack11l11l1ll11_opy_
    def bstack11l11ll111l_opy_(self, bstack11l11ll1ll1_opy_):
        def bstack11l11ll11ll_opy_(this, *args, **kwargs):
            self.bstack11l11ll1l11_opy_(this, bstack11l11ll1ll1_opy_)
            self._11l11l1llll_opy_[bstack11l11ll1ll1_opy_](this, *args, **kwargs)
        return bstack11l11ll11ll_opy_