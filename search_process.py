from pickle import load
from clojure_fn import group_by

# (((제목), (날짜), (내용), (별점), (분류), [히스토리]), ... )

def get_data() -> tuple:

    with open("./DATA.txt", "rb") as f: return load(f)


def search_simple(search_term: str, data: tuple) -> tuple: return tuple({i for v in data for i, u in enumerate(v)[:3] if search_term in u})


def search_detail(category: str, utility: str, start_when: str, end_when: str, data: tuple) -> tuple:

    return tuple(i for i, v in enumerate(data) if all((v[1][:2] >= start_when[2:], v[1][:2] <= end_when[2:], v[3] >= utility, v[4] == category)))


def date_sort(data: tuple) -> tuple:

    when_data: dict = group_by(lambda x: x[1], data)

    return tuple(i for k in sorted(when_data.keys(), reverse=True) for i in when_data[k])


def date_rsort(data: tuple) -> tuple: return tuple(reversed(date_sort(data)))


def utility_sort(data: tuple) -> tuple:

    utility_data: dict = {i[3] : i for i in data}

    return tuple(utility_data[k] for k in sorted(utility_data.keys(), reverse=True))


def spell_sort(data: tuple) -> tuple: return tuple(sorted(data))


def simple_search_process(search_term: str) -> tuple: return date_sort(search_simple(search_term, get_data()))


def detail_search_process(category: str, help: str, start_when: str, end_when: str) -> tuple:

    return date_sort(search_detail(category, help, start_when, end_when, get_data()))


def new_contents_process() -> tuple:

    data_len = len(get_data())

    return date_sort(get_data()[:10 if data_len > 10 else data_len])


def resort_by_sorting_type_change(result: tuple, type: str) -> tuple:

    return (spell_sort if type == 'spell' else date_sort if type == 'new' else date_rsort if type == 'old' else utility_sort)(result)
