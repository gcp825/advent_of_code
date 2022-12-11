from collections import deque

def main(num_of_players,num_of_marbles):

    circle = deque([0])
    player = num_of_players - 1
    scores = [0] * num_of_players

    for marble in range(1,(num_of_marbles * 100) + 1):

        player = (player+1) % num_of_players

        if marble % 23 == 0:

            circle.rotate(7)
            scores[player] += (circle.popleft() + marble)

        else:
            circle.insert(2,marble)
            while circle[0] != marble: circle.rotate(-1)

        if marble == num_of_marbles:
            pt1 = max(scores)

    return pt1, max(scores)

print(main(459,71320))