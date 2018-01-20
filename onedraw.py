# -*- coding: utf-8 -*-
"""
onedraw.py
v0.0.1
git管理を始めた
v0.0.2
複数ファイルを渡したときにうまく動作しない不具合を修正
月や日付が1桁のときに名前が短くなってしまう不具合を修正
onedrawディレクトリが存在しない時にエラーになる不具合を修正
"""

import sys
import os
import datetime
import shutil
from pathlib import Path

version = '0.0.2'

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
    dt = dts[0]
    # 違う時間が混ざってた場合はエラーにする
    for x in dts:
        if dt.year != x.year or dt.month != x.month or dt.day != x.day:
            print('diffday exist!')
            exit(1)

    new_dir_name = "{}_{}".format(dt.strftime('%y%m%d'), path.stem)

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
