#       Bulls and Cows
#       featuring GUI with raylib
# Copyright © 2022 Rico040 <Ruci001@yandex.ru>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2. as published by Sam Hocevar.
# See the COPYING.TXT or http://www.wtfpl.net/ for more details.

# todo: [+]Cyrillic text draw: so i just generate my font. see resources/unifont.fnt
#       [+]DO GUI: proud to say, i'm get drawing on raylib - some kind likes GML
#       [+]Input box: (almost, but mostly usable)  (pretty simple but works
#       [+]Output box: well it doesn't support scrolling but wroks XD
#       [+]Import game logic: hard? not much
#       [+]Improve game logic: what to improve Nikita? nothing to improve i guess...
#       [+] - Restarting
#       [+]About window
#       [ ]make it beauty: ima tired for while (and forgor)
#       [+]Translate russian comments to english, and make more comments
#       [ ]Android port:
#          [ ]DL Android Studio: impossible - need to dl 8gb of junk to make port (internet speed 64kbps)
#          [ ]also rewrite anything to PySDL2 (more works lol)
#          [ ]Ensure it won't be slow
#          [ ]bugs will be
#          [ ]Touch screen input (more works yep)
#          [ ]hmm... if i did it then post it on gp :)
#       [+]Main menu!!!! (IN MY VISION ITS SHIT!)
#       [ ]Multiplayer!!!!!1 (BATTLE BETWEN PEEPS WITH 1 PC!!!)
#       [+]README.txt
#       [ ]JSON language
import math

import pyray as pr
from pyray import Font
import os
import random
import time
from sys import exit

# length of game. it should be from 1 to 10
max_input_char = 4

# set many things
global cows, bulls, step, l_result, l_gueesp, gueesp
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 450
SET_FPS = 60
pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Быки и коровы")  # Make window
pr.init_audio_device()
pr.init_physics()
pr.set_target_fps(SET_FPS)  # why i only now write it?... set target frame per seconds
font: Font = pr.load_font("resources/unifont.fnt")  # DON'T WRITE IT ON MAIN LOOP AND DON'T LOAD IT FIRST!
moonpng = pr.load_texture('resources/moon.png')
sunpng = pr.load_texture('resources/sun.png')
exitd = pr.load_texture('resources/exitd.png')
exitl = pr.load_texture('resources/exitl.png')
bigPlay = pr.load_texture('resources/play.png')
bigGear = pr.load_texture('resources/settings.png')
bigDoor = pr.load_texture('resources/exit.png')
mutetex = pr.load_texture('resources/mute.png')
mutedtex = pr.load_texture('resources/muted.png')
the_page_is = 0
the_heit_is = 190
color1 = pr.Color(0, 0, 0, 255)
color2 = pr.Color(255, 255, 255, 255)
output_set = 0
xmusicBtn = 140
music_on = False


def make_secret(length):
    # Return digits for 4digits
    # example:
    # >>> mydigits = make_secret(4)
    #   > mydigits
    #   > 6281
    result = []
    while len(result) != length:  # делаем сикрет с гарантом на уник
        junko = random.randint(0, 9)
        if junko not in result:
            result.append(junko)
            # if len(result) != 4: print("Make..:",result)

    # print("Result:", result)
    print(result)
    return result


