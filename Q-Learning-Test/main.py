"""
Known bugs: If pressed on the black of the screen, it throws errors for dividing by 0. Too tired to fix right now.
ALSO LIKE AN IDIOT I FLIPPED ROW AND COLUMN some places, ill have to fix that in order not to go mad.
Next implementation: Add a right click feature to choose the goal location.
"""

import numpy as np
import pygame as pg
environment_rows = 11
environment_columns = 11
q_values = np.zeros((environment_rows, environment_columns, 4))
actions = ['up', 'right', 'down', 'left']
rewards = np.full((environment_rows, environment_columns), -100.)
rewards[0, 5] = 100.
reward_grid_y, reward_grid_x = 0, 5
aisles = {}
aisles[1] = [i for i in range(1, 10)]
aisles[2] = [1, 7, 9]
aisles[3] = [i for i in range(1, 8)]
aisles[3].append(9)
aisles[4] = [3, 7]
aisles[5] = [i for i in range(11)]
aisles[6] = [5]
aisles[7] = [i for i in range(1, 10)]
aisles[8] = [3, 7]
aisles[9] = [i for i in range(11)]
for row_index in range(1, 10):
    for column_index in aisles[row_index]:
        rewards[row_index, column_index] = -1
for row in rewards:
    print(row)
def is_terminal_state(current_row_index, current_column_index):
    if rewards[current_row_index, current_column_index] == -1.:
        return False
    else:
        return True
def get_starting_location():
    current_row_index = np.random.randint(environment_rows)
    current_column_index = np.random.randint(environment_columns)
    while is_terminal_state(current_row_index, current_column_index):
        current_row_index = np.random.randint(environment_rows)
        current_column_index = np.random.randint(environment_columns)
    return current_row_index, current_column_index
def get_next_action(current_row_index, current_column_index, epsilon):
    if np.random.random() < epsilon:
        return np.argmax(q_values[current_row_index, current_column_index])
    else:
        return np.random.randint(4)
def get_next_location(current_row_index, current_column_index, action_index):
    new_row_index = current_row_index
    new_column_index = current_column_index
    if actions[action_index] == 'up' and current_row_index > 0:
        new_row_index -= 1
    elif actions[action_index] == 'right' and current_column_index < environment_columns - 1:
        new_column_index += 1
    elif actions[action_index] == 'down' and current_row_index < environment_rows -1:
        new_row_index += 1
    elif actions[action_index] == 'left' and current_column_index > 0:
        new_column_index -= 1
    return new_row_index, new_column_index
def get_shortest_path(start_row_index, start_column_index):
    if is_terminal_state(start_row_index, start_column_index):
        return []
    else:
        current_row_index, current_column_index = start_row_index, start_column_index
        shortest_path = []
        shortest_path.append([current_row_index, current_column_index])
        while not is_terminal_state(current_row_index, current_column_index):
            action_index = get_next_action(current_row_index, current_column_index, 1.)
            current_row_index, current_column_index = get_next_location(current_row_index, current_column_index, action_index)
            shortest_path.append([current_row_index, current_column_index])
        return shortest_path


epsilon = 0.9
discount_factor = 0.9
learning_rate = 0.9
for episode in range(1000):
    row_index, column_index = get_starting_location()
    while not is_terminal_state(row_index, column_index):
        action_index = get_next_action(row_index, column_index, epsilon)
        old_row_index, old_column_index = row_index, column_index
        row_index, column_index = get_next_location(row_index, column_index, action_index)
        reward = rewards[row_index, column_index]
        old_q_value = q_values[old_row_index, old_column_index, action_index]
        temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value
        new_q_value = old_q_value + (learning_rate * temporal_difference)
        q_values[old_row_index, old_column_index, action_index] = new_q_value
print('Training complete!')
# print(get_shortest_path(3, 9))
# print(get_shortest_path(5, 0))
# print(get_shortest_path(9, 5))
# path = get_shortest_path(5, 2)
# path.reverse()
# print(path)

