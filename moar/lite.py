import pyray as pr
import random

bulls, cows = 0, 0
result = []
length = 4
while len(result) != length:
    check_var = random.randint(0, 9)
    if check_var not in result:
        result.append(check_var)

pr.init_window(300, 450, "Быки и коровы")
pr.set_target_fps(60)
font = pr.load_font("resources/unifont.fnt")
textbox = pr.Rectangle(10, 40, 200, 30)
confirmBtn = pr.Rectangle(220, 40, 70, 30)
gueesp = ''
outputlog = []


class Button(object):
    def __init__(self, x1, y1, x2, y2):
        self.rectangle = pr.Rectangle(x1, y1, x2, y2)

    def pressed(self):
        if pr.check_collision_point_rec(pr.get_mouse_position(), self.rectangle):
            pr.draw_rectangle_lines_ex(self.rectangle, 1, pr.RED)
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                return True
        else:
            pr.draw_rectangle_lines_ex(self.rectangle, 1, pr.WHITE)

    def draw_me(self):
        pr.draw_rectangle_lines_ex(self.rectangle, 1, pr.WHITE)


test = Button(100, 100, 100, 30)

while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    pr.draw_text_ex(font, 'Быки и коровы', pr.Vector2(10, 10), 16, 0, pr.WHITE)
    pr.draw_rectangle_lines(10, 80, 280, 300, pr.WHITE)
    pr.draw_rectangle_lines_ex(textbox, 1, pr.WHITE)
    pr.draw_text_ex(font, 'Ввод', pr.Vector2(238, 46), 16, 0, pr.WHITE)
    if len(outputlog) <= 16:
        for i in range(len(outputlog)):
            pr.draw_text_ex(font, outputlog[i], pr.Vector2(15, 85 + 18 * i), 16, 0, pr.WHITE)
    else:
        outputlog.pop(0)
    key = int(pr.get_char_pressed())
    while key > 0:
        if 48 <= key <= 57 and len(gueesp) != length:
            gueesp += chr(key)
        key = int(pr.get_char_pressed())
    if pr.is_key_pressed(pr.KEY_BACKSPACE):
        gueesp = gueesp[:-1]
    pr.draw_text_ex(font, gueesp, pr.Vector2(15, 45), 16, 0, pr.WHITE)
    if pr.check_collision_point_rec(pr.get_mouse_position(), confirmBtn):
        pr.draw_rectangle_lines_ex(confirmBtn, 1, pr.RED)
        if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT) and len(gueesp) == length:
            l_gueesp = list(map(int, gueesp))

            for i in range(length):
                for e in range(length):
                    if result[i] == l_gueesp[e] and i == e:
                        bulls += 1
                    elif result[i] == l_gueesp[e] and i != e:
                        cows += 1
            outputlog += [f'{gueesp}: {bulls}б{cows}к']
            bulls, cows = 0, 0
            gueesp = ''
    else:
        pr.draw_rectangle_lines_ex(confirmBtn, 1, pr.WHITE)
    pr.end_drawing()
pr.close_window()
