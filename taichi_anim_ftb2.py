# Shadertoy "Fractal Tiling", reference ==> https://www.shadertoy.com/view/Ml2GWy#

import taichi as ti
import taichi_helper as th

ti.init(arch=ti.cpu)

res_x = 768
res_y = 512
pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))

@ti.kernel
def render(t: ti.f32):
    for i_, j_ in pixels:
        color = ti.Vector([0.0, 0.0, 0.0])
        # 拼块大小
        tile_size = 96
        # 移动
        offset = int(t * 5)
        i = i_ + offset
        j = j_ + offset

        layers = 6
        for k in range(layers):
            # 确保在拼块内移动
            pos = ti.Vector([i % tile_size, j % tile_size])
            # 将拼块ID作为随机种子
            tile_id = ti.Vector([i // tile_size, j // tile_size])
            # uv坐标范围：[0.0, 1.0) 
            uv = pos / float(tile_size) 
            time_dependent_rand = th.frac(ti.sin(tile_id[0] * 7 + tile_id[1] * 31 + 0.0005 * t) * 128)
            # 为不透明度添加随机性
            square_opacity = th.smooth_step(0.45, 0.55, time_dependent_rand)
            # 颜色强度范围：[0.0, 1.0]，且中间亮，边缘暗
            square_intensity = time_dependent_rand * ti.sqrt(16.0 * uv[0] * uv[1] * (1.0-uv[0]) * (1.0-uv[1]))
            # 颜色随时间变化
            square_color = ti.Vector([1, time_dependent_rand * 0.8, time_dependent_rand * 0.8]) 
            layer_color = square_color * square_intensity * square_opacity
            layer_color *= 0.5 ** k

            color += layer_color
            tile_size = tile_size // 2

        color = th.clamp(color, 0.0, 1.0)

        pixels[i_, j_] = color

gui = ti.GUI("拼块分形", res=(res_x, res_y))

t = 0.0
while gui.running:
    render(t)
    gui.set_image(pixels)
    t += 0.05
    gui.show()