from search_process import design_simple, design_detail, origin, define_type, newContentsProcess
from flask import Flask, render_template, request, redirect, url_for
from AdvancedFunction import modificationOrigin
from slang_filter import slangFilter
from datetime import datetime
from time import ctime
import pickle

app = Flask(__name__)

result = list()
DATA = list()


def List_menu():

    with open(".\DATA.txt", "rb") as f: return tuple(set(pickle.load(f)[4]))


def List_title():

    with open(".\DATA.txt", "rb") as f: return tuple(set(pickle.load(f)[0]))


@app.route('/')
def index(): return render_template('index.html', YorN=True)


@app.route('/Search', methods=['GET'])
def Search():

    global result
    global DATA

    if request.args.get('S_D') == 'S':

        word = request.args.get('word')

        result = design_simple(word)

        return render_template('search.html', result=result, word=word, filename='search.html')

    elif request.args.get('S_D') == 'D':

        category = request.args.get('category')
        startWhen = request.args.get('startWhen')
        endWhen = request.args.get('endWhen')
        help = request.args.get('help')

        DATA = design_detail(category, help, startWhen, endWhen, origin())

        return render_template('in_menu.html', LIST=List_menu(), thisYear=datetime.now().year, DATA=DATA, filename='in_menu.html')


@app.route('/type', methods=['GET'])
def type():

    global type
    filename = request.args.get('filename')

    if filename == 'search.html':

        result = globals()['result']
        type = request.args.get('type')
        word = request.args.get('word')

        return render_template(filename, result=define_type(result, type), word=word, filename=filename)

    elif filename == 'in_menu.html':

        thisYear = request.args.get('thisYear')
        type = request.args.get('type')
        DATA = globals()['DATA']

        return render_template(filename, LIST=List_menu(), thisYear=thisYear, DATA=define_type(DATA, type), filename=filename)


@app.route('/add')
def add(): return render_template("add_content.html", LIST=List_menu())


@app.route('/Add', methods=['POST'])
def Add():

    content = slangFilter(request.form['content']).strip()
    AorM = request.form['AorM']
    DATA = origin()

    if AorM == 'A':

        title = slangFilter(request.form['title']).strip()
        category = request.form['category']

        try: help = request.form['help']

        except: help = 1

        input_info = [title, ctime(), content, [content], category, help]

        for i in range(6): DATA[i].append(input_info[i])

    else:

        index = int(request.form['index'][:-1])

        DATA[1][index] = ctime()

        DATA[2][index] = content

        DATA[3][index].append(content)

    with open("DATA.txt", "wb") as f: pickle.dump(DATA, f)

    if AorM == 'A': return redirect(url_for('newContents'))

    else: return redirect(url_for('info', infoTitle=DATA[0][int(request.form['index'][:-1])]))


@app.route('/modification', methods=['POST'])
def modification():

    index = int(request.form['index'])
    title = origin()[0][index]
    content = origin()[2][index]
    category = origin()[4][index]
    help = origin()[5][index]

    return render_template("Modification.html", LIST=List_menu(), index=index, title=title, content=content, category=category, help=help)


@app.route("/menu")
def menu(): return render_template('in_menu.html', LIST=List_menu(), thisYear=datetime.now().year)


@app.route("/newContents")
def newContents():

    data = newContentsProcess()

    if len(data) > 10: return render_template('pre_in_menu.html', LIST=List_menu(), thisYear=datetime.now().year, DATA=data[:10])

    else: return render_template('pre_in_menu.html', LIST=List_menu(), thisYear=datetime.now().year, DATA=data)



@app.route("/info/<infoTitle>")
def info(infoTitle): return render_template('info.html', Info=[origin()[i][origin()[0].index(infoTitle)] for i in range(6)], index=origin()[0].index(infoTitle), infoTitle=infoTitle)


@app.route("/helpCalc", methods=['POST'])
def helpCalc():

    Origin = origin()

    infoTitle = request.form['infoTitle']

    Origin[5][int(request.form['index'])] = (int(Origin[5][int(request.form['index'])]) + int(request.form['help'])) / 2

    with open("DATA.txt", "wb") as f: pickle.dump(Origin, f)

    return render_template('info.html', Info=[origin()[i][origin()[0].index(infoTitle)] for i in range(6)], index=origin()[0].index(infoTitle), infoTitle=infoTitle)


@app.route("/helpContent")
def helpContent(): return render_template('helpContent.html')


@app.route("/{!!/[%$$%/%&&%]/!!/}")
def check_given(): return render_template("check.html")


@app.route("/{!!/[%^%/%&%]/!!/}", methods=['POST'])
def check():
     if request.form['pw'] == '&Admin&': return redirect(url_for('data'))
     else: return redirect(url_for('index'))


@app.route("/{!![%$%/%&%]/!!/}")
def data():

    Origin = origin()

    process = [[Origin[0][i], Origin[1][i], Origin[2][i], Origin[4][i], Origin[5][i], Origin[3][i]] for i in range(len(Origin[0]))]

    return render_template("watch.html", DATA=process)


@app.route("/{!![%*%/%&%]/!!/}", methods=['POST'])
def CalC():

    modificationOrigin(request.form['modification'])

    return redirect(url_for('data'))


if __name__ == '__main__':
    app.run()

