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
import os
from uuid import uuid4
from bstack_utils.helper import bstack11lllll1l_opy_, bstack11l1ll11l11_opy_
from bstack_utils.bstack1l1llllll_opy_ import bstack111l1l1l1ll_opy_
class bstack111l11ll1l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111l11111ll_opy_=None, bstack111l11111l1_opy_=True, bstack1l111ll111l_opy_=None, bstack11l11lll1_opy_=None, result=None, duration=None, bstack111ll11l1l_opy_=None, meta={}):
        self.bstack111ll11l1l_opy_ = bstack111ll11l1l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack111l11111l1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111l11111ll_opy_ = bstack111l11111ll_opy_
        self.bstack1l111ll111l_opy_ = bstack1l111ll111l_opy_
        self.bstack11l11lll1_opy_ = bstack11l11lll1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111lll1l1l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l111l11l_opy_(self, meta):
        self.meta = meta
    def bstack11l111111l_opy_(self, hooks):
        self.hooks = hooks
    def bstack111l1111111_opy_(self):
        bstack111l1111l1l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11111ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᶪ"): bstack111l1111l1l_opy_,
            bstack11111ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᶫ"): bstack111l1111l1l_opy_,
            bstack11111ll_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ᶬ"): bstack111l1111l1l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11111ll_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥᶭ") + key)
            setattr(self, key, val)
    def bstack111l1111l11_opy_(self):
        return {
            bstack11111ll_opy_ (u"ࠪࡲࡦࡳࡥࠨᶮ"): self.name,
            bstack11111ll_opy_ (u"ࠫࡧࡵࡤࡺࠩᶯ"): {
                bstack11111ll_opy_ (u"ࠬࡲࡡ࡯ࡩࠪᶰ"): bstack11111ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᶱ"),
                bstack11111ll_opy_ (u"ࠧࡤࡱࡧࡩࠬᶲ"): self.code
            },
            bstack11111ll_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᶳ"): self.scope,
            bstack11111ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᶴ"): self.tags,
            bstack11111ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᶵ"): self.framework,
            bstack11111ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᶶ"): self.started_at
        }
    def bstack111l1111lll_opy_(self):
        return {
         bstack11111ll_opy_ (u"ࠬࡳࡥࡵࡣࠪᶷ"): self.meta
        }
    def bstack1111lllll1l_opy_(self):
        return {
            bstack11111ll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩᶸ"): {
                bstack11111ll_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫᶹ"): self.bstack111l11111ll_opy_
            }
        }
    def bstack1111llll1l1_opy_(self, bstack111l111l1l1_opy_, details):
        step = next(filter(lambda st: st[bstack11111ll_opy_ (u"ࠨ࡫ࡧࠫᶺ")] == bstack111l111l1l1_opy_, self.meta[bstack11111ll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᶻ")]), None)
        step.update(details)
    def bstack1l11lll1_opy_(self, bstack111l111l1l1_opy_):
        step = next(filter(lambda st: st[bstack11111ll_opy_ (u"ࠪ࡭ࡩ࠭ᶼ")] == bstack111l111l1l1_opy_, self.meta[bstack11111ll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᶽ")]), None)
        step.update({
            bstack11111ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᶾ"): bstack11lllll1l_opy_()
        })
    def bstack11l111ll1l_opy_(self, bstack111l111l1l1_opy_, result, duration=None):
        bstack1l111ll111l_opy_ = bstack11lllll1l_opy_()
        if bstack111l111l1l1_opy_ is not None and self.meta.get(bstack11111ll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᶿ")):
            step = next(filter(lambda st: st[bstack11111ll_opy_ (u"ࠧࡪࡦࠪ᷀")] == bstack111l111l1l1_opy_, self.meta[bstack11111ll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ᷁")]), None)
            step.update({
                bstack11111ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺ᷂ࠧ"): bstack1l111ll111l_opy_,
                bstack11111ll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ᷃"): duration if duration else bstack11l1ll11l11_opy_(step[bstack11111ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ᷄")], bstack1l111ll111l_opy_),
                bstack11111ll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ᷅"): result.result,
                bstack11111ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ᷆"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1111llll1ll_opy_):
        if self.meta.get(bstack11111ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭᷇")):
            self.meta[bstack11111ll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ᷈")].append(bstack1111llll1ll_opy_)
        else:
            self.meta[bstack11111ll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ᷉")] = [ bstack1111llll1ll_opy_ ]
    def bstack1111lllll11_opy_(self):
        return {
            bstack11111ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᷊"): self.bstack111lll1l1l_opy_(),
            **self.bstack111l1111l11_opy_(),
            **self.bstack111l1111111_opy_(),
            **self.bstack111l1111lll_opy_()
        }
    def bstack111l1111ll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11111ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᷋"): self.bstack1l111ll111l_opy_,
            bstack11111ll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭᷌"): self.duration,
            bstack11111ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᷍"): self.result.result
        }
        if data[bstack11111ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺ᷎ࠧ")] == bstack11111ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᷏"):
            data[bstack11111ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ᷐")] = self.result.bstack1111ll1l11_opy_()
            data[bstack11111ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ᷑")] = [{bstack11111ll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ᷒"): self.result.bstack11l1l1111l1_opy_()}]
        return data
    def bstack1111llll11l_opy_(self):
        return {
            bstack11111ll_opy_ (u"ࠬࡻࡵࡪࡦࠪᷓ"): self.bstack111lll1l1l_opy_(),
            **self.bstack111l1111l11_opy_(),
            **self.bstack111l1111111_opy_(),
            **self.bstack111l1111ll1_opy_(),
            **self.bstack111l1111lll_opy_()
        }
    def bstack111ll1l1l1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11111ll_opy_ (u"࠭ࡓࡵࡣࡵࡸࡪࡪࠧᷔ") in event:
            return self.bstack1111lllll11_opy_()
        elif bstack11111ll_opy_ (u"ࠧࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᷕ") in event:
            return self.bstack1111llll11l_opy_()
    def bstack111lll1lll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l111ll111l_opy_ = time if time else bstack11lllll1l_opy_()
        self.duration = duration if duration else bstack11l1ll11l11_opy_(self.started_at, self.bstack1l111ll111l_opy_)
        if result:
            self.result = result
class bstack111llll1ll_opy_(bstack111l11ll1l_opy_):
    def __init__(self, hooks=[], bstack11l1111111_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l1111111_opy_ = bstack11l1111111_opy_
        super().__init__(*args, **kwargs, bstack11l11lll1_opy_=bstack11111ll_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᷖ"))
    @classmethod
    def bstack111l111111l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11111ll_opy_ (u"ࠩ࡬ࡨࠬᷗ"): id(step),
                bstack11111ll_opy_ (u"ࠪࡸࡪࡾࡴࠨᷘ"): step.name,
                bstack11111ll_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬᷙ"): step.keyword,
            })
        return bstack111llll1ll_opy_(
            **kwargs,
            meta={
                bstack11111ll_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭ᷚ"): {
                    bstack11111ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᷛ"): feature.name,
                    bstack11111ll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬᷜ"): feature.filename,
                    bstack11111ll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᷝ"): feature.description
                },
                bstack11111ll_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫᷞ"): {
                    bstack11111ll_opy_ (u"ࠪࡲࡦࡳࡥࠨᷟ"): scenario.name
                },
                bstack11111ll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᷠ"): steps,
                bstack11111ll_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧᷡ"): bstack111l1l1l1ll_opy_(test)
            }
        )
    def bstack111l111l11l_opy_(self):
        return {
            bstack11111ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᷢ"): self.hooks
        }
    def bstack1111llllll1_opy_(self):
        if self.bstack11l1111111_opy_:
            return {
                bstack11111ll_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᷣ"): self.bstack11l1111111_opy_
            }
        return {}
    def bstack1111llll11l_opy_(self):
        return {
            **super().bstack1111llll11l_opy_(),
            **self.bstack111l111l11l_opy_()
        }
    def bstack1111lllll11_opy_(self):
        return {
            **super().bstack1111lllll11_opy_(),
            **self.bstack1111llllll1_opy_()
        }
    def bstack111lll1lll_opy_(self):
        return bstack11111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᷤ")
class bstack11l111llll_opy_(bstack111l11ll1l_opy_):
    def __init__(self, hook_type, *args,bstack11l1111111_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1111lllllll_opy_ = None
        self.bstack11l1111111_opy_ = bstack11l1111111_opy_
        super().__init__(*args, **kwargs, bstack11l11lll1_opy_=bstack11111ll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᷥ"))
    def bstack111lll1ll1_opy_(self):
        return self.hook_type
    def bstack111l111l111_opy_(self):
        return {
            bstack11111ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᷦ"): self.hook_type
        }
    def bstack1111llll11l_opy_(self):
        return {
            **super().bstack1111llll11l_opy_(),
            **self.bstack111l111l111_opy_()
        }
    def bstack1111lllll11_opy_(self):
        return {
            **super().bstack1111lllll11_opy_(),
            bstack11111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩᷧ"): self.bstack1111lllllll_opy_,
            **self.bstack111l111l111_opy_()
        }
    def bstack111lll1lll_opy_(self):
        return bstack11111ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧᷨ")
    def bstack111lllllll_opy_(self, bstack1111lllllll_opy_):
        self.bstack1111lllllll_opy_ = bstack1111lllllll_opy_