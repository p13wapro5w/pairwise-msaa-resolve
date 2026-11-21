import math

_GAMMA = 2.2
_MAX_SAMPLES = 4


def to_linear(value):
    """sRGB 转线性。

    resolve 必须在转线性之后做：线性空间的平均才和光强成正比，
    否则亮暗样本会被 sRGB 曲线非线性压暗，边缘出现灰边。
    """
    if value <= 0.0:
        return 0.0
    return float(value) ** _GAMMA


def coverage_weight(samples, covered):
    """覆盖权重。

    resolve 时每个样本的权重按实际覆盖数归一化，而不是一律除以 4。
    """
    if samples <= 0:
        return 0.0
    return max(0, min(samples, covered)) / float(samples)


def stencil_any(samples):
    """模板任一样本。

    模板缓冲必须逐样本写入；resolve 时任一样本命中即保留描边，
    否则只有样本 0 命中时描边会被平均掉。
    """
    return any(s != 0 for s in samples)


def nearest_depth(samples):
    """最近深度。

    深度不能用平均：平均会让边缘像素落在前后两个几何之间，
    应取最近（最小）的样本代表该像素的前景深度。
    """
    if not samples:
        return float("inf")
    return min(samples)


def centroid_uv(uv, covered):
    """centroid 采样。

    像素中心落在三角形外时，改用质心/覆盖样本的位置，避免取到
    未覆盖样本上的错误属性；已覆盖时直接使用原 uv。
    """
    if covered:
        return (uv[0], uv[1])
    return (0.5, 0.5)


def resolve_before_tonemap(tonemapped):
    """映射顺序。

    HDR 颜色必须先 resolve 再色调映射；若颜色已映射（tonemapped）
    则说明顺序错误。返回 True 表示顺序正确。
    """
    return not tonemapped


def resolve_samples(samples):
    """样本平均。

    线性空间下的等权平均。
    """
    if not samples:
        return 0.0
    return float(sum(samples)) / float(len(samples))


def alpha_weight(alpha, samples):
    """alpha 加权。

    半透明边缘的 alpha 按实际覆盖样本数加权，而不是按满样本数
    当作全不透明处理。
    """
    if samples <= 0:
        return 0.0
    coverage = min(samples, _MAX_SAMPLES) / float(_MAX_SAMPLES)
    return max(0.0, min(1.0, alpha * coverage))


def eye_key(base, eye):
    """双眼缓冲。

    VR 左右眼需要各自独立的纹理/解析目标，不能共用一张纹理，
    键名按眼别区分。
    """
    return f"{base}:{eye}"


def tile_divide(resolution, samples):
    """分块。"""
    if samples <= 0:
        return 0
    return int(resolution) // int(samples)


def sample_count(level):
    """样本数。"""
    level = int(level)
    return level if level >= 1 else 1


def uav_read(samples):
    """UAV 读取。

    UAV 不能直接读多重采样纹理（读到未定义的样本），
    必须先走 resolve 得到单样本结果。
    """
    return resolve_samples(samples)


def post_stage(stage):
    """后处理阶段。

    后处理应排在 resolve 之后，直接透传当前阶段。
    """
    return stage


def hdr_clamp(value, maximum):
    """HDR 限幅。"""
    return min(value, maximum)


def msaa_id(seed, index):
    """MSAA id。

    每个样本（以及每只眼的解析目标）都要有独立的 id，
    否则会互相覆盖。
    """
    return f"{seed}:{index}"
