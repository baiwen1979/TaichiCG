import taichi as ti
import math

ti.init(arch = ti.gpu)
# 画布大小
res_x = 512
res_y = 512
# 画布
pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))

PI = math.pi
TAU = 2 * PI

@ti.func
def clamp(v, v_min, v_max):
    return ti.max(ti.min(v, v_max), v_min)

@ti.kernel
def render(time:ti.f32):
    # 在画布上绘图
    for i,j in pixels:
        # 画布背景为黑色
        color = ti.Vector([0.0, 0.0, 0.0]) 

        uv = ti.Vector([float(i)/res_x, float(j)/res_y])

        p = (uv * TAU) % TAU - 250.0       
        
        p2 = p
        c = 1.0
        inten = 0.005

        max_iter = 5
        for k in range(max_iter):
            t = time * (1.0 - (3.5 / float(k+1)))
            p2 = p + ti.Vector([ti.cos(t - p2.x) + ti.sin(t + p2.y), ti.sin(t - p2.y) + ti.cos(t + p2.x)])
            c += 1.0/(ti.Vector([p.x / (ti.sin(p2.x + t) / inten), p.y / (ti.cos(p2.y + t) / inten)])).norm()
        
        c /= float(max_iter)
        # 取反
        c = 1.17 - c**1.4
        # 锐化
        c = c ** 8 
        color = ti.Vector([1.0, 1.0, 1.0]) * c
        # 蓝色调
        color += clamp(ti.Vector([0.0, 0.35, 0.5]), 0.0, 1.0) 

        pixels[i,j] = color

gui = ti.GUI("太极动画：波光粼粼", res=(res_x, res_y))

t = 0.0
while gui.running:
    t += 0.03
    render(t)
    gui.set_image(pixels)
    gui.show()