color_path = []
color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_green = (0, 255, 0)
color_grey = (200, 200, 200)
color_blue = (0, 0, 255)
mouse_click = 0

pg.init()
size = (560, 560)
width = 40
height = 40
margin = 10
grid = []
for row in range(11):
    grid.append([])
    for column in range(11):
        grid[row].append(0)
# grid[1][5] = 1
basic_rect = (0, 0, width, height)


screen = pg.display.set_mode(size)
pg.display.set_caption('AI Warehouse')
complete = False
clock = pg.time.Clock()

# Row = X
# Column = Y idiot
def reduce(pos):
    path_row = 1
    path_column = 1

    if pos[0] >= 10 and pos[0] <= 50:
        path_row = 0
    elif pos[0] >= 60 and pos[0] <= 100:
        path_row = 1
    elif pos[0] >= 110 and pos[0] <= 150:
        path_row = 2
    elif pos[0] >= 160 and pos[0] <= 200:
        path_row = 3
    elif pos[0] >= 210 and pos[0] <= 250:
        path_row = 4
    elif pos[0] >= 260 and pos[0] <= 300:
        path_row = 5
    elif pos[0] >= 310 and pos[0] <= 350:
        path_row = 6
    elif pos[0] >= 360 and pos[0] <= 400:
        path_row = 7
    elif pos[0] >= 410 and pos[0] <= 450:
        path_row = 8
    elif pos[0] >= 460 and pos[0] <= 500:
        path_row = 9
    elif pos[0] >= 510 and pos[0] <= 560:
        path_row = 10
    elif pos[1] >= 10 and pos[1] <= 50:
        path_column = 0
    elif pos[1] >= 60 and pos[1] <= 100:
        path_column = 1
    elif pos[1] >= 110 and pos[1] <= 150:
        path_column = 2
    elif pos[1] >= 160 and pos[1] <= 200:
        path_column = 3
    elif pos[1] >= 210 and pos[1] <= 250:
        path_column = 4
    elif pos[1] >= 260 and pos[1] <= 300:
        path_column = 5
    elif pos[1] >= 310 and pos[1] <= 350:
        path_column = 6
    elif pos[1] >= 360 and pos[1] <= 400:
        path_column = 7
    elif pos[1] >= 410 and pos[1] <= 450:
        path_column = 8
    elif pos[1] >= 460 and pos[1] <= 500:
        path_column = 9
    elif pos[1] >= 510 and pos[1] <= 560:
        path_column = 10
    else:
        print('Could not choose position.')
        path_row = 2
        path_column = 1
    ''



def draw_path(path, neural_list):
    # print('Drawing a greyscale path from start point to optimal destination...')
    # print('path: ' + str(path))
    path_count = 0
    for i in range(len(neural_list)):
        element = neural_list[i]
        row = element[0]
        column = element[1]
        color = path[path_count]
        path_count += 1
        # print("color: " + str(color))
        x = (margin + width) * column + margin
        y = (margin + height) * row + margin
        pg.draw.rect(screen, color, (x, y, width, height))
    """
    for l in range(len(neural_list)):
        for i in range(len(path)):
            element = neural_list[i]
            column = element[0]
            row = element[1]
            color = path[i]
            x = (margin + width) * column + margin
            y = (margin + height) * row + margin
            pg.draw.rect(screen, color, (x, y, width, height))
    """

def grey_path(current_path):
    # need to calculate len the shortest path
    cx = 220
    cy = 220
    cz = 220
    change_x = 220
    change_y = 220
    change_z = 220
    color_start_grey = (220, 220, 220)
    shortest_path_length = len(current_path)
    # print(shortest_path_length)
    count = int((220 - 50)/shortest_path_length)
    # path_range = 1, shortest_path_length
    # print(path_range)
    i = 1
    color_path = [color_start_grey]
    while i != shortest_path_length:
        cx = change_x - count * i
        cy = change_y - count * i
        cz = change_z - count * i
        color_path_grey = (cx, cy, cz)
        color_path.append(color_path_grey)
        i += 1
    # print('color path: ' + str(color_path))

    #color_path[0] = (255, 0, 0)
    #color_path[-1] = color_green
    for i in range(len(color_path)):
        color_path[i] = (255, 0, 0)
    color_path[-1] = color_green
    color_path[0] = color_blue
    draw_path(path=color_path, neural_list=get_shortest_path(start_row_index=set_path_row, start_column_index=set_path_column))



