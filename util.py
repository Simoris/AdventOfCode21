def load_data(path):
    file = open(path, "r")
    data = file.read()
    data = data.split('\n')[:-1]
    return data
