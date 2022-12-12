import math
import taichi as ti
import taichi_helper as th

ti.init(arch=ti.gpu)

# 摄像机参数
res = (800, 600)
far = 3600
near = 400
fov = 60
shutter = 0.1
tanfov = math.tan(fov * math.pi / 180)

# 星星和网格
grid_size = 40
radius = 2
n_grids = (res[0] // grid_size, res[1] // grid_size, (far - near) // grid_size)
n_stars = int(n_grids[0] * n_grids[1] * n_grids[2])

pos = ti.Vector.field(3, ti.f32, shape=n_stars)
colors = ti.Vector.field(3, ti.f32, shape=n_stars)
speed = ti.field(ti.f32, shape=())

pixels = ti.Vector.field(3, ti.f32, shape=res)

@ti.func
def draw_star(i, color, radius):
    pass

@ti.func
def respaw_far(i):
    pass

@ti.kernel
def render(t: ti.f32):
    for i in pos:
        draw_star(pos[i], colors[i], radius)
        pos[i][2] = pos[i][2] - speed[None]
        if pos[i][2] < near:
            respaw_far(i)

def init_stars():
    pass

gui = ti.GUI('星际飞越', res)

init_stars()
speed[None] = 10
t = 0.0
while gui.running:
    t += 0.1
    render(t)
    gui.set_image(pixels)
    gui.show()