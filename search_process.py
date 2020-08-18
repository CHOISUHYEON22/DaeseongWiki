from clojure_fn import group_by
from collections import namedtuple


def sort_macro(index_of_standard: int, want2reverse: bool):

    def sort_fn(data_searched_to_sort: list) -> list:

        x_data: dict = group_by(lambda x: x[index_of_standard], data_searched_to_sort)

        return [i for k in sorted(x_data.keys(), reverse=want2reverse) for i in x_data[k]]

    return sort_fn


def search_simple(data: list, search_term: str) -> list: return [v for i, v in enumerate(data) if search_term in ''.join(v[:3])]


def search_detail(data: list, start_when: str, end_when: str, category: str) -> list:

    return [v for v in data if all((v[1][:8] >= start_when[2:], v[1][:8] <= end_when[2:], v[4] == category))]


def spell_sort(data_searched_to_sort: list) -> list: return sort_macro(0, False)(data_searched_to_sort)


def r_date_sort(data_searched_to_sort: list) -> list: return sort_macro(1, False)(data_searched_to_sort)


def date_sort(data_searched_to_sort: list) -> list: return sort_macro(1, True)(data_searched_to_sort)


def new_contents_process(data: list) -> list: return data[-10 if len(data) > 10 else 0:]


def sort_bunch(data_searched_to_sort: list) -> namedtuple:

    fn_names = namedtuple('fn_names', 'date r_date spell')

    return fn_names(**{f.__name__[:-5]: f(data_searched_to_sort) for f in (date_sort, r_date_sort, spell_sort)})
