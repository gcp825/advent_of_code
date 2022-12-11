from intcode import IntcodeComputer    # see intcode.py in this repo

def reply_and_return_response(g,cmd=None):

    output = []
    out = g.run() if cmd is None else g.run(cmd)
    while g.active:
        output += [out]
        out = g.run()   

    return ''.join([chr(x) for x in output])

def parse(cmd):

    return [ord(x) for x in list(cmd)+['\n']]

def main(f):

    moves = [[101, 97, 115, 116], [116, 97, 107, 101, 32, 102, 111, 111, 100, 32, 114, 97, 116, 105, 111, 110], 
             [115, 111, 117, 116, 104], [116, 97, 107, 101, 32, 112, 114, 105, 109, 101, 32, 110, 117, 109, 98, 101, 114], [110, 111, 114, 116, 104], 
             [101, 97, 115, 116], [101, 97, 115, 116], [110, 111, 114, 116, 104], [110, 111, 114, 116, 104], 
             [116, 97, 107, 101, 32, 102, 117, 101, 108, 32, 99, 101, 108, 108], [115, 111, 117, 116, 104], [115, 111, 117, 116, 104], [119, 101, 115, 116], 
             [119, 101, 115, 116], [119, 101, 115, 116], [110, 111, 114, 116, 104], [110, 111, 114, 116, 104], [119, 101, 115, 116], 
             [116, 97, 107, 101, 32, 109, 117, 103], [101, 97, 115, 116], [115, 111, 117, 116, 104], [119, 101, 115, 116], [110, 111, 114, 116, 104], 
             [119, 101, 115, 116], [110, 111, 114, 116, 104]]   

    while True:
        mode = input("Please choose game mode:\n1) Interactive\n2) Cheat\n")
        if mode.isnumeric() and mode in ('1','2'): break

    g = IntcodeComputer(load=f)
    response = reply_and_return_response(g)
    if mode == 1: print(response)
    
    while response[-9:-1] == 'Command?':
        cmd = parse(input(response)) if mode == '1' else moves.pop(0) + [ord('\n')]
        response = reply_and_return_response(g,cmd)

    if mode == '2' and 'keypad' in response: 
        print(response[response.find('Oh'):])
    else:
        print(response)

    return 'Congratulations!' if 'keypad' in response else 'Bad Luck! Please try again.'

print(main('25.txt'))
