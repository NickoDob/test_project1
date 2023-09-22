import webbrowser

import pandas as pd
from flask import Flask, render_template, redirect, url_for, request
from pymsgbox import alert

from controllers import global_table, keyboxes, check_replacer, validator, downloads_path, checkboxes

app = Flask(__name__)

gt, keys, checks = [], [], []
datFrame, fileName = '', ''

@app.route('/', methods=['GET', 'POST'])
def upload():
    global gt, keys, checks
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
    alert("Файл успешно выгружен в папку Downloads.", "Уведомление", button='OK')
    return redirect(url_for('.upload'))


@app.post('/coincidences')
def coincidences():
    global gt, keys, checks, datFrame, fileName, downloads_path
    keyslist = keyboxes(keys)
    checklist = checkboxes(checks)
    for i in gt:
        check_replacer(i)
    df = pd.merge(gt[0], gt[1], on=keyslist, how='inner')
    fileName = 'coincidences.xlsx'
    datFrame = df[keyslist + checklist]
    return render_template('result.html', tables=[df[keyslist + checklist].to_html(classes='mystyle')])


@app.post('/differences')
def differences():
    global gt, keys, datFrame, fileName, downloads_path
    df = pd.concat(gt)
    keyslist = keyboxes(keys)
    checklist = checkboxes(checks)
    check_replacer(df)
    df = df.drop_duplicates(subset=keyslist, keep=False).reset_index(drop=True)
    fileName = 'differences.xlsx'
    datFrame = df[keyslist + checklist]
    return render_template('result.html', tables=[df[keyslist + checklist].to_html(classes='mystyle')])


@app.post('/joined')
def joined():
    global gt, keys, checks, datFrame, fileName, downloads_path
    keyslist = keyboxes(keys)
    checklist = checkboxes(checks)
    for i in gt:
        check_replacer(i)
    df = pd.concat(gt)
    df1 = pd.merge(gt[0], gt[1][keyslist + checklist], how='left', on=keyslist)
    df2 = df.drop_duplicates(subset=keyslist, keep=False).reset_index(drop=True)
    df = pd.concat([df1, df2], ignore_index=True)
    fileName = 'joined.xlsx'
    datFrame = df[keyslist + checklist]
    return render_template('result.html', tables=[df[keyslist + checklist].to_html(classes='mystyle')])


if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False)