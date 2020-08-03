from clojure_fn import group_by

# <대전제>
## (((제목), (날짜), (내용), (별점), (분류), [히스토리]), ... )
## 출력할 때를 제외하고 모든 데이터의 이동은 인덱스로 한다.


def sort_macro(index_of_standard: int, want2reverse: bool):

    def sort_fn(data_i: tuple, data: tuple):

        x_data: dict = group_by(lambda x: data[x][index_of_standard], data_i)

        return tuple(i for k in sorted(x_data.keys(), reverse=want2reverse) for i in x_data[k])

    return sort_fn


def search_simple(search_term: str, data: tuple) -> tuple: return tuple(i for i, v in enumerate(data) if search_term in ''.join(v[:3]))


def search_detail(start_when: str, end_when: str, category: str, utility: str, data: tuple) -> tuple:

    return tuple(i for i, v in enumerate(data) if all((v[1][:2] >= start_when[2:], v[1][:2] <= end_when[2:], v[3] >= int(utility), v[4] == category)))


def spell_sort(data_i: tuple, data: tuple) -> tuple: return sort_macro(0, False)(data_i, data)


def r_date_sort(data_i: tuple, data: tuple) -> tuple: return sort_macro(1, False)(data_i, data)


def date_sort(data_i: tuple, data: tuple) -> tuple: return sort_macro(1, True)(data_i, data)


def utility_sort(data_i: tuple, data: tuple) -> tuple: return sort_macro(3, True)(data_i, data)


def simple_search_process(search_term: str, data: tuple) -> tuple: return date_sort(search_simple(search_term, data), data)


def detail_search_process(start_when: str, end_when: str, category: str, utility: str, data: tuple) -> tuple:

    return date_sort(search_detail(start_when, end_when, category, utility, data), data)


def new_contents_process(data: tuple, len_data: int) -> tuple: return date_sort(tuple(range((len_data - 10) if len_data > 10 else 0, len_data)), data)


def resort_by_sorting_type_change(result: tuple, type: str, data: tuple) -> tuple:

    return next((i for i in (date_sort, r_date_sort, utility_sort, spell_sort) if i.__name__[:-5] == type))(result, data)
