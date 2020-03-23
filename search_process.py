from pickle import load


def origin():

    with open(".\DATA.txt", "rb") as f: return load(f)


def search(word: str, DATA: list): return [j for i in range(3) for j in range(len(DATA[0])) if word in DATA[i][j]]


def search_detail(category:str, help:str, startWhen:str, endWhen:str, DATA:list):

    return [j for j in range(len(DATA[0])) if all((int(DATA[1][j][20:]) >= int(startWhen),
            int(DATA[1][j][20:]) <= int(endWhen), DATA[4][j] == category, float(DATA[5][j]) >= float(help)))]


def date_compare(date1:str, date2:str): #date1 > date2에 대한 답

    Month = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

    if int(date1[20:]) > int(date2[20:]): return True
    elif int(date1[20:]) < int(date2[20:]): return False

    if Month.index(date1[4:7]) > Month.index(date2[4:7]): return True
    elif Month.index(date1[4:7]) < Month.index(date2[4:7]): return False

    for i in range(8, 18, 3):

        if int(date1[i:i+2]) > int(date2[i:i+2]): return True
        elif int(date1[i:i+2]) < int(date2[i:i+2]): return False

    return True


def date_sort(List: list):

    date, sign = list(), list()

    for i in range(len(List)):

        if List[i][1] not in sign: date.append([i]); sign.append(List[i][1])

        else: date[sign.index(List[i][1])].append(i)

    Dict = dict(zip(date, sign))

    for i in range(len(sign)-1):

        for j in range(1, len(sign)-i):

            if date_compare(sign[j-1], sign[j]):

                sign[j-1], sign[j] = sign[j], sign[j-1]

    return [List[j] for i in sign for j in Dict[i]]


def utility_sort(List:list):

    utility_sep = [[], [], [], [], []]

    for i in List: utility_sep[int(float(i[3])) - 1].append(i)

    for j in range(5):

        if len(utility_sep[j]) not in range(2):

            utility_sep[j] = date_sort(utility_sep[j])

    return [n for m in utility_sep[::-1] for n in m]


def spell_sort(List: list):

    spell = {i[0] : i for i in List}

    return [spell[i] for i in sorted(spell.keys())]


def design_search(preprocess):

    origin_data = origin()
    result = list()
    used = list()

    for j in preprocess:

        if j not in used:

            result.append([origin_data[i][j] for i in (0, 1, 5)])

            result[-1].insert(2, origin_data[2][j][:19] if len(origin_data[2]) > 20 else origin_data[2][j])

            used.append(j)

    return result


def design_simple(word: str): return date_sort(design_search(search(word, origin())))


def design_detail(category:str, help:str, startWhen:str, endWhen:str, DATA:list):

    return date_sort(design_search(search_detail(category, help, startWhen, endWhen, DATA)))


def newContentsProcess(): return date_sort(design_search([i for i in range(len(origin()[0]))]))[::-1]


def define_type(result:list, type:str):

    if type == 'new': return [i for i in date_sort(result)[::-1]]

    elif type == 'old': return date_sort(result)

    elif type == 'spell': return spell_sort(result)

    else: return utility_sort(result)
