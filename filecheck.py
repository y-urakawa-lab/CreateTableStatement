#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CSVデータの存在ををチェックするクラス
存在が確認できたらデータをpandasで読み込んで返す
"""
import re
import pandas as pd
import tkinter, tkinter.filedialog, tkinter.messagebox
import traceback


class FileChecker:

    def __init__(self):
        self.header = 0  # ヘッダーが一番最初にある前提
        self.dtype = "str"  # データはすべて文字列として取得
        self.sep = ""

    def file_path_check(self, filepath):
        try:
            if re.search("\.csv", filepath):
                self.sep = ","
            elif re.search("\.tsv", filepath):
                self.sep = "\t"
            elif re.search("\.txt", filepath):
                f = open(filepath, 'r')
                line = f.readline()
                tab = line.count('\t')
                comma = line.count(',')

                if tab > comma:
                    self.sep = "\t"
                    print('タブ区切りで解析します')
                elif tab < comma:
                    self.sep = ","
                    print('カンマ区切りで解析します')
                else:
                    self.sep = ","
                    print('カンマ区切りで解析します')
                    f.close()
            else:
                print("ファイルを選択してください")
                return

            data = pd.read_csv(filepath, header=self.header, dtype=self.dtype, sep=self.sep, escapechar="\\")
            return data

        except KeyError:
            tkinter.messagebox.showerror('設定ファイルが違います', '設定ファイルを確認してください')
            return
        except UnicodeDecodeError:
            tkinter.messagebox.showerror('文字コードエラー', '読み込むCSV・TSV・TXTファイルは\nUTF-8に変換してください')
            return

        else:
            print(traceback.format_exc())
            print("filecheker")
            tkinter.messagebox.showerror('エラー', '処理に失敗しました。')
            exit
