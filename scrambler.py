import random
import argparse

# Add argparse for command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--s", type=int, help="number of scrambles to generate", default=1)
parser.add_argument("--c", type=int, help="type of cube to generate scrambles for", default=3)
parser.add_argument("--m", type=int, help="number of moves in each scramble", default=20)
args = parser.parse_args()

# Moves for 2x2x2, 3x3x3 and 4x4x4 cubes
moves_2x2 = ["R", "U", "F"]
moves_3x3 = ["U", "D", "F", "B", "R", "L"]
moves_4x4 = moves_3x3 + ["u", "d", "l", "r", "f", "b"]
dir = ["", "'", "2"]

wide_move_prob = 0.1  # probability of wide move for 4x4x4 cube

def gen_scramble(c_type, slen):
    # Choose moves based on cube type
    if c_type == 2:
        moves = moves_2x2
    elif c_type == 3:
        moves = moves_3x3
    elif c_type == 4:
        moves = moves_3x3  # start with standard moves
        for i in range(int(slen * wide_move_prob)):  # add some wide moves
            moves.append(random.choice(moves_4x4[6:]))  # choose from wide moves
        random.shuffle(moves)  # shuffle the moves
    else:
        print(f"Unsupported cube type: {c_type}")
        return
    
    # Make array of arrays that represent moves ex. U' = ['U', "'"]
    s = valid([[random.choice(moves), random.choice(dir)] for x in range(slen)], moves)

    # Format scramble to a string with movecount
    return ''.join(str(s[x][0]) + str(s[x][1]) + ' ' for x in range(len(s))) + "[" + str(slen) + "]"

def valid(ar, moves):
    # Check if Move behind or 2 behind is the same as the random move
    # this gets rid of 'R R2' or 'R L R2' or similar for all moves
    for x in range(1, len(ar)):
        while ar[x][0] == ar[x-1][0]:
            ar[x][0] = random.choice(moves)
    for x in range(2, len(ar)):
        while ar[x][0] == ar[x-2][0] or ar[x][0] == ar[x-1][0]:
            ar[x][0] = random.choice(moves)
    return ar

for i in range(args.s):
    s = gen_scramble(args.c, args.m)
    if s:
        print(s)

