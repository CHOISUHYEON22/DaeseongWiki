from search_process import sort_bunch, search_simple, search_detail, new_contents_process
from flask import Flask, render_template, request, redirect, url_for
from collections import namedtuple
from datetime import datetime
from time import strftime
import pickle

app = Flask(__name__)


def list_category() -> list: return list({i[4] for i in gain_data()})


def list_title() -> list: return list({i[0] for i in gain_data()})


def find_index_by_title(data: list, cnt_title: str) -> int:

    return next((i for i, v in enumerate(data) if v[0] == cnt_title))


def gain_data() -> list:

    with open("./DATA.txt", "rb") as f: return pickle.load(f)


@app.route('/')
def index():

    sorts: namedtuple = sort_bunch(new_contents_process(gain_data()))

    return render_template('index_n.html', date_sort=sorts.date, r_date_sort=sorts.r_date, spell_sort=sorts.spell, title='최신 업로드', utility_sort=sorts.utility, list_category=list_category(), did_find=bool(sorts[0]))


@app.route('/search', methods=['GET'])
def search():

    if request.args.get('simple_or_detail') == 'S': sorts: namedtuple = sort_bunch(search_simple(gain_data(), request.args.get('search_term')))

    else: sorts: namedtuple = sort_bunch(search_detail(gain_data(), *(request.args.get(i) for i in ('start_when', 'end_when', 'category'))))

    return render_template('index_n.html', date_sort=sorts.date, r_date_sort=sorts.r_date, spell_sort=sorts.spell, utility_sort=sorts.utility, list_category=list_category(), did_find=bool(sorts[0]))


@app.route('/add')
def add(): return render_template('add_content_n.html', list_category=list_category())


@app.route('/modify', methods=['GET'])
def modify():

    title, category, content = (request.args.get(i) for i in ('title', 'amp;category', 'amp;content'))

    return render_template('modify_content_n.html', title=title, category=[category], content=content)


@app.route('/process_add_modify', methods=['POST'])
def process_add_modify() -> None:

    data = gain_data()

    title, content, category = (request.form[i].strip() for i in ('title', 'content', 'category'))

    if request.form['add_or_modify'] == 'M':

        index_num = find_index_by_title(data, title)

        data[index_num] = [title, strftime('%y-%m-%d %H:%M:%S'), content, data[index_num][3], category, data[index_num][5].append(content)]

    else: data.append([title, strftime('%y-%m-%d %H:%M:%S'), content, (0, 1), category, [content]])

    with open("./DATA.txt", "wb") as f: pickle.dump(data, f)


@app.route('/content')
def display_content():

    data = gain_data()

    return render_template('content_n.html', content=data[find_index_by_title(data, request.args.get('cnt_title'))])


if __name__ == '__main__':
    app.run()

