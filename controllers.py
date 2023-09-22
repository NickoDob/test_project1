import pathlib
from shutil import rmtree

import pandas as pd
from dbfread import DBF
from flask import request
from pymsgbox import alert

downloads_path = str(pathlib.Path.home() / "Downloads")


def check_page_creator(gt):
    keylist, checklist = [], set()
    for column1 in gt[0]:
        for column2 in gt[1]:
            if column2 == column1:
                keylist.append(column2)
            checklist.add(column2)
    if len(keylist) == 0:
        return alert("Отсутствуют общие заголовки столбцов", "Ошибка", button='OK')
    else:
        keys = keylist
        checks = [elem for elem in checklist if elem not in keylist]
        return [gt, keys, checks]


def validator(gt):
    if isinstance(gt, str):
        return alert("Выбран файл с неподходящим расширением", "Ошибка", button='OK')
    else:
        return check_page_creator(gt)


def checkboxes(taglist):
    checklist = []
    for checkbox in taglist:
        value = request.form.get(checkbox)
        if value:
            checklist.append(checkbox)
    return checklist


def keyboxes(taglist):
    keylist = []
    for keybox in taglist:
        value = request.form.get(keybox)
        if value:
            keylist.append(keybox)
    return keylist


def check_replacer(df):
    value = request.form.get('Замена')
    if value:
        for column in df:
            df[column] = df[column].astype(str).str.replace('ё', 'е')
    return df


def global_table():
    global downloads_path
    pathlib.Path(downloads_path + "/results/").mkdir(parents=True, exist_ok=True)
    pathlib.Path(downloads_path + "/tables/").mkdir(parents=True, exist_ok=True)
    data = []
    files = [request.files['file1'], request.files['file2']]
    for file in files:
        if pathlib.Path(file.filename).suffix == '.xlsx' or pathlib.Path(file.filename).suffix == '.xls':
            file.save(downloads_path + '/tables/' + file.filename)
            df = pd.read_excel(downloads_path + '/tables/' + file.filename, parse_dates=False, index_col=None)
            df.columns = [column.strip() for column in df]
            data.append(df)
        elif pathlib.Path(file.filename).suffix == '.csv':
            file.save(downloads_path + '/tables/' + file.filename)
            df = pd.read_csv(downloads_path + '/tables/' + file.filename, sep=";", encoding="cp1251", index_col=None)
            df.columns = [column.strip() for column in df]
            data.append(df)
        elif pathlib.Path(file.filename).suffix == '.DBF':
            file.save(downloads_path + '/tables/' + file.filename)
            df = pd.DataFrame(iter(DBF(downloads_path + '/tables/' + file.filename)))
            df.columns = [column.strip() for column in df]
            data.append(df)
        else:
            return 'Ошибка'
    rmtree(downloads_path + "/tables")
    return data