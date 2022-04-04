import random
import time


length = 4  # Сетаем много чисел ааааа помогите, дайте рейлиб
cows, bulls, step = 0, 0, 0
digitslol = [False, False, False, False, False, False, False, False, False, False]
result = ""
gueesp = ""

while len(result) != length:  # делаем сикрет с гарантом на уник
    junko = random.randint(0, 9)
    if not digitslol[junko]:
        result += "%d" % junko
        digitslol[junko] = True

del digitslol  # Удаляем лист и создаем другой лист xd
l_result = list(map(int, result))
start_timee = time.time()

while gueesp != result:
    step += 1
    gueesp = str(input(f"Enter {length} (unique) digits\nGuess.: "))
    l_gueesp = list(map(int, gueesp))
    print(l_gueesp)

    for reisen in range(length):  # Считаем быков и коров p.s. & НЕ ОПЕРАТОР!!!1
        for tewi in range(length):
            if l_result[reisen] == l_gueesp[tewi] and tewi == reisen:
                bulls += 1
            elif l_result[reisen] == l_gueesp[tewi] and tewi != reisen:
                cows += 1

    print(f"{bulls} Bull(s) and {cows} Cow(s).")
    if bulls == length:
        end_time = time.time()
        print(f"Congrats! You've made it for {step} steps\nand {end_time - start_timee:.2f} seconds.")
        input("")
    reisen, tewi = 0, 0
    cows, bulls = 0, 0
