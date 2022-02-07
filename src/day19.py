import numpy as np
import collections


def load_data(path):
    file = open(path, "r")
    data = file.read()
    data = data.split('\n\n')
    data = [chunk.split('\n') for chunk in data]
    return data


class Scanner:
    def __init__(self, string_list, n_scanners, rotations):
        self.id = int(string_list[0].split(' ')[2])
        self.known = False
        if self.id == 0:
            self.known = True
            self.position = np.array([0, 0, 0])
        beacons = [line.split(',') for line in string_list[1:]]
        self.beacons = np.array(beacons, dtype=int)
        self.not_checked = np.full(n_scanners, True)
        self.rotations = rotations

    def fit_against(self, scanner):
        # Check whether it fits
        for rotation in self.rotations:
            offsets = []
            for beacon1 in self.beacons@rotation:
                for beacon2 in scanner.beacons:
                    offsets.append(tuple(beacon1 - beacon2))
            # if offset has multiple
            counter = collections.Counter(offsets)
            if counter.most_common()[0][1] >= 12:
                # Transform
                self.beacons = self.beacons@rotation
                offset = np.array(counter.most_common()[0][0])
                self.beacons -= offset
                self.position = offset
                return True
        return False

    def fit(self, scanners, known):
        to_check = known & self.not_checked
        self.not_checked[to_check] = False
        for scanner, is_to_check in zip(scanners, to_check):
            if is_to_check:
                if self.fit_against(scanner):
                    return True
        return False


def generate_rotations():
    lines = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    lines += [[-num for num in line] for line in lines]
    rotations = []
    rotation = np.zeros((3, 3))

    for line0 in lines:
        rotation[0, :] = line0
        for line1 in lines:
            rotation[1, :] = line1
            for line2 in lines:
                rotation[2, :] = line2
                if np.linalg.det(rotation) == 1:
                    rotations.append(rotation.copy())
    return rotations


def task1():
    data = load_data("input/day19.txt")
    rotations = generate_rotations()
    scanners = [Scanner(scanner, len(data), rotations) for scanner in data]
    known = np.full_like(scanners, False, dtype=bool)
    known[0] = True

    # Fit scanners together
    while not known.all():
        print(sum(known))
        for i in range(len(scanners)):
            if not known[i]:
                if scanners[i].fit(scanners, known):
                    known[i] = True

    # Count beacons
    beacons = set()
    for scanner in scanners:
        for beacon in scanner.beacons:
            beacons.add(tuple(beacon))
    print(beacons)
    print(len(beacons))


def task2():
    data = load_data("input/day19.txt")
    rotations = generate_rotations()
    scanners = [Scanner(scanner, len(data), rotations) for scanner in data]
    known = np.full_like(scanners, False, dtype=bool)
    known[0] = True

    # Fit scanners together
    while not known.all():
        print(sum(known))
        for i in range(len(scanners)):
            if not known[i]:
                if scanners[i].fit(scanners, known):
                    known[i] = True

    # Count beacons
    positions = [scanner.position for scanner in scanners]
    max_dist = 0
    for p1 in positions:
        for p2 in positions:
            dist = sum(abs(p1 - p2))
            if dist > max_dist:
                max_dist = dist
    print(max_dist)
