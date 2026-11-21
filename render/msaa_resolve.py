import math

def to_linear(value):
    """sRGB 转线性。"""
    raise NotImplementedError("TODO: to_linear")

def coverage_weight(samples, covered):
    """覆盖权重。"""
    raise NotImplementedError("TODO: coverage_weight")

def stencil_any(samples):
    """模板任一样本。"""
    raise NotImplementedError("TODO: stencil_any")

def nearest_depth(samples):
    """最近深度。"""
    raise NotImplementedError("TODO: nearest_depth")

def centroid_uv(uv, covered):
    """centroid 采样。"""
    raise NotImplementedError("TODO: centroid_uv")

def resolve_before_tonemap(tonemapped):
    """映射顺序。"""
    raise NotImplementedError("TODO: resolve_before_tonemap")

def resolve_samples(samples):
    """样本平均。"""
    raise NotImplementedError("TODO: resolve_samples")

def alpha_weight(alpha, samples):
    """alpha 加权。"""
    raise NotImplementedError("TODO: alpha_weight")

def eye_key(base, eye):
    """双眼缓冲。"""
    raise NotImplementedError("TODO: eye_key")

def tile_divide(resolution, samples):
    """分块。"""
    raise NotImplementedError("TODO: tile_divide")

def sample_count(level):
    """样本数。"""
    raise NotImplementedError("TODO: sample_count")

def uav_read(samples):
    """UAV 读取。"""
    raise NotImplementedError("TODO: uav_read")

def post_stage(stage):
    """后处理阶段。"""
    raise NotImplementedError("TODO: post_stage")

def hdr_clamp(value, maximum):
    """HDR 限幅。"""
    raise NotImplementedError("TODO: hdr_clamp")

def msaa_id(seed, index):
    """MSAA id。"""
    raise NotImplementedError("TODO: msaa_id")