def main():  # Main game function
    global music_file
    length = max_input_char  # How length will be (see top of code)
    l_result = make_secret(length)
    start_time = time.time()
    end_time = time.time()
    bulls, cows, step = 0, 0, 0
    win = False
    dontrepeatwin = False
    gueesp = ''
    outputLog = []
    inputCount = 0
    textbox = pr.Rectangle(10, 40, 200, 30)
    confirmBtn = pr.Rectangle(220, 40, 70, 30)
    exitBtn = pr.Rectangle(270, 10, 20, 20)
    muteBtn = pr.Rectangle(240, 10, 20, 20)
    blink = float(0)  # its hack
    fade_out = 255
    can_view = False
    global music_on
    if music_on:
        # maybe a better sound system but ok. at least this work.
        music_ext = ".wav", ".mp3", ".flac", ".ogg", ".xm", ".mod"
        music_dir = 'resources/music/'
        try:
            music_file = music_dir + (random.choice([_ for _ in os.listdir(music_dir) if _.endswith(music_ext)]))
            music_loaded = True
        except IndexError or FileNotFoundError:
            music_loaded = False
            pass
        if music_loaded:
            my_music = pr.load_music_stream(music_file)
            pr.set_music_volume(my_music, (xmusicBtn - 40) / 100)
            pr.play_music_stream(my_music)
            muted = False
        else:
            music_on = False

    if color1.r == 0:
        exitIcon = exitd
    else:
        exitIcon = exitl
    while not pr.window_should_close():  # Main game loop.
        # if not win: timer won't stop
        if not win:
            end_time = time.time()
        # F2 will procedure restart of game TODO: analysis for possible bugs
        elif win and pr.is_key_pressed(pr.KEY_F2):
            bulls, cows, step = 0, 0, 0
            del outputLog
            outputLog = []
            del l_result
            l_result = make_secret(length)
            start_time = time.time()
            win = False
        if music_on:
            pr.update_music_stream(my_music)
        pr.begin_drawing()
        pr.clear_background(color1)
        # Draw GUI
        pr.draw_text_ex(font, 'Быки и коровы', pr.Vector2(10, 10), 16, 0, color2)
        if fade_out != 0:
            pr.draw_text_ex(font, f'Для мануала жми F1\nFPS: {pr.get_fps()}\nFrametime: {pr.get_frame_time():.8f}s',
                            pr.Vector2(20, 380), 16, 0, pr.Color(color2.r, color2.g, color2.b, fade_out))
        # Timer
        timertext = f'{end_time - start_time:.1f}'
        pr.draw_text_ex(font, timertext, pr.Vector2(152 - 4 * len(timertext), 10), 16, 0, color2)
        pr.draw_rectangle_lines(10, 80, 280, 300, color2)  # Log box
        if (end_time - start_time) > 5 and fade_out != 0:
            fade_out -= 5
        # Check mouse is inside input box/button
        if pr.check_collision_point_rec(pr.get_mouse_position(), textbox):
            pr.draw_rectangle_lines_ex(textbox, 1, pr.RED)
            mouse_on_text = True
            # blinking underscore
            if inputCount < max_input_char:
                blink += 1
                if blink > SET_FPS:
                    blink = 0
                if blink > (SET_FPS / 2):
                    pr.draw_text_ex(font, '_', pr.Vector2(15 + (inputCount * 8), 45), 16, 0, color2)
            # TEH INPUT!!!1 key will get int
            key = int(pr.get_char_pressed())
            while key > 0 and not win:
                # 48-57 is 0-9. Means only digits can be typed.
                # TODO: no repeating input (done)
                #       hope classmate(s) will TODOit for me (no)
                # chr(key) not in gueesp  -  check if key not in
                if 48 <= key <= 57 and inputCount < max_input_char and chr(key) not in gueesp:
                    gueesp += chr(key)
                    inputCount += 1
                key = int(pr.get_char_pressed())
            # Backspace function
            if pr.is_key_pressed(pr.KEY_BACKSPACE):
                inputCount -= 1
                if inputCount < 0:
                    inputCount = 0
                gueesp = gueesp[:-1]
        else:
            pr.draw_rectangle_lines_ex(textbox, 1, color2)
            mouse_on_text = False

        if pr.check_collision_point_rec(pr.get_mouse_position(), confirmBtn):
            pr.draw_rectangle_lines_ex(confirmBtn, 1, pr.RED)
            mouse_on_cbtn = True
        else:
            pr.draw_rectangle_lines_ex(confirmBtn, 1, color2)
            mouse_on_cbtn = False

        pr.draw_text_ex(font, 'Ввод', pr.Vector2(238, 46), 16, 0, color2)
        pr.draw_text_ex(font, gueesp, pr.Vector2(15, 45), 16, 0, color2)

        pr.draw_texture_ex(exitIcon, pr.Vector2(271, 12), 0, 2, pr.Color(255, 255, 255, 255))
        if pr.check_collision_point_rec(pr.get_mouse_position(), exitBtn):
            pr.draw_rectangle_lines_ex(exitBtn, 1, pr.RED)
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                break
        else:
            pr.draw_rectangle_lines_ex(exitBtn, 1, color2)

        if music_on:
            if muted:
                pr.draw_texture_ex(mutedtex, pr.Vector2(242, 12), 0, 2, color2)
            else:
                pr.draw_texture_ex(mutetex, pr.Vector2(242, 12), 0, 2, color2)
            if pr.check_collision_point_rec(pr.get_mouse_position(), muteBtn):
                pr.draw_rectangle_lines_ex(muteBtn, 1, pr.RED)
                if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                    if music_on:
                        if muted:
                            pr.set_music_volume(my_music, (xmusicBtn - 40) / 100)
                            muted = False
                        else:
                            pr.set_music_volume(my_music, 0)
                            muted = True
            else:
                pr.draw_rectangle_lines_ex(muteBtn, 1, color2)

        # if not can_view:  # Don't show logs when about screen opened

        if len(outputLog) <= 16:  # it's blinking. can be fixed with 120 fps :/ nope rarely blink
            for i in range(len(outputLog)):
                pr.draw_text_ex(font, outputLog[i], pr.Vector2(15, 85 + 18 * i), 16, 0, color2)
        else:
            outputLog.pop(0)

        # while len(outputLog) > 16:  # outputLog limit. why is slow?
        #    outputLog.pop(0)
        #    countOutL = 16

        # After input done, it will count result (bulls/cows).
        if (pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT) and mouse_on_cbtn) or (
                pr.is_key_pressed(pr.KEY_ENTER) and mouse_on_text):
            l_gueesp = list(map(int, gueesp))
            if inputCount == max_input_char:  # defense from stupid
                step += 1
                for reisen in range(length):  # 2hu rabbits counts cows
                    for tewi in range(length):
                        if l_result[reisen] == l_gueesp[tewi] and tewi == reisen:
                            bulls += 1
                            # print(bulls, "Bull(s)")
                        elif l_result[reisen] == l_gueesp[tewi] and tewi != reisen:
                            cows += 1
                            # print(cows, "Cow(s)")
                # Grammar
                match output_set:
                    case 0:
                        if bulls > 1:
                            mokou = ' Быков и '
                        else:
                            mokou = ' Бык и '
                        if cows > 1:
                            kaguya = ' Коров '
                        else:
                            kaguya = ' Корова '
                    case 1:
                        mokou = 'б'
                        kaguya = 'к'

                # Output result P.S. outputLog is list, so It's fine to do this
                outputLog += [f'{gueesp}: {bulls}{mokou}{cows}{kaguya}']
                # if we hit limit. TODO: nuke it. we already has limit. see line 142. hmm now it get slowed...
                # if countOutL > 16:
                #    outputLog.pop(0)
                #    countOutL = 16
                # 'cuz it can get worst here poppoppop
                #    if bulls == length:
                #        outputLog.pop(0)
                #        outputLog.pop(0)
                #        outputLog.pop(0)
                #        outputLog += [f' Вы выйграли за {end_time - start_time:.2f} секунд']
                #        outputLog += [f' и за {step} ходов']
                #        outputLog += ['Чтобы начать занова жми F2']
                #        dontrepeatwin = True
                #        win = True
                # if player get 4 bulls (which means win)
                if bulls == length:
                    outputLog += [f' Вы выиграли за {end_time - start_time:.1f} секунд']
                    outputLog += [f' и за {step} ходов']
                    outputLog += ['Чтобы начать заново жми F2']
                    win = True
                # Reset to repeat procedure
                bulls, cows = 0, 0
                gueesp = ''
                inputCount = 0

        if pr.is_key_pressed(pr.KEY_F1):
            can_view = not can_view
        about(can_view)

        pr.end_drawing()
    if music_on:
        pr.stop_music_stream(my_music)
        pr.unload_music_stream(my_music)
    print('INFO: USER RAGE QUITED! LMAO!')
    # Teh best part of every program: QUIT


