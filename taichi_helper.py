import taichi as ti

@ti.func
def clamp(v, v_min, v_max):
    return ti.max(v_min, ti.min(v_max, v))

@ti.func
def step(edge, v):
    ret = 1.0
    if (v < edge): ret = 0.0
    return ret

@ti.func
def linear_step(edge1, edge2, v):
    assert(edge1 != edge2)
    t = (v - edge1) / float(edge2 - edge1)
    t = clamp(t, 0.0, 1.0)
    return t

@ti.func
def smooth_step(edge1, edge2, v):
    t = linear_step(edge1, edge2, v)
    return (3 - 2 * t) * t ** 2

@ti.func
def blend_alpha(color1, color2, alpha):
    alpha = clamp(alpha, 0.0, 1.0)
    return alpha * color1 + (1 - alpha) * color2

@ti.func
def frac(x):
    return x - ti.floor(x)
