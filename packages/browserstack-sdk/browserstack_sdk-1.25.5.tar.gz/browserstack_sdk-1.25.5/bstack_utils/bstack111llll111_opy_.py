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
import os
from uuid import uuid4
from bstack_utils.helper import bstack1lllllll11_opy_, bstack11l1lll1l11_opy_
from bstack_utils.bstack1l1l1lll_opy_ import bstack111l1l1ll1l_opy_
class bstack111lll1l1l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111l1111l11_opy_=None, bstack111l1111111_opy_=True, bstack1l1lll1lll1_opy_=None, bstack1l11l1ll1l_opy_=None, result=None, duration=None, bstack111lll1lll_opy_=None, meta={}):
        self.bstack111lll1lll_opy_ = bstack111lll1lll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack111l1111111_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111l1111l11_opy_ = bstack111l1111l11_opy_
        self.bstack1l1lll1lll1_opy_ = bstack1l1lll1lll1_opy_
        self.bstack1l11l1ll1l_opy_ = bstack1l11l1ll1l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l1ll1ll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l111l1l1_opy_(self, meta):
        self.meta = meta
    def bstack111llll11l_opy_(self, hooks):
        self.hooks = hooks
    def bstack111l111l111_opy_(self):
        bstack1111llll1ll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1ll1l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᶨ"): bstack1111llll1ll_opy_,
            bstack1ll1l11_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᶩ"): bstack1111llll1ll_opy_,
            bstack1ll1l11_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᶪ"): bstack1111llll1ll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1ll1l11_opy_ (u"ࠢࡖࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡀࠠࠣᶫ") + key)
            setattr(self, key, val)
    def bstack1111llll1l1_opy_(self):
        return {
            bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᶬ"): self.name,
            bstack1ll1l11_opy_ (u"ࠩࡥࡳࡩࡿࠧᶭ"): {
                bstack1ll1l11_opy_ (u"ࠪࡰࡦࡴࡧࠨᶮ"): bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᶯ"),
                bstack1ll1l11_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᶰ"): self.code
            },
            bstack1ll1l11_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ᶱ"): self.scope,
            bstack1ll1l11_opy_ (u"ࠧࡵࡣࡪࡷࠬᶲ"): self.tags,
            bstack1ll1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᶳ"): self.framework,
            bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᶴ"): self.started_at
        }
    def bstack1111lllllll_opy_(self):
        return {
         bstack1ll1l11_opy_ (u"ࠪࡱࡪࡺࡡࠨᶵ"): self.meta
        }
    def bstack111l111l1l1_opy_(self):
        return {
            bstack1ll1l11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧᶶ"): {
                bstack1ll1l11_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩᶷ"): self.bstack111l1111l11_opy_
            }
        }
    def bstack1111llllll1_opy_(self, bstack111l1111lll_opy_, details):
        step = next(filter(lambda st: st[bstack1ll1l11_opy_ (u"࠭ࡩࡥࠩᶸ")] == bstack111l1111lll_opy_, self.meta[bstack1ll1l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᶹ")]), None)
        step.update(details)
    def bstack1l111ll1l_opy_(self, bstack111l1111lll_opy_):
        step = next(filter(lambda st: st[bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫᶺ")] == bstack111l1111lll_opy_, self.meta[bstack1ll1l11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᶻ")]), None)
        step.update({
            bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᶼ"): bstack1lllllll11_opy_()
        })
    def bstack111lllllll_opy_(self, bstack111l1111lll_opy_, result, duration=None):
        bstack1l1lll1lll1_opy_ = bstack1lllllll11_opy_()
        if bstack111l1111lll_opy_ is not None and self.meta.get(bstack1ll1l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᶽ")):
            step = next(filter(lambda st: st[bstack1ll1l11_opy_ (u"ࠬ࡯ࡤࠨᶾ")] == bstack111l1111lll_opy_, self.meta[bstack1ll1l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᶿ")]), None)
            step.update({
                bstack1ll1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᷀"): bstack1l1lll1lll1_opy_,
                bstack1ll1l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ᷁"): duration if duration else bstack11l1lll1l11_opy_(step[bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ᷂࠭")], bstack1l1lll1lll1_opy_),
                bstack1ll1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ᷃"): result.result,
                bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ᷄"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1111lllll11_opy_):
        if self.meta.get(bstack1ll1l11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ᷅")):
            self.meta[bstack1ll1l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ᷆")].append(bstack1111lllll11_opy_)
        else:
            self.meta[bstack1ll1l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭᷇")] = [ bstack1111lllll11_opy_ ]
    def bstack111l11111ll_opy_(self):
        return {
            bstack1ll1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᷈"): self.bstack111l1ll1ll_opy_(),
            **self.bstack1111llll1l1_opy_(),
            **self.bstack111l111l111_opy_(),
            **self.bstack1111lllllll_opy_()
        }
    def bstack111l1111ll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ᷉"): self.bstack1l1lll1lll1_opy_,
            bstack1ll1l11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶ᷊ࠫ"): self.duration,
            bstack1ll1l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ᷋"): self.result.result
        }
        if data[bstack1ll1l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ᷌")] == bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᷍"):
            data[bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ᷎࠭")] = self.result.bstack1111ll1111_opy_()
            data[bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦ᷏ࠩ")] = [{bstack1ll1l11_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩ᷐ࠬ"): self.result.bstack11l11llll11_opy_()}]
        return data
    def bstack111l111l11l_opy_(self):
        return {
            bstack1ll1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᷑"): self.bstack111l1ll1ll_opy_(),
            **self.bstack1111llll1l1_opy_(),
            **self.bstack111l111l111_opy_(),
            **self.bstack111l1111ll1_opy_(),
            **self.bstack1111lllllll_opy_()
        }
    def bstack111ll1l11l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1ll1l11_opy_ (u"ࠫࡘࡺࡡࡳࡶࡨࡨࠬ᷒") in event:
            return self.bstack111l11111ll_opy_()
        elif bstack1ll1l11_opy_ (u"ࠬࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᷓ") in event:
            return self.bstack111l111l11l_opy_()
    def bstack111l11l111_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l1lll1lll1_opy_ = time if time else bstack1lllllll11_opy_()
        self.duration = duration if duration else bstack11l1lll1l11_opy_(self.started_at, self.bstack1l1lll1lll1_opy_)
        if result:
            self.result = result
class bstack11l11l1111_opy_(bstack111lll1l1l_opy_):
    def __init__(self, hooks=[], bstack11l1111lll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l1111lll_opy_ = bstack11l1111lll_opy_
        super().__init__(*args, **kwargs, bstack1l11l1ll1l_opy_=bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࠫᷔ"))
    @classmethod
    def bstack111l1111l1l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪᷕ"): id(step),
                bstack1ll1l11_opy_ (u"ࠨࡶࡨࡼࡹ࠭ᷖ"): step.name,
                bstack1ll1l11_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪᷗ"): step.keyword,
            })
        return bstack11l11l1111_opy_(
            **kwargs,
            meta={
                bstack1ll1l11_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫᷘ"): {
                    bstack1ll1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᷙ"): feature.name,
                    bstack1ll1l11_opy_ (u"ࠬࡶࡡࡵࡪࠪᷚ"): feature.filename,
                    bstack1ll1l11_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᷛ"): feature.description
                },
                bstack1ll1l11_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩᷜ"): {
                    bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᷝ"): scenario.name
                },
                bstack1ll1l11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᷞ"): steps,
                bstack1ll1l11_opy_ (u"ࠪࡩࡽࡧ࡭ࡱ࡮ࡨࡷࠬᷟ"): bstack111l1l1ll1l_opy_(test)
            }
        )
    def bstack111l11111l1_opy_(self):
        return {
            bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᷠ"): self.hooks
        }
    def bstack1111lllll1l_opy_(self):
        if self.bstack11l1111lll_opy_:
            return {
                bstack1ll1l11_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫᷡ"): self.bstack11l1111lll_opy_
            }
        return {}
    def bstack111l111l11l_opy_(self):
        return {
            **super().bstack111l111l11l_opy_(),
            **self.bstack111l11111l1_opy_()
        }
    def bstack111l11111ll_opy_(self):
        return {
            **super().bstack111l11111ll_opy_(),
            **self.bstack1111lllll1l_opy_()
        }
    def bstack111l11l111_opy_(self):
        return bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᷢ")
class bstack11l11111l1_opy_(bstack111lll1l1l_opy_):
    def __init__(self, hook_type, *args,bstack11l1111lll_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1111llll11l_opy_ = None
        self.bstack11l1111lll_opy_ = bstack11l1111lll_opy_
        super().__init__(*args, **kwargs, bstack1l11l1ll1l_opy_=bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᷣ"))
    def bstack111l1lll11_opy_(self):
        return self.hook_type
    def bstack111l111111l_opy_(self):
        return {
            bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᷤ"): self.hook_type
        }
    def bstack111l111l11l_opy_(self):
        return {
            **super().bstack111l111l11l_opy_(),
            **self.bstack111l111111l_opy_()
        }
    def bstack111l11111ll_opy_(self):
        return {
            **super().bstack111l11111ll_opy_(),
            bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧᷥ"): self.bstack1111llll11l_opy_,
            **self.bstack111l111111l_opy_()
        }
    def bstack111l11l111_opy_(self):
        return bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬᷦ")
    def bstack11l111111l_opy_(self, bstack1111llll11l_opy_):
        self.bstack1111llll11l_opy_ = bstack1111llll11l_opy_