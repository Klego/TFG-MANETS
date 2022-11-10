import os
import random


def main():
    min_x = 250
    min_y = 250
    max_x = 400
    max_y = 400
    timestamps = [90, 150, 210, 270, 330, 390, 450, 510, 560]
    seed = 2022
    path = os.path.dirname(os.path.abspath(__file__)) + '/replayingMobility/escenario5/'
    random.seed(seed)
    for i in range(1, 11):
        filename = "node_sta" + str(i) + ".dat"
        filepath = f"{path}/{filename}"
        with open(filepath, 'w') as f:
            for j in range(0, 9):
                line = str(random.randint(min_x, max_x)) + " " + str(random.randint(min_y, max_y)) + " " + \
                       str(timestamps[j]) + "\n"
                f.write(line)


if __name__ == "__main__":
    main()