#start_column_index = set_path_column, start_row_index = set_path_row
while not complete:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            complete = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_click += 1
            pos = pg.mouse.get_pos()
            try:
                print("Last clicked row: " + str(path_row))
                print("Last clicked column: " + str(path_column))
                print(pos[1])
            except:
                print('there is no path row')

    screen.fill(color_black)

    for row in range(11):
        for column in range(11):
            color = color_black
            x = (margin + width) * column + margin
            y = (margin + height) * row + margin
            pg.draw.rect(screen, color, (x, y, width, height))
    for row in range(1, 10):
        for column in aisles[row]:
            color = color_white
            x = (margin + width) * column + margin
            y = (margin + height) * row + margin
            pg.draw.rect(screen, color, (x, y, width, height))
    color = color_green
    x = (margin + width) * reward_grid_x + margin
    y = (margin + height) * reward_grid_y + margin
    pg.draw.rect(screen, color, (x, y, width, height))

    # set_path_row, set_path_column = 5, 10
    # grey_path(current_path=get_shortest_path(start_row_index=set_path_row, start_column_index=set_path_column))
    #for event in pg.event.get():
      #  if event.type == pg.MOUSEBUTTONDOWN:
       #     position = pg.mouse.get_pos()
       #     mouse_click += 1
       #     set_path_row = 2
       #     set_path_column = 1

    if mouse_click != 0:
        path_row = 1
        path_column = 1
        if pos[0] >= 10 and pos[0] <= 50:
            path_row = 0
        elif pos[0] >= 60 and pos[0] <= 100:
            path_row = 1
        elif pos[0] >= 110 and pos[0] <= 150:
            path_row = 2
        elif pos[0] >= 160 and pos[0] <= 200:
            path_row = 3
        elif pos[0] >= 210 and pos[0] <= 250:
            path_row = 4
        elif pos[0] >= 260 and pos[0] <= 300:
            path_row = 5
        elif pos[0] >= 310 and pos[0] <= 350:
            path_row = 6
        elif pos[0] >= 360 and pos[0] <= 400:
            path_row = 7
        elif pos[0] >= 410 and pos[0] <= 450:
            path_row = 8
        elif pos[0] >= 460 and pos[0] <= 500:
            path_row = 9
        elif pos[0] >= 510 and pos[0] <= 560:
            path_row = 10
        if pos[1] >= 10 and pos[1] <= 50:
            path_column = 0
        elif pos[1] >= 60 and pos[1] <= 100:
            path_column = 1
        elif pos[1] >= 110 and pos[1] <= 150:
            path_column = 2
        elif pos[1] >= 160 and pos[1] <= 200:
            path_column = 3
        elif pos[1] >= 210 and pos[1] <= 250:
            path_column = 4
        elif pos[1] >= 260 and pos[1] <= 300:
            path_column = 5
        elif pos[1] >= 310 and pos[1] <= 350:
            path_column = 6
        elif pos[1] >= 360 and pos[1] <= 400:
            path_column = 7
        elif pos[1] >= 410 and pos[1] <= 450:
            path_column = 8
        elif pos[1] >= 460 and pos[1] <= 500:
            path_column = 9
        elif pos[1] >= 510 and pos[1] <= 560:
            path_column = 10
        else:
            print('Could not choose position.')
            path_row = 2
            path_column = 1
        set_path_row = path_column
        set_path_column = path_row
        grey_path(current_path=get_shortest_path(start_row_index=set_path_row, start_column_index=set_path_column))

    clock.tick(60)
    pg.display.flip()
pg.quit()
