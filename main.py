import os, tkinter, tkinter.filedialog, tkinter.messagebox
import traceback, sys
import filecheck as fc
import nomalize
import sqlwriter


class Menu:
    def __init__(self):
        self.size = '300x200'
        self.title = 'preprocessor'


def select():
    file_type = [("", "*.csv"), ("", "*.txt"), ("", "*.tsv")]
    init_path = os.path.abspath(os.path.dirname(__file__))

    label.configure(text='実行中の処理：検索')
    tkinter.messagebox.showinfo('データ解析', 'CreateTable文（SQL)を生成します。\n解析するファイルを選択してください。(UTF-8のCSV推奨)')

    file_path = tkinter.filedialog.askopenfilename(filetypes=file_type, initialdir=init_path)

    # ファイルが正しいかをチェック
    check = fc.FileChecker()
    raw_data = check.file_path_check(file_path)
    raw_data = raw_data.fillna('.')

    nom = nomalize.Nomalize()
    # データをマージしたときなど、カラム名が複数あるケースでは1行目以外を削除する
    np_data = raw_data.values
    np_cols = raw_data.columns
    np_data = nom.header_delete(np_data, np_cols)

    # 改行コード・不正文字列の除外
    np_data = nom.line_feed(np_data)

    # 型の解析：型,データ,最大数（ユニーク）,重複なし配列
    type_array, data_array, length_array, unique_type = nom.type_check(np_data)

    sql = sqlwriter.SqlWriter()
    sql.create_table_text(raw_data, unique_type, length_array)


def exit_command():
    sys.exit(0)

# ----------------------------------


if __name__ == "__main__":
    try:
        params = Menu()
        root = tkinter.Tk()
        root.geometry(params.size)
        root.title(params.title)

        val = tkinter.IntVar()
        label = tkinter.Label(root, text='CreateTable文を生成します')
        label.pack()

        b = tkinter.Button(root, text='決定', command=select)
        b.pack(fill='x', padx=100, expand=1)
        exit_btn = tkinter.Button(root, text="終了", bg='#f0e68c', command=exit_command)
        exit_btn.pack(padx=20, side='right')

        root.mainloop()

    except SystemExit:
        print("終了")
    except:
        print(traceback.format_exc())
        tkinter.messagebox.showerror('エラー', '処理に失敗しました。')
        exit
    else:
        sys.exit(0)
