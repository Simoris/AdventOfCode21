import util
import numpy as np


def to_bin_string(hex_string):
    bin_string = bin(int(hex_string, 16))[2:]
    while len(bin_string) < 4*len(hex_string):
        bin_string = '0' + bin_string
    return bin_string


class Package:
    def __init__(self, version, type_id, content):
        self.version = version
        self.type_id = type_id
        self.content = content

    def get_version_sum(self):
        if self.type_id == 4:
            return self.version
        else:
            version_sum = self.version
            for pkg in self.content:
                version_sum += pkg.get_version_sum()
            return version_sum

    def evaluate(self):
        if self.type_id == 4:
            # print(self.content)
            return self.content
        else:
            inputs = []
            for pkg in self.content:
                inputs.append(pkg.evaluate())
            if self.type_id == 0:  # Sum
                return np.sum(inputs, dtype=np.uint64)
            elif self.type_id == 1:  # Product
                return np.prod(inputs, dtype=np.uint64)
            elif self.type_id == 2:  # Minimum
                return min(inputs)
            elif self.type_id == 3:  # Maximum
                return max(inputs)
            elif self.type_id == 5:  # Greater than
                if inputs[0] > inputs[1]:
                    return 1
                else:
                    return 0
            elif self.type_id == 6:  # Less than
                if inputs[0] < inputs[1]:
                    return 1
                else:
                    return 0
            elif self.type_id == 7:  # Equal to
                if inputs[0] == inputs[1]:
                    return 1
                else:
                    return 0

    @classmethod
    def parse_package(cls, bin_string):
        version = int(bin_string[:3], 2)
        type_id = int(bin_string[3:6], 2)
        used_bits = 6

        if type_id == 4:
            lit_bin_string = ""
            i = used_bits
            while True:
                lit_bin_string += bin_string[i+1:i+5]
                if bin_string[i] == '0':
                    break
                i += 5
            used_bits = i + 5
            content = int(lit_bin_string, 2)
        else:
            content = []
            length_type_id = int(bin_string[used_bits])
            used_bits += 1
            if length_type_id == 0:
                bit_length = int(bin_string[used_bits:used_bits+15], 2)
                used_bits += 15
                localy_used_bits = 0
                while True:
                    next_pkg, n_bits = Package.parse_package(bin_string[used_bits + localy_used_bits:])
                    content.append(next_pkg)
                    localy_used_bits += n_bits
                    if localy_used_bits + 6 > bit_length:  # TODO: Sharp enough?
                        break
                used_bits += localy_used_bits
            else:
                n_sub_packages = int(bin_string[used_bits:used_bits+11], 2)
                used_bits += 11
                for i in range(n_sub_packages):
                    next_pkg, n_bits = Package.parse_package(bin_string[used_bits:])
                    content.append(next_pkg)
                    used_bits += n_bits

        return cls(version, type_id, content), used_bits


def task1():
    data = util.load_data("input/day16.txt")[0]
    bin_string = to_bin_string(data)
    pkg = Package.parse_package(bin_string)[0]
    print(pkg.get_version_sum())


def task2():
    data = util.load_data("input/day16.txt")[0]
    bin_string = to_bin_string(data)
    pkg = Package.parse_package(bin_string)[0]
    print(pkg.evaluate())