def about(can_view: bool):  # No required part of program. Can be easy to remove.
    # TODO: Make about() behave like docs too (pages like) - done
    global the_page_is, the_heit_is, abouttext
    if can_view:
        # use outputLog method of text rendering. for some reason \n create big SPACE
        about_origin = pr.Vector2(12, 82)
        pr.draw_rectangle(int(about_origin.x), int(about_origin.y), 276, the_heit_is, color1)
        pr.draw_rectangle_lines(int(about_origin.x), int(about_origin.y), 276, the_heit_is, color2)
        prevBtn = pr.Rectangle(int(about_origin.x) + 107, int(about_origin.y) + the_heit_is - 30, 30, 20)
        nextBtn = pr.Rectangle(int(about_origin.x) + 139, int(about_origin.y) + the_heit_is - 30, 30, 20)
        pr.draw_text_ex(font, '<   >', pr.Vector2(130, the_heit_is + 53), 16, 0, color2)
        pr.draw_text_ex(font, f'{the_page_is + 1}', pr.Vector2(190, the_heit_is + 53), 16, 0, color2)

        if pr.check_collision_point_rec(pr.get_mouse_position(), prevBtn):
            pr.draw_rectangle_lines(int(prevBtn.x), int(prevBtn.y), int(prevBtn.width), int(prevBtn.height),
                                    pr.RED)
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT) or pr.is_key_pressed(pr.KEY_LEFT):
                if the_page_is != 0:
                    the_page_is -= 1
        else:
            pr.draw_rectangle_lines(int(prevBtn.x), int(prevBtn.y), int(prevBtn.width), int(prevBtn.height),
                                    color2)
            if pr.is_key_pressed(pr.KEY_LEFT):
                if the_page_is != 0:
                    the_page_is -= 1

        if pr.check_collision_point_rec(pr.get_mouse_position(), nextBtn):
            pr.draw_rectangle_lines(int(nextBtn.x), int(nextBtn.y), int(nextBtn.width), int(nextBtn.height),
                                    pr.RED)
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT) or pr.is_key_pressed(pr.KEY_RIGHT):
                if the_page_is != 7:
                    the_page_is += 1
        else:
            pr.draw_rectangle_lines(int(nextBtn.x), int(nextBtn.y), int(nextBtn.width), int(nextBtn.height),
                                    color2)
            if pr.is_key_pressed(pr.KEY_RIGHT):
                if the_page_is != 7:
                    the_page_is += 1

        match the_page_is:
            case 0:
                the_heit_is = 190  # высота страницы
                pr.draw_line(17, 191, 283, 191, color2)
                abouttext = ['О программе:',
                             '',
                             'Бычки и коровки',
                             'на Python c интерфейсом',
                             'Под лицензий WTFPL без гарантии.',
                             '',
                             'Листать справку можно при помощи',
                             'клавиш стрелок или кнопок ниже.']
            case 1:
                the_heit_is = 180
                abouttext = ['Быки и коровы - логическая игра',
                             'в ходе которой за несколько',
                             'попыток один из игроков',
                             'должен определить, что задумал',
                             'другой игрок.',
                             '',
                             'Вы играете против компьютера.']
            case 2:
                the_heit_is = 190
                abouttext = ['Компьютер загадывает тайное',
                             '4-х значное число.',
                             'Числа в нём не повторяются т.е.',
                             'не будет числа как 1233.',
                             '',
                             'Ваша задача отгадать число',
                             'оппонента за меньшое количество',
                             'ходов и как можно быстрее.']
            case 3:
                the_heit_is = 210
                pr.draw_line(8, 72, 212, 72, pr.RED)
                abouttext = ['Это поле ввода (подчёркнута)',
                             'В этом поле вы вводите число',
                             'с не повторяющими числами.',
                             '(повтор не вводится)',
                             'После ввода данных, либо',
                             'нажимаете на кнопку "Ввод"',
                             'либо на клавишу Enter.',
                             'Компьютер должен вывести',
                             'информацию.']
            case 4:
                the_heit_is = 120
                pr.draw_rectangle_lines(9, 79, 282, 302, pr.RED)
                abouttext = ['Компьютер выводит информацию',
                             'на этом выделенном поле.',
                             'Вмешает 16 строк.',
                             'По сути, помогает с счётам.']
            case 5:
                the_heit_is = 190
                pr.draw_line(33, 143, 47, 143, pr.GOLD)
                pr.draw_line(47, 143, 56, 143, pr.GREEN)
                pr.draw_line(153, 179, 167, 179, pr.GOLD)
                pr.draw_line(176, 179, 184, 179, pr.GREEN)
                abouttext = ['Вывод может выгладить',
                             'следующим образом:',
                             '4795: 1 Бык и 2 Коров',
                             '',
                             'Загадано число: 7925',
                             '7 и 9 угаданы на',
                             'неверных позициях.',
                             '5 угадана вплоть до позиции.']
            case 6:
                the_heit_is = 160
                abouttext = ['Победа зачитывается если',
                             'игрок отгадал всю',
                             'последовательность цифр.',
                             '',
                             'гуд лак',
                             'май френдс.']
            case 7:
                the_heit_is = 160
                pr.update_physics()
                pr.draw_text_ex(font, 'Радушный текст :/', pr.Vector2(24, 92), 16, 0,
                                pr.color_from_hsv(pr.get_time() * 120, 1, 1))
                pr.draw_text_pro(font, 'зачем?', pr.Vector2(84, 182), pr.Vector2(0, 0), pr.get_time() * 120, 16, 0,
                                 pr.color_from_hsv(pr.get_time() * 120, 1, 1))
                pr.draw_text('Powered by', 180, 90, 10, pr.WHITE)
                phystext = ['P', 'h', 'y', 's', 'a', 'c']
                pr.draw_text_ex(pr.get_font_default(), phystext[0],
                                pr.Vector2(170, 100 + (math.sin((pr.get_time() * 10)) * 4)), 30, 0,
                                pr.color_from_hsv(pr.get_time() * 480, 1, 1))
                pr.draw_text_ex(pr.get_font_default(), phystext[1],
                                pr.Vector2(191, 100 + (math.sin((pr.get_time() * 10) + 5) * 4)), 30, 0,
                                pr.color_from_hsv(pr.get_time() * 480 + 60, 1, 1))
                pr.draw_text_ex(pr.get_font_default(), phystext[2],
                                pr.Vector2(209, 100 + (math.sin((pr.get_time() * 10) + 10) * 4)), 30, 0,
                                pr.color_from_hsv(pr.get_time() * 480 + 120, 1, 1))
                pr.draw_text_ex(pr.get_font_default(), phystext[3],
                                pr.Vector2(227, 100 + (math.sin((pr.get_time() * 10) + 15) * 4)), 30, 0,
                                pr.color_from_hsv(pr.get_time() * 480 + 180, 1, 1))
                pr.draw_text_ex(pr.get_font_default(), phystext[4],
                                pr.Vector2(245, 100 + (math.sin((pr.get_time() * 10) + 20) * 4)), 30, 0,
                                pr.color_from_hsv(pr.get_time() * 480 + 240, 1, 1))
                pr.draw_text_ex(pr.get_font_default(), phystext[5],
                                pr.Vector2(263, 100 + (math.sin((pr.get_time() * 10) + 25) * 4)), 30, 0,
                                pr.color_from_hsv(pr.get_time() * 480 + 300, 1, 1))

                # pr.draw_text('Physac', 170, 140, 30, pr.color_from_hsv(pr.get_time() * 480, 1, 1))

                budcount = pr.get_physics_bodies_count()
                if budcount != 3:
                    pr.create_physics_body_polygon(pr.Vector2(84, 54), 40, 8, 10)
                    pr.create_physics_body_polygon(pr.Vector2(90, 0), 40, 4, 10)
                    floor = pr.create_physics_body_rectangle(pr.Vector2(112, 200), 290, 10, 10)
                    floor.enabled = False
                for i in range(budcount):
                    polybody = pr.get_physics_body(i)
                    vetCount = pr.get_physics_shape_vertices_count(i)
                    for j in range(vetCount):
                        verA = pr.get_physics_shape_vertex(polybody, j)
                        jj = (j + 1) if (j + 1 < vetCount) else 0
                        verB = pr.get_physics_shape_vertex(polybody, jj)
                        pr.draw_line_v(verA, verB, pr.Color(random.randint(0, 255), random.randint(0, 255),
                                                            random.randint(0, 255), 255))
                abouttext = ['']
        if abouttext is not None:
            for i in range(len(abouttext)):  # Draw the text
                pr.draw_text_ex(font, abouttext[i], pr.Vector2(24, 92 + 18 * i), 16, 0, color2)


