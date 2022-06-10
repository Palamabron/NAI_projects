def getData(path="Data/plecak_wyzarzanie.txt"):
    with open(path) as file:
        data = file.read()
    data = data.split("\n")
    data[0] = data[0].split(" ")
    data[1] = data[1].split(",")
    data[2] = data[2].split(",")
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = int(data[i][j])
    print(data)
    return data
