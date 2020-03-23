import pickle


def slangFilter(text:str):

    with open("Slang.txt", "rb") as f: slang_list = pickle.load(f)

    text_list = text.split()

    for i in range(len(text_list)):

        for j in slang_list:

            if j in text_list[i]:

                text_list[i] = '*' * len(text_list[i])

                break

    return ' '.join(text_list)