def menu():
    # TODO: Main menu with some options
    #       like Settings(done), Docs (already has), VS Player, VS CPU and etc.
    #       See resources/mainmenu_concept.png
    global color1, color2
    startBtn = pr.Rectangle(108, 70, 96, 96)
    settingBtn = pr.Rectangle(108, 170, 96, 96)
    quitBtn = pr.Rectangle(108, 270, 96, 96)
    toggleDarkBtn = pr.Rectangle(10, 420, 20, 20)
    titleY = -30
    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(color1)
        if color1.r == 0:
            iconDarkBtn = moonpng
        else:
            iconDarkBtn = sunpng
        if titleY != 10:  # simple animation
            titleY += 1
        pr.draw_texture_ex(iconDarkBtn, pr.Vector2(12, 422), 0, 2, pr.Color(255, 255, 255, 255))
        pr.draw_texture_ex(bigPlay, pr.Vector2(120, 70), 0, 5, color2)
        pr.draw_texture_ex(bigGear, pr.Vector2(119, 172), 0, 5, color2)
        pr.draw_texture_ex(bigDoor, pr.Vector2(114, 270), 0, 5, color2)
        pr.draw_rectangle_lines_ex(settingBtn, 1, color2)
        pr.draw_rectangle_lines_ex(quitBtn, 1, color2)
        pr.draw_text_ex(font, 'Быки и коровы', pr.Vector2(105, titleY), 16, 0, color2)
        pr.draw_text_ex(font, 'ИГРАТЬ', pr.Vector2(134, 146), 16, 0, color2)
        pr.draw_text_ex(font, 'ПАРАМЕТРЫ', pr.Vector2(121, 246), 16, 0, color2)
        pr.draw_text_ex(font, 'ВЫХОД', pr.Vector2(137, 346), 16, 0, color2)
        pr.draw_text_ex(font, 'Copyright © 2022 Rico040', pr.Vector2(96, 410), 16, 0, color2)
        pr.draw_text_ex(font, 'WTFPL License w/o warranty', pr.Vector2(86, 426), 16, 0, color2)
        # pr.draw_text_ex(font, 'Copyright © 20XX ur name', pr.Vector2(96, 410), 16, 0, color2)
        # pr.draw_text_ex(font, 'ur own license', pr.Vector2(86, 426), 16, 0, color2)
        if pr.check_collision_point_rec(pr.get_mouse_position(), toggleDarkBtn):  # Dark/Light mode toggle btn
            pr.draw_rectangle_lines_ex(toggleDarkBtn, 1, pr.RED)
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                color1, color2 = color2, color1
        else:
            pr.draw_rectangle_lines_ex(toggleDarkBtn, 1, color2)

        if pr.check_collision_point_rec(pr.get_mouse_position(), startBtn):  # Yes this is somehow work :/
            # TODO: MULTIPLAYER FAGGOT!
            pr.draw_rectangle_lines_ex(startBtn, 1, pr.RED)
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                main()
        else:
            pr.draw_rectangle_lines_ex(startBtn, 1, color2)

        if pr.check_collision_point_rec(pr.get_mouse_position(), settingBtn):  # Settings button
            pr.draw_rectangle_lines_ex(settingBtn, 1, pr.RED)
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                settings()
        else:
            pr.draw_rectangle_lines_ex(settingBtn, 1, color2)

        if pr.check_collision_point_rec(pr.get_mouse_position(), quitBtn):  # exit button
            pr.draw_rectangle_lines_ex(quitBtn, 1, pr.RED)
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                its_quit()
        else:
            pr.draw_rectangle_lines_ex(quitBtn, 1, color2)
        pr.end_drawing()
    its_quit()


