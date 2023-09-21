import webbrowser
from pathlib import Path

import pandas as pd
from flask import Flask, render_template, redirect, url_for, request
from pymsgbox import alert

from controllers import global_table, keyboxes, check_replacer, validator, downloads_path


app = Flask(__name__)

gt, keys = [], []
datFrame, fileName = '', ''

@app.route('/', methods=['GET', 'POST'])
def upload():
    global gt, keys
    Path(downloads_path + "/results/").mkdir(parents=True, exist_ok=True)
    Path(downloads_path + "/tables/").mkdir(parents=True, exist_ok=True)
    if request.method == 'POST':
        gt = global_table()
        val = validator(gt)
        if isinstance(val, list):
            keys = val[1]
            return render_template('checkpage.html', keylist=keys)
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
    global gt, keys, datFrame, fileName, downloads_path
#    df = pd.concat(gt)
    keyslist = keyboxes(keys)
    for i in gt:
        check_replacer(i)
    df = pd.merge(gt[0], gt[1], on=keyslist, how='inner')
    fileName = 'coincidences.xlsx'
#    coinc = df[df.duplicated(keyslist, keep=False)].reset_index(drop=True)
    datFrame = df
    return render_template('result.html', tables=[df.to_html(classes='mystyle')])


@app.post('/differences')
def differences():
    global gt, keys, datFrame, fileName, downloads_path
    df = pd.concat(gt)
    keyslist = keyboxes(keys)
    check_replacer(df)
    fileName = 'differences.xlsx'
    df = df.drop_duplicates(subset=keyslist, keep=False).reset_index(drop=True)
    datFrame = df
    return render_template('result.html', tables=[df.to_html(classes='mystyle')])

"""
@app.post('/joined')
def joined():
    global gt, keys, checks, datFrame, fileName, downloads_path
    keyslist = keyboxes(keys)
    checklist = checkboxes(checks)
    fileName = 'joined.xlsx'
    df = pd.merge(gt[0], gt[1][keyslist + checklist], how='left', left_on=keyslist, right_on=keyslist)
    datFrame = check_replacer(df)
    return render_template('result.html', tables=[df.to_html(classes='mystyle')])



@app.post('/fulled')
def fulled():
    global gt, keys, checks, datFrame, fileName, downloads_path
    keyslist = keyboxes(keys)
    checklist = checkboxes(checks)
    fileName = 'fulled.xlsx'
    df = pd.concat(gt)
    df1 = pd.merge(gt[0], gt[1][keyslist + checklist], how='left', left_on=keyslist, right_on=keyslist)
    df2 = df.drop_duplicates(subset=keyslist, keep=False).reset_index(drop=True)
    df_full = pd.concat([df1, df2], ignore_index=True)
    datFrame = check_replacer(df_full)
    return render_template('result.html', tables=[df_full.to_html(classes='mystyle')])
"""


if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False)