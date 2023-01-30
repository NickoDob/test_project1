from pathlib import Path

import pandas as pd

from flask import Flask, render_template, redirect, url_for, request

from controllers import global_table, checkboxes, keyboxes, check_replacer, validator


app = Flask(__name__)

gt, keys, checks = [], [], []


@app.route('/', methods=['GET', 'POST'])
def upload():
    global gt, keys, checks
    Path("./results/").mkdir(parents=True, exist_ok=True)
    Path("./tables/").mkdir(parents=True, exist_ok=True)
    if request.method == 'POST':
        gt = global_table()
        val = validator(gt)
        if isinstance(val, list):
            keys, checks = val[1], val[2]
            return render_template('checkpage.html', keylist=keys, checklist=checks)
        else:
            return redirect(url_for('.upload'))
    return render_template('index.html')


@app.post('/coincidences')
def coincidences():
    global gt, keys
    df = pd.concat(gt)
    check_replacer(df)
    keyslist = keyboxes(keys)
    coinc = df[df.duplicated(keyslist, keep=False)].reset_index(drop=True)
    coinc.to_excel('./results/coincidences.xlsx')
    return render_template('result.html', tables=[coinc.to_html(classes='mystyle')])


@app.post('/differences')
def differences():
    global gt, keys
    df = pd.concat(gt)
    check_replacer(df)
    keyslist = keyboxes(keys)
    diff = df.drop_duplicates(subset=keyslist, keep=False).reset_index(drop=True)
    diff.to_excel('./results/differences.xlsx')
    return render_template('result.html', tables=[diff.to_html(classes='mystyle')])


@app.post('/joined')
def joined():
    global gt, keys, checks
    keyslist = keyboxes(keys)
    checklist = checkboxes(checks)
    df = pd.merge(gt[0], gt[1][keyslist + checklist], how='left', left_on=keyslist, right_on=keyslist)
    check_replacer(df)
    df.to_excel('./results/joined.xlsx')
    return render_template('result.html', tables=[df.to_html(classes='mystyle')])


if __name__ == '__main__':
    app.run(debug=True)