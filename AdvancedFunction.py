import pickle


def modificationOrigin(DATA: str):

    outcome = [[], [], [], [], [], []]

    machining1st = [i.split(" | ") for i in DATA.strip()[:-1].split("&\r\n")]

    for i in machining1st: i[0] = i[0].replace("\r\n", "").strip()

    for i in range(len(machining1st)):

        temp = machining1st[i][5][1:-1]
        result = list()

        while True:

            try:

                temp = temp[temp.index('\'') + 1:]

                result.append(temp[:temp.index('\'')])

                temp = temp[temp.index('\'') + 1:]

            except: break

        # noinspection PyTypeChecker
        machining1st[i][5] = result

    for i in machining1st:

        for j in range(len(i)):

            outcome[j].append(i[j])

    dummy = outcome[-1]

    outcome = outcome[:-1]

    outcome.insert(3, dummy)

    with open("DATA.txt", "wb") as f: pickle.dump(outcome, f)
