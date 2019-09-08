import json
import sys

def create_map(filename):
    with open(filename, 'r') as f:
        msg = f.readline()
        # First 5 digits represents msg_id, thus eliminated
        leg_start = json.loads(msg[5:])

        width = leg_start['map_size']['width']
        height = leg_start['map_size']['height']
        belts = leg_start['belts']
        walls = leg_start['walls']
        gates = leg_start['gates']

        # mines (power) and players info
        msg = f.readline()
        round0 = json.loads(msg[5:])
        mines = round0['mines']
        players = round0['players']
    f.close()

    grid = [['.'] * width for c in range(height)]
    direction = {"down": 'v', 'up': '^', 'left': '<', 'right': '>'}
    for belt in belts:
        grid[belt['y']][belt['x']]=direction[belt['dir']]
    gatelist = []
    for gate in gates:
        x = chr(gate['name'])
        if x not in gatelist:
            gatelist.append(x)
        else:
            x = x.lower()
            gatelist.append(x)
        grid[gate['y']][gate['x']]=x
    for wall in walls:
        grid[wall['y']][wall['x']]='#'
    for mine in mines:
        grid[mine['y']][mine['x']]=str(mine['value'])

    for player in players:
        if player['player_id'] // 4 == 0:
            grid[player['y']][player['x']] = 'X'
        else:
            grid[player['y']][player['x']] = 'O'

    for i in range(height):
        print(''.join(grid[i]))


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 2:
        print("The parameters has error. (Please enter correct replay file)")
    filename = sys.argv[1]
    create_map(filename)