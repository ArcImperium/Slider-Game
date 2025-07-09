import pandas as pd
import random
import keyboard

def print_frame(game_list):
    a = game_list[0]
    b = game_list[1]
    c = game_list[2]
    d = game_list[3]
    e = game_list[4]
    f = game_list[5]
    g = game_list[6]
    h = game_list[7]
    i = game_list[8]
    
    game_frame = pd.DataFrame([
        [a, b, c],
        [d, e, f],
        [g, h, i]
    ])

    print(game_frame.to_string(index=False, header=False))

def find_o(o_index):
    if o_index == 0:
        print('↓ →')
    elif o_index == 1:
        print('← ↓ →')
    elif o_index == 2:
        print('← ↓')
    elif o_index == 3:
        print('↑ ↓ →')
    elif o_index == 4:
        print('← ↑ ↓ →')
    elif o_index == 5:
        print('← ↑ ↓')
    elif o_index == 6:
        print('↑ →')
    elif o_index == 7:
        print('← ↑ →')
    elif o_index == 8:
        print('← ↑')

def find_key(o_index):
    key = keyboard.read_key()
    while keyboard.is_pressed(key):
        pass
    if key == 'left' or key == 'a':
        game_list[o_index], game_list[o_index - 1] = game_list[o_index - 1], game_list[o_index]
    elif key == 'up' or key == 'w':
        game_list[o_index], game_list[o_index - 3] = game_list[o_index - 3], game_list[o_index]
    elif key == 'down' or key == 's':
        game_list[o_index], game_list[o_index + 3] = game_list[o_index + 3], game_list[o_index]
    elif key == 'right' or key == 'd':
        game_list[o_index], game_list[o_index + 1] = game_list[o_index + 1], game_list[o_index]


def check_over(game_list):
    check_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    if check_list == game_list:
        print_frame(game_list)
        run = False
    else:
        pass

game_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
random.shuffle(game_list)

run = True
while run == True:
    print_frame(game_list)
    print()

    o_index = game_list.index(0)
    find_o(o_index)
    print()
    print()

    find_key(o_index)

    check_over(game_list)