import pickle
import time

if __name__ == '__main__':
    # ((제목), (날짜), (내용), (별점), (분류), (히스토리)) 날짜 : '20-07-31 19:14:33'
    data = (("데이터 입니다", time.strftime('%y-%m-%d %H:%M:%S'), "데이터고요", 5, "데이터", ["데이터고요"]),
            ("2 입니다", time.strftime('%y-%m-%d %H:%M:%S'), "2고요", 5, "데이터", ["2고요"]))
    with open("./DATA.txt", "wb") as f: pickle.dump(data, f)