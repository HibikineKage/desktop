# -*- coding: utf-8 -*-
"""
onedraw.py
v0.0.1
git管理を始めた
v0.0.2
複数ファイルを渡したときにうまく動作しない不具合を修正
月や日付が1桁のときに名前が短くなってしまう不具合を修正
onedrawディレクトリが存在しない時にエラーになる不具合を修正
v0.0.3
複数ファイルで日付が異なる場合、日付を選ばせるようにした
年を4桁にした
v0.0.4
単一画像ファイルだとdtが存在しないためにエラーになるバグを修正
"""

import sys
import os
import datetime
import shutil
from pathlib import Path

version = '0.0.3'


def is_diff_day_exist(dts):
    dt = dts[0]
    # 違う時間が混ざってた場合はエラーにする
    for x in dts:
        if dt.year != x.year or dt.month != x.month or dt.day != x.day:
            return True
    return False


if __name__ == '__main__':
    print('onedraw.py v{}'.format(version))

    args = sys.argv
    if len(args) == 1:
        print('USAGE')
        print('onedraw.bat <files>')
        print('onedraw.bat <directory>')
        exit(1)

    # ファイルパスを一通り取ってくる
    paths = [Path(i) for i in args[1:]]
    is_single_dir = len(paths) == 1 and paths[0].is_dir()

    path = paths[0]
    if is_single_dir:
        files = [x for x in path.iterdir()]
        timestamps = [os.stat("{}/{}".format(path.name, f.name)
                              ).st_mtime for f in files]
    else:
        files = paths
        timestamps = [os.stat(path.name).st_mtime for f in files]

    # 時間を取得
    dts = [datetime.datetime.fromtimestamp(ts) for ts in timestamps]
    if is_diff_day_exist(dts):
        print('diffday exist!')
        print('please select true day! (-1 cancel)')
        for i, [d, f] in enumerate(zip(dts, files)):
            print('[{}]{}: {}'.format(i, f.name, d.strftime('%Y/%m/%d')))
        value = int(input())
        if value == -1:
            print('stop moving files.')
            exit(1)
        try:
            dt = dts[value]
        except IndexError:
            print('out of range!')
            exit(1)
    else:
        dt = dts[0]

    new_dir_name = "{}_{}".format(dt.strftime('%Y%m%d'), path.stem)

    onedraw_path = Path('onedraw')
    if not onedraw_path.exists():
        onedraw_path.mkdir()

    if is_single_dir:
        shutil.move(path.name, "onedraw/{}".format(new_dir_name))
    else:
        os.mkdir('onedraw/{}'.format(new_dir_name))
        for i in files:
            shutil.move(i.name, 'onedraw/{}/{}'.format(new_dir_name, i.name))
    print('moved!')
    exit(0)
