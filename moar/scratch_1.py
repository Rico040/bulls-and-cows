import pyray as pr
import math
import random

pr.init_window(800, 450, "Имя окна")
pr.set_target_fps(60)
font = pr.load_font("resources/unifont.fnt")
tenshi = pr.load_texture("resources/tenshi_patchcon.png")
x, y, z = 0, 0, 0
while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    #pr.clear_background(pr.color_from_hsv(y, 1, z))
    #if z == 1:
    #    z = 0
    #else:
    #    z = 1
    y += 10
    #x += 9
    #pr.draw_texture_ex(tenshi, pr.Vector2(600 + math.sin(x) * 32, 100 + math.cos(x) * 32), 0, 1, pr.WHITE)
    pr.draw_text_ex(font, "Чипсы", pr.Vector2(random.randint(200, 400), random.randint(200, 400)), 16, 0, pr.color_from_hsv(97 + y, 1, 1))
    pr.draw_rectangle(10, 10, 120, 30, pr.RED)
    pr.draw_fps(13,10)
    pr.end_drawing()
pr.close_window()
