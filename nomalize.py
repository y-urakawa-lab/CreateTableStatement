#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import numpy as np
# 正規表現パターンを正規表現オブジェクトにコンパイルする。match()やsearch()、sub()でマッチングできる
ILLEGAL_CHARACTERS_RE = re.compile(
        r'[\000-\010]|[\013-\014]|[\016-\037]|[\x00-\x1f\x7f-\x9f]|[\uffff]')

"""
正規化クラス
"""


class Nomalize:

    """
    改行コードと例外文字の除外
    """
    def line_feed(self, np_data):
        data_col_count = np_data.shape[1]
        data_row_count = np_data.shape[0]
        for i in range(data_col_count):
            for j in range(data_row_count):
                np_data[j][i] = np_data[j][i].replace("\r\n", "").replace("\r", "").replace("\n", "")
                np_data[j][i] = ILLEGAL_CHARACTERS_RE.sub("", np_data[j][i])

        return np_data

    """
    CSVを解析して型とデータを返す  
    """
    def type_check(self, np_data):
        type_a = []
        type_list = []

        unique_type = []

        length_a = []
        length_list = []

        data_a = []
        data_list = []

        # リストのスライシング X[:, 0]
        for i in range(np_data.shape[1]):
            for j in range(np_data.shape[0]):

                loop_data = np_data[:, i][j]

                if any(x in str(loop_data) for x in ("@", "＠")):
                    t = "str"
                    d = str(loop_data)

                # スラかハイフンは日付か文字列
                elif any(x in str(loop_data) for x in ("/", "-", ":")):
                    if re.match(r"[a-z]+|[A-Z]+", str(np_data[:, i][j])):
                        t = "str"
                        d = str(loop_data)
                    elif re.match(
                            r"([2-9][0-1][0-9][0-9](-|/)([0-1][0-9]|[0-9]+)(-|/)([0-3][0-9]|[0-9]+))\Z",
                            str(np_data[:, i][j])):
                        t = "date"
                        d = str(loop_data)
                    elif re.match(
                            r"([2-9][0-1][0-9][0-9](-|/)([0-1][0-9]|[0-9]+)(-|/)([0-3][0-9]|[0-9]+)) [0-9]+:[0-9]+:[0-9]+\Z",
                            str(np_data[:, i][j])):
                        t = "datetime"
                        d = str(loop_data)
                    elif re.match(
                            r"[0-9]+:[0-9]+:[0-9]+\Z",
                            str(np_data[:, i][j])):
                        t = "time"
                        d = str(loop_data)

                    else:
                        t = "str"
                        d = str(loop_data)

                # ドットが複数あるのはIPアドレス
                elif re.match(r"[0-9]+\.[0-9]+\.[0-9]", str(loop_data)):
                    t = "str"
                    d = str(loop_data)
                # ドット一つは小数点とする
                elif re.match(r"[0-9]+\.[0-9]+", str(loop_data)):
                    t = "double"
                    d = str(loop_data)
                # 頭が0の数値は文字列
                elif re.match(r"[0][0-9]+", str(loop_data)):
                    t = "str"
                    d = str(loop_data)
                elif re.match(r"^[1-9][0-9]+$", str(loop_data)):
                    t = "int"
                    d = str(loop_data)
                elif re.match(r"^[0-9]+$", str(loop_data)):
                    t = "int"
                    d = str(loop_data)
                else:
                    t = type(loop_data)
                    d = str(loop_data)

                type_a.append(t)
                data_a.append(d)
                length_a.append(len(str(loop_data)))

            # データをそのまま配列へ格納
            type_list.append(type_a)
            data_list.append(data_a)
            length_list.append(max(length_a))
            unique_type.append(set(type_a))

            type_a = []
            length_a = []
            data_a = []

        return type_list, data_list, length_list, unique_type

    """
    ヘッダと同じ行があったら最初の行を除いて削除する
    """
    def header_delete(self, np_data, np_cols):
        del_key = []
        for i in range(np_data.shape[0]):

            if (np.array(np_cols) == np_data[i]).all():
                print(i)
                del_key.append(i)

        a = np.delete(np_data, del_key, axis=0)
        return a


