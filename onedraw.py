# -*- coding: utf-8 -*-
"""
onedraw.py
"""

import sys
import os
import datetime
import shutil
from pathlib import Path

version = '0.0.1'

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

    new_dir_name = "{}{}{}_{}".format(dt.year, dt.month, dt.day, path.stem)
    
    if is_single_dir:
        shutil.move(path.name, "onedraw/{}".format(new_dir_name))
    else:
        for i in files:
            shutil.move(i.name, 'onedraw/{}/'.format(new_dir_name))
    print('moved!')
    exit(0)
