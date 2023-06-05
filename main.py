from pathlib import Path

import pandas as pd
import webbrowser

from flask import Flask, render_template, redirect, url_for, request
from pymsgbox import alert

from controllers import global_table, checkboxes, keyboxes, check_replacer, validator, downloads_path


app = Flask(__name__)

gt, keys, checks = [], [], []
datFrame, fileName = '', ''

@app.route('/', methods=['GET', 'POST'])
def upload():
    global gt, keys, checks
    Path(downloads_path + "/results/").mkdir(parents=True, exist_ok=True)
    Path(downloads_path + "/tables/").mkdir(parents=True, exist_ok=True)
    if request.method == 'POST':
        gt = global_table()
        val = validator(gt)
        if isinstance(val, list):
            keys, checks = val[1], val[2]
            return render_template('checkpage.html', keylist=keys, checklist=checks)
        else:
            return redirect(url_for('.upload'))
    return render_template('index.html')


@app.route('/resultTable', methods=['GET', 'POST'])
def resultTable():
    global datFrame, fileName, downloads_path
    datFrame.to_excel(downloads_path + '/results/' + fileName)
    alert("Файл успешно выгружен.", "Уведомление", button='OK')
    return redirect(url_for('.upload'))


@app.post('/coincidences')
def coincidences():
    global gt, keys, datFrame, fileName, downloads_path
    df = pd.concat(gt)
    check_replacer(df)
    keyslist = keyboxes(keys)
    fileName = 'coincidences.xlsx'
    coinc = df[df.duplicated(keyslist, keep=False)].reset_index(drop=True)
    datFrame = coinc
#    coinc.to_excel(downloads_path + '/results/coincidences.xlsx')
    return render_template('result.html', tables=[coinc.to_html(classes='mystyle')])


@app.post('/differences')
def differences():
    global gt, keys, datFrame, fileName, downloads_path
    df = pd.concat(gt)
    check_replacer(df)
    keyslist = keyboxes(keys)
    fileName = 'differences.xlsx'
    diff = df.drop_duplicates(subset=keyslist, keep=False).reset_index(drop=True)
    datFrame = diff
#    diff.to_excel(downloads_path + '/results/differences.xlsx')
    return render_template('result.html', tables=[diff.to_html(classes='mystyle')])


@app.post('/joined')
def joined():
    global gt, keys, checks, datFrame, fileName, downloads_path
    keyslist = keyboxes(keys)
    checklist = checkboxes(checks)
    fileName = 'joined.xlsx'
    df = pd.merge(gt[0], gt[1][keyslist + checklist], how='left', left_on=keyslist, right_on=keyslist)
    datFrame = check_replacer(df)
#    df.to_excel(downloads_path + '/results/joined.xlsx')
    return render_template('result.html', tables=[df.to_html(classes='mystyle')])


if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False)