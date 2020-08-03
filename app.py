from search_process import simple_search_process, detail_search_process, resort_by_sorting_type_change, new_contents_process
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from time import strftime
import pickle

app = Flask(__name__)


#def list_category() -> tuple: return tuple({i[4] for i in get_data()})


#def list_title() -> tuple: return tuple({i[0] for i in get_data()})

def get_data() -> tuple:

    with open("./DATA.txt", "rb") as f: return pickle.load(f)


def save_data(data: tuple) -> None:

    with open("./DATA.txt", "wb") as f: pickle.dump(data, f)


@app.route('/')
def index(): return render_template('index.html', data=get_data())


@app.route('/search', methods=['GET'])
def search():

    if request.args.get('simple_or_detail') == 'S':

        search_term = request.args.get('search_term')

        return render_template('search_simple.html', result=simple_search_process(search_term, get_data()), search_term=search_term, file_name='search_simple.html', data=get_data())

    else:

        cond = tuple(request.args.get(i) for i in ('start_when', 'end_when', 'category', 'utility')) + (get_data(),)

        return render_template('search_detail.html', start_when=cond[0], end_when=cond[1], result=detail_search_process(*cond), file_name='search_detail.html')


@app.route('/type', methods=['GET'])
def type():

    file_name = request.args.get('file_name')

    result = resort_by_sorting_type_change(eval(request.args.get('result')), request.args.get('type'), get_data())

    if file_name == 'search_simple.html': return render_template(file_name, result=result, search_term=request.args.get('search_term'), file_name=file_name, data=get_data())

    else: return render_template(file_name, this_year=request.args.get('this_year'), result=result, file_name=file_name, data=get_data())


@app.route('/add')
def add(): return render_template("add_content.html")


@app.route('/process_add_modify', methods=['POST'])
def process_add_modify():

    content, data = request.form['content'].strip(), get_data()

    if request.form['add_or_modify'] == 'A':

        title, category = request.form['title'].strip(), request.form['category']

        data += (title, strftime('%y-%m-%d %H:%M:%S'), content, 1, category, [content])

        redirect_add_modify(data)

    else:

        index = int(request.form['index'][:-1])

        data[index] = data[index][0] + (strftime('%y-%m-%d %H:%M:%S'), content) + data[index][3:5] + data[index][5].append(content)

        redirect_add_modify(data, index)


def redirect_add_modify(data: tuple, index: int = None):

    save_data(data)

    return redirect(url_for('info', info_title=data[index][0] if index else url_for('new_contents')))


@app.route('/modification', methods=['POST'])
def modification():

    data = get_data()

    index = int(request.form['index'])

    title, content, utility, category = (data[index][i] for i in (0, 2, 3, 4))

    return render_template("Modification.html", list_category=list_category(), index=index, title=title, content=content, category=category, utility=utility)


@app.route("/menu")
def menu(): return render_template('search_detail.html', this_year=datetime.now().year)


@app.route("/new_contents")
def new_contents():

    data = get_data()

    return render_template('pre_in_menu.html', start_when=datetime.now().year, end_when=datetime.now().year,  data=new_contents_process(data, len(data)))


@app.route("/info/<info_title>")
def info(info_title):
    return render_template('info.html', info=[get_data()[list_title().index(info_title)][i] for i in range(6)], index=get_data()[0].index(info_title), info_title=info_title)


@app.route("/utility_calc", methods=['POST'])
def utility_calc():

    data = get_data()

    info_title = request.form['info_title']

    data[5][int(request.form['index'])] = (int(data[5][int(request.form['index'])]) + int(request.form['help'])) / 2

    with open("DATA.txt", "wb") as f: pickle.dump(data, f)

    return render_template('info.html', Info=[get_data()[i][get_data()[0].index(info_title)] for i in range(6)], index=get_data()[0].index(info_title), infoTitle=info_title)


if __name__ == '__main__':
    app.run()

