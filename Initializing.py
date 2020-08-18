import pickle

if __name__ == '__main__':
    data = [["데이터 입니다", '20-07-31 17:17:33', "데이터고요", "데이터", ["데이터고요"]],
            ["2 입니다", '20-08-31 17:17:33', "2고요", "데이터", ["2고요"]]]
    with open("./DATA.txt", "wb") as f: pickle.dump(data, f)
