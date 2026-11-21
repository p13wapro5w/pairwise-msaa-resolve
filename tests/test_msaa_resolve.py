import pytest
import math
from render import msaa_resolve as mod

CASES = [
    ("linear", 'm.to_linear(0.5) == approx(0.2176, abs=1e-3)'),
    ("coverage", 'm.coverage_weight(4, 2) == approx(0.5)'),
    ("stencil", 'm.stencil_any([0, 1, 0, 0]) is True'),
    ("depth", 'm.nearest_depth([0.9, 0.5, 0.7]) == 0.5'),
    ("centroid", 'm.centroid_uv((0.5, 0.5), True) == (0.5, 0.5)'),
    ("before", 'm.resolve_before_tonemap(True) is False'),
    ("samples", 'm.resolve_samples([1, 3]) == approx(2.0)'),
    ("alpha", 'm.alpha_weight(0.5, 4) == approx(0.5)'),
    ("eye", 'm.eye_key("base", 1) == "base:1"'),
    ("tile", 'm.tile_divide(1920, 4) == 480'),
    ("count", 'm.sample_count(4) == 4'),
    ("uav", 'm.uav_read([1, 2, 3]) == approx(2.0)'),
    ("post", 'm.post_stage("resolve") == "resolve"'),
    ("clamp", 'm.hdr_clamp(1200, 1000) == 1000'),
    ("id", 'm.msaa_id(3, 2) == "3:2"')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx, "math": math})
