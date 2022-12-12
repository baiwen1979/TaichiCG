import taichi as ti
import taichi_helper as th

ti.init(ti.gpu)

res_x = 512
res_y = 512

pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))

@ti.kernel
def render(t: ti.f32):
    for i, j in pixels:
        color = grad_color(i, j)
        # c = tiled_circle(ti.Vector([i, j]), 512)
        c = fractal_tiled_circle(ti.Vector([i,j]), k=int(4 * ti.cos(t * 2)) + 1)
        r = 0.5 + ti.sin(t) * 0.5
        g = 0.5 + ti.cos(2*t) * 0.5
        b = 0.5 + ti.sin(3*t) * 0.5
        pixels[i, j] = th.blend_alpha(color, c * ti.Vector([r, g, b]), 0.25)

@ti.func
def tiled_circle(pos, size = 64, radius=None):
    pos = pos % size
    t = circle(pos, ti.Vector([size / 2, size / 2]), size / 2, 0.1)
    return t

@ti.func
def fractal_tiled_circle(pos, k=3, tiled_size=16):
    t = 0.0
    for i in range(k):
        t += tiled_circle(pos, size=tiled_size)
        t /= 2
        tiled_size *= 2
    return t
        

@ti.func
def grad_color(i:ti.i32, j:ti.i32):
    r = 0.5 * ti.sin(float(i) / res_x) + 0.5
    g = 0.5 * ti.sin(float(j) / res_y + 2) + 0.5
    b = 0.5 * ti.sin(float(i) / res_x + 4) + 0.5
    return ti.Vector([r, g, b])

@ti.func
def circle(pos, center, radius, blur):
    d = (pos - center).norm()
    t = 0.0
    if blur > 1.0: blur = 1.0
    if blur <= 0.0:
        t = 1.0 - th.step(1.0, d / radius)
    else:
        t = th.linear_step(1.0, 1.0 - blur, d / radius)
    return t


gui = ti.GUI("Canvas", res=(res_x, res_y))

i = 0
while gui.running:
    t = i * 0.1
    render(t)
    i += 1
    gui.set_image(pixels)
    gui.show()