def settings():
    global max_input_char, output_set, color1, color2, SET_FPS, xmusicBtn, music_on
    insLengthBtn = pr.Rectangle(264, 101, 16, 16)
    desLengthBtn = pr.Rectangle(224, 101, 16, 16)
    outputSetBtn = pr.Rectangle(145, 129, 100, 19)
    toggleDarkBtn = pr.Rectangle(10, 420, 20, 20)
    exitBtn = pr.Rectangle(120, 420, 70, 20)
    setFpsBtn = pr.Rectangle(158, 179, 30, 19)
    mbpressed = False
    musictogBtn = pr.Rectangle(130, 210, 45, 19)
    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(color1)
        if color1.r == 0:
            iconDarkBtn = moonpng
        else:
            iconDarkBtn = sunpng
        pr.draw_text_ex(font, 'Настройки', pr.Vector2(115, 10), 16, 0, color2)
        pr.draw_text_ex(font, 'Длина последовательности:', pr.Vector2(20, 100), 16, 0, color2)
        pr.draw_text_ex(font, str(max_input_char), pr.Vector2(252 - 4 * len(str(max_input_char)), 100), 16, 0, color2)
        pr.draw_text_ex(font, '<', pr.Vector2(227, 99), 16, 0, color2)
        pr.draw_text_ex(font, '>', pr.Vector2(269, 99), 16, 0, color2)
        if output_set == 0:
            pr.draw_text_ex(font, 'Вариант вывода: Расширенный', pr.Vector2(20, 130), 16, 0, color2)
            pr.draw_text_ex(font, '1234: 1 Бык и 2 Коров', pr.Vector2(20, 150), 16, 0, color2)
        elif output_set == 1:
            pr.draw_text_ex(font, 'Вариант вывода: Сокращенный', pr.Vector2(20, 130), 16, 0, color2)
            pr.draw_text_ex(font, '1234: 1б2к', pr.Vector2(20, 150), 16, 0, color2)
        if pr.check_collision_point_rec(pr.get_mouse_position(), insLengthBtn):
            pr.draw_rectangle_lines_ex(insLengthBtn, 1, pr.RED)
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                if max_input_char != 10:
                    max_input_char += 1
        else:
            pr.draw_rectangle_lines_ex(insLengthBtn, 1, color2)

        if pr.check_collision_point_rec(pr.get_mouse_position(), desLengthBtn):
            pr.draw_rectangle_lines_ex(desLengthBtn, 1, pr.RED)
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                if max_input_char != 1:
                    max_input_char -= 1
        else:
            pr.draw_rectangle_lines_ex(desLengthBtn, 1, color2)

        if pr.check_collision_point_rec(pr.get_mouse_position(), outputSetBtn):
            pr.draw_rectangle_lines_ex(outputSetBtn, 1, pr.RED)
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                if output_set == 0:
                    output_set = 1
                else:
                    output_set = 0
        else:
            pr.draw_rectangle_lines_ex(outputSetBtn, 1, color2)

        pr.draw_text_ex(font, f'Ограничение FPS:  {SET_FPS}', pr.Vector2(20, 179), 16, 0, color2)
        if pr.check_collision_point_rec(pr.get_mouse_position(), setFpsBtn):
            pr.draw_rectangle_lines_ex(setFpsBtn, 1, pr.RED)
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                if SET_FPS == 60:
                    SET_FPS = 30
                else:
                    SET_FPS = 60
                pr.set_target_fps(SET_FPS)
        else:
            pr.draw_rectangle_lines_ex(setFpsBtn, 1, color2)

        musicBtn = pr.Rectangle(xmusicBtn, 266, 10, 10)
        pr.draw_text_ex(font, f'Громкость музыки: {int(xmusicBtn - 40)}', pr.Vector2(20, 240), 16, 0, color2)
        pr.draw_line(40, 270, 150, 270, color2)
        pr.draw_rectangle(int(xmusicBtn), 266, 10, 10, color1)
        if pr.check_collision_point_rec(pr.get_mouse_position(), musicBtn) or mbpressed:
            pr.draw_rectangle_lines_ex(musicBtn, 1, pr.RED)
            if pr.is_mouse_button_down(pr.MOUSE_BUTTON_LEFT):
                mbpressed = True
                tempx = pr.get_mouse_position()
                xmusicBtn = tempx.x - 3
                if xmusicBtn > 140:
                    xmusicBtn = 140
                if xmusicBtn < 40:
                    xmusicBtn = 40
            else:
                mbpressed = False
        else:
            pr.draw_rectangle_lines_ex(musicBtn, 1, color2)

        pr.draw_text_ex(font, 'Вкл. Музыку:', pr.Vector2(20, 210), 16, 0, color2)
        if pr.check_collision_point_rec(pr.get_mouse_position(), musictogBtn):
            pr.draw_rectangle_lines_ex(musictogBtn, 1, pr.RED)
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                if music_on:
                    music_on = False
                else:
                    music_on = True
        else:
            pr.draw_rectangle_lines_ex(musictogBtn, 1, color2)

        if music_on:
            pr.draw_text_ex(font, 'Да', pr.Vector2(144, 210), 16, 0, color2)
        else:
            pr.draw_text_ex(font, 'Нет', pr.Vector2(140, 210), 16, 0, color2)

        pr.draw_texture_ex(iconDarkBtn, pr.Vector2(12, 422), 0, 2, pr.Color(255, 255, 255, 255))
        pr.draw_text_ex(font, 'B/W Режим', pr.Vector2(12, 400), 16, 0, color2)
        if pr.check_collision_point_rec(pr.get_mouse_position(), toggleDarkBtn):  # Dark/Light mode toggle btn
            pr.draw_rectangle_lines_ex(toggleDarkBtn, 1, pr.RED)
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                color1, color2 = color2, color1
        else:
            pr.draw_rectangle_lines_ex(toggleDarkBtn, 1, color2)

        if pr.check_collision_point_rec(pr.get_mouse_position(), exitBtn):
            pr.draw_rectangle_lines_ex(exitBtn, 1, pr.RED)
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                break
        else:
            pr.draw_rectangle_lines_ex(exitBtn, 1, color2)
        pr.draw_text_ex(font, 'Выйти', pr.Vector2(135, 420), 16, 0, color2)

        pr.end_drawing()


def its_quit():
    # im lazy
    # unload everything! (but seems like game isn't memory hungry)
    # also it more like not very mega important cuz when process stopping its unloading
    pr.close_window()
    pr.unload_font(font)
    pr.unload_texture(moonpng)
    pr.unload_texture(sunpng)
    pr.unload_texture(exitl)
    pr.unload_texture(exitd)
    pr.unload_texture(bigPlay)
    pr.unload_texture(bigDoor)
    pr.unload_texture(bigGear)
    # seems like pyinstaller can't define quit()
    exit()


if __name__ == "__main__":  # Magic: executing code as main if it loaded as main code not imported
    menu()