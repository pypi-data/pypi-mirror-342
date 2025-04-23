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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l1llll111_opy_
from browserstack_sdk.bstack11l1lll1ll_opy_ import bstack11llll1l_opy_
def _11l11ll1l11_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l11lll1l1_opy_:
    def __init__(self, handler):
        self._11l11ll1111_opy_ = {}
        self._11l11l1l1ll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11llll1l_opy_.version()
        if bstack11l1llll111_opy_(pytest_version, bstack11111ll_opy_ (u"ࠦ࠽࠴࠱࠯࠳ࠥ᮰")) >= 0:
            self._11l11ll1111_opy_[bstack11111ll_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᮱")] = Module._register_setup_function_fixture
            self._11l11ll1111_opy_[bstack11111ll_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᮲")] = Module._register_setup_module_fixture
            self._11l11ll1111_opy_[bstack11111ll_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᮳")] = Class._register_setup_class_fixture
            self._11l11ll1111_opy_[bstack11111ll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᮴")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11l11ll11l1_opy_(bstack11111ll_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᮵"))
            Module._register_setup_module_fixture = self.bstack11l11ll11l1_opy_(bstack11111ll_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᮶"))
            Class._register_setup_class_fixture = self.bstack11l11ll11l1_opy_(bstack11111ll_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᮷"))
            Class._register_setup_method_fixture = self.bstack11l11ll11l1_opy_(bstack11111ll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᮸"))
        else:
            self._11l11ll1111_opy_[bstack11111ll_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᮹")] = Module._inject_setup_function_fixture
            self._11l11ll1111_opy_[bstack11111ll_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᮺ")] = Module._inject_setup_module_fixture
            self._11l11ll1111_opy_[bstack11111ll_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᮻ")] = Class._inject_setup_class_fixture
            self._11l11ll1111_opy_[bstack11111ll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᮼ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11l11ll11l1_opy_(bstack11111ll_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᮽ"))
            Module._inject_setup_module_fixture = self.bstack11l11ll11l1_opy_(bstack11111ll_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᮾ"))
            Class._inject_setup_class_fixture = self.bstack11l11ll11l1_opy_(bstack11111ll_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᮿ"))
            Class._inject_setup_method_fixture = self.bstack11l11ll11l1_opy_(bstack11111ll_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᯀ"))
    def bstack11l11ll1lll_opy_(self, bstack11l11ll11ll_opy_, hook_type):
        bstack11l11ll1l1l_opy_ = id(bstack11l11ll11ll_opy_.__class__)
        if (bstack11l11ll1l1l_opy_, hook_type) in self._11l11l1l1ll_opy_:
            return
        meth = getattr(bstack11l11ll11ll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l11l1l1ll_opy_[(bstack11l11ll1l1l_opy_, hook_type)] = meth
            setattr(bstack11l11ll11ll_opy_, hook_type, self.bstack11l11l1lll1_opy_(hook_type, bstack11l11ll1l1l_opy_))
    def bstack11l11l1llll_opy_(self, instance, bstack11l11l1ll1l_opy_):
        if bstack11l11l1ll1l_opy_ == bstack11111ll_opy_ (u"ࠢࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᯁ"):
            self.bstack11l11ll1lll_opy_(instance.obj, bstack11111ll_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤᯂ"))
            self.bstack11l11ll1lll_opy_(instance.obj, bstack11111ll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨᯃ"))
        if bstack11l11l1ll1l_opy_ == bstack11111ll_opy_ (u"ࠥࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠦᯄ"):
            self.bstack11l11ll1lll_opy_(instance.obj, bstack11111ll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠥᯅ"))
            self.bstack11l11ll1lll_opy_(instance.obj, bstack11111ll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠢᯆ"))
        if bstack11l11l1ll1l_opy_ == bstack11111ll_opy_ (u"ࠨࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᯇ"):
            self.bstack11l11ll1lll_opy_(instance.obj, bstack11111ll_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠧᯈ"))
            self.bstack11l11ll1lll_opy_(instance.obj, bstack11111ll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠤᯉ"))
        if bstack11l11l1ll1l_opy_ == bstack11111ll_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᯊ"):
            self.bstack11l11ll1lll_opy_(instance.obj, bstack11111ll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠤᯋ"))
            self.bstack11l11ll1lll_opy_(instance.obj, bstack11111ll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩࠨᯌ"))
    @staticmethod
    def bstack11l11ll111l_opy_(hook_type, func, args):
        if hook_type in [bstack11111ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫᯍ"), bstack11111ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᯎ")]:
            _11l11ll1l11_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l11l1lll1_opy_(self, hook_type, bstack11l11ll1l1l_opy_):
        def bstack11l11lll11l_opy_(arg=None):
            self.handler(hook_type, bstack11111ll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧᯏ"))
            result = None
            try:
                bstack1111l1l1l1_opy_ = self._11l11l1l1ll_opy_[(bstack11l11ll1l1l_opy_, hook_type)]
                self.bstack11l11ll111l_opy_(hook_type, bstack1111l1l1l1_opy_, (arg,))
                result = Result(result=bstack11111ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᯐ"))
            except Exception as e:
                result = Result(result=bstack11111ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᯑ"), exception=e)
                self.handler(hook_type, bstack11111ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᯒ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11111ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᯓ"), result)
        def bstack11l11lll111_opy_(this, arg=None):
            self.handler(hook_type, bstack11111ll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬᯔ"))
            result = None
            exception = None
            try:
                self.bstack11l11ll111l_opy_(hook_type, self._11l11l1l1ll_opy_[hook_type], (this, arg))
                result = Result(result=bstack11111ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᯕ"))
            except Exception as e:
                result = Result(result=bstack11111ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᯖ"), exception=e)
                self.handler(hook_type, bstack11111ll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᯗ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11111ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᯘ"), result)
        if hook_type in [bstack11111ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᯙ"), bstack11111ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᯚ")]:
            return bstack11l11lll111_opy_
        return bstack11l11lll11l_opy_
    def bstack11l11ll11l1_opy_(self, bstack11l11l1ll1l_opy_):
        def bstack11l11l1ll11_opy_(this, *args, **kwargs):
            self.bstack11l11l1llll_opy_(this, bstack11l11l1ll1l_opy_)
            self._11l11ll1111_opy_[bstack11l11l1ll1l_opy_](this, *args, **kwargs)
        return bstack11l11l1ll11_opy_