from intcode import IntcodeComputer

def play(f):

    game = IntcodeComputer(load=f);  game.set_addr(0,2);  screen = {};  bat, blocks, score, x = (0,0,0,0)

    while game.active:

        x = game.run()

        if game.active:

            y = game.run();  z = game.run()

            if x <  0: score = z
            if x >= 0: screen[(y,x)] = z

            if z == 2: blocks += 1
            if z == 3: bat = x
            if z == 4:
                ball = x
                move = 0 if bat in (0,ball) else 1 if bat < ball else -1
                game.read(move)

    return blocks, score

def main(f):

    return play(f)

print(main('13.txt'))